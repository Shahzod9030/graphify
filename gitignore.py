"""`.gitignore` ni o'qib, qaysi fayllarni tashlab ketishni aniqlaydi.

Bu — sodda versiya: eng ko'p ishlatiladigan shablonlarni qo'llab-quvvatlaydi
(masalan `*.log`, `build/`, `/secret.txt`). Murakkab negatsiya (`!`) qoidalari
o'tkazib yuboriladi.
"""
from __future__ import annotations

import fnmatch
from pathlib import Path
from typing import Callable, List


def load_gitignore(root: Path) -> Callable[[str], bool]:
    patterns: List[str] = []
    gi = root / ".gitignore"
    if gi.exists():
        try:
            for raw in gi.read_text(encoding="utf-8", errors="ignore").splitlines():
                line = raw.strip()
                if not line or line.startswith("#") or line.startswith("!"):
                    continue
                patterns.append(line)
        except OSError:
            pass

    def is_ignored(rel: str) -> bool:
        rel = rel.replace("\\", "/")
        segments = rel.split("/")
        for pat in patterns:
            p = pat.rstrip("/")
            anchored = p.startswith("/")
            p = p.lstrip("/")
            if "/" in p:
                if fnmatch.fnmatch(rel, p) or fnmatch.fnmatch(rel, p + "/*"):
                    return True
            elif anchored:
                if fnmatch.fnmatch(segments[0], p):
                    return True
            else:
                if any(fnmatch.fnmatch(seg, p) for seg in segments):
                    return True
        return False

    return is_ignored
