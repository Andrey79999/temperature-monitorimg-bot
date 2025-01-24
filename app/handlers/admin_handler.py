from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from utils import get_user_credentials, user_activate, get_inactive_users
from keyboards.all_kb import KeyBoardText as kb_text
from keyboards.all_kb import user_list_kb, main_kb

admin_router = Router()


class AdminState(StatesGroup):
    waiting_for_activate_user = State()


@admin_router.message(F.text == kb_text.inactive_users)
async def get_inactive_user(message: Message, state: FSMContext):
    inactive_users = get_inactive_users()
    await message.answer('Список неактивированных пользователей\nПо нажатию Активация',
                         reply_markup=user_list_kb(inactive_users, 'update_user_data'))
    await state.set_state(AdminState.waiting_for_activate_user)


@admin_router.message(F.text == kb_text.all_users)
async def get_all_user(message: Message, state: FSMContext):
    user_credentials = get_user_credentials()
    await message.answer('Список пользователей\nПо нажатию вывод информации',
                         reply_markup=user_list_kb(user_credentials, 'user_data_info'))


@admin_router.callback_query(F.data.endswith('update_user_data'))
async def update_user_data(call: CallbackQuery, state: FSMContext):
    user_id = call.data.split('update_user_data')[0]
    user_activate(user_id=int(user_id))
    inactive_users = get_inactive_users()
    await call.message.edit_text('Список неактивированных пользователей\nПо нажатию Активация',
                                 reply_markup=user_list_kb(inactive_users, 'update_user_data'))


@admin_router.callback_query(F.data.endswith('user_data_info'))
async def update_user_data(call: CallbackQuery, state: FSMContext):
    user_id = call.data.split('user_data_info')[0]
    user_credentials = get_user_credentials()
    user_info = str(user_credentials[int(user_id)])
    await call.message.edit_text(user_info, reply_markup=user_list_kb(user_credentials, 'user_data_info'))


@admin_router.callback_query(F.data == kb_text.back)
async def back(call: CallbackQuery, state: FSMContext):
    user_id = call.message.from_user.id
    print(user_id)
    await call.answer(kb_text.back, reply_markup=main_kb(user_id))
    await state.clear()
