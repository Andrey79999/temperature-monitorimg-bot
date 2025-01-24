from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import io
from create_bot import pg_db
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

graph_router = Router()

class GraphPeriod(StatesGroup):
    waiting_period = State()

@graph_router.message(F.text == 'График температуры')
async def select_graph_period(message: Message, state: FSMContext):
    periods = {
        '1 час': 1,
        '6 часов': 6,
        'Сутки': 24,
        'Неделя': 168,
        'Месяц': 720
    }
    buttons = [[InlineKeyboardButton(text=k, callback_data=f'period_{v}')] for k, v in periods.items()]
    await message.answer('Выберите период:', reply_markup=InlineKeyboardMarkup(inline_keyboard=buttons))

@graph_router.callback_query(F.data.startswith('period_'))
async def generate_graph(callback: CallbackQuery):
    hours = int(callback.data.split('_')[1])
    end_time = datetime.now()
    start_time = end_time - timedelta(hours=hours)
    
    records = await pg_db.pool.fetch(
        'SELECT timestamp, temperature, humidity FROM sensor_data WHERE timestamp BETWEEN $1 AND $2',
        start_time, end_time
    )
    
    # Построение графика
    fig, ax = plt.subplots()
    ax.plot([r['timestamp'] for r in records], [r['temperature'] for r in records], label='Температура')
    ax.plot([r['timestamp'] for r in records], [r['humidity'] for r in records], label='Влажность')
    ax.legend()
    
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    
    await callback.message.answer_photo(buf, caption=f'График за последние {hours} часов')
    plt.close()