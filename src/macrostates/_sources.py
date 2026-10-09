"""GitHub transport. Tokens never enter manifests, locks, URLs or diagnostics."""

import json
import os
import re
import shutil
import subprocess
from importlib.metadata import PackageNotFoundError, version
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
