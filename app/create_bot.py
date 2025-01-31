from aiogram import Bot, Dispatcher, BaseMiddleware
from aiogram.types import Message
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
import os
from dotenv import load_dotenv
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from db_handler.db_class import PostgresHandler
# from apscheduler.schedulers.asyncio import AsyncIOScheduler

# from db_handler.db_class import PostgresHandler

# pg_db = PostgresHandler(config('PG_LINK'))
# scheduler = AsyncIOScheduler(timezone='Europe/Moscow')

load_dotenv(override=True)

TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
ADMIN_ID = int(os.getenv('ADMIN_ID'))
admins = [ADMIN_ID]
DATABASE_URL = os.getenv('DATABASE_URL')

pg_db = PostgresHandler(DATABASE_URL)
scheduler = AsyncIOScheduler(timezone='Asia/Novosibirsk')

class UserCheckMiddleware(BaseMiddleware):
    async def __call__(self, handler, event: Message, data):
        if event.message is not None:
            if event.message.text and event.message.text.startswith('/start'):
                return await handler(event, data)
        
            user_id = event.message.from_user.id
            if user_id in admins:
                return await handler(event, data)
                
            user = await pg_db.get_user(user_id)
            if not user or not user['active']:
                await event.message.answer("❌ Доступ запрещен. Ожидайте активации администратором.")
                return
            else:
                return await handler(event, data)
        if event.callback_query is not None:
            # print(event.callback_query)
            # print(dir(event.callback_query))
            user_id = event.callback_query.from_user.id
            if user_id in admins:
                return await handler(event, data)
                
            user = await pg_db.get_user(user_id)
            if not user or not user['active']:
                await event.callback_query.answer("❌ Доступ запрещен. Ожидайте активации администратором.")
                return
            else:
                return await handler(event, data)

print('start')
bot = Bot(token=TELEGRAM_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher(storage=MemoryStorage())
dp.update.middleware.register(UserCheckMiddleware())