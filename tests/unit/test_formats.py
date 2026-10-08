import copy
from pathlib import Path

import pytest
import yaml

from macrostates import MacrostatesError, Project
from macrostates._formats import read_composition, read_metadata
from macrostates._io import parse_yaml
from macrostates._sources import github_repository

from ..conftest import composition, metadata


@pytest.mark.parametrize("schema", [None, 0, 1])
def test_composition_versions_preserve_selection(schema):
    model = read_composition(composition(schema=schema))
    assert model.schema_version == (schema or 0)
    assert model.packages[0].name == "meta"
    assert model.authority_order == ("meta",)


@pytest.mark.parametrize("schema", [2, -1, "1", True])
def test_unknown_format_fails_before_initialization(tmp_path, schema):
    with pytest.raises(MacrostatesError):
        Project.initialize(tmp_path, manifest=composition(schema=schema))
    assert list(tmp_path.iterdir()) == []


@pytest.mark.parametrize(
    "field,value",
    [
        ("path", "../outside"),
        ("path", "/absolute"),
        ("path", "C:\\outside"),
        ("path", "main.md/child"),
        ("entrypoint", "../outside"),
    ],
)
def test_unsafe_paths_rejected(tmp_path, field, value):
    data = composition()
    data["packages"][0][field] = value
    with pytest.raises(MacrostatesError):
        Project.initialize(tmp_path, manifest=data)
    assert not list(tmp_path.iterdir())


def test_duplicate_and_overlapping_selections():
    data = composition(("meta", "process"))
    for path in ("000_meta", "000_meta/child", "000_META"):
        changed = copy.deepcopy(data)
        changed["packages"][1]["path"] = path
        with pytest.raises(MacrostatesError):
            read_composition(changed)


@pytest.mark.parametrize("text", ["project: a\nproject: b\n", "a: &a [*a]\n", "{[a]: b}"])
def test_unsafe_yaml_rejected(text):
    with pytest.raises(MacrostatesError):
        parse_yaml(text)


@pytest.mark.parametrize(
    "value",
    [
        "https://github.com/example/repo.git",
        "git@github.com:example/repo.git",
        "https://github.com/example/repo",
    ],
)
def test_repository_spellings(value):
    assert github_repository(value) == "example/repo"


def test_credentials_in_repository_are_rejected_without_echoing():
    secret_url = "https://user:example-secret@github.com/example/repo.git"
    with pytest.raises(MacrostatesError) as error:
        github_repository(secret_url)
    assert "example-secret" not in str(error.value)


HISTORICAL = yaml.safe_load(
    (Path(__file__).parents[1] / "fixtures/historical-metadata.yaml").read_text()
)

CURRENT = yaml.safe_load((Path(__file__).parents[1] / "fixtures/current-metadata.yaml").read_text())


@pytest.mark.parametrize("snapshot", HISTORICAL + CURRENT, ids=lambda value: value["release"])
def test_all_existing_release_metadata(snapshot):
    actual = read_metadata(snapshot["metadata"])
    assert actual.name == snapshot["name"]
    assert actual.version == snapshot["version"]


def test_future_metadata_requires_a_new_adapter():
    data = metadata()
    data["schema_version"] = 2
    with pytest.raises(MacrostatesError, match="metadata schema_version"):
        read_metadata(data)
