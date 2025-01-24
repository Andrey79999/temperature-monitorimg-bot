from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton
from create_bot import admins


class KeyBoardText:
    profile = '👤 Профиль'
    end_cont = 'Температура'
    start_cont = 'График температуры'
    status = 'Статус'
    admin = '⚙️ Админ панель'
    all_users = 'Посмотреть всех пользователей'
    inactive_users = 'Посмотреть не активированных пользователей'
    back = 'назад'


def main_kb(user_telegram_id: int):
    kb_list = [
        [KeyboardButton(text=KeyBoardText.start_cont), KeyboardButton(text=KeyBoardText.end_cont)],
        [KeyboardButton(text=KeyBoardText.status), KeyboardButton(text=KeyBoardText.profile)]
    ]
    if user_telegram_id in admins:
        kb_list.append([KeyboardButton(text=KeyBoardText.admin)])
    keyboard = ReplyKeyboardMarkup(keyboard=kb_list, resize_keyboard=True, one_time_keyboard=True)
    return keyboard


def admin_kb(user_telegram_id: int):
    if user_telegram_id in admins:
        kb_list = [[KeyboardButton(text=KeyBoardText.all_users), KeyboardButton(text=KeyBoardText.inactive_users)],
                   [KeyboardButton(text=KeyBoardText.back)]]
        keyboard = ReplyKeyboardMarkup(keyboard=kb_list, resize_keyboard=True, one_time_keyboard=True)
        return keyboard


def back_kb():
    kb_list = [
        [KeyboardButton(text=KeyBoardText.back)]
    ]
    keyboard = ReplyKeyboardMarkup(keyboard=kb_list, resize_keyboard=True, one_time_keyboard=True)
    return keyboard


def user_list_kb(users, prefix):
    kb_list = []
    for user_id, user_data in users.items():
        kb_list.append([InlineKeyboardButton(
            text=user_data['username'],
            callback_data=str(user_id) + prefix)]
        )
    return InlineKeyboardMarkup(inline_keyboard=kb_list)
