import io
import json
from urllib.error import HTTPError
from urllib.request import Request

import pytest

from macrostates import GitHubSource, MacrostatesError
from macrostates._sources import SafeRedirect


class FakeOpener:
    def __init__(self, responses):
        self.responses = iter(responses)
        self.requests = []

    def open(self, request, *, timeout):
        self.requests.append(request)
        response = next(self.responses)
        if isinstance(response, Exception):
            raise response
        return io.BytesIO(response)


def configure(monkeypatch, responses):
    opener = FakeOpener(responses)
    monkeypatch.setattr("macrostates._sources.build_opener", lambda *args: opener)
    return opener


def test_annotated_tag_resolves_before_archive_download(monkeypatch):
    commit = "a" * 40
    tag = "b" * 40
    opener = configure(
        monkeypatch,
        [
            json.dumps({"object": {"type": "tag", "sha": tag}}).encode(),
            json.dumps({"object": {"type": "commit", "sha": commit}}).encode(),
            b"archive",
        ],
    )
    source = GitHubSource(token="test-token")
    assert source.resolve("git@github.com:example/specs.git", "v1.0.0") == commit
    assert source.download("https://github.com/example/specs.git", commit) == b"archive"
    assert opener.requests[0].full_url.endswith("/git/ref/tags/v1.0.0")
    assert opener.requests[2].full_url.endswith("/tarball/" + commit)
    assert opener.requests[0].get_header("Authorization") == "Bearer test-token"


@pytest.mark.parametrize(
    "response",
    [
        b"not-json",
        b"[]",
        b'{"object": []}',
        b'{"object": {"sha":"invalid"}}',
        b'{"object": {"sha":"aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa","type":"blob"}}',
    ],
)
def test_invalid_github_responses_are_controlled_errors(monkeypatch, response):
    configure(monkeypatch, [response])
    with pytest.raises(MacrostatesError):
        GitHubSource(token="").resolve("https://github.com/example/specs", "v1.0.0")


def test_http_error_does_not_echo_sensitive_response(monkeypatch):
    configure(
        monkeypatch, [HTTPError("https://api.github.com/", 403, "sensitive response", {}, None)]
    )
    with pytest.raises(MacrostatesError) as error:
        GitHubSource(token="test-token").resolve("https://github.com/example/specs", "v1.0.0")
    assert "HTTP 403" in str(error.value)
    assert "sensitive response" not in str(error.value)
    assert "test-token" not in str(error.value)


def test_redirect_strips_authentication_on_host_change():
    request = Request(
        "https://api.github.com/repos/example/specs/tarball/commit",
        headers={"Authorization": "Bearer test-token"},
    )
    redirected = SafeRedirect().redirect_request(
        request, None, 302, "Found", {}, "https://codeload.github.com/example/specs/tar.gz/commit"
    )
    assert redirected is not None
    assert redirected.get_header("Authorization") is None


@pytest.mark.parametrize(
    "url", ["http://codeload.github.com/example/specs", "https://untrusted.example/archive"]
)
def test_untrusted_redirects_rejected(url):
    with pytest.raises(MacrostatesError):
        SafeRedirect().redirect_request(
            Request("https://api.github.com/"), None, 302, "Found", {}, url
        )


def test_explicit_credentials_take_precedence(monkeypatch):
    monkeypatch.setenv("GH_TOKEN", "environment-token")
    opener = configure(
        monkeypatch,
        [b'{"object":{"type":"commit","sha":"aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"}}'],
    )
    GitHubSource(token="explicit-token").resolve("https://github.com/example/specs", "v1.0.0")
    assert opener.requests[0].get_header("Authorization") == "Bearer explicit-token"
