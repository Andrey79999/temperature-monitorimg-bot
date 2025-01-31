from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton
from create_bot import admins
from locales.texts import Texts

def main_kb(user_telegram_id: int):
    kb_list = [
        [KeyboardButton(text=Texts.BTN_TEMPERATURE_GRAPH), KeyboardButton(text=Texts.BTN_TEMPERATURE)],
        [KeyboardButton(text=Texts.BTN_STATUS), KeyboardButton(text=Texts.BTN_PROFILE)]
    ]
    if user_telegram_id in admins:
        kb_list.append([KeyboardButton(text=Texts.BTN_ADMIN_PANEL)])
    return ReplyKeyboardMarkup(keyboard=kb_list, resize_keyboard=True, one_time_keyboard=True)

def admin_kb():
    kb_list = [
        [KeyboardButton(text=Texts.BTN_ALL_USERS), KeyboardButton(text=Texts.BTN_INACTIVE_USERS)],
        [KeyboardButton(text=Texts.BTN_BACK)]
    ]
    return ReplyKeyboardMarkup(keyboard=kb_list, resize_keyboard=True, one_time_keyboard=True)

def back_kb():
    return ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text=Texts.BTN_BACK)]], resize_keyboard=True)

def user_list_kb(users, prefix):
    kb_list = []
    for user in users[0]:
        if user:
            user = user
            kb_list.append([InlineKeyboardButton(
                text=user.get('username'),
                callback_data=str(user.get('user_id')) + prefix)]
            )
    return InlineKeyboardMarkup(inline_keyboard=kb_list)

def period_kb():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=k, callback_data=f'period_{v}')] for k, v in Texts.PERIODS.items()
    ])