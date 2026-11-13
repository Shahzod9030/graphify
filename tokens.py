"""Token hisoblash.

Iloji bo'lsa `tiktoken` (cl100k_base) ishlatiladi — bu aniqroq.
O'rnatilmagan bo'lsa, taxminiy hisob (~4 belgi = 1 token) ishlaydi.

Eslatma: Claude o'z tokenizatoridan foydalanadi, lekin budjet rejalash
uchun bu hisob yetarlicha yaqin.
"""
from __future__ import annotations

try:
    import tiktoken

    _enc = tiktoken.get_encoding("cl100k_base")

    def count_tokens(text: str) -> int:
        return len(_enc.encode(text, disallowed_special=()))

    EXACT = True
except Exception:  # tiktoken yo'q yoki yuklanmadi

    def count_tokens(text: str) -> int:
        # Taxminiy: o'rtacha ~4 belgi bitta tokenga to'g'ri keladi
        return max(1, round(len(text) / 4))

    EXACT = False


def human(n: int) -> str:
    """Katta sonlarni o'qishbop qiladi: 12345 -> '12.3k'."""
    if n < 1000:
        return str(n)
    if n < 1_000_000:
        return f"{n / 1000:.1f}k"
    return f"{n / 1_000_000:.2f}M"


def cost(tokens: int, price_per_1m: float) -> float:
    """Token sonini $ narxga aylantiradi (1 million token narxiga qarab)."""
    return tokens / 1_000_000 * price_per_1m
