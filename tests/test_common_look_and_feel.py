from __future__ import annotations

import re
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / ".agents" / "skills" / "common-look-and-feel"
SKILL_MD = SKILL / "SKILL.md"
REFERENCE = SKILL / "references" / "asia-allied-baseline.md"
TEMPLATE = SKILL / "templates" / "admin-cms.html"
EXPECTED_COLORS = {
    "primary": "#006a63",
    "primary-dark": "#003531",
    "primary-active": "#001c19",
    "accent": "#e6762d",
    "accent-accessible": "#b15315",
    "accent-selected": "#733208",
    "text-on-accent": "#001c19",
    "text": "#333333",
    "text-muted": "#6c757d",
    "surface": "#ffffff",
    "surface-subtle": "#f7f7f7",
    "surface-muted": "#ececec",
    "surface-disabled": "#eaeaea",
    "border": "#cecece",
    "table-header": "#fff2ea",
    "focus": "#006a63",
    "danger": "#dc3545",
    "success": "#006a63",
    "logo-orange": "#f7941d",
    "logo-olive": "#7b7a1b",
}
EXPECTED_RADII = {
    "none": "0px",
    "sm": "2px",
    "md": "4px",
    "pill": "999px",
}


class TemplateParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.start_tags: list[tuple[str, dict[str, str | None]]] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        self.start_tags.append((tag, dict(attrs)))


def test_skill_metadata_and_source_precedence_are_explicit() -> None:
    skill = SKILL_MD.read_text(encoding="utf-8")
    frontmatter = skill.split("---", 2)[1]

    assert re.search(r"^name: common-look-and-feel$", frontmatter, re.MULTILINE)
    description = re.search(r"^description: (.+)$", frontmatter, re.MULTILINE)
    assert description is not None
    assert description.group(1).startswith("Use when ")
    assert len(description.group(1)) <= 57
    for field in ("version:", "author:", "license:", "metadata:"):
        assert field in frontmatter

    assert "Root `DESIGN.md` defines normative visual tokens" in skill
    assert "Never hand-edit them" in skill
    assert "not an official corporate brand manual" in skill
    assert "Only the Admin / CMS profile has a bundled HTML reference" in skill
    assert "never imply a missing template exists" in skill
    assert "loading, empty, error, unauthorized, pending" in skill
    assert "Traditional Chinese" in skill
    assert skill.index("Product requirements") < skill.index("templates/admin-cms.html")
    for artifact in (
        "design-system/foundation.css",
        "design-system/theme.css",
        "design-system/tailwind.preset.cjs",
        "design-system/tailwind.theme.json",
        "design-system/tokens.json",
        "design-system/components.json",
    ):
        assert artifact in skill
        assert (ROOT / artifact).is_file()


def test_reference_records_bounded_evidence_and_usage_limits() -> None:
    reference = REFERENCE.read_text(encoding="utf-8")

    for phrase in (
        "10,669",
        "10,666",
        "559 locale-specific route signatures",
        "43 profiles rendered",
        "Neither 559 nor 43 is a count of independently authored website templates",
        "not an official corporate brand manual",
        "does not claim that every one of the 10,666 unique content URLs",
        "Accessibility corrections",
        "hotlink production UI",
    ):
        assert phrase in reference

    tracked_text = "\n".join(
        path.read_text(encoding="utf-8") for path in (SKILL_MD, REFERENCE, TEMPLATE)
    )
    assert str(ROOT) not in tracked_text
    assert not re.search(
        r"(?i)(api[_-]?key|password|secret|token)\s*[=:]\s*[\"'][^\"']{6,}",
        tracked_text,
    )


def test_admin_template_is_dependency_free_and_semantic() -> None:
    html = TEMPLATE.read_text(encoding="utf-8")
    parser = TemplateParser()
    parser.feed(html)

    assert not any(tag == "script" for tag, _ in parser.start_tags)
    assert not any(
        tag == "link" and attrs.get("rel") == "stylesheet"
        for tag, attrs in parser.start_tags
    )
    assert not re.search(r"(?:href|src)=[\"']https?://", html)
    assert '<main id="main-content"' in html
    assert 'class="skip-link"' in html
    assert ":focus-visible" in html
    assert "@media (max-width: 767px)" in html
    assert "@media (prefers-reduced-motion: reduce)" in html
    assert '<section class="table-scroll"' in html
    assert 'aria-label="Recent projects table"' in html
    assert html.count('scope="col"') == 5
    assert 'type="search"' in html
    assert 'role="img"' in html
    assert "var(--color-logo-orange)" not in html
    assert "var(--color-logo-olive)" not in html
    assert "Static composition reference" in html
    assert (
        ".lede { max-width: 680px; margin: 8px 0 0; color: var(--color-text); }" in html
    )

    fragment_targets = {
        (attrs.get("href") or "")[1:]
        for _, attrs in parser.start_tags
        if (attrs.get("href") or "").startswith("#")
    }
    element_ids = {
        attrs.get("id") or ""
        for _, attrs in parser.start_tags
        if attrs.get("id") is not None
    }
    assert fragment_targets <= element_ids


def test_admin_template_color_tokens_match_normative_exports() -> None:
    html = TEMPLATE.read_text(encoding="utf-8")
    template_colors = dict(re.findall(r"--color-([a-z0-9-]+):\s*(#[0-9a-f]{6});", html))
    assert template_colors == EXPECTED_COLORS

    theme = (ROOT / "design-system" / "theme.css").read_text(encoding="utf-8")
    generated_colors = dict(
        re.findall(r"--color-([a-z0-9-]+):\s*(#[0-9a-f]{6});", theme)
    )
    assert template_colors == generated_colors

    template_radii = dict(re.findall(r"--radius-([a-z0-9-]+):\s*([0-9]+px);", html))
    generated_radii = dict(re.findall(r"--radius-([a-z0-9-]+):\s*([0-9]+px);", theme))
    assert template_radii == EXPECTED_RADII
    assert template_radii == generated_radii


def test_skill_has_no_broken_local_file_references() -> None:
    skill = SKILL_MD.read_text(encoding="utf-8")
    local_paths = set(
        re.findall(
            r"`((?:references|templates)/[a-zA-Z0-9._/-]+)`",
            skill,
        )
    )
    assert local_paths == {
        "references/asia-allied-baseline.md",
        "templates/admin-cms.html",
    }
    assert all((SKILL / path).is_file() for path in local_paths)
