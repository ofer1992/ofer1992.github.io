"""
Markdown extension that converts Obsidian-style embeds (e.g. ![[image.png|Alt]])
to HTML elements during the Pelican build step.
"""

from __future__ import annotations

import html
import re
from pathlib import Path
from typing import Iterable
from urllib.parse import quote

from markdown.extensions import Extension
from markdown.preprocessors import Preprocessor


def _looks_like_dimension(value: str) -> bool:
    stripped = value.strip()
    if not stripped:
        return False
    if stripped.isdigit():
        return True
    if stripped.endswith("px") and stripped[:-2].isdigit():
        return True
    if stripped.endswith("%") and stripped[:-1].isdigit():
        return True
    return False


class ObsidianEmbedPreprocessor(Preprocessor):
    pattern = re.compile(r"!\[\[([^\]]+)\]\]")
    image_exts = {".png", ".jpg", ".jpeg", ".gif", ".bmp", ".svg", ".webp", ".avif"}
    audio_exts = {".mp3", ".wav", ".m4a", ".ogg", ".flac"}
    video_exts = {".mp4", ".mov", ".m4v", ".webm", ".ogv"}

    def __init__(self, md, content_root: Path, static_dirs: list[Path]):
        super().__init__(md)
        self.content_root = content_root
        self.static_dirs = self._normalise_static_dirs(static_dirs)
        self._lookup_cache: dict[str, str] = {}

    def _normalise_static_dirs(self, static_dirs: list[Path]) -> list[Path]:
        seen: set[Path] = set()
        result: list[Path] = []
        for path in static_dirs:
            resolved = (self.content_root / path).resolve()
            if resolved not in seen:
                seen.add(resolved)
                result.append(resolved)
        return result

    def run(self, lines: Iterable[str]) -> list[str]:
        return [self.pattern.sub(self._replace, line) for line in lines]

    def _resolve_src(self, src: str) -> str:
        cached = self._lookup_cache.get(src)
        if cached is not None:
            return cached

        candidate = Path(src)

        if candidate.is_absolute():
            self._lookup_cache[src] = src
            return src

        direct = (self.content_root / candidate).resolve()
        if direct.exists():
            resolved = direct.relative_to(self.content_root).as_posix()
            self._lookup_cache[src] = resolved
            return resolved

        for static_dir in self.static_dirs:
            path = (static_dir / candidate).resolve()
            if path.exists():
                resolved = path.relative_to(self.content_root).as_posix()
                self._lookup_cache[src] = resolved
                return resolved

        if candidate.name:
            matches = list(self.content_root.rglob(candidate.name))
            if len(matches) == 1:
                resolved = matches[0].relative_to(self.content_root).as_posix()
                self._lookup_cache[src] = resolved
                return resolved

        self._lookup_cache[src] = src
        return src

    def _to_site_url(self, path: str) -> str:
        safe_chars = "/:@?&=#+,;.%~*-"
        prefixes = ("http://", "https://", "mailto:", "data:", "#")
        if path.startswith(prefixes):
            return path
        if path.startswith("/"):
            return quote(path, safe=safe_chars)
        return "/" + quote(path, safe=safe_chars)

    def _render_image(
        self,
        resolved_src: str,
        alt: str,
        title: str | None,
        width: str | None,
        height: str | None,
        classes_str: str | None,
        style: str | None,
    ) -> str:
        attrs = [("src", self._to_site_url(resolved_src)), ("alt", alt)]
        if title:
            attrs.append(("title", title))
        if width:
            attrs.append(("width", width))
        if height:
            attrs.append(("height", height))
        if classes_str:
            attrs.append(("class", classes_str))
        default_style = ["display:block", "margin:1.5rem auto"]
        if not width and not self._style_mentions(style, "width"):
            default_style.extend(["width:70%", "max-width:900px"])
        default_style.append("height:auto")
        style_value = self._merge_style(style, default_style)
        if style_value:
            attrs.append(("style", style_value))
        rendered = " ".join(
            f'{name}="{html.escape(value, quote=True)}"' for name, value in attrs
        )
        return f"<img {rendered} />"

    def _render_audio(
        self,
        resolved_src: str,
        title: str | None,
        classes_str: str | None,
        style: str | None,
    ) -> str:
        attrs = [("src", self._to_site_url(resolved_src))]
        if classes_str:
            attrs.append(("class", classes_str))
        if title:
            attrs.append(("title", title))
        default_style = ["display:block", "margin:1.5rem auto"]
        if not self._style_mentions(style, "width"):
            default_style.extend(["width:100%", "max-width:720px"])
        style_value = self._merge_style(style, default_style)
        if style_value:
            attrs.append(("style", style_value))
        rendered = " ".join(
            f'{name}="{html.escape(value, quote=True)}"' for name, value in attrs
        )
        return f"<audio controls {rendered}></audio>"

    def _render_video(
        self,
        resolved_src: str,
        title: str | None,
        classes_str: str | None,
        width: str | None,
        height: str | None,
        style: str | None,
    ) -> str:
        attrs = [("src", self._to_site_url(resolved_src))]
        if classes_str:
            attrs.append(("class", classes_str))
        if width:
            attrs.append(("width", width))
        if height:
            attrs.append(("height", height))
        if title:
            attrs.append(("title", title))
        default_style = ["display:block", "margin:1.5rem auto"]
        if not width and not self._style_mentions(style, "width"):
            default_style.extend(["width:100%", "max-width:720px"])
        style_value = self._merge_style(style, default_style)
        if style_value:
            attrs.append(("style", style_value))
        rendered = " ".join(
            f'{name}="{html.escape(value, quote=True)}"' for name, value in attrs
        )
        return f"<video controls {rendered}></video>"

    def _render_link(
        self,
        resolved_src: str,
        alt: str,
        title: str | None,
        classes_str: str | None,
        style: str | None,
    ) -> str:
        link_classes = (
            f' class="{html.escape(classes_str, quote=True)}"' if classes_str else ""
        )
        title_attr = f' title="{html.escape(title, quote=True)}"' if title else ""
        label = html.escape(alt, quote=False)
        href = html.escape(self._to_site_url(resolved_src), quote=True)
        style_attr = ""
        if style:
            style_attr = f' style="{html.escape(style, quote=True)}"'
        return f"<a href=\"{href}\"{link_classes}{title_attr}{style_attr}>{label}</a>"

    def _replace(self, match: re.Match[str]) -> str:
        before = match.string[: match.start()]
        if "<!--" in before and "-->" not in before:
            return match.group(0)

        inner = match.group(1).strip()
        parts = [part.strip() for part in inner.split("|")]
        if not parts:
            return match.group(0)

        src = parts[0]
        alt: str | None = None
        title: str | None = None
        width: str | None = None
        height: str | None = None
        classes: list[str] = ["obsidian-embed"]
        style: str | None = None

        for raw_part in parts[1:]:
            if not raw_part:
                continue
            if "=" in raw_part:
                key, value = raw_part.split("=", 1)
                key = key.strip().lower()
                value = value.strip()
                if key == "alt":
                    alt = value
                elif key == "title":
                    title = value
                elif key == "width":
                    width = value
                elif key == "height":
                    height = value
                elif key == "class":
                    classes.extend(token for token in value.split() if token)
                elif key == "style":
                    style = value if not style else f"{style.rstrip(';')}; {value}"
                else:
                    if value:
                        classes.append(value)
                continue

            if _looks_like_dimension(raw_part):
                width = raw_part
                continue

            if alt is None:
                alt = raw_part
            else:
                classes.append(raw_part)

        resolved_src = self._resolve_src(src)

        if not alt:
            alt = Path(resolved_src).stem.replace("_", " ")

        suffix = Path(resolved_src).suffix.lower()
        classes_str = " ".join(classes) if classes else None

        if suffix in self.image_exts or not suffix:
            html = self._render_image(
                resolved_src, alt, title, width, height, classes_str, style
            )
        elif suffix in self.audio_exts:
            html = self._render_audio(resolved_src, title, classes_str, style)
        elif suffix in self.video_exts:
            html = self._render_video(
                resolved_src, title, classes_str, width, height, style
            )
        else:
            html = self._render_link(resolved_src, alt, title, classes_str, style)

        return self._finalize_output(match, html)

    def _finalize_output(self, match: re.Match[str], html: str) -> str:
        if match.string.strip() == match.group(0):
            return f"\n{html}\n"
        return html

    @staticmethod
    def _merge_style(user_style: str | None, default_parts: list[str]) -> str:
        default_parts = [part for part in default_parts if part]
        default = ""
        if default_parts:
            default = "; ".join(default_parts).strip().rstrip(";")
            if default:
                default = f"{default};"
        if user_style:
            stripped = user_style.strip().rstrip(";")
            if stripped:
                if default:
                    return f"{default} {stripped};"
                return f"{stripped};"
        return default

    @staticmethod
    def _style_mentions(style: str | None, prop: str) -> bool:
        if not style:
            return False
        prop = prop.lower()
        for chunk in style.split(";"):
            if chunk.strip().lower().startswith(prop):
                return True
        return False


class ObsidianEmbedExtension(Extension):
    def __init__(self, **kwargs):
        self.config = {
            "content_root": [".", "Root directory for content files"],
            "static_dirs": [[], "Static directories within the content root"],
        }
        super().__init__(**kwargs)

    def extendMarkdown(self, md):  # noqa: N802 (markdown API)
        content_root = Path(self.getConfig("content_root")).resolve()
        static_dirs = [Path(p) for p in self.getConfig("static_dirs")]
        md.preprocessors.register(
            ObsidianEmbedPreprocessor(md, content_root, static_dirs),
            "obsidian_embed_preprocessor",
            priority=175,
        )


def makeExtension(**kwargs):
    return ObsidianEmbedExtension(**kwargs)
