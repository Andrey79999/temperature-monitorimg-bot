import threading

from aiogram import Router, F
from aiogram.filters import Command, StateFilter
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from keyboards.all_kb import KeyBoardText as kb_text
from keyboards.all_kb import back_kb, main_kb, admin_kb

user_router = Router()


class LoginForm(StatesGroup):
    waiting_for_login_password = State()



@user_router.message(F.text == kb_text.back)
async def user_go_back(message: Message, state: FSMContext):
    await message.answer('Начало',
                         reply_markup=main_kb(message.from_user.id))
    await state.clear()


