from aiogram import Router, F
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message
from utils import get_user_credentials
from keyboards.all_kb import main_kb, admin_kb
from keyboards.all_kb import KeyBoardText as kb_text
from handlers.admin_handler import AdminState
from create_bot import pg_db

main_router = Router()


@main_router.message(CommandStart())
async def cmd_start(message: Message):
    await pg_db.create_user(message.from_user.id, message.from_user.username)
    await message.answer("✅ Ваш запрос отправлен администратору. Ожидайте активации.")


@main_router.message(F.text == kb_text.profile)
async def add_user(message: Message):
    user_credentials = get_user_credentials()
    if message.from_user.id in user_credentials:
        user_data = str(user_credentials[message.from_user.id])
        await message.answer(user_data)
    else:
        await message.answer('Данных о пользователе нет.')


@main_router.message(F.text == kb_text.admin)
async def admin_panel(message: Message):
    await message.answer('Панель администратора',
                         reply_markup=admin_kb(message.from_user.id))
