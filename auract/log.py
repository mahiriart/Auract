import os
import textwrap
import sys
import logging


def log(message='', end='\n', type=''):
    if type != 'debug':
        print(message, file=sys.stderr, flush=True, end=end)
    if type == 'debug':
        logging.debug(message)
    elif type == 'info':
        logging.info(message)
    elif type == 'warning':
        logging.warning(message)
    elif type == 'error':
        logging.error(message)
    elif type == 'critical':
        logging.critical(message)


def quit_with_error(text):
    terminal_width, _ = get_terminal_size_stderr()
    log()
    for line in textwrap.wrap(text, width=terminal_width - 1):
        log(message=('Error: ' + line))
        logging.error(line)
    log()
    sys.exit()


def get_terminal_size_stderr(fallback=(80, 24)):
    try:
        size = os.get_terminal_size(sys.__stderr__.fileno())
    except (AttributeError, ValueError, OSError):
        size = os.terminal_size(fallback)
    return size
