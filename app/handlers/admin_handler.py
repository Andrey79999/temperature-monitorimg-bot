from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from utils import get_user_credentials, user_activate, get_inactive_users, get_user_info
from keyboards.all_kb import user_list_kb, main_kb
import asyncio
from locales.texts import Texts
admin_router = Router()


class AdminState(StatesGroup):
    waiting_for_activate_user = State()


@admin_router.message(F.text == Texts.BTN_INACTIVE_USERS)
async def get_inactive_user(message: Message, state: FSMContext):
    inactive_users = await asyncio.gather(get_inactive_users())
    await message.answer(Texts.INACTIVE_USERS,
                         reply_markup=user_list_kb(inactive_users, 'update_user_data'))
    await state.set_state(AdminState.waiting_for_activate_user)


@admin_router.message(F.text == Texts.BTN_ALL_USERS)
async def get_all_user(message: Message, state: FSMContext):
    user_credentials = await asyncio.gather(get_user_credentials())
    await message.answer(Texts.ACTIVE_USERS,
                         reply_markup=user_list_kb(user_credentials, 'user_data_info'))


@admin_router.callback_query(F.data.endswith('update_user_data'))
async def update_user_data(call: CallbackQuery, state: FSMContext):
    user_id = call.data.split('update_user_data')[0]
    await user_activate(user_id=int(user_id))
    inactive_users = await asyncio.gather(get_inactive_users())
    await call.message.edit_text(Texts.INACTIVE_USERS,
                                 reply_markup=user_list_kb(inactive_users, 'update_user_data'))


@admin_router.callback_query(F.data.endswith('user_data_info'))
async def user_data_info(call: CallbackQuery, state: FSMContext):
    user_id = call.data.split('user_data_info')[0]
    user_credentials = await asyncio.gather(get_user_credentials())
    user_info = await asyncio.gather(get_user_info(int(user_id)))
    msg =str({key: val for key, val in user_info[0].items()}) 
    await call.message.edit_text(msg, reply_markup=user_list_kb(user_credentials, 'user_data_info'))


@admin_router.callback_query(F.data == Texts.BTN_BACK)
async def back(call: CallbackQuery, state: FSMContext):
    user_id = call.message.from_user.id
    await call.answer(Texts.BTN_BACK, reply_markup=main_kb(user_id))
    await state.clear()
