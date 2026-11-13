# Graphify

**Claude Code / LLM uchun token tejash tooli.**

## Oddiy tilda (5 yoshli bolaga tushuntirgandek)

Tasavvur qiling, Claude — bu juda aqlli robot. Lekin u o'qigan har bir
so'z uchun pul olasiz. Agar unga **butun kitobni** (ya'ni butun loyihangizni)
o'qitsangiz — ko'p pul ketadi.

Graphify — bu yordamchi. U:
- Qaysi **daftar eng qalin** (ko'p token yeydi) ekanini aytadi 📚
- Butun kitob o'rniga **qisqa mundarija** (map) yasaydi — robot shuni o'qisa yetadi 📝
- Daftarlar bir-biri bilan qanday **bog'langanini rasm** (graf) qilib ko'rsatadi 🔗
- Har bir o'qish **qancha pul** turishini aytadi 💰

Shunday qilib, robotga kam so'z berib, kam pul to'laysiz. Tamom!

---

Katta loyihani to'liq Claude'ga berish ko'p token (va pul) sarflaydi. Graphify
repoyingizni skanerlab:

- qaysi fayl eng ko'p token "yeyayotganini" ko'rsatadi,
- butun kod o'rniga beriladigan **ixcham xarita** (faqat funksiya/klass imzolari) chiqaradi,
- fayllar orasidagi **import grafini** (Mermaid) yasaydi.

Shunda siz Claude'ga butun loyiha emas, kerakli qism yoki yengil "skelet"ni
berasiz — token ancha tejaladi.

## O'rnatish

```bash
git clone https://github.com/<username>/graphify.git
cd graphify
pip install -e .

# aniqroq token hisobi uchun (ixtiyoriy):
pip install -e ".[exact]"
```

`tiktoken` bo'lmasa ham ishlaydi — u holda token taxminiy (~4 belgi = 1 token)
hisoblanadi.

## Foydalanish

### 1. Token sarfini (va narxini) ko'rish
```bash
graphify scan .
graphify scan ./myproject --top 30
graphify scan . --price-per-1m 3     # 1M token narxini o'z modelingizga qarab kiriting
```
Natija: eng ko'p token sarflaydigan fayllar ro'yxati, jami token soni va
taxminiy **narx ($)**. `.gitignore`dagi fayllar avtomatik tashlab ketiladi.

### 2. Ixcham xarita (Claude'ga berish uchun)
```bash
graphify map . -o map.md
```
`map.md` — loyihaning yengil skeletini saqlaydi. Uni Claude'ga berib:
"avval shu xaritani o'qi, keyin kerakli faylni so'ra" deysiz.

### 3. Import grafi
```bash
graphify graph . -o deps.mmd
```
Mermaid grafi chiqadi — GitHub, Claude yoki https://mermaid.live ochib ko'radi.

## Token tejash maslahatlari (Claude Code)

1. Har yangi vazifaga `/clear` qiling.
2. `CLAUDE.md` da loyiha qoidalarini bir marta yozing.
3. Noaniq so'rov o'rniga aniq fayl/qatorni ko'rsating.
4. Katta fayllarni to'liq o'qitmang — `graphify map` dan foydalaning.
5. Keraksiz MCP/connector'larni o'chiring.
6. Oddiy ishga arzon model (Haiku) tanlang.

## Litsenziya

MIT
