# Kitobxonlar Bot — Clean V30

Telegram uchun qisqa, kitobxonlarga mo‘ljallangan quiz bot. Ushbu versiya oldingi murakkab variantlardan qayta qurilgan.

## Dizayn falsafasi

- HTML va Markdown `parse_mode` ishlatilmaydi.
- Asosiy navigatsiya pastdagi Reply Keyboard orqali.
- Dinamik ro‘yxatlar va URL tugmalari Inline Keyboard orqali.
- Kitob muqovasi, emoji, progress-bar va message edit/step-by-step oqimlar vizual effekt vazifasini bajaradi.
- Referral, haftalik/oylik/mavsumiy TOP va boshqa ortiqcha gamification modullari mavjud emas.

## User bo‘limlari

- 📚 KITOBLAR — qidirish, barcha kitoblar, kitob tafsiloti, kanal postiga va batafsil postga URL.
- 🧠 TEST — kitob bo‘yicha, tasodifiy, bugungi savol, xato savollar.
- 🏆 TOP — faqat umumiy TOP kitobxonlar va shaxsiy o‘rin.
- 👤 PROFIL — ball, testlar, to‘g‘ri/xato, aniqlik, streak, TOP o‘rni.
- ℹ️ YORDAM — bot haqida, qanday ishlashi, admin bilan bog‘lanish.

## Admin bo‘limlari

- 📚 KONTENT — kitoblar, savollar, TXT import.
- 👥 FOYDALANUVCHILAR — qidirish, statistika, ban/unban, statistikani tozalash, broadcast.
- 📢 KANALLAR — majburiy kanallar, reaction, kitob postini target kanalga yuborish.
- 🏆 REYTING — umumiy TOP sozlamalari va reset.
- 🧠 TEST — ball, daily savol, test statistikasi, natijalarni tozalash.
- ⚙️ SOZLAMALAR — Super Admin yangi admin qo‘shadi yoki o‘chiradi.

## Book metadata

Admin kitob qo‘shayotganda:

1. Nomi
2. Muallif
3. Qisqa ma’lumot
4. Kanal post URL
5. Batafsil ma’lumot URL
6. Muqova (ixtiyoriy)

User kitobni qidirganda aynan admin biriktirgan URL tugmalarini ko‘radi.

## Majburiy kanallar

Admin kanal nomi, `chat_id` va invite URL qo‘shadi. Bot `/start` va foydalanuvchi oqimlarida barcha faol kanallarga obuna bo‘lishni tekshiradi.

## TXT import

Admin avval kitobni tanlaydi, so‘ng `.txt` fayl yuboradi. Maksimum 100 ta valid savol import qilinadi. Duplicate savollar va format xatolari alohida ko‘rsatiladi.

Namuna:

```text
1. Savol matni?
A: Variant A
B: Variant B
C: Variant C
D: Variant D
ANSWER: B
EXPLANATION: Ixtiyoriy izoh.
```

## Local run

```bash
python -m venv .venv
.venv\\Scripts\\activate   # Windows
pip install -r requirements.txt
copy .env.example .env
alembic upgrade head
python -m uvicorn app.main:app --host 0.0.0.0 --port 8080
```

## Render

**Build Command**

```bash
pip install -r requirements.txt
```

**Start Command**

```bash
alembic upgrade head && python -m uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

`render.yaml` PostgreSQL va Render Key Value (Redis-compatible) resurslarini ham tariflaydi.

Render Blueprints `fromDatabase` va `fromService` orqali servislarni o‘zaro bog‘lashni qo‘llab-quvvatlaydi; Key Value hozir Redis-compatible Valkey bilan ishlaydi. Render yangi servislar uchun Python versiyasini `PYTHON_VERSION` bilan pin qilishga ruxsat beradi. 

## Muhim Environment Variables

```text
BOT_TOKEN=
ADMIN_IDS=123456789,987654321
TARGET_CHANNEL_ID=-1001234567890
WEBHOOK_URL=https://your-service.onrender.com
WEBHOOK_SECRET=
DATABASE_URL=
REDIS_URL=
```

`WEBHOOK_URL` Render servisining `https://...onrender.com` manzili bo‘lishi kerak. Agar `WEBHOOK_URL` berilmasa, dastur polling rejimiga o‘tadi.

## Texnik stack

- Python 3.13.5
- aiogram 3.31.0
- FastAPI
- PostgreSQL + SQLAlchemy async
- Alembic
- Redis/Valkey + aiogram RedisStorage
- Render Blueprint

Arxitektura modular Router/FSM, PostgreSQL/Redis va webhook yondashuviga qurilgan. Aiogram 3.31 router/FSM/webhook imkoniyatlarini beradi; RedisStorage production FSM uchun ishlatiladi. 
