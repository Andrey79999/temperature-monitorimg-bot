import asyncpg
from asyncpg import Pool

class PostgresHandler:
    def __init__(self, database_url: str):
        self.pool: Pool = None
        self.database_url = database_url

    async def connect(self):
        self.pool = await asyncpg.create_pool(self.database_url)
        await self.create_tables()

    async def create_tables(self):
        async with self.pool.acquire() as conn:
            await conn.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    user_id BIGINT PRIMARY KEY,
                    username TEXT,
                    active BOOLEAN DEFAULT FALSE,
                    temp_min FLOAT DEFAULT 18.0,
                    temp_max FLOAT DEFAULT 25.0,
                    humidity_min FLOAT DEFAULT 30.0,
                    humidity_max FLOAT DEFAULT 60.0
                )
            ''')
            
            await conn.execute('''
                CREATE TABLE IF NOT EXISTS sensor_data (
                    id SERIAL PRIMARY KEY,
                    timestamp TIMESTAMP DEFAULT NOW(),
                    temperature FLOAT,
                    humidity FLOAT
                )
            ''')

    async def save_sensor_data(self, temperature: float, humidity: float):
        async with self.pool.acquire() as conn:
            await conn.execute('''
                INSERT INTO sensor_data (temperature, humidity)
                VALUES ($1, $2)
            ''', temperature, humidity)

    async def create_user(self, user_id: int, username: str):
        await self.pool.execute('''
            INSERT INTO users (user_id, username) 
            VALUES ($1, $2)
            ON CONFLICT (user_id) DO NOTHING
        ''', user_id, username)
    
    async def get_user(self, user_id: int):
        return await self.pool.fetchrow('SELECT * FROM users WHERE user_id = $1', user_id)

    async def update_user_settings(self, user_id: int, **kwargs):
        set_clause = ', '.join([f"{k} = ${i+2}" for i, k in enumerate(kwargs)])
        query = f'UPDATE users SET {set_clause} WHERE user_id = $1'
        await self.pool.execute(query, user_id, *kwargs.values())