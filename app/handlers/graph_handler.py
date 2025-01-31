from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, FSInputFile
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from datetime import datetime, timedelta, timezone 
import matplotlib.pyplot as plt
from create_bot import pg_db
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from keyboards.all_kb import period_kb
from locales.texts import Texts

graph_router = Router()

class GraphPeriod(StatesGroup):
    waiting_period = State()

@graph_router.message(F.text == Texts.BTN_TEMPERATURE_GRAPH)
async def select_graph_period(message: Message, state: FSMContext):
    await message.answer(Texts.SELECT_PERIOD, reply_markup=period_kb())

@graph_router.callback_query(F.data.startswith('period_'))
async def generate_graph(callback: CallbackQuery):
    hours = int(callback.data.split('_')[1])
    end_time = datetime.strptime(str(datetime.now(timezone.utc)).split('+')[0], "%Y-%m-%d %H:%M:%S.%f")
    start_time = end_time - timedelta(hours=hours)
    
    records = await pg_db.pool.fetch(
        'SELECT timestamp, temperature, humidity FROM sensor_data WHERE timestamp BETWEEN $1 AND $2 ORDER BY timestamp',
        start_time, end_time
    )

    fig, ax = plt.subplots()
    ax.plot([r['timestamp'] for r in records], [r['temperature'] for r in records], label='temperature')
    ax.plot([r['timestamp'] for r in records], [r['humidity'] for r in records], label='humidity')
    ax.legend()
    
    plt.savefig('tmp.jpg')
    await callback.message.answer_photo(FSInputFile('tmp.jpg'), caption=Texts.GRAPH_CAPTION.format(hours=hours))
    plt.close()