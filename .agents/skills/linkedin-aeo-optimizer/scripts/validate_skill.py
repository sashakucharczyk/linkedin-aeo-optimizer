#!/usr/bin/env python3
"""Validate the portable LinkedIn AEO Optimizer skill without dependencies."""

from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path
from urllib.parse import unquote, urlsplit


SKILL_DIR = Path(__file__).resolve().parent.parent
REPO_ROOT = SKILL_DIR.parents[2]

REQUIRED_SKILL_FILES = (
    "SKILL.md",
    "references/methodology.md",
    "references/positioning-profile.example.md",
    "assets/post-template.md",
    "scripts/validate_skill.py",
)

REQUIRED_REPO_FILES = (
    "AGENTS.md",
    "README.md",
    ".gitignore",
    ".github/workflows/validate-skill.yml",
    "posts/drafts/.gitkeep",
    "posts/published/.gitkeep",
)

PRIVATE_PROBES = (
    "private/positioning-profile.md",
    "private/experiments.md",
    "private/.validation/nested-probe.txt",
)

FRONTMATTER_FIELD = re.compile(r"^([A-Za-z][A-Za-z0-9_-]*):\s*(.*?)\s*$")
SKILL_NAME = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
MARKDOWN_LINK = re.compile(r"!?\[[^\]]*\]\(([^)]+)\)")


def read_text(path: Path, errors: list[str]) -> str:
    try:
        return path.read_text(encoding="utf-8-sig")
    except (OSError, UnicodeError) as exc:
        errors.append(f"Cannot read {path.relative_to(REPO_ROOT)}: {exc}")
        return ""


def parse_scalar(value: str, key: str, line_number: int, errors: list[str]) -> str:
    """Parse the flat, one-line string subset accepted by this validator."""
    value = value.strip()
    if not value:
        errors.append(
            f"SKILL.md frontmatter field '{key}' on line {line_number} is empty."
        )
        return ""

    if value[0] in {"'", '"'}:
        if len(value) < 2 or value[-1] != value[0]:
            errors.append(
                f"SKILL.md frontmatter field '{key}' on line {line_number} has an unmatched quote."
            )
            return ""
        scalar = value[1:-1]
        if not scalar.strip():
            errors.append(
                f"SKILL.md frontmatter field '{key}' on line {line_number} is empty."
            )
        return scalar

    lowered = value.lower()
    unsupported_starts = ("[", "{", "|", ">", "&", "*", "!", "%", "@", "`", "#")
    if (
        value.startswith(unsupported_starts)
        or value.startswith(("- ", "? ", ": "))
        or lowered in {"null", "~", "true", "false"}
        or re.search(r":\s", value)
    ):
        errors.append(
            f"SKILL.md frontmatter field '{key}' on line {line_number} must be a one-line string scalar."
        )
        return ""

    if " #" in value:
        value = value.split(" #", maxsplit=1)[0].rstrip()
    return value


def parse_frontmatter(text: str, errors: list[str]) -> dict[str, str]:
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        errors.append("SKILL.md must start with YAML frontmatter delimited by ---. ")
        return {}

    try:
        closing_index = next(
            index for index, line in enumerate(lines[1:], start=1) if line.strip() == "---"
        )
    except StopIteration:
        errors.append("SKILL.md frontmatter is missing its closing --- delimiter.")
        return {}

    fields: dict[str, str] = {}
    for line_number, line in enumerate(lines[1:closing_index], start=2):
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        if line[:1].isspace():
            errors.append(
                f"SKILL.md frontmatter line {line_number} is indented; only flat key/value fields are supported."
            )
            continue
        match = FRONTMATTER_FIELD.fullmatch(line)
        if not match:
            errors.append(
                f"SKILL.md frontmatter line {line_number} is not a simple YAML key/value field."
            )
            continue
        key, raw_value = match.groups()
        if key in fields:
            errors.append(f"SKILL.md frontmatter repeats the '{key}' field.")
            continue
        fields[key] = parse_scalar(raw_value, key, line_number, errors)

    return fields


def validate_frontmatter(skill_text: str, errors: list[str]) -> None:
    fields = parse_frontmatter(skill_text, errors)
    name = fields.get("name", "")
    description = fields.get("description", "")

    if not name:
        errors.append("SKILL.md frontmatter requires a nonempty 'name'.")
    elif not SKILL_NAME.fullmatch(name):
        errors.append("SKILL.md 'name' must use lowercase kebab-case.")
    elif name != SKILL_DIR.name:
        errors.append(
            f"SKILL.md name '{name}' must match its directory '{SKILL_DIR.name}'."
        )

    if not description:
        errors.append("SKILL.md frontmatter requires a nonempty 'description'.")


def local_link_targets(markdown: str) -> list[str]:
    targets: list[str] = []
    for raw_target in MARKDOWN_LINK.findall(markdown):
        target = raw_target.strip()
        if target.startswith("<") and ">" in target:
            target = target[1 : target.index(">")]
        else:
            target = target.split(maxsplit=1)[0]

        parsed = urlsplit(target)
        if not target or target.startswith("#") or parsed.scheme or parsed.netloc:
            continue
        targets.append(unquote(parsed.path))
    return targets


def validate_links(skill_text: str, errors: list[str]) -> int:
    targets = local_link_targets(skill_text)
    for target in targets:
        link_path = (SKILL_DIR / target).resolve()
        try:
            link_path.relative_to(SKILL_DIR)
        except ValueError:
            errors.append(f"SKILL.md local reference escapes the skill directory: {target}")
            continue
        if not link_path.is_file():
            errors.append(f"SKILL.md references a missing local file: {target}")
    return len(targets)


def run_git(*args: str) -> subprocess.CompletedProcess[str]:
    try:
        return subprocess.run(
            ["git", "-C", str(REPO_ROOT), *args],
            check=False,
            capture_output=True,
            text=True,
        )
    except OSError as exc:
        return subprocess.CompletedProcess(
            args=["git", *args], returncode=127, stdout="", stderr=str(exc)
        )


def validate_private_ignores(errors: list[str]) -> None:
    gitignore = read_text(REPO_ROOT / ".gitignore", errors)
    patterns = [
        line.strip()
        for line in gitignore.splitlines()
        if line.strip() and not line.lstrip().startswith("#")
    ]
    if "/private/" not in patterns:
        errors.append(".gitignore must contain the repository-root rule '/private/'.")

    private_negations = [
        pattern
        for pattern in patterns
        if pattern.startswith("!")
        and pattern[1:].lstrip("/").startswith("private/")
    ]
    if private_negations:
        errors.append(
            ".gitignore must not re-include paths under private/: "
            + ", ".join(private_negations)
        )

    tracked = run_git("ls-files", "--", "private/")
    if tracked.returncode != 0:
        detail = tracked.stderr.strip() or "unknown Git error"
        errors.append(f"Cannot inspect tracked private files: {detail}")
    elif tracked.stdout.strip():
        listed = ", ".join(tracked.stdout.splitlines())
        errors.append(f"Files under private/ are tracked by Git: {listed}")

    probes = set(PRIVATE_PROBES)
    private_dir = REPO_ROOT / "private"
    if private_dir.is_dir():
        probes.update(
            path.relative_to(REPO_ROOT).as_posix()
            for path in private_dir.rglob("*")
            if path.is_file()
        )

    for probe in sorted(probes):
        result = run_git("check-ignore", "--no-index", "--quiet", "--", probe)
        if result.returncode == 1:
            errors.append(f"Git does not ignore {probe}.")
        elif result.returncode != 0:
            detail = result.stderr.strip() or "unknown Git error"
            errors.append(f"Cannot verify Git ignore status for {probe}: {detail}")


def main() -> int:
    errors: list[str] = []

    for relative_path in REQUIRED_SKILL_FILES:
        path = SKILL_DIR / relative_path
        if not path.is_file():
            errors.append(f"Missing required skill file: {path.relative_to(REPO_ROOT)}")

    for relative_path in REQUIRED_REPO_FILES:
        path = REPO_ROOT / relative_path
        if not path.is_file():
            errors.append(f"Missing required repository file: {relative_path}")

    skill_text = ""
    skill_path = SKILL_DIR / "SKILL.md"
    if skill_path.is_file():
        skill_text = read_text(skill_path, errors)
        if skill_text:
            validate_frontmatter(skill_text, errors)

    reference_count = validate_links(skill_text, errors) if skill_text else 0
    validate_private_ignores(errors)

    if errors:
        print("Skill validation failed:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1

    total_required = len(REQUIRED_SKILL_FILES) + len(REQUIRED_REPO_FILES)
    print(
        "Skill validation passed: "
        f"{total_required} required files, {reference_count} local references, "
        f"and {len(PRIVATE_PROBES)} private ignore probes checked."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
