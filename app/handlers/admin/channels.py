from __future__ import annotations

from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message, ReactionTypeEmoji
from sqlalchemy import select, delete

from app.database.models import Book, MandatoryChannel
from app.database.session import Database
from app.keyboards.inline import channels_list_keyboard
from app.keyboards.reply import admin_channels_keyboard
from app.services.settings import get_setting, set_setting
from app.states.admin import AdminChannelStates, AdminReactionStates
from app.utils.auth import require_admin, can_manage_content, can_manage_users, is_super

router = Router(name="admin_channels")


@router.message(F.text == "📢 KANALLAR")
async def channels_home(message: Message, db: Database) -> None:
    role = await require_admin(message, db)
    if not role:
        return
    await message.answer("📢 KANALLAR", reply_markup=admin_channels_keyboard())


@router.message(F.text == "📡 MAJBURIY KANALLAR")
async def mandatory_channels(message: Message, db: Database) -> None:
    role = await require_admin(message, db)
    if not role:
        return
    async with db.session() as session:
        result = await session.execute(select(MandatoryChannel).order_by(MandatoryChannel.id))
        channels = list(result.scalars().all())
    if not channels:
        await message.answer("📭 Majburiy kanallar hali qo‘shilmagan.")
        return
    await message.answer("📡 MAJBURIY KANALLAR", reply_markup=channels_list_keyboard(channels))


@router.message(F.text == "➕ KANAL QO‘SHISH")
async def add_channel_start(message: Message, state: FSMContext, db: Database) -> None:
    role = await require_admin(message, db)
    if not role:
        return
    await state.set_state(AdminChannelStates.title)
    await message.answer("1/3 📢 Kanal nomini yuboring.")


@router.message(AdminChannelStates.title)
async def add_channel_title(message: Message, state: FSMContext) -> None:
    await state.update_data(title=message.text.strip())
    await state.set_state(AdminChannelStates.chat_id)
    await message.answer("2/3 🆔 Kanal Chat ID sini yuboring. Masalan: -1001234567890")


@router.message(AdminChannelStates.chat_id)
async def add_channel_id(message: Message, state: FSMContext) -> None:
    if not message.text.lstrip("-").isdigit():
        await message.answer("Chat ID raqam bo‘lishi kerak.")
        return
    await state.update_data(chat_id=int(message.text))
    await state.set_state(AdminChannelStates.invite_url)
    await message.answer("3/3 🔗 Kanalga kirish linkini yuboring.")


@router.message(AdminChannelStates.invite_url)
async def add_channel_finish(message: Message, state: FSMContext, db: Database) -> None:
    data = await state.get_data()
    async with db.session() as session:
        session.add(MandatoryChannel(title=data["title"], chat_id=int(data["chat_id"]), invite_url=message.text.strip(), is_active=True))
        try:
            await session.commit()
        except Exception:
            await session.rollback()
            await message.answer("❌ Kanal saqlanmadi. Bu Chat ID allaqachon mavjud bo‘lishi mumkin.")
            return
    await state.clear()
    await message.answer("✅ Majburiy kanal qo‘shildi.", reply_markup=admin_channels_keyboard())


@router.callback_query(lambda c: c.data and c.data.startswith("admchannel:"))
async def channel_detail(callback: CallbackQuery, db: Database) -> None:
    role = await require_admin(callback, db)
    if not role:
        await callback.answer()
        return
    cid = int(callback.data.split(":", 1)[1])
    async with db.session() as session:
        channel = await session.get(MandatoryChannel, cid)
    if not channel:
        await callback.answer("Kanal topilmadi.", show_alert=True)
        return
    await callback.answer()
    from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🟢/🔴 HOLAT", callback_data=f"channel_toggle:{cid}")],
        [InlineKeyboardButton(text="🗑 O‘CHIRISH", callback_data=f"channel_delete:{cid}")],
    ])
    await callback.message.answer(f"📢 {channel.title}\n\n🆔 {channel.chat_id}\n🔗 {channel.invite_url}\n{'🟢 Faol' if channel.is_active else '🔴 O‘chiq'}", reply_markup=keyboard)


@router.callback_query(lambda c: c.data and c.data.startswith("channel_toggle:"))
async def toggle_channel(callback: CallbackQuery, db: Database) -> None:
    role = await require_admin(callback, db)
    if not role:
        await callback.answer()
        return
    cid = int(callback.data.split(":", 1)[1])
    async with db.session() as session:
        channel = await session.get(MandatoryChannel, cid)
        if not channel:
            await callback.answer("Kanal topilmadi.", show_alert=True)
            return
        channel.is_active = not channel.is_active
        await session.commit()
        state = channel.is_active
    await callback.answer("Faol" if state else "O‘chirildi")


@router.callback_query(lambda c: c.data and c.data.startswith("channel_delete:"))
async def delete_channel(callback: CallbackQuery, db: Database) -> None:
    role = await require_admin(callback, db)
    if not role:
        await callback.answer()
        return
    cid = int(callback.data.split(":", 1)[1])
    async with db.session() as session:
        await session.execute(delete(MandatoryChannel).where(MandatoryChannel.id == cid))
        await session.commit()
    await callback.answer("Kanal o‘chirildi ✅")
    await callback.message.edit_text("✅ Majburiy kanal o‘chirildi.")


@router.message(F.text == "❤️ REACTION")
async def reaction_home(message: Message, db: Database) -> None:
    role = await require_admin(message, db)
    if not role:
        return
    async with db.session() as session:
        enabled = await get_setting(session, "reaction_enabled", "0")
        emoji = await get_setting(session, "reaction_emoji", "🔥")
    from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🟢/🔴 ON/OFF", callback_data="reaction:toggle")],
        [InlineKeyboardButton(text="✏️ EMOJI", callback_data="reaction:set")],
    ])
    await message.answer(f"❤️ REACTION\n\nHolat: {'🟢 ON' if enabled == '1' else '🔴 OFF'}\nEmoji: {emoji}", reply_markup=keyboard)


@router.callback_query(lambda c: c.data == "reaction:toggle")
async def reaction_toggle(callback: CallbackQuery, db: Database) -> None:
    role = await require_admin(callback, db)
    if not role:
        await callback.answer()
        return
    async with db.session() as session:
        current = await get_setting(session, "reaction_enabled", "0")
        await set_setting(session, "reaction_enabled", "0" if current == "1" else "1")
    await callback.answer("Reaction holati yangilandi")


@router.callback_query(lambda c: c.data == "reaction:set")
async def reaction_set(callback: CallbackQuery, state: FSMContext, db: Database) -> None:
    role = await require_admin(callback, db)
    if not role:
        await callback.answer()
        return
    await state.set_state(AdminReactionStates.emoji)
    await callback.answer()
    await callback.message.answer("✏️ Reaction uchun bitta emoji yuboring. Masalan: 🔥")


@router.message(AdminReactionStates.emoji)
async def reaction_value(message: Message, state: FSMContext, db: Database) -> None:
    role = await require_admin(message, db)
    if not role:
        return
    value = (message.text or "").strip()
    if not value or len(value) > 12:
        await message.answer("Bitta emoji yuboring.")
        return
    await state.clear()
    async with db.session() as session:
        await set_setting(session, "reaction_emoji", value)
    await message.answer(f"✅ Reaction saqlandi: {value}")


@router.callback_query(lambda c: c.data and c.data.startswith("publish:"))
async def publish_book(callback: CallbackQuery, db: Database, bot) -> None:
    role = await require_admin(callback, db)
    if not can_manage_content(role):
        await callback.answer()
        return
    from app.config import get_settings
    settings = get_settings()
    if not settings.target_channel_id:
        await callback.answer("TARGET_CHANNEL_ID sozlanmagan.", show_alert=True)
        return
    book_id = int(callback.data.split(":", 1)[1])
    async with db.session() as session:
        book = await session.get(Book, book_id)
        if not book:
            await callback.answer("Kitob topilmadi.", show_alert=True)
            return
        text = f"📚 {book.title}\n\n✍️ {book.author}\n\n{book.description}"
        from app.keyboards.inline import book_detail_keyboard
        markup = book_detail_keyboard(book)
    if book.cover_file_id:
        sent = await bot.send_photo(settings.target_channel_id, book.cover_file_id, caption=text, reply_markup=markup)
    else:
        sent = await bot.send_message(settings.target_channel_id, text, reply_markup=markup)
    async with db.session() as session:
        enabled = await get_setting(session, "reaction_enabled", "0")
        emoji = await get_setting(session, "reaction_emoji", "🔥")
    if enabled == "1":
        try:
            await bot.set_message_reaction(settings.target_channel_id, sent.message_id, reaction=[ReactionTypeEmoji(emoji=emoji)], is_big=True)
        except Exception:
            pass
    await callback.answer("Kanalga yuborildi ✅")
