"""Ixcham repo xaritasi (map) — fayl daraxti + faqat funksiya/klass imzolari.

Maqsad: butun kodni Claude'ga bermasdan, loyihaning "skeleti"ni berish.
Bu ko'p marta kam token sarflaydi.
"""
from __future__ import annotations

import re
from pathlib import Path
from typing import List

from scan import iter_files, read_text

# Har bir til uchun imzo (signature) qatorlarini tutadigan shablonlar
PATTERNS = {
    ".py": [
        re.compile(r"^\s*class\s+\w+.*?:"),
        re.compile(r"^\s*(?:async\s+)?def\s+\w+\s*\(.*?\).*?:"),
    ],
    ".js": [
        re.compile(r"^\s*(?:export\s+)?(?:default\s+)?(?:async\s+)?function\s+\w+\s*\("),
        re.compile(r"^\s*(?:export\s+)?class\s+\w+"),
        re.compile(r"^\s*(?:export\s+)?const\s+\w+\s*=\s*(?:async\s*)?\("),
    ],
    ".go": [
        re.compile(r"^\s*func\s+.*?\{?$"),
        re.compile(r"^\s*type\s+\w+\s+(?:struct|interface)"),
    ],
}
# ts/tsx/jsx js bilan bir xil, vue/svelte ham
for _ext in (".ts", ".tsx", ".jsx", ".mjs", ".cjs"):
    PATTERNS[_ext] = PATTERNS[".js"]

MAX_SYMBOLS_PER_FILE = 40


def symbols_for(path: Path, text: str) -> List[str]:
    pats = PATTERNS.get(path.suffix.lower())
    if not pats:
        return []
    out: List[str] = []
    for line in text.splitlines():
        if len(line) > 200:
            continue
        for pat in pats:
            if pat.match(line):
                out.append(line.strip().rstrip("{").strip())
                break
        if len(out) >= MAX_SYMBOLS_PER_FILE:
            break
    return out


def build_map(root: str) -> str:
    root_path = Path(root).resolve()
    lines: List[str] = [f"# Repo xaritasi: {root_path.name}", ""]
    files = sorted(iter_files(root_path), key=lambda p: str(p))
    for p in files:
        text = read_text(p)
        if text is None:
            continue
        rel = p.relative_to(root_path)
        syms = symbols_for(p, text)
        if syms:
            lines.append(f"## {rel}")
            for s in syms:
                lines.append(f"  {s}")
            lines.append("")
        else:
            # kod bo'lmagan yoki imzosiz fayl — faqat nomi
            lines.append(f"## {rel}  (— {text.count(chr(10)) + 1} qator)")
            lines.append("")
    return "\n".join(lines)
