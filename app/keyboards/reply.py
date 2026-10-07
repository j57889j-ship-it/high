from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

from app.constants import ADMIN_MENU_BUTTONS, MAIN_MENU_BUTTONS


def main_keyboard(is_admin: bool = False) -> ReplyKeyboardMarkup:
    rows = [
        [KeyboardButton(text=MAIN_MENU_BUTTONS["books"]), KeyboardButton(text=MAIN_MENU_BUTTONS["quiz"])],
        [KeyboardButton(text=MAIN_MENU_BUTTONS["top"]), KeyboardButton(text=MAIN_MENU_BUTTONS["profile"])],
        [KeyboardButton(text=MAIN_MENU_BUTTONS["help"])],
    ]
    if is_admin:
        rows[-1].append(KeyboardButton(text=MAIN_MENU_BUTTONS["admin"]))
    return ReplyKeyboardMarkup(keyboard=rows, resize_keyboard=True, is_persistent=True)


def books_keyboard() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="🔎 KITOB QIDIRISH")],
            [KeyboardButton(text="📖 BARCHA KITOBLAR")],
            [KeyboardButton(text="⬅️ ASOSIY MENYU")],
        ],
        resize_keyboard=True,
    )


def quiz_keyboard() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="📖 KITOB BO‘YICHA")],
            [KeyboardButton(text="🎲 TASODIFIY TEST")],
            [KeyboardButton(text="🔥 BUGUNGI SAVOL")],
            [KeyboardButton(text="❌ XATO SAVOLLARIM")],
            [KeyboardButton(text="⬅️ ASOSIY MENYU")],
        ],
        resize_keyboard=True,
    )


def quiz_count_keyboard() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="5 TA"), KeyboardButton(text="10 TA")],
            [KeyboardButton(text="20 TA"), KeyboardButton(text="30 TA")],
            [KeyboardButton(text="⬅️ TESTLAR")],
        ],
        resize_keyboard=True,
    )


def answers_keyboard() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="A"), KeyboardButton(text="B")],
            [KeyboardButton(text="C"), KeyboardButton(text="D")],
        ],
        resize_keyboard=True,
        is_persistent=False,
    )


def profile_keyboard() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="📊 STATISTIKA"), KeyboardButton(text="❌ XATOLARIM")],
            [KeyboardButton(text="🔥 STREAK")],
            [KeyboardButton(text="⬅️ ASOSIY MENYU")],
        ],
        resize_keyboard=True,
    )


def help_keyboard() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="📖 BOT HAQIDA")],
            [KeyboardButton(text="❓ QANDAY ISHLAYDI")],
            [KeyboardButton(text="💬 ADMIN BILAN BOG‘LANISH")],
            [KeyboardButton(text="⬅️ ASOSIY MENYU")],
        ],
        resize_keyboard=True,
    )


def admin_keyboard() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=ADMIN_MENU_BUTTONS["content"]), KeyboardButton(text=ADMIN_MENU_BUTTONS["users"])],
            [KeyboardButton(text=ADMIN_MENU_BUTTONS["channels"]), KeyboardButton(text=ADMIN_MENU_BUTTONS["leaderboard"])],
            [KeyboardButton(text="🧠 TEST BOSHQARUVI"), KeyboardButton(text=ADMIN_MENU_BUTTONS["settings"])],
            [KeyboardButton(text=ADMIN_MENU_BUTTONS["back"])],
        ],
        resize_keyboard=True,
        is_persistent=True,
    )


def admin_content_keyboard() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="📖 KITOBLARNI BOSHQARISH")],
            [KeyboardButton(text="❓ SAVOLLARNI BOSHQARISH")],
            [KeyboardButton(text="📥 TXT IMPORT")],
            [KeyboardButton(text="⬅️ ADMIN PANEL")],
        ],
        resize_keyboard=True,
    )


def admin_books_keyboard() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="➕ KITOB QO‘SHISH")],
            [KeyboardButton(text="🔎 KITOB TOPISH"), KeyboardButton(text="🗑 KITOB O‘CHIRISH")],
            [KeyboardButton(text="⬅️ KONTENT")],
        ],
        resize_keyboard=True,
    )


def admin_questions_keyboard() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="➕ SAVOL QO‘SHISH")],
            [KeyboardButton(text="📋 SAVOLLAR RO‘YXATI")],
            [KeyboardButton(text="⬅️ KONTENT")],
        ],
        resize_keyboard=True,
    )


def admin_users_keyboard() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="🔎 USER QIDIRISH")],
            [KeyboardButton(text="📊 USER STATISTIKASI")],
            [KeyboardButton(text="🚫 BLOK / UNBLOK")],
            [KeyboardButton(text="🧹 USER STATISTIKASINI TOZALASH")],
            [KeyboardButton(text="📣 XABAR YUBORISH")],
            [KeyboardButton(text="⬅️ ADMIN PANEL")],
        ],
        resize_keyboard=True,
    )


def admin_channels_keyboard() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="📡 MAJBURIY KANALLAR")],
            [KeyboardButton(text="➕ KANAL QO‘SHISH")],
            [KeyboardButton(text="🗑 KANALNI O‘CHIRISH")],
            [KeyboardButton(text="❤️ REACTION")],
            [KeyboardButton(text="⬅️ ADMIN PANEL")],
        ],
        resize_keyboard=True,
    )


def admin_leaderboard_keyboard() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="👑 TOP KITOBXONLAR")],
            [KeyboardButton(text="⚙️ TOP SOZLAMALARI")],
            [KeyboardButton(text="🧹 TOP RESET")],
            [KeyboardButton(text="⬅️ ADMIN PANEL")],
        ],
        resize_keyboard=True,
    )


def admin_quiz_keyboard() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="⚙️ TEST SOZLAMALARI")],
            [KeyboardButton(text="📊 TEST STATISTIKASI")],
            [KeyboardButton(text="🧹 NATIJALARNI TOZALASH")],
            [KeyboardButton(text="⬅️ ADMIN PANEL")],
        ],
        resize_keyboard=True,
    )


def admin_settings_keyboard() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="👑 ADMINLAR")],
            [KeyboardButton(text="⬅️ ADMIN PANEL")],
        ],
        resize_keyboard=True,
    )
