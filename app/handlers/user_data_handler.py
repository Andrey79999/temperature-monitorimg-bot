
from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from keyboards.all_kb import main_kb
from locales.texts import Texts

user_router = Router()


class LoginForm(StatesGroup):
    waiting_for_login_password = State()



@user_router.message(F.text == Texts.BTN_BACK)
async def user_go_back(message: Message, state: FSMContext):
    await message.answer(Texts.BEGIN,
                         reply_markup=main_kb(message.from_user.id))
    await state.clear()


