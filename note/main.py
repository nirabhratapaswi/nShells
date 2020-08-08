import note.db_setup
from datetime import datetime
from note.display import DisplayModule as display
from note.note_handler import handle
from note.reminder_handler import reminder_handle
import uuid
import sys
import readchar
from PyInquirer import prompt
from note.helpers import clear_screen, exit_animation
from note.cli import cli
from time import sleep

clear_screen()
argument_list = sys.argv

# TODO(nirabhra): Add reminders
REV_OPTIONS = {
    'Take a Note': 'n_1',
    'View all Notes': 'n_2',
    'Edit Note': 'n_10',
    'Filter Notes by Tag': 'n_7',
    'View Note': 'n_4',
    'View tags': 'n_6',
    'Delete a Note': 'n_5',
    'Delete a Tag': 'n_8',
    'View all Notes with id': 'n_3',
    'Create a reminder': 'r_1',
    'View all Reminders': 'r_2',
    'View Reminder': 'r_3',
    'Delete reminders for a Note': 'r_4',
    'Done for now? - Exit :)': 'q',
}

def interact():
    """
    Interact for user input
    """
    ret_val = True

    questions = [
        {
            'type': 'list',
            'name': 'choice',
            'message': 'What would you like to do?',
            'choices': [key for key, value in REV_OPTIONS.items()]
        },
    ]
    answers = prompt(questions)

    clear_screen()

    choice = REV_OPTIONS[answers['choice']]
    if choice.startswith('n_'):
        ret_val = handle.switch(choice.split('n_')[1])
    elif choice.startswith('r_'):
        ret_val = reminder_handle.switch(choice.split('r_')[1])
    elif choice == 'q':
        farewell_text = 'Thankyou for using notes!\nBye 🖐'
        total_animation_time = 1.5

        exit_animation(farewell_text, total_animation_time)
        ret_val = False

    return ret_val

if __name__ == '__main__':
    continue_ = True
    while continue_:
        continue_ = interact()

def main():
    """
    Main function
    """
    continue_ = True

    continue_ = cli.evaluate(argument_list[1:])

    if continue_:
        while continue_:
            continue_ = interact()

        clear_screen()