import os
import logging
from datetime import date

from src import renderer, reader

DATA_FILE = 'C:\\Users\\User\\MAIN\\174517\\domestico\\ricorrenze.yml'
LOG_FILE = 'event-reminder.log'
LOG_FORMAT = '%(asctime)s - %(levelname)7s - %(filename)10s - %(message)s'

logging.basicConfig(filename=os.path.join(os.path.dirname(__file__), LOG_FILE),
                    filemode='a',
                    format=LOG_FORMAT,
                    level=logging.INFO)
LOG = logging.getLogger()

if __name__ == '__main__':
    try:
        today = date.today()
        day = today.day
        month = today.month
        weekday = today.weekday()

        data = reader.read_lines(DATA_FILE, day, month, weekday)

        LOG.info('%s: %d entries found', today, len(data.events))

        if data.errors:
            LOG.warning('Bad lines: %s', data.errors)

        if data.events:
            renderer.open_window(f'{day} {month}', data.events)
    except Exception as ex:
        LOG.error(ex)
