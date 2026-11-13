"""Repoyni skanerlab, har bir fayl bo'yicha token sarfini hisoblaydi."""
from __future__ import annotations

import os
from pathlib import Path
from typing import Iterator, List, Tuple

from .gitignore import load_gitignore
from .tokens import count_tokens

SKIP_DIRS = {
    ".git", "node_modules", ".venv", "venv", "env", "__pycache__",
    "dist", "build", ".next", ".nuxt", ".idea", ".vscode", "target",
    "coverage", ".pytest_cache", ".mypy_cache", "vendor",
}

TEXT_EXT = {
    ".py", ".js", ".ts", ".jsx", ".tsx", ".vue", ".svelte", ".java",
    ".go", ".rb", ".php", ".c", ".h", ".cpp", ".hpp", ".cs", ".rs",
    ".kt", ".swift", ".scala", ".md", ".txt", ".json", ".yaml", ".yml",
    ".toml", ".ini", ".html", ".css", ".scss", ".sql", ".sh", ".dockerfile",
}

MAX_BYTES = 2_000_000  # 2 MB dan katta fayllar o'tkazib yuboriladi


def iter_files(root: Path) -> Iterator[Path]:
    is_ignored = load_gitignore(root)
    for dirpath, dirnames, filenames in os.walk(root):
        # yashirin, keraksiz va .gitignore'dagi papkalarni tashlab ketish
        dirnames[:] = [
            d for d in dirnames
            if d not in SKIP_DIRS
            and not d.startswith(".")
            and not is_ignored(os.path.relpath(os.path.join(dirpath, d), root))
        ]
        for fn in filenames:
            p = Path(dirpath) / fn
            if p.suffix.lower() in TEXT_EXT:
                if is_ignored(os.path.relpath(p, root)):
                    continue
                yield p


def read_text(p: Path) -> str | None:
    try:
        if p.stat().st_size > MAX_BYTES:
            return None
        return p.read_text(encoding="utf-8", errors="ignore")
    except OSError:
        return None


def scan(root: str) -> Tuple[List[Tuple[str, int, int]], int]:
    """Qaytaradi: [(nisbiy_yo'l, tokenlar, qatorlar)], jami_tokenlar."""
    root_path = Path(root).resolve()
    rows: List[Tuple[str, int, int]] = []
    total = 0
    for p in iter_files(root_path):
        text = read_text(p)
        if text is None:
            continue
        tok = count_tokens(text)
        lines = text.count("\n") + 1
        total += tok
        rows.append((os.path.relpath(p, root_path), tok, lines))
    rows.sort(key=lambda r: r[1], reverse=True)
    return rows, total
