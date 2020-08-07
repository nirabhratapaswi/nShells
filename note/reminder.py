import multiprocessing
import time
import sys
import os
import logging

def notify(title, body):
    """ Notify """
    os.system(f'notify-send -u critical "{title}" "{body}"')

def _create_reminder(delay, title, body=''):
    """ Create a reminder """
    # Store pid for termination
    pid = os.getpid()
    logging.info(f'Starting reminder on process {pid}')

    time.sleep(delay)
    notify(title, body)

    logging.info(f'Exiting reminder on process {pid}')


def create_reminder(delay, title, body=''):
    """ Create reminder """
    # Fork the current process

    if not isinstance(delay, int):
        raise TypeError('delay is not of type Number')

    fid = os.fork()

    if fid > 0:
        # Return parent process response
        return True

    # Continue with forked code
    _create_reminder(delay, title, body)
