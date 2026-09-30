#!/usr/bin/env python3
"""Prompt Library 카탈로그 생성 및 메타데이터 검증기.

외부 의존성 없이 Markdown 파일의 간단한 YAML front matter를 읽어
CATALOG.md를 생성한다.
"""

from __future__ import annotations

import argparse
import re
import sys
from collections import Counter
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
CATALOG_PATH = ROOT / "CATALOG.md"

EXCLUDED_TOP_LEVEL = {
    ".git",
    ".github",
    "cases",
    "scripts",
    "templates",
}
EXCLUDED_FILES = {"README.md", "CATALOG.md"}
ALLOWED_STATUS = {"VERIFIED", "EXPERIMENTAL", "DEPRECATED"}
ALLOWED_LANGUAGES = {"ko", "en", "any"}
DOMAIN_LABELS = {
    "image": "이미지",
    "music": "음악",
    "video": "비디오",
    "text": "텍스트",
    "agents": "에이전트",
}
LANGUAGE_LABELS = {"ko": "한글", "en": "영문", "any": "무관"}


class MetadataError(ValueError):
    pass


def _scalar(value: str) -> Any:
    value = value.strip()
    if not value:
        return ""
    if (value.startswith('"') and value.endswith('"')) or (
        value.startswith("'") and value.endswith("'")
    ):
        return value[1:-1]
    if value.lower() == "true":
        return True
    if value.lower() == "false":
        return False
    return value


def parse_front_matter(text: str, path: Path) -> dict[str, Any]:
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        raise MetadataError("YAML front matter가 없습니다.")

    try:
        end = next(i for i in range(1, len(lines)) if lines[i].strip() == "---")
    except StopIteration as exc:
        raise MetadataError("YAML front matter 종료 구분자(---)가 없습니다.") from exc

    metadata: dict[str, Any] = {}
    current_key: str | None = None

    for raw in lines[1:end]:
        if not raw.strip() or raw.lstrip().startswith("#"):
            continue

        indent = len(raw) - len(raw.lstrip(" "))
        stripped = raw.strip()

        if indent == 0 and ":" in raw:
            key, value = raw.split(":", 1)
            key = key.strip()
            value = value.strip()
            current_key = key
            metadata[key] = _scalar(value) if value else None
            continue

        if indent > 0 and stripped.startswith("-") and current_key:
            item = _scalar(stripped[1:].strip())
            if metadata.get(current_key) is None:
                metadata[current_key] = []
            if not isinstance(metadata[current_key], list):
                raise MetadataError(
                    f"{current_key}: 스칼라와 목록을 함께 사용할 수 없습니다."
                )
            metadata[current_key].append(item)
            continue

        # locks 같은 중첩 mapping은 카탈로그에 필요하지 않으므로 읽지 않는다.
        if indent > 0:
            continue

        raise MetadataError(f"해석할 수 없는 front matter 행: {raw}")

    return metadata


def prompt_files() -> list[Path]:
    files: list[Path] = []
    for path in ROOT.rglob("*.md"):
        rel = path.relative_to(ROOT)
        if rel.name in EXCLUDED_FILES:
            continue
        if rel.parts and rel.parts[0] in EXCLUDED_TOP_LEVEL:
            continue
        files.append(path)
    return sorted(files)


def has_heading(text: str, heading: str) -> bool:
    return re.search(rf"(?mi)^##\s+{re.escape(heading)}\s*$", text) is not None


def validate(path: Path, metadata: dict[str, Any], text: str) -> list[str]:
    errors: list[str] = []
    rel = path.relative_to(ROOT)

    required = [
        "id",
        "title",
        "status",
        "category",
        "task",
        "recommended_prompt_language",
        "prompt_languages",
    ]
    for key in required:
        if metadata.get(key) in (None, "", []):
            errors.append(f"필수 metadata 누락: {key}")

    status = str(metadata.get("status", ""))
    if status and status not in ALLOWED_STATUS:
        errors.append(
            f"status는 {sorted(ALLOWED_STATUS)} 중 하나여야 합니다: {status}"
        )

    language = str(metadata.get("recommended_prompt_language", ""))
    if language and language not in ALLOWED_LANGUAGES:
        errors.append(
            "recommended_prompt_language는 "
            f"{sorted(ALLOWED_LANGUAGES)} 중 하나여야 합니다: {language}"
        )

    domain = str(metadata.get("domain") or (rel.parts[0] if rel.parts else ""))
    if metadata.get("domain") and rel.parts and domain != rel.parts[0]:
        errors.append(
            f"domain({domain})이 최상위 디렉터리({rel.parts[0]})와 일치하지 않습니다."
        )

    prompt_languages = metadata.get("prompt_languages") or []
    if not isinstance(prompt_languages, list):
        errors.append("prompt_languages는 목록이어야 합니다.")
        prompt_languages = []

    # 저장소 언어 정책: 한글 권장일 때만 영문 병기 생략 가능.
    if language == "ko":
        if "ko" not in prompt_languages or not has_heading(text, "프롬프트 — 한글"):
            errors.append(
                "한글 권장 프롬프트에는 '프롬프트 — 한글' 섹션이 필요합니다."
            )
    elif language in {"en", "any"}:
        if "ko" not in prompt_languages or not has_heading(text, "프롬프트 — 한글"):
            errors.append(
                "영문/무관 권장 프롬프트에는 한글 병기 섹션이 필요합니다."
            )
        if "en" not in prompt_languages or not has_heading(text, "Prompt — English"):
            errors.append(
                "영문/무관 권장 프롬프트에는 영문 프롬프트 섹션이 필요합니다."
            )

    if status == "VERIFIED":
        if not metadata.get("verified_at"):
            errors.append("VERIFIED 프롬프트에는 verified_at이 필요합니다.")
        if not metadata.get("model_family"):
            errors.append("VERIFIED 프롬프트에는 model_family가 필요합니다.")

    return errors


def escape_table(value: Any) -> str:
    if value in (None, ""):
        return "-"
    return str(value).replace("|", "\\|").replace("\n", " ")


def build_catalog(records: list[dict[str, Any]]) -> str:
    status_counts = Counter(r["status"] for r in records)
    domain_counts = Counter(r["domain"] for r in records)

    lines = [
        "# Prompt Catalog",
        "",
        "> 이 파일은 `scripts/build_catalog.py`가 자동 생성합니다. 직접 수정하지 마십시오.",
        "",
        "## 요약",
        "",
        f"- 총 프롬프트: **{len(records)}**",
    ]

    for status in ("VERIFIED", "EXPERIMENTAL", "DEPRECATED"):
        lines.append(f"- {status}: **{status_counts.get(status, 0)}**")

    if domain_counts:
        lines.extend(["", "### 분야별", ""])
        for domain in sorted(domain_counts):
            label = DOMAIN_LABELS.get(domain, domain)
            lines.append(f"- {label}: **{domain_counts[domain]}**")

    lines.extend(
        [
            "",
            "## 카탈로그",
            "",
            "| ID | 분야 | 카테고리 | 작업 | 제목 | 상태 | 권장 언어 | 검증 모델 | 태그 |",
            "|---|---|---|---|---|---|---|---|---|",
        ]
    )

    for r in records:
        tags = r.get("tags") or []
        if isinstance(tags, list):
            tags_text = ", ".join(str(x) for x in tags) or "-"
        else:
            tags_text = str(tags)

        title_link = f"[{escape_table(r['title'])}]({r['path']})"
        row = [
            escape_table(r["id"]),
            escape_table(DOMAIN_LABELS.get(r["domain"], r["domain"])),
            escape_table(r["category"]),
            escape_table(r["task"]),
            title_link,
            escape_table(r["status"]),
            escape_table(
                LANGUAGE_LABELS.get(
                    r["recommended_prompt_language"],
                    r["recommended_prompt_language"],
                )
            ),
            escape_table(r.get("model_family")),
            escape_table(tags_text),
        ]
        lines.append("| " + " | ".join(row) + " |")

    lines.extend(
        [
            "",
            "## 메타데이터 규칙",
            "",
            "- `status`: `VERIFIED`, `EXPERIMENTAL`, `DEPRECATED` 중 하나",
            "- `recommended_prompt_language`: `ko`, `en`, `any` 중 하나",
            "- `VERIFIED`는 `verified_at`과 `model_family` 필수",
            "- 권장 언어가 `en` 또는 `any`이면 한글/영문 프롬프트를 모두 포함",
            "- 권장 언어가 `ko`이면 영문 프롬프트 생략 가능",
            "",
        ]
    )
    return "\n".join(lines)


def collect() -> tuple[list[dict[str, Any]], list[str]]:
    records: list[dict[str, Any]] = []
    errors: list[str] = []
    seen_ids: dict[str, Path] = {}

    for path in prompt_files():
        rel = path.relative_to(ROOT)
        text = path.read_text(encoding="utf-8")
        try:
            metadata = parse_front_matter(text, path)
        except MetadataError as exc:
            errors.append(f"{rel}: {exc}")
            continue

        for error in validate(path, metadata, text):
            errors.append(f"{rel}: {error}")

        prompt_id = str(metadata.get("id", ""))
        if prompt_id:
            if prompt_id in seen_ids:
                errors.append(
                    f"{rel}: 중복 ID {prompt_id} "
                    f"(기존: {seen_ids[prompt_id].relative_to(ROOT)})"
                )
            else:
                seen_ids[prompt_id] = path

        domain = str(metadata.get("domain") or rel.parts[0])
        records.append(
            {
                **metadata,
                "domain": domain,
                "path": rel.as_posix(),
            }
        )

    records.sort(
        key=lambda r: (str(r.get("domain", "")), str(r.get("id", "")))
    )
    return records, errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--check",
        action="store_true",
        help="CATALOG.md를 수정하지 않고 최신 상태인지 검사합니다.",
    )
    args = parser.parse_args()

    records, errors = collect()
    if errors:
        print("메타데이터 검증 실패:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1

    catalog = build_catalog(records)

    if args.check:
        current = (
            CATALOG_PATH.read_text(encoding="utf-8")
            if CATALOG_PATH.exists()
            else ""
        )
        if current != catalog:
            print("CATALOG.md가 최신 상태가 아닙니다.", file=sys.stderr)
            return 1
        print(f"CATALOG.md 확인 완료: {len(records)}개 프롬프트")
        return 0

    CATALOG_PATH.write_text(catalog, encoding="utf-8")
    print(f"CATALOG.md 생성 완료: {len(records)}개 프롬프트")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
