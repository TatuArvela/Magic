import getopt
import os
import sys
import yaml
import locale
import time
from datetime import datetime


starttime = time.time()
version = "3.0.0"
spellbook = {}

class colors:
    BLACK = "\u001b[30m"
    RED = "\u001b[31m"
    GREEN = "\u001b[32m"
    YELLOW = "\u001b[33m"
    BLUE = "\u001b[34m"
    MAGENTA = "\u001b[35m"
    CYAN = "\u001b[36m"
    WHITE = "\u001b[37m"
    RESET = "\u001b[0m"

def perform_magic(args):
    spellcast = []
    if not args:
        show_information()
    else:
        for index, arg in enumerate(args):
            if arg.endswith(','):
                spellcast.append(arg[:-1])
                cast_spell(spellcast)
                spellcast = []
            elif index == len(args) - 1:
                spellcast.append(arg)
                cast_spell(spellcast)
            else:
                spellcast.append(arg)
        print(f'''{colors.GREEN}✔️{colors.RESET}  All spells cast successfully
{colors.GREEN}🕒{colors.RESET}  {datetime.now().strftime('%H:%M:%S')} | {colors.GREEN}⏱{colors.RESET}  {round((time.time() - starttime), 2)}s''')


def open_spellbook():
    try:
        spellbook = yaml.safe_load(open(os.path.expanduser(
            '~') + '/.config/magic/spellbook.yml', 'r'))
        return spellbook
    except yaml.YAMLError as error:
        print(f'{colors.RED}🔥  Failed to open spellbook file:{colors.RESET}')
        print(error)
        sys.exit()


def examine_spellbook():
    try:
        if not spellbook:
            raise ValueError(
                'Your spellbook is empty. Check the documentation for correct formatting.')
        elif isinstance(spellbook, list):
            magic_word_list = []
            for spell in spellbook:
                if not isinstance(spell, dict):
                    raise ValueError(
                        'Unexpected type of spell. Check the documentation for correct formatting.')
                elif not (
                    'message' in spell and
                    'magic_words' in spell and
                    'conjurations' in spell
                ):
                    raise ValueError(
                        'Unexpected contents in spellbook. Check the documentation for correct formatting.')
                magic_word_list = magic_word_list + spell['magic_words']
            if len(magic_word_list) != len(set(magic_word_list)):
                duplicates = set(
                    [x for x in magic_word_list if magic_word_list.count(x) > 1])
                raise ValueError(
                    'Duplicate magic words {0}'.format(duplicates)
                )
        else:
            raise ValueError(
                'Unexpected type of spellbook. Check the documentation for correct formatting.')

    except Exception as error:
        print(f'{colors.RED}🔥  Found an error in your spellbook:{colors.RESET}', error)
        sys.exit()


def find_spell(magic_word):
    for spell in spellbook:
        if magic_word in spell['magic_words']:
            return spell
    print(f'{colors.RED}🔥  No spell in spellbook with magic word \'{magic_word}\'{colors.RESET}')
    sys.exit()


def cast_spell(spellcast):
    spell = find_spell(spellcast[0])

    if ('variables_expected' in spell):
        if (len(spellcast) - 1) < spell['variables_expected']:
            print(
                f'{colors.RED}🔥  Not enough variables passed in spell {spellcast}{colors.RESET}')
            sys.exit()

    message = spell['message']
    for index, _ in enumerate(spellcast):
        if (index > 0):
            message = message.replace(
                '$' + str(index), spellcast[index])
    print(f'{colors.BLUE}✨{colors.RESET}  {message}')

    for raw_conjuration in spell['conjurations']:
        conjuration = raw_conjuration
        for index, _ in enumerate(spellcast):
            if (index > 0):
                conjuration = conjuration.replace(
                    '$' + str(index), spellcast[index])
        return_value = os.system(conjuration)
        if (return_value > 1):
            print(f'{colors.RED}🔥  Casting \'{spellcast[0]}\' failed{colors.RESET}')
            sys.exit()


def main(args):
    global spellbook
    spellbook = open_spellbook()
    load_config()
    examine_spellbook()
    perform_magic(args)
