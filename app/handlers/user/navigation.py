from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from app.database.session import Database
from app.keyboards.reply import main_keyboard
from app.services.admins import is_admin
from app.utils.ui import menu_text, require_subscription

router = Router(name="user_navigation")


@router.message(F.text == "⬅️ ASOSIY MENYU")
async def main_menu(message: Message, state: FSMContext, db: Database, bot) -> None:
    await state.clear()
    if not await require_subscription(message, bot, db):
        return
    async with db.session() as session:
        admin = await is_admin(session, message.from_user.id)
    await message.answer(menu_text(), reply_markup=main_keyboard(admin))


@router.message(F.text == "⬅️ TESTLAR")
async def back_tests(message: Message, state: FSMContext, db: Database, bot) -> None:
    from app.keyboards.reply import quiz_keyboard
    await state.clear()
    if not await require_subscription(message, bot, db):
        return
    await message.answer("🧠 TEST", reply_markup=quiz_keyboard())


@router.message(F.text == "⬅️ KONTENT")
async def back_content(message: Message, state: FSMContext, db: Database) -> None:
    from app.keyboards.reply import admin_content_keyboard
    await state.clear()
    async with db.session() as session:
        if not await is_admin(session, message.from_user.id):
            return
    await message.answer("📚 KONTENT", reply_markup=admin_content_keyboard())


@router.message(F.text == "⬅️ ADMIN PANEL")
async def back_admin(message: Message, state: FSMContext, db: Database) -> None:
    from app.keyboards.reply import admin_keyboard
    await state.clear()
    async with db.session() as session:
        if not await is_admin(session, message.from_user.id):
            return
    await message.answer("🛠 ADMIN PANEL", reply_markup=admin_keyboard())
