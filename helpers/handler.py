from datetime import datetime
import uuid
import setup
from helpers import crud
from helpers.display import DisplayModule as display
import readchar

class Handle(object):
    """
    Handle Module
    """

    @classmethod
    def switch(cls, option, *args):
        return getattr(cls, 'handle_option_' + str(option), cls.incorrect_option)(*args)

    @staticmethod
    def handle_option_1():
        """
        Take a Note
        """
        title_text = 'Enter Title:'
        display.display_text(f'\n{"~"*len(title_text)}\n{title_text} ')
        title = str(input())
        display.display_text('Enter Description: ')
        description = str(input())
        display.display_text('Enter Tag(blank if no tag): ')
        tag_name = str(input()) # TODO: have functionality for blank tag

        time = str(datetime.now())
        shell_id = str(uuid.uuid4()).replace('-', '')
        tag_id = str(uuid.uuid4()).replace('-', '')
        shell_data = (shell_id, title, description, tag_name, time)
        tag_data = (tag_id, tag_name)

        crud.create_shell(shell_data)
        tag = crud.get_tag_by_name(tag_name)
        print('tag: ', tag)
        if tag:
            tag_id = tag['tag_id']
        else:
            crud.create_tag(tag_data)
        print('tag_id: ', tag_id)
        crud.create_shell_tag((shell_id, tag_id))

        display.display_text('Note saved, rest assured :)\n')
        return True

    @staticmethod
    def handle_option_2():
        """
        View all Notes
        """
        shells = crud.list_shells_compact()
        display.display_notes(shells)
        return True

    @staticmethod
    def handle_option_3():
        """
        View all Notes with id
        """
        shells = crud.list_shells()
        display.display_notes(shells, include_id=True)
        return True

    @staticmethod
    def handle_option_4():
        """
        View Note <index>(select from list)
        """
        display.display_text('\nEnter index of the note to view: ')
        index = int(input())

        note = crud.get_shell_by_offset(index - 1)

        display.display_text(f'\n{"~"*50}\n')
        display.display_text(f'Vision:    {note["vision"]}\n\n')
        display.display_text(f'Thought:   {note["thought"]}\n\n')
        display.display_text(f'Timestamp: {note["vision"]}')

        display.display_text('\n\n\n')
        display.display_text('Press any key to continue')
        readchar.readkey()
        display.display_text('\n')

        return True

    @staticmethod
    def handle_option_5():
        """
        Delete a Note
        """
        skip_delete = False

        display.display_text('\nDelete by index - press 1')
        display.display_text('\nDelete by id    - press 2 ')
        type_ = readchar.readkey()
        print('type: ', type_)

        if str(type_) == '1':
            display.display_text('\nEnter index of the note to delete: ')
            index = int(input())

            note = crud.get_shell_by_offset(index - 1)
            shell_id = note['shell_id']
        elif str(type_) == '2':
            display.display_text('\nEnter id of the note to delete: ')
            shell_id = str(input())
            note = crud.get_shell_from_id(shell_id)
        else:
            display.display_text('\nOnly 1 / 2 are valid delete choices .. aborting delete\n')
            skip_delete = True

        if shell_id and not skip_delete:
            print('shell id: ', shell_id)
            vision_hint = note['vision'] if len(note['vision']) <= 25 else ''.join([note['vision'][:23], '...'])
            display.display_text(f'\nAre you sure to delete {vision_hint} ?\n')
            display.display_text(f'\nPress y to continue deletion ')
            key = readchar.readkey()
            display.display_text(f'\n')
            if key == 'y' or key == 'Y':
                crud.delete_shell(shell_id)
                tag = crud.get_tag_by_name(note['tag_name'])
                x = crud.delete_shell_tag((shell_id, tag['tag_id']))
                print('\nx: ', x, '\n')
                display.display_text('\nDeleted successfully')
            else:
                display.display_text('\nAborting ..\n')
        elif not skip_delete:
            display.display_text('\nNote not found !\n')

        return True

    @staticmethod
    def handle_option_6():
        """
        View all tags
        """
        tags = crud.list_tags()
        display.display_tags(tags)
        return True

    @staticmethod
    def handle_option_7():
        """
        List all Notes for a Tag
        """
        display.display_text('\nEnter tag name to view: ')
        name = str(input())

        tag = crud.get_tag_by_name(name)

        shell_ids = crud.get_shell_ids_from_tag(tag['tag_id'])

        shells = crud.get_shell_from_ids(shell_ids)
        display.display_notes(shells)

        return True

    @staticmethod
    def handle_option_8():
        """
        Delete a Tag <index>(select from list
        """
        return True

    @staticmethod
    def handle_option_exit():
        """
        Done for now? - Exit :)
        """
        return False

    @staticmethod
    def incorrect_option():
        display.display_text('\nIncorrect option selected, exiting !!!\n')
        return False
