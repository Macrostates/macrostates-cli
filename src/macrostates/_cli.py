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
        ("identity", "Inspect finalized and development identities"),
        ("start-work", "Capture original development provenance"),
        ("deliverables", "Inspect optional application release policies"),
        ("change-create", "Create an explicit impact record"),
        ("change-check", "Check impact records and coverage evidence"),
        ("closure-request", "List workflows requiring definer closure authorization"),
        ("branch-status", "Inspect divergence against cached Git references"),
        ("branch-sync", "Explicitly fetch and merge or rebase a development branch"),
        ("integration-check", "Validate exact combined contents before integration"),
        ("release-plan", "Calculate a target-bound baseline release plan"),
        ("release-prepare", "Prepare candidate files from a reviewed release plan"),
        ("release-check", "Validate baseline release readiness"),
        ("migrate-versioning", "Explicitly migrate legacy baseline declarations"),
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
        elif command == "identity":
            sub.add_argument("--work", help="Explicit change/work identifier")
        elif command == "start-work":
            sub.add_argument("--id", required=True, dest="identifier")
            sub.add_argument(
                "--origin-commit", help="Explicit original commit for late provenance capture"
            )
        elif command == "change-create":
            sub.add_argument("--id", required=True, dest="identifier")
            sub.add_argument("--summary", required=True)
            sub.add_argument("--work", help="Previously captured work identifier")
            sub.add_argument(
                "--origin-commit", help="Explicit original commit when no work record exists"
            )
            for side in ("specification", "implementation"):
                sub.add_argument(
                    "--" + side + "-impact",
                    required=True,
                    choices=["none", "patch", "minor", "major"],
                )
            for label in ("deliverable", "evidence", "gap"):
                sub.add_argument("--" + label, action="append", default=[])
            sub.add_argument(
                "--requirements", type=Path, help="YAML document with a requirements coverage list"
            )
        elif command in {"branch-status", "integration-check", "release-check", "release-plan"}:
            sub.add_argument(
                "--target", help="Explicit target ref; defaults to the configured primary branch"
            )
            if command == "integration-check":
                sub.add_argument("--expected-target", help="Expected full target commit identity")
            if command == "release-check":
                sub.add_argument(
                    "--publication",
                    action="store_true",
                    help="Require integrated immutable annotated release tags",
                )
        elif command == "branch-sync":
            sub.add_argument("--target", required=True)
            sub.add_argument("--strategy", required=True, choices=["merge", "rebase"])
            sub.add_argument("--primary", help="Explicit primary branch override")
            sub.add_argument(
                "--fetch-remote", help="Explicit configured remote to fetch before synchronization"
            )
        elif command == "release-prepare":
            sub.add_argument("--plan", required=True, type=Path)
            sub.add_argument("--date", required=True, help="Finalization date YYYY-MM-DD")
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
                f"  {package['name']} {package['version']}: {package['path']} ({source.get('type', 'unspecified')})"
            )
            if source.get("repository"):
                print(f"    {source['repository']} @ {source['tag']}")
            for dependency in package.get("dependencies", []):
                print(
                    f"    requires {dependency['name']} {dependency['constraint']} {dependency['version']}"
                )
        print("Reading order: " + " → ".join(payload["reading_order"]))
        print("Authority (highest first): " + " → ".join(payload["authority_order"]))
        for scope in payload.get("directory_specifications", []):
            print(f"Directory scope: {scope['scope']}: {scope['entrypoint']}")
    else:
        if "message" in payload:
            print(payload["message"])
        else:
            print(json.dumps(payload, indent=2, ensure_ascii=False))


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
        payload: dict[str, Any] | None = None
        match arguments.command:
            case "identity":
                payload = project.identity(work=arguments.work)
            case "start-work":
                created = project.start_work(
                    arguments.identifier, origin_commit=arguments.origin_commit
                )
                payload = {
                    "path": created.relative_to(project.root).as_posix(),
                    "message": "Original provenance captured; keep it unchanged when incorporating upstream changes.",
                }
            case "deliverables":
                payload = {"deliverables": project.deliverables()}
            case "closure-request":
                payload = project.closure_request()
            case "branch-status":
                payload = project.branch_status(target=arguments.target)
            case "branch-sync":
                payload = project.sync_branch(
                    target=arguments.target,
                    strategy=arguments.strategy,
                    primary=arguments.primary,
                    fetch_remote=arguments.fetch_remote,
                )
            case "change-create":
                from ._io import read_yaml

                coverage = (
                    read_yaml(arguments.requirements).get("requirements", [])
                    if arguments.requirements
                    else []
                )
                created = project.create_change(
                    arguments.identifier,
                    arguments.summary,
                    specification=arguments.specification_impact,
                    implementation=arguments.implementation_impact,
                    deliverables=arguments.deliverable,
                    requirements=coverage,
                    evidence=arguments.evidence,
                    gaps=arguments.gap,
                    work=arguments.work,
                    origin_commit=arguments.origin_commit,
                )
                payload = {
                    "path": created.relative_to(project.root).as_posix(),
                    "message": "Change record created; review its impact and complete validation evidence before integration.",
                }
            case "release-plan":
                payload = project.plan_release(target=arguments.target)
            case "release-prepare":
                from ._io import read_yaml

                selected = read_yaml(arguments.plan)
                payload = project.prepare_release(
                    selected.get("plan", selected), date=arguments.date
                )
            case "migrate-versioning":
                payload = project.migrate_versioning()
        if payload is not None:
            display(payload, json_output=arguments.json)
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
            case "change-check":
                report = project.check_changes()
            case "integration-check":
                report = project.check_integration(
                    target=arguments.target, expected_target=arguments.expected_target
                )
            case "release-check":
                report = project.check_release(
                    target=arguments.target, publication=arguments.publication
                )
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
