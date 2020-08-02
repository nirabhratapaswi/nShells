from datetime import datetime
import uuid
from note import crud
from note.display import DisplayModule as display
import readchar
from PyInquirer import prompt
from note.helpers import clear_screen
from time import sleep

def select_from_shells(shells=None):
    """ Select prompt for shells """
    shells = shells if shells else crud.list_shells()
    shells_ = {
        element['shell_id']: element
        for element in shells
    }

    options = {
        value['vision']: key
        for key, value in shells_.items()
    }
    questions = [
        {
            'type': 'list',
            'name': 'choice',
            'message': 'Choose note to expand',
            'choices': [key for key, value in options.items()]
        },
    ]
    answers = prompt(questions)

    id_ = options[answers['choice']]

    note = crud.get_shell_from_id(id_)

    clear_screen()

    return note

def select_from_tags():
    """ Select prompt for tags """
    tags = crud.list_tags()

    options = ['Enter manually'] + [tag['tag_name'] for tag in tags]
    questions = [
        {
            'type': 'list',
            'name': 'choice',
            'message': 'Select tag',
            'choices': options
        },
    ]
    answers = prompt(questions)

    tag = answers['choice']

    if tag == 'Enter manually':
        tag = str(input())

    clear_screen()

    return tag

class Handle(object):
    """
    Handle Module
    """
    _default_tag_name = 'default'

    @classmethod
    def switch(cls, option, *args):
        return getattr(cls, 'handle_option_' + str(option), cls.incorrect_option)(*args)

    @classmethod
    def handle_option_1(cls, title=None, description=None, tag_name=None):
        """
        OPERATION: CREATE
        Take a Note
        """
        if not title and not description and not tag_name:
            display.display_text('* - optional\n')
        if not title:
            display.display_text('Title: ')
            title = str(input())
        else:
            title = str(title)
        if not description:
            display.display_text('Add some description: ')
            description = description or str(input())
        else:
            description = str(description)
        if not tag_name:
            tags = crud.list_tags()
            choices =  ['Create New'] + [t['tag_name'] for t in tags]
            questions = [
                {
                    'type': 'list',
                    'name': 'choice',
                    'message': 'Choose a tag',
                    'choices': choices
                },
            ]
            answers = prompt(questions)

            type_ = answers['choice']

            if type_ == 'Create New':
                display.display_text('*(leave blank for default) Add a tag: ')
                tag_name = tag_name or str(input())
            else:
                tag_name = type_
        else:
            tag_name = str(tag_name)

        if tag_name == '' or tag_name == None:
            tag_name = cls._default_tag_name

        time = datetime.now()
        shell_id = str(uuid.uuid4()).replace('-', '')
        shell_data = (shell_id, title, description, tag_name, time)

        crud.create_shell(shell_data)
        crud.create_shell_search((title, description, shell_id))

        display.display_text('Note saved, rest assured :)')
        display.display_text('\n')

        return True

    @staticmethod
    def handle_option_2():
        """
        OPERATION: READ
        View all Notes
        """
        shells = crud.list_shells_compact()
        display.display_notes(shells)

        display.display_text('\n')

        return True

    @staticmethod
    def handle_option_3():
        """
        OPERATION: READ
        View all Notes with id
        """
        shells = crud.list_shells()
        display.display_notes(shells, include_id=True)

        display.display_text('\n')

        return True

    @staticmethod
    def handle_option_4(type_=None, id_=None, text=None):
        """
        TODO(nirabhra): Add option to read by id
        OPERATION: READ
        View Note
        """
        if not type_:
            options = {
                'Search': '1',
                'Read by id': '2',
                'List all': '3',
                'Filter by tag': '4',
            }
            questions = [
                {
                    'type': 'list',
                    'name': 'choice',
                    'message': 'Please select an option: ',
                    'choices': [key for key, value in options.items()]
                },
            ]
            answers = prompt(questions)

            type_ = options[answers['choice']]
        else:
            type_ = str(type_)

        if str(type_) == '1':
            if not text:
                display.display_text('\nType to search: ')
                text = str(input())
                clear_screen()
            else:
                text = str(text)

            shells = crud.search_shell(text)

            note = select_from_shells(shells)
        elif str(type_) == '2':
            if not id_:
                display.display_text('\nEnter id of the note to view: ')
                id_ = str(input())
                clear_screen()
            else:
                id_ = str(id_)

            note = crud.get_shell_from_id(id_)
        elif str(type_) == '3':
            shells = crud.list_shells()

            note = select_from_shells(shells)
        elif str(type_) == '4':
            tag = select_from_tags()
            shells = crud.get_shells_from_tag(tag)
            note = select_from_shells(shells)

        display.display_text(f'Vision  :   {note.get("vision")}\n')
        display.display_text(f'Thought :   {note.get("thought")}\n\n')
        display.display_text(f'Tag : {note.get("tag_name")}\n')
        display.display_text(f'Created on {note.get("created").split(".")[0]} ; ')
        display.display_text(f'id - {note.get("shell_id")}')

        display.display_text('\n\n\n')
        display.display_text('Press any key to continue')
        readchar.readkey()

        display.display_text('\n')

        return True

    @staticmethod
    def handle_option_5(type_=None, index=None, shell_id=None, confirm=False):
        """
        OPERATION: DELETE
        Delete a Note
        """

        if not type_:
            options = {
                'Select from list': '3',
                'Search': '2',
                'Delete by id': '1',
            }
            questions = [
                {
                    'type': 'list',
                    'name': 'choice',
                    'message': 'Select an option',
                    'choices': [key for key, value in options.items()]
                },
            ]
            answers = prompt(questions)

            type_ = options[answers['choice']]
        else:
            type_ = str(type_)

        if str(type_) == '1':
            if not shell_id:
                display.display_text('Enter id of the note to delete: ')
                shell_id = str(input())
            else:
                shell_id = str(shell_id)

            note = crud.get_shell_from_id(shell_id)
        elif str(type_) == '2':
            display.display_text('\nType to search: ')
            text = str(input())
            clear_screen()

            shells = crud.search_shell(text)

            note = select_from_shells(shells)
        elif str(type_) == '3':
            note = select_from_shells()

        key = 'n'
        if not confirm:
            vision_hint = note['vision'] if len(note['vision']) <= 25 else ''.join([note['vision'][:23], '...'])
            display.display_text(f'\nAre you sure to delete {vision_hint} ?\n')
            display.display_text(f'\nPress y to continue deletion ')
            key = readchar.readkey()
            display.display_text(f'\n')

        if key == 'y' or key == 'Y' or confirm:
            crud.delete_shell(note['shell_id'])
            display.display_text('Deleted successfully')
        else:
            display.display_text('Aborting ..')

        display.display_text('\n')

        return True

    @staticmethod
    def handle_option_6():
        """
        OPERATION: READ
        View all tags
        """
        tags = crud.list_tags()
        display.display_tags(tags)

        display.display_text('\n')

        return True

    @staticmethod
    def handle_option_7(tag_name=None):
        """
        OPERATION: READ
        List all Notes for a Tag
        """
        tag_name = tag_name or select_from_tags()

        shells = crud.get_shells_from_tag(tag_name)
        display.display_notes(shells)

        display.display_text('\n')

        return True

    @classmethod
    def handle_option_8(cls, type_=None, index=None, tag_id=None, name=None, confirm=False):
        """
        OPERATION: DELETE
        Delete a Tag (select from list)
        """
        tag_name = select_from_tags()

        key = 'n'
        skip_note_delete = False
        tag_hint = tag_name if len(tag_name) <= 25 else ''.join([tag_name[:23], '...'])

        if not confirm:
            display.display_text(f'Are you sure to delete tag "{tag_hint}" ?\n')
            display.display_text(f'Press y to continue deletion ')
            key = readchar.readkey()
            display.display_text(f'\n')

        if (key == 'y' or key == 'Y' or confirm) and not skip_note_delete:
            crud.delete_shell_by_tag_name(tag_name)
            display.display_text('\nNotes deleted successfully')
        elif not skip_note_delete:
            display.display_text('\nAborting ..\n')

        display.display_text('\n')

        return True

    @staticmethod
    def _handle_option_9():
        """
        Not accesible via console !
        OPERATION: READ
        View all shell_tags
        """
        shell_tags = crud.list_shell_tags()
        display.display_shell_tags(shell_tags)

        display.display_text('\n')

        return True

    @classmethod
    def handle_option_q(cls):
        """
        Done for now? - Exit :)
        """
        farewell_text = 'Thankyou for using notes!\nBye 🖐'

        total_animation_time = 1.5
        animation_speed = total_animation_time / len(farewell_text)
        for i in range(0, len(farewell_text)):
            display.display_text(farewell_text[i])
            sleep(animation_speed)

        sleep(0.75)

        return False

    @staticmethod
    def incorrect_option():
        display.display_text('Incorrect option selected, exiting !!!')

        display.display_text('\n')

        return False

handle = Handle()
