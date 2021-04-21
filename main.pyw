import os
import logging
from datetime import date

from src import renderer, reader

DATA_FILE = 'C:\\Users\\User\\MAIN\\174517\\domestico\\ricorrenze.yml'
LOG_FILE = 'event-reminder.log'
LOG_FORMAT = '%(asctime)s - %(levelname)5s - %(filename)10s - %(message)s'

logging.basicConfig(filename=os.path.join(os.path.dirname(__file__), LOG_FILE),
                    filemode='a',
                    format=LOG_FORMAT,
                    level=logging.INFO)
LOG = logging.getLogger()

if __name__ == '__main__':
    try:
        today = date.today()
        month: str = reader.get_month(today.month)
        day = today.day

        daily_data = reader.read_data(DATA_FILE, month, day)

        LOG.info(f"{today}: {len(daily_data)} entries found")

        if daily_data:
            renderer.open_window(f'{day} {month}', daily_data)
    except Exception as e:
        LOG.error(e)
