import importlib.util
from pathlib import Path

import pytest

import macrostates


def load_build_version(tmp_path, declaration):
    # Exercise the standalone helper as setuptools loads it in build isolation.
    module_path = tmp_path / "src/macrostates/_build_version.py"
    module_path.parent.mkdir(parents=True)
    module_path.write_bytes((Path(macrostates.__file__).parent / "_build_version.py").read_bytes())
    release = tmp_path / ".macrostates/implementation/release.yaml"
    release.parent.mkdir(parents=True)
    release.write_text(declaration)
    spec = importlib.util.spec_from_file_location("isolated_build_version", module_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.VERSION


def test_build_uses_release_declaration_without_installed_application(tmp_path):
    assert (
        load_build_version(
            tmp_path, 'version: "4.5.8"\nspecification: "spec-4.5.2"\nrelease_date: "2026-10-08"\n'
        )
        == "4.5.8"
    )


@pytest.mark.parametrize(
    "declaration",
    [
        'version: "1.2.0"\nspecification: "spec-1.3.0"\nrelease_date: "2026-10-08"\n',
        'version: "1.2.0"\nspecification: "spec-1.2.0"\nrelease_date: "2026-02-30"\n',
        'version: "1.2.0"\nversion: "1.2.1"\n',
        'version: "1.2.0-dev"\nspecification: "spec-1.2.0"\nrelease_date: "2026-10-08"\n',
        'version: "1.2.0"\nspecification: "1.2.0"\nrelease_date: "2026-10-08"\n',
    ],
)
def test_invalid_build_declaration_never_falls_back(tmp_path, declaration):
    with pytest.raises(ValueError):
        load_build_version(tmp_path, declaration)
