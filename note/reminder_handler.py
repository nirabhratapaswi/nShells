import os
from datetime import datetime, timedelta
import uuid
import readchar
from prompt_toolkit import prompt as prompt_tk
from prompt_toolkit.history import FileHistory
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory
from prompt_toolkit.contrib.completers import WordCompleter
from PyInquirer import prompt
from time import sleep
from note.helpers import clear_screen, exit_animation
from note import note_crud
from note import reminder_crud as crud
from note.display import DisplayModule as display
from note.reminder import create_reminder
from click import edit as editor
from time import sleep

DIR_PATH = os.path.dirname(os.path.realpath(__file__))

STANDARD_CHOICE_MESSAGES = {
    'general': 'Please select an option: ',
}
STANDARD_MESSAGES = {
    'notes_not_found': 'No notes found, please create a note first.\n',
    'reminders_not_found': 'No reminders found, start by creating one ->\n',
}

def shorten(text: str, max_length: int = 50) -> str:
    """ Shorten text """
    return text if len(text) <= max_length else text[:max_length-3] + '...'

def select_from_shells(shells=None):
    """ Select prompt for shells """
    shells = shells if shells else note_crud.list_shells()
    if not shells or len(shells) == 0:
        return None

    shells_ = {
        element['shell_id']: element
        for element in shells
    }

    options = {
        shorten(value['vision']): key
        for key, value in shells_.items()
    }
    questions = [
        {
            'type': 'list',
            'name': 'choice',
            'message': 'Choose note:',
            'choices': [key for key, value in options.items()]
        },
    ]
    answers = prompt(questions)

    id_ = options[answers['choice']]

    note = note_crud.get_shell_from_id(id_)

    clear_screen()

    return note

def select_from_reminders(reminders=None):
    """ Select prompt for reminders """
    reminders = reminders if reminders else crud.list_reminders()
    if not reminders or len(reminders) == 0:
        return None

    for reminder in reminders:
        reminder['target_time'] = reminder['target_time'] if 'target_time' in reminder else []
        reminders_ = crud.list_reminders_from_shell_id(reminder['shell_id'])
        reminder['target_time'] = ', '.join([str(r['target_time']) for r in reminders_])

    reminders_ = {
        element['shell_id']: element
        for element in reminders
    }

    options = {
        shorten(value['title']): key
        for key, value in reminders_.items()
    }
    questions = [
        {
            'type': 'list',
            'name': 'choice',
            'message': 'Choose reminder',
            'choices': [key for key, value in options.items()]
        },
    ]
    answers = prompt(questions)

    id_ = options[answers['choice']]

    clear_screen()

    return reminders_[id_]

class ReminderHandle(object):
    """
    Reminder Handle Module
    """
    _default_tag_name = '@reminder'

    @classmethod
    def switch(cls, option, *args):
        return getattr(cls, 'handle_option_' + str(option), cls.incorrect_option)(*args)

    @classmethod
    def handle_option_1(cls, type_=None, delay=None, title=None, body=None):
        """
        OPERATION: CREATE
        Create a Reminder
        """
        if not type_:
            options = {
                'Create new': '1',
                'Select from notes': '2',
            }
            questions = [
                {
                    'type': 'list',
                    'name': 'choice',
                    'message': STANDARD_CHOICE_MESSAGES['general'],
                    'choices': [key for key, value in options.items()]
                },
            ]
            answers = prompt(questions)

            type_ = options[answers['choice']]
        else:
            type_ = str(type_)

        if str(type_) == '1':
            if not title:
                title = prompt_tk('Title: ')
            if not body:
                body = prompt_tk('Details(optional)?: ')
            if not delay:
                delay = int(prompt_tk('Enter delay(in sec): '))

            try:
                time = datetime.now()
                target_time = time + timedelta(seconds=delay)
                shell_id = str(uuid.uuid4()).replace('-', '')
                shell_data = (shell_id, title, body, cls._default_tag_name, time)
                reminder_id = str(uuid.uuid4()).replace('-', '')
                reminder_data = (reminder_id, target_time, shell_id)

                # Create database entries
                note_crud.create_shell(shell_data)
                crud.create_reminder(reminder_data)

                create_reminder(delay, title, body)
            except Exception as e:
                display.display_text(f'Error: {str(e)}')
        elif str(type_) == '2':
            skip = False
            note = select_from_shells()
            if not note:
                display.display_text(STANDARD_MESSAGES['notes_not_found'])
                skip = True

            if not skip:
                if not delay:
                    delay = int(prompt_tk('Enter delay(in sec): '))

                title = note['vision'] \
                            if len(note['vision']) <= 50 \
                            else note['vision'][:47] + '...'
                body = note['thought'] \
                            if len(note['thought']) <= 50 \
                            else note['thought'][:47] + '...'

                time = datetime.now()
                target_time = time + timedelta(seconds=delay)
                reminder_id = str(uuid.uuid4()).replace('-', '')
                reminder_data = (reminder_id, target_time, note['shell_id'])

                crud.create_reminder(reminder_data)

                create_reminder(delay, title, body)

        return True

    @staticmethod
    def handle_option_2():
        """
        Operation: READ
        List all Reminders
        """
        reminders = crud.list_reminders()
        for reminder in reminders:
            reminder['target_time'] = reminder['target_time'] if 'target_time' in reminder else []
            reminders_ = crud.list_reminders_from_shell_id(reminder['shell_id'])
            reminder['target_time'] = ', '.join([str(r['target_time']) for r in reminders_])

        display.display_reminders(reminders)
        return True

    @classmethod
    def handle_option_3(cls):
        """
        Operation: READ
        View a Reminder
        """
        reminder = select_from_reminders()
        if not reminder:
            display.display_text(STANDARD_MESSAGES['reminders_not_found'])
            return cls.handle_option_1()

        display.display_text(f'Title  :   {reminder.get("title")}\n')
        display.display_text(f'Body :   {reminder.get("body")}\n\n')
        display.display_text(f'Target Times : {reminder.get("target_time")}\n')
        display.display_text(f'shell_id - {reminder.get("shell_id")}')

        display.display_text('\n\n\n')
        display.display_text('Press any key to continue')
        readchar.readkey()

        display.display_text('\n')

        return True

    @classmethod
    def handle_option_4(cls, type_=None, shell_id=None, confirm=False):
        """
        Operation: DELETE
        Delete all Reminders for note
        """
        reminder = select_from_reminders()
        if not reminder:
            display.display_text('No reminder found, start creating one -> ')
            return cls.handle_option_1()

        note = note_crud.get_shell_from_id(reminder['shell_id'])

        key = 'n'
        if not confirm:
            vision_hint = note['vision'] if len(note['vision']) <= 25 else ''.join([note['vision'][:23], '...'])
            display.display_text(f'\nAre you sure to delete reminders of "{vision_hint}" ?\n')
            display.display_text(f'\nPress y to continue deletion ')
            key = readchar.readkey()
            display.display_text(f'\n')

        if key == 'y' or key == 'Y' or confirm:
            crud.delete_reminder_by_shell_id(note['shell_id'])
            if note['tag_name'] == cls._default_tag_name:
                note_crud.delete_shell(note['shell_id'])
            display.display_text('Deleted successfully')
        else:
            display.display_text('Aborting ..')

        display.display_text('\n')

        return True

    @staticmethod
    def incorrect_option():
        display.display_text('Incorrect option selected, exiting !!!')
        display.display_text('\n')
        sleep(2)
        return False

reminder_handle = ReminderHandle()
