import multiprocessing
import time
import sys
import os
import logging
from note.reminder_crud import update_reminder_pid, delete_reminder_by_rowid

def notify(title, body):
    """ Notify """
    os.system(f'notify-send -u critical "{title}" "{body}"')

def _create_reminder(rowid, delay, title, body=''):
    """ Create a reminder """
    # Store pid for termination
    pid = os.getpid()

    try:
        update_reminder_pid(rowid, pid)
    except Exception:
        pass

    time.sleep(delay)
    notify(title, body)

    try:
        delete_reminder_by_rowid(rowid)

    except Exception:
        pass

    os._exit(0)


def create_reminder(rowid, delay, title, body='', ):
    """ Create reminder """
    # Fork the current process

    if not isinstance(delay, int):
        raise TypeError('delay is not of type Number')

    fid = os.fork()

    if fid > 0:
        # Return parent process response
        return True

    # Continue with forked code
    _create_reminder(rowid, delay, title, body)
