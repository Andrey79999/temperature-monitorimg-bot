from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.types import Message
from keyboards.all_kb import main_kb, admin_kb
from create_bot import pg_db, admins
from sensors_handler import read_and_save_sensor_data
import asyncio
from utils import get_user_info
from locales.texts import Texts

main_router = Router()


@main_router.message(CommandStart())
async def cmd_start(message: Message):
    user_id = message.from_user.id
    user = await pg_db.get_user(user_id)
    
    if user:
        await message.answer(Texts.START_EXISTING_USER, reply_markup=main_kb(user_id))
    else:
        await pg_db.create_user(user_id, message.from_user.username)
        await message.answer(Texts.START_NEW_USER, reply_markup=main_kb(user_id))


@main_router.message(F.text == Texts.BTN_PROFILE)
async def profile_info(message: Message):
    user_id = message.from_user.id
    user_info = await asyncio.gather(get_user_info(int(user_id)))
    msg =str({key: val for key, val in user_info[0].items()})
    await message.answer(msg)
        

@main_router.message(F.text == Texts.BTN_TEMPERATURE)
async def current_temperature(message: Message):
    data = str(await asyncio.gather(read_and_save_sensor_data()))
    await message.answer(data)


@main_router.message(F.text == Texts.BTN_ADMIN_PANEL)
async def admin_panel(message: Message):
    await message.answer(Texts.ADMIN_PANEL,
                         reply_markup=admin_kb())


@main_router.message(F.text == Texts.BTN_STATUS)
async def status(message: Message):
    await message.answer('🛠️',
                         reply_markup=main_kb(message.from_user.id))