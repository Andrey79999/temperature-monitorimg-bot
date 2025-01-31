import serial
import sys
from create_bot import pg_db
import glob
from config.logging_config import logger


def serial_ports():
    """ Lists serial port names

        :raises EnvironmentError:
            On unsupported or unknown platforms
        :returns:
            A list of the serial ports available on the system
    """
    if sys.platform.startswith('win'):
        ports = ['COM%s' % (i + 1) for i in range(256)]
    elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
        # this excludes your current terminal "/dev/tty"
        ports = glob.glob('/dev/tty[A-Za-z]*')
    elif sys.platform.startswith('darwin'):
        ports = glob.glob('/dev/tty.*')
    else:
        raise EnvironmentError('Unsupported platform')

    result = []
    for port in ports:
        try:
            s = serial.Serial(port)
            s.close()
            result.append(port)
        except (OSError, serial.SerialException):
            pass
    return result

   
    
async def read_and_save_sensor_data():
    # ports = serial_ports()
    # ser = serial.Serial(ports[1], 9600)
    max_retry = 5
    for _ in range(max_retry):
        try:
            with serial.Serial('COM4', 9600, timeout=2) as ser:
                response = ser.readline()
                decoded_response = response.decode('utf-8', errors='ignore')
                temperature = float(decoded_response.split('Температура:')[1].split(';')[0])
                humidity = float(decoded_response.split('Влажность:')[1])
                await pg_db.save_sensor_data(temperature, humidity)
        except Exception as e:
            logger.error(f"Read sensor data error: {e}")
            temperature = None
            humidity = None
        if temperature is not None and humidity is not None:
            break
    return {'temperature': temperature, 'humidity': humidity}

async def check_notifications():
    latest = await pg_db.pool.fetchrow('SELECT * FROM sensor_data ORDER BY id DESC LIMIT 1')
    users = await pg_db.pool.fetch('SELECT * FROM users WHERE active = TRUE')
    
    for user in users:
        if (latest['temperature'] < user['temp_min'] or latest['temperature'] > user['temp_max'] or
            latest['humidity'] < user['humidity_min'] or latest['humidity'] > user['humidity_max']):
            await bot.send_message(
                user['user_id'],
                f"⚠️ Превышены пределы: Температура {latest['temperature']}°C, Влажность {latest['humidity']}%"
            )


async def test():
    import asyncio
    r = await asyncio.gather(read_and_save_sensor_data())
    print(r)

if __name__ == "__main__":
    import asyncio
    loop = asyncio.get_event_loop()
    loop.run_until_complete(test())
