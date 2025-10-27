import asyncio
from collections import defaultdict
import random
from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import os

BOT_TOKEN = os.getenv('BOT_TOKEN')
ADMIN_IDS = os.getenv('ADMIN_IDS')
CHANNEL_IDS = os.getenv('CHANNEL_IDS')

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

authorized_users = set()
user_ids = defaultdict()


async def check_subscriptions(user_id: int) -> bool:
    for chat_id in CHANNEL_IDS:
        user_channel_status = await bot.get_chat_member(chat_id=chat_id, user_id=user_id)
        if user_channel_status.status != 'member':
            return False
    return True


check_kb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Канал 1', url='https://t.me/channel1')],
    [InlineKeyboardButton(text='Канал 2', url='https://t.me/channel2')],
    [InlineKeyboardButton(text='Канал 3', url='https://t.me/channel3')],
    [InlineKeyboardButton(text='Проверить подписки', callback_data='check_sub')]
])

member_kb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Канал 1', url='https://t.me/channel1')],
    [InlineKeyboardButton(text='Канал 2', url='https://t.me/channel2')],
    [InlineKeyboardButton(text='Канал 3', url='https://t.me/channel3')]
])

admin_kb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Выбрать победителя', callback_data='choose_winner')],
    [InlineKeyboardButton(text='Посмотреть всех участников', callback_data='view_users')]
])


@dp.message(CommandStart())
async def start(message):
    if message.from_user.id in ADMIN_IDS:
        await message.answer("Привет, админ!", reply_markup=admin_kb)
    elif message.from_user.username in authorized_users:
        await message.answer("Ты участвуешь в розыгрыше! Жди результаты)", reply_markup=member_kb)
    else:
        text = "Привет! 👋 Чтобы принять участие в розыгрыше, подпишись на 3 канала:"
        await message.answer(text, reply_markup=check_kb)


@dp.callback_query(F.data == "check_sub")
async def check_sub(callback):
    user = callback.from_user
    ok = await check_subscriptions(user.id)

    if ok:
        authorized_users.add(user.username)
        user_ids[user.username] = user.id
        await callback.message.edit_text(
            "✅ Отлично! Ты зарегистрирован в розыгрыше 🎉"
        )
    else:
        await callback.answer("Ты подписан не на все каналы (", show_alert=True, reply_markup=check_kb)


@dp.callback_query(F.data == "choose_winner")
async def choose_winner(callback):
    if callback.from_user.id not in ADMIN_IDS:
        return await callback.answer("Нет доступа", show_alert=True)

    if not authorized_users:
        return await callback.answer("Список участников пуст!", show_alert=True, reply_markup=admin_kb)

    winner = random.choice(list(authorized_users))
    winner_id = user_ids[winner]
    await callback.message.answer(f"🎉 Победитель: @{winner}")
    await bot.send_message(winner_id, "Поздравляем с победой!")


@dp.callback_query(F.data == "view_users")
async def view_users(callback):
    if callback.from_user.id not in ADMIN_IDS:
        return await callback.answer("Нет доступа", show_alert=True)

    if not authorized_users:
        await callback.message.answer("📝 Список участников пуст!", reply_markup=admin_kb)
        return

    users_list = list(authorized_users)
    total_count = len(users_list)
    
    message_text = f"👥 Участники розыгрыша (всего: {total_count}):\n\n"
    message_text += "\n".join(f"• @{user}" for user in users_list)
    
    await callback.message.answer(message_text)


async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
