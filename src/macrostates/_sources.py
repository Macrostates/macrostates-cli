"""Explicit tagged source transports; credentials never enter persisted metadata."""

import json
import os
import re
import shutil
import subprocess
import tempfile
from importlib.metadata import PackageNotFoundError, version
from pathlib import Path
from typing import Any, Protocol
from urllib.error import HTTPError, URLError
from urllib.parse import quote, urlparse
from urllib.request import HTTPRedirectHandler, Request, build_opener

from ._integrity import MAX_ARCHIVE
from ._models import MacrostatesError


class SourceProvider(Protocol):
    """Injectable source boundary used by install and lock."""

    def resolve(self, repository: str, tag: str) -> str:
        """Return the full commit ID selected by a release tag."""
        ...

    def download(self, repository: str, commit: str) -> bytes:
        """Return a tar archive of that exact commit with a single root directory."""
        ...


def git_repository(value: str) -> str:
    """Validate a Git URL, SCP-style remote, or explicitly configured local path."""
    if not isinstance(value, str) or not value or value.startswith("-"):
        raise MacrostatesError("Git sources need an explicit repository URL or local path")
    if any(ord(char) < 32 or ord(char) == 127 for char in value):
        raise MacrostatesError("Git repository addresses must not contain control characters")
    parsed = urlparse(value)
    if parsed.scheme in {"https", "http", "ssh", "git", "file"}:
        if parsed.password or parsed.query or parsed.fragment:
            raise MacrostatesError(
                "Credentials and query parameters must not be stored in Git source addresses"
            )
        if parsed.scheme in {"http", "https"} and parsed.username:
            raise MacrostatesError("Use external Git authentication, not URL credentials")
        if parsed.scheme != "file" and not parsed.hostname:
            raise MacrostatesError("Git repository URL needs a host")
        if parsed.scheme == "file" and parsed.netloc not in {"", "localhost"}:
            raise MacrostatesError("File Git URLs must identify a local repository")
        if not parsed.path:
            raise MacrostatesError("Git repository URL needs a path")
        return value
    if re.fullmatch(r"(?:[A-Za-z0-9_.-]+@)?[A-Za-z0-9_.-]+:[^\s]+", value):
        return value
    if Path(value).is_absolute() or value.startswith(("./", "../")):
        return value
    raise MacrostatesError(
        "Unsupported Git repository address; use a Git URL or explicit local path"
    )


class GitSource:
    """Fetch an explicit annotated release tag using the user's Git authentication.

    Archives are materialized at the resolved commit, never a moving branch.
    Creating the provider performs no I/O; operations use temporary repositories.
    """

    def __init__(self, *, timeout: float = 120) -> None:
        self.timeout = timeout
        self._archives: dict[tuple[str, str], bytes] = {}

    def resolve(self, repository: str, tag: str) -> str:
        repository = git_repository(repository)
        if not re.fullmatch(r"v(?:0|[1-9][0-9]*)\.(?:0|[1-9][0-9]*)\.(?:0|[1-9][0-9]*)", tag):
            raise MacrostatesError("Git package sources require an explicit vMAJOR.MINOR.PATCH tag")
        with tempfile.TemporaryDirectory(prefix="macrostates-source-") as directory:
            root = Path(directory)
            environment = {**os.environ, "GIT_TERMINAL_PROMPT": "0"}

            def run(*args: str) -> str:
                try:
                    result = subprocess.run(
                        [
                            "git",
                            "-C",
                            str(root),
                            "-c",
                            "core.hooksPath=" + str(root / "no-hooks"),
                            *args,
                        ],
                        capture_output=True,
                        text=True,
                        timeout=self.timeout,
                        env=environment,
                        check=False,
                    )
                except (OSError, subprocess.SubprocessError) as exc:
                    raise MacrostatesError(
                        "Git source operation is unavailable or timed out"
                    ) from exc
                if result.returncode:
                    raise MacrostatesError(
                        "Git source operation failed; check access and the exact annotated release tag"
                    )
                return result.stdout.strip()

            run("init", "--quiet")
            run("remote", "add", "origin", repository)
            run("fetch", "--quiet", "--no-tags", "--depth=1", "origin", "refs/tags/" + tag)
            if run("cat-file", "-t", "FETCH_HEAD") != "tag":
                raise MacrostatesError("Git specification release tags must be annotated")
            selected = run("rev-parse", "FETCH_HEAD^{commit}")
            if not re.fullmatch(r"[0-9a-f]{40}|[0-9a-f]{64}", selected):
                raise MacrostatesError("Git returned an invalid package commit identity")
            archive = root / "snapshot.tar"
            run(
                "archive", "--format=tar", "--prefix=package/", "--output=" + str(archive), selected
            )
            if archive.stat().st_size > MAX_ARCHIVE:
                raise MacrostatesError("Git archive exceeds the download limit")
            self._archives[repository, selected] = archive.read_bytes()
            return selected

    def download(self, repository: str, commit: str) -> bytes:
        repository = git_repository(repository)
        try:
            return self._archives.pop((repository, commit))
        except KeyError as exc:
            raise MacrostatesError(
                "Resolve the exact Git release tag before downloading its commit"
            ) from exc


def github_repository(value: str) -> str:
    patterns = (
        r"https://github\.com/([A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+?)(?:\.git)?/?",
        r"git@github\.com:([A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+?)(?:\.git)?",
    )
    for pattern in patterns:
        match = re.fullmatch(pattern, value)
        if match:
            if any(part in (".", "..") for part in match[1].split("/")):
                break
            return match[1]
    raise MacrostatesError("Sources must use a credential-free github.com repository URL")


class SafeRedirect(HTTPRedirectHandler):
    def redirect_request(
        self, req: Request, fp: Any, code: int, msg: str, headers: Any, newurl: str
    ) -> Request | None:
        parsed = urlparse(newurl)
        if parsed.scheme != "https" or parsed.hostname not in (
            "github.com",
            "api.github.com",
            "codeload.github.com",
        ):
            raise MacrostatesError("GitHub archive redirected to an unsupported host")
        redirected = super().redirect_request(req, fp, code, msg, headers, newurl)
        if redirected and parsed.hostname != urlparse(req.full_url).hostname:
            redirected.remove_header("Authorization")
        return redirected


class GitHubSource:
    """Download GitHub snapshots using an explicit token, environment, or gh login.

    Creating this object performs no I/O. Credential lookup occurs only when a
    request is made. Passing token explicitly takes precedence over environment.
    """

    def __init__(self, *, token: str | None = None, timeout: float = 30) -> None:
        self._explicit_token = token
        self.timeout = timeout

    def _token(self) -> str | None:
        if self._explicit_token is not None:
            return self._explicit_token
        token = os.environ.get("GH_TOKEN") or os.environ.get("GITHUB_TOKEN")
        if token:
            return token
        if shutil.which("gh"):
            try:
                result = subprocess.run(
                    ["gh", "auth", "token", "--hostname", "github.com"],
                    capture_output=True,
                    text=True,
                    timeout=self.timeout,
                    check=False,
                )
            except (OSError, subprocess.SubprocessError) as exc:
                raise MacrostatesError("GitHub CLI credential lookup failed") from exc
            if result.returncode == 0:
                return result.stdout.strip()
        return None

    def _request(self, endpoint: str, *, archive: bool = False) -> bytes:
        try:
            user_agent = "macrostates-cli/" + version("macrostates-cli")
        except PackageNotFoundError:
            user_agent = "macrostates-cli"
        headers = {
            "Accept": "application/vnd.github+json",
            "User-Agent": user_agent,
            "X-GitHub-Api-Version": "2022-11-28",
        }
        token = self._token()
        if token:
            headers["Authorization"] = "Bearer " + token
        request = Request("https://api.github.com/" + endpoint, headers=headers)
        limit = MAX_ARCHIVE if archive else 2 * 1024 * 1024
        try:
            with build_opener(SafeRedirect()).open(request, timeout=self.timeout) as response:
                data = response.read(limit + 1)
        except HTTPError as exc:
            raise MacrostatesError(
                f"GitHub request failed (HTTP {exc.code}); check access and the release tag"
            ) from None
        except (URLError, OSError, ValueError) as exc:
            raise MacrostatesError(
                "GitHub request failed; check connectivity and authentication"
            ) from exc
        if len(data) > limit:
            raise MacrostatesError("GitHub response exceeds the download limit")
        return data

    def _json(self, endpoint: str) -> dict[str, Any]:
        try:
            result = json.loads(self._request(endpoint))
        except (ValueError, UnicodeError) as exc:
            raise MacrostatesError("Invalid GitHub API response") from exc
        if not isinstance(result, dict):
            raise MacrostatesError("Invalid GitHub API response")
        return result

    def resolve(self, repository: str, tag: str) -> str:
        repository_id = github_repository(repository)
        result = self._json(f"repos/{repository_id}/git/ref/tags/{quote(tag, safe='')}")
        for _ in range(8):
            obj = result.get("object", {})
            if not isinstance(obj, dict):
                raise MacrostatesError("GitHub returned an invalid tag object")
            sha = obj.get("sha")
            if not isinstance(sha, str) or not re.fullmatch(r"[0-9a-f]{40}|[0-9a-f]{64}", sha):
                raise MacrostatesError("GitHub returned an invalid object ID")
            if obj.get("type") == "commit":
                return sha
            if obj.get("type") != "tag":
                raise MacrostatesError("Release tag does not select a commit")
            result = self._json(f"repos/{repository_id}/git/tags/{sha}")
        raise MacrostatesError("Release tag nesting exceeds the supported depth")

    def download(self, repository: str, commit: str) -> bytes:
        repository_id = github_repository(repository)
        if not re.fullmatch(r"[0-9a-f]{40}|[0-9a-f]{64}", commit):
            raise MacrostatesError("Archive download requires a full commit ID")
        return self._request(f"repos/{repository_id}/tarball/{commit}", archive=True)
