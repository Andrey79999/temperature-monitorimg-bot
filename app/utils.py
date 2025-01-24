from create_bot import pg_db

async def get_user_credentials():
    return await pg_db.pool.fetch('SELECT * FROM users')

async def user_activate(user_id: int):
    await pg_db.pool.execute('UPDATE users SET active = TRUE WHERE user_id = $1', user_id)

async def get_inactive_users():
    return await pg_db.pool.fetch('SELECT * FROM users WHERE NOT active')
