import os
import logging
import configparser
import sys
from datetime import date

from eventreminder import reader, renderer

LOG_FILE = 'event-reminder.log'
LOG_FORMAT = '%(asctime)s - %(levelname)7s - %(message)s'
logging.basicConfig(filename=os.path.join(os.path.dirname(__file__), LOG_FILE),
                    filemode='a',
                    format=LOG_FORMAT,
                    level=logging.INFO)
LOG = logging.getLogger()


def read_conf() -> configparser.ConfigParser:
    config_file = os.path.join(os.path.dirname(__file__), 'config.ini')
    if not os.path.exists(config_file):
        LOG.fatal("config.ini not found")
        sys.exit(1)
    config = configparser.ConfigParser()
    config.read(config_file)
    return config


def get_event_path(config: configparser.ConfigParser) -> str:
    file_path = config['EVENT-REMINDER']['event-file']
    if '\\' not in file_path and '/' not in file_path:
        return os.path.join(os.path.dirname(__file__), file_path)
    if not os.path.exists(file_path):
        LOG.fatal("ini file: event file %s not found", file_path)
        sys.exit(1)


def get_log_opt(config: configparser.ConfigParser) -> bool:
    return bool(config['EVENT-REMINDER']['log-day'] == '1')


def main():
    try:
        cfg = read_conf()
        event_path = get_event_path(cfg)
        do_log_day = get_log_opt(cfg)

        today = date.today()
        data = reader.read_lines(event_path, today.day, today.month, today.isoweekday())

        if do_log_day:
            LOG.info('%s: %d events found', today, len(data.events))

        if data.errors:
            LOG.warning('Bad lines: %s', data.errors)

        if data.events:
            renderer.open_window(f'{today : %Y-%m-%d}', data.events)

    except KeyError as ex:
        LOG.fatal("ini file: %s value not found", ex)
    except Exception as ex:
        LOG.error(ex)


if __name__ == '__main__':
    main()
