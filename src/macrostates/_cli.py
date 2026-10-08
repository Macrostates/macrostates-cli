"""Thin argparse interface over the public project API."""

import argparse
import json
import logging
import sys
from collections.abc import Sequence
from dataclasses import asdict
from pathlib import Path
from typing import Any

from . import Project, Report, __version__
from ._models import MacrostatesError


def parser() -> argparse.ArgumentParser:
    result = argparse.ArgumentParser(
        prog="macrostates", description="Compose, install and check Macrostates specifications."
    )
    result.add_argument("--version", action="version", version=f"macrostates {__version__}")
    result.add_argument(
        "--project", default=".", help="Project directory (default: current directory)"
    )
    result.add_argument("--json", action="store_true", help="Output structured JSON")
    commands = result.add_subparsers(dest="command", required=True)
    for command, description in (
        ("init", "Prepare project specification files"),
        ("install", "Install selected archive packages"),
        ("lock", "Verify existing copies against source and record integrity"),
        ("verify", "Check package integrity offline"),
        ("lint", "Check specification structure offline"),
        ("info", "Show composition and package dependencies"),
        ("check", "Run lint and integrity verification"),
    ):
        sub = commands.add_parser(command, help=description)
        sub.add_argument("--project", default=argparse.SUPPRESS)
        sub.add_argument("--json", action="store_true", default=argparse.SUPPRESS)
        if command == "init":
            sub.add_argument("--name", help="Project name when selecting packages")
            sub.add_argument(
                "--package",
                action="append",
                default=[],
                metavar="NAME@VERSION",
                help="Explicit package selection, repeatable",
            )
            sub.add_argument(
                "--from",
                dest="manifest",
                type=Path,
                help="Copy a supplied composition, preserving extension fields",
            )
            sub.add_argument("--layout", choices=["modern", "legacy"], default="modern")
        elif command == "install":
            sub.add_argument(
                "--locked", action="store_true", help="Require existing, unchanged lock selections"
            )
        elif command == "check":
            sub.add_argument(
                "--staged", action="store_true", help="Check the Git index instead of working files"
            )
    return result


def display(payload: dict[str, Any], *, json_output: bool) -> None:
    if json_output:
        print(json.dumps(payload, indent=2, ensure_ascii=False))
        return
    if "diagnostics" in payload:
        for diagnostic in payload["diagnostics"]:
            path = f" ({diagnostic['path']})" if diagnostic["path"] else ""
            print(f"{diagnostic['severity']}: [{diagnostic['code']}] {diagnostic['message']}{path}")
        print("Checks passed." if payload["ok"] else "Checks failed.")
    elif "packages" in payload:
        print(
            f"Project: {payload['project']}\nSpecifications: {payload['specs']}\nFormat: {payload['schema_version']}"
        )
        for package in payload["packages"]:
            source = package["source"]
            print(
                f"  {package['name']} {package['version']} — {package['path']} ({source.get('type', 'unspecified')})"
            )
            if source.get("repository"):
                print(f"    {source['repository']} @ {source['tag']}")
            for dependency in package.get("dependencies", []):
                print(
                    f"    requires {dependency['name']} {dependency['constraint']} {dependency['version']}"
                )
        print("Reading order: " + " → ".join(payload["reading_order"]))
        print("Authority (highest first): " + " → ".join(payload["authority_order"]))
    else:
        print(payload.get("message", "Done."))


def main(argv: Sequence[str] | None = None) -> int:
    arguments = parser().parse_args(argv)
    logging.basicConfig(level=logging.WARNING)
    try:
        if arguments.command == "init":
            packages = []
            for selection in arguments.package:
                parts = selection.rsplit("@", 1)
                if len(parts) != 2:
                    raise MacrostatesError("Package selections must be NAME@VERSION")
                packages.append((parts[0], parts[1]))
            project = Project.initialize(
                arguments.project,
                name=arguments.name,
                packages=packages,
                manifest=arguments.manifest,
                layout=arguments.layout,
            )
            display(
                {
                    "ok": True,
                    "message": f"Initialized {project.specs.relative_to(project.root).as_posix()}; review authority and reading order, then run macrostates install.",
                },
                json_output=arguments.json,
            )
            return 0
        project = Project.open(arguments.project)
        if arguments.command == "info":
            display(project.info(), json_output=arguments.json)
            return 0
        report: Report
        match arguments.command:
            case "install":
                report = project.install(locked=arguments.locked)
            case "lock":
                report = project.lock()
            case "verify":
                report = project.verify()
            case "lint":
                report = project.lint()
            case "check":
                report = project.check(staged=arguments.staged)
            case _:
                raise MacrostatesError("Unknown command")
        display(
            {"ok": report.ok, "diagnostics": [asdict(item) for item in report.diagnostics]},
            json_output=arguments.json,
        )
        return 0 if report.ok else 1
    except (MacrostatesError, OSError, UnicodeError) as exc:
        if arguments.json:
            print(
                json.dumps(
                    {"ok": False, "error": {"code": "operation.invalid", "message": str(exc)}}
                )
            )
        else:
            print(f"error: {exc}", file=sys.stderr)
        return 2
    except KeyboardInterrupt:
        print("Operation interrupted.", file=sys.stderr)
        return 130
