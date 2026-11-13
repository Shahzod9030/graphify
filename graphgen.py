"""Import grafini chiqaradi (Mermaid formatida).

Fayllar orasidagi ichki bog'liqliklarni (import) ko'rsatadi — loyihaning
tuzilishini bitta rasmda ko'rish uchun. Mermaid'ni GitHub, Claude yoki
mermaid.live ochib ko'rsatadi.
"""
from __future__ import annotations

import re
from pathlib import Path
from typing import Dict, List, Set, Tuple

from scan import iter_files, read_text

JS_IMPORT = re.compile(r"""(?:import\s.*?from\s+|require\(\s*)['"](\.[^'"]+)['"]""")
PY_FROM = re.compile(r"^\s*from\s+(\.[\w.]+)\s+import", re.M)


def _node_id(name: str) -> str:
    return re.sub(r"[^0-9A-Za-z_]", "_", name)


def build_graph(root: str) -> str:
    root_path = Path(root).resolve()
    files = list(iter_files(root_path))
    stems: Dict[str, Path] = {}
    for p in files:
        stems[str(p.relative_to(root_path))] = p

    edges: Set[Tuple[str, str]] = set()

    for p in files:
        text = read_text(p)
        if text is None:
            continue
        rel = str(p.relative_to(root_path))
        ext = p.suffix.lower()

        if ext in {".js", ".ts", ".jsx", ".tsx", ".mjs", ".cjs"}:
            for m in JS_IMPORT.finditer(text):
                target = (p.parent / m.group(1)).resolve()
                # kengaytmasini topishga urinish
                for cand in (target, target.with_suffix(ext)):
                    try:
                        tr = str(cand.relative_to(root_path))
                    except ValueError:
                        continue
                    if tr in stems and tr != rel:
                        edges.add((rel, tr))
        elif ext == ".py":
            for m in PY_FROM.finditer(text):
                mod = m.group(1).lstrip(".").replace(".", "/")
                for cand in (f"{mod}.py", f"{mod}/__init__.py"):
                    # p.parent ichidagi nisbiy import
                    guess = str((p.parent / cand))
                    try:
                        tr = str(Path(guess).resolve().relative_to(root_path))
                    except ValueError:
                        continue
                    if tr in stems and tr != rel:
                        edges.add((rel, tr))

    lines: List[str] = ["```mermaid", "graph LR"]
    if not edges:
        lines.append("  empty[Ichki import topilmadi]")
    for src, dst in sorted(edges):
        lines.append(f"  {_node_id(src)}[{src}] --> {_node_id(dst)}[{dst}]")
    lines.append("```")
    return "\n".join(lines)
