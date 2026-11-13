"""Graphify buyruq qatori interfeysi (CLI)."""
from __future__ import annotations

import argparse
import sys

__version__ = "0.2.0"
from graphgen import build_graph
from mapgen import build_map
from scan import scan
from tokens import EXACT, cost, human


def cmd_scan(args: argparse.Namespace) -> int:
    rows, total = scan(args.path)
    if not rows:
        print("Fayl topilmadi.")
        return 0
    mode = "aniq (tiktoken)" if EXACT else "taxminiy (~4 belgi/token)"
    price = args.price_per_1m
    print(f"Token hisobi — {mode}  |  narx: ${price:g} / 1M token\n")
    top = rows[: args.top]
    width = max((len(r[0]) for r in top), default=10)
    print(f"{'FAYL'.ljust(width)}  {'TOKEN':>8}  {'QATOR':>6}  {'NARX':>8}")
    print("-" * (width + 30))
    for rel, tok, lines in top:
        print(f"{rel.ljust(width)}  {human(tok):>8}  {lines:>6}  {'$' + format(cost(tok, price), '.4f'):>8}")
    print("-" * (width + 30))
    print(f"{'JAMI'.ljust(width)}  {human(total):>8}  {'':>6}  {'$' + format(cost(total, price), '.4f'):>8}")
    print(f"\nFayllar soni: {len(rows)}  |  Jami token: {total:,}  |  Taxminiy narx: ${cost(total, price):.4f}")
    if top:
        big = top[0]
        share = big[1] / total * 100 if total else 0
        print(
            f"\nMaslahat: eng katta fayl '{big[0]}' jami tokenning "
            f"{share:.0f}% ini egallaydi. Claude'ga butun loyihani bermang — "
            f"kerakli fayllarni alohida bering yoki `graphify map` ishlating."
        )
    return 0


def cmd_map(args: argparse.Namespace) -> int:
    out = build_map(args.path)
    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(out)
        print(f"Xarita yozildi: {args.output}")
    else:
        print(out)
    return 0


def cmd_graph(args: argparse.Namespace) -> int:
    out = build_graph(args.path)
    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(out)
        print(f"Graf yozildi: {args.output}")
    else:
        print(out)
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="graphify",
        description="Claude Code / LLM uchun token tejash tooli.",
    )
    parser.add_argument("--version", action="version", version=f"graphify {__version__}")
    sub = parser.add_subparsers(dest="command", required=True)

    p_scan = sub.add_parser("scan", help="Fayllar bo'yicha token sarfini ko'rsatadi")
    p_scan.add_argument("path", nargs="?", default=".", help="Loyiha papkasi (default: .)")
    p_scan.add_argument("--top", type=int, default=20, help="Nechta eng katta faylni ko'rsatish")
    p_scan.add_argument(
        "--price-per-1m", type=float, default=3.0,
        help="1 million token narxi, $ (default: 3.0 — o'z modelingiz narxini kiriting)",
    )
    p_scan.set_defaults(func=cmd_scan)

    p_map = sub.add_parser("map", help="Ixcham repo xaritasini chiqaradi")
    p_map.add_argument("path", nargs="?", default=".")
    p_map.add_argument("-o", "--output", help="Natijani faylga yozish")
    p_map.set_defaults(func=cmd_map)

    p_graph = sub.add_parser("graph", help="Import grafini (Mermaid) chiqaradi")
    p_graph.add_argument("path", nargs="?", default=".")
    p_graph.add_argument("-o", "--output", help="Natijani faylga yozish")
    p_graph.set_defaults(func=cmd_graph)

    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
