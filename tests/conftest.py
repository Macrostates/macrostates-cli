import hashlib
import io
import tarfile
from pathlib import Path

import pytest
import yaml

from macrostates import Project


def metadata(name="meta", version="1.0.0", *, dependencies=None, optional=None):
    return {
        "name": name,
        "version": version,
        "versioned_at": "2026-01-01 12:00",
        "description": "Synthetic test specification.",
        "entrypoint": "README.md",
        "dependencies": dependencies or [],
        "optional_dependencies": optional or [],
    }


def archive(files, *, modes=None):
    buffer = io.BytesIO()
    with tarfile.open(fileobj=buffer, mode="w:gz") as stream:
        for path, content in files.items():
            info = tarfile.TarInfo("snapshot/" + path)
            data = content.encode() if isinstance(content, str) else content
            info.size = len(data)
            info.mode = (modes or {}).get(path, 0o644)
            stream.addfile(info, io.BytesIO(data))
    return buffer.getvalue()


class FakeSource:
    def __init__(self):
        self.tags = {}
        self.archives = {}
        self.calls = []

    def add(
        self,
        name="meta",
        version="1.0.0",
        *,
        dependencies=None,
        optional=None,
        extra=None,
        text="# Test specifications\n",
        modes=None,
    ):
        repository = f"https://github.com/example/{name}.git"
        files = {
            "package.yaml": yaml.safe_dump(
                metadata(name, version, dependencies=dependencies, optional=optional)
            ),
            "README.md": text,
            **(extra or {}),
        }
        payload = archive(files, modes=modes)
        commit = hashlib.sha1(payload).hexdigest()
        self.tags[(repository, "v" + version)] = commit
        self.archives[commit] = payload
        return repository, commit

    def resolve(self, repository, tag):
        self.calls.append(("resolve", repository, tag))
        return self.tags[(repository, tag)]

    def download(self, repository, commit):
        self.calls.append(("download", repository, commit))
        return self.archives[commit]


def composition(names=("meta",), *, versions=None, schema=1, source_type="github-archive"):
    packages = []
    for index, name in enumerate(names):
        selected = (versions or {}).get(name, "1.0.0")
        source = {
            "type": source_type,
            "repository": f"https://github.com/example/{name}.git",
            "tag": "v" + selected,
        }
        path = f"{index:03d}_{name}"
        if source_type == "git-subtree":
            source.update(branch="main", prefix="specs/" + path)
        packages.append(
            {
                "name": name,
                "version": selected,
                "path": path,
                "entrypoint": "README.md",
                "source": source,
            }
        )
    data = {
        "project": {"name": "example", "entrypoint": "main.md"},
        "packages": packages,
        "authority_order": list(names),
        "reading_order": list(names),
    }
    if schema is not None:
        data["schema_version"] = schema
    return data


@pytest.fixture
def source():
    result = FakeSource()
    result.add()
    return result


@pytest.fixture
def project(tmp_path: Path, source: FakeSource):
    result = Project.initialize(tmp_path, manifest=composition(), source=source)
    assert result.install().ok
    return result
