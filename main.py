import setup
from datetime import datetime
from helpers import crud
from helpers.display import DisplayModule as display
from helpers.handler import Handle as handle
import uuid
import sys
from collections import OrderedDict
import readchar

# TODO(nirabhra): Add reminders
OPTIONS = OrderedDict()
OPTIONS['1'] = 'Take a Note'
OPTIONS['2'] = 'View all Notes'
OPTIONS['3'] = 'View all Notes with id'
OPTIONS['4'] = 'View Note <index>(select from list)'
OPTIONS['5'] = 'Delete a Note <index>(select from list)'
OPTIONS['6'] = 'View tags'
OPTIONS['7'] = 'List all Notes for a Tag'
OPTIONS['8'] = 'Delete a Tag <index>(select from list)'
OPTIONS['q'] = 'Done for now? - Exit :)'

def interact():
    """
    Interact for user input
    """
    ret_val = True
    display.display_options(OPTIONS)

    option = readchar.readkey()
    if option == '\x03':
        return False

    ret_val = handle.switch(option)

    return ret_val

if __name__ == '__main__':
    continue_ = True
    while continue_:
        continue_ = interact()
