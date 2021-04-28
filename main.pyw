import os
import logging
import configparser
import sys
from datetime import date

from src import renderer, reader

LOG_FILE = 'event-reminder.log'
LOG_FORMAT = '%(asctime)s - %(levelname)7s - %(message)s'
logging.basicConfig(filename=os.path.join(os.path.dirname(__file__), LOG_FILE),
                    filemode='a',
                    format=LOG_FORMAT,
                    level=logging.INFO)
LOG = logging.getLogger()

EVENT_FILE = ''
LOG_DAY = False
try:
    config_file = os.path.join(os.path.dirname(__file__), 'config.ini')
    if not os.path.exists(config_file):
        LOG.fatal("config.ini not found")
        sys.exit(1)
    CFG = configparser.ConfigParser()
    CFG.read(config_file)

    EVENT_FILE = CFG['EVENT-REMINDER']['event-file']
    if '\\' not in EVENT_FILE and '/' not in EVENT_FILE:
        EVENT_FILE = os.path.join(os.path.dirname(__file__), EVENT_FILE)
    if not os.path.exists(EVENT_FILE):
        LOG.fatal("ini file: event file %s not found", EVENT_FILE)
        sys.exit(1)

    LOG_DAY = bool(CFG['EVENT-REMINDER']['log-day'] == '1')
except KeyError as ex:
    LOG.fatal("ini file: %s value not found", ex)
    sys.exit(1)

if __name__ == '__main__':
    try:
        today = date.today()
        day = today.day
        month = today.month
        weekday = today.weekday()

        data = reader.read_lines(EVENT_FILE, day, month, weekday)

        if LOG_DAY:
            LOG.info('%s: %d events found', today, len(data.events))

        if data.errors:
            LOG.warning('Bad lines: %s', data.errors)

        if data.events:
            renderer.open_window(f'{day} {month}', data.events)
    except Exception as ex:
        LOG.error(ex)
