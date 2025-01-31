import asyncio

from create_bot import bot, dp
from handlers.main_handler import main_router
from handlers.admin_handler import admin_router
from handlers.user_data_handler import user_router
from handlers.graph_handler import graph_router
from create_bot import pg_db, scheduler
from sensors_handler import read_and_save_sensor_data, check_notifications

# from work_time.time_func import send_time_msg


async def main():
    await pg_db.connect()
    # scheduler.add_job(
    #     check_notifications,
    #     'interval',
    #     seconds=5,
    #     max_instances=1
    # )
    scheduler.add_job(
        read_and_save_sensor_data,
        'interval',
        seconds=3,
        max_instances=1
    )
    scheduler.start()
    
    dp.include_router(main_router)
    dp.include_router(admin_router)
    dp.include_router(user_router)
    dp.include_router(graph_router)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
