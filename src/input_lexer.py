import sys


class InputError(Exception):
    def __init__(self, msg=''):
        super().__init__(msg)

# Why use tools like typer when you can code your own lexer-parser inefficient system?


class InputLexer:
    token_names = [
        'COMMAND',
        'PARAM',
        'ID',
        'START_STAR',
        'END_STARS'
    ]

    commands = [
        'show',
        'add',
        'del',
        'modify',
    ]

    params = {
        'show': ['--scope', '-s', '-t', '--time'],
        'del': ['--scope', '-s'],
        'add': ['--scope', '-s', '-t', '--time'],
        'modify': ['--scope', 's']
    }

    def __init__(self):
        self.__input = sys.argv[1:]
        self.__tokens = []

    def create_token_stream(self):
        for string in self.__input:
            if self._is_command(string):
                self.__tokens.append(('COMMAND', string))

            elif self._is_start_acronym(string):
                self.__tokens.append(('START_STAR', '*'))
                self.__tokens.append(('ID', string.lstrip('*')))

            elif self._is_end_acronym(string):
                self.__tokens.append(('END_STARS', '**'))
                self.__tokens.append(('ID', string.rstrip('**')))

            elif self._is_params(string):
                self.__tokens.append(('PARAM', string))

            else:
                if self._acceptable_id(string):
                    self.__tokens.append(('ID', string))
                else:
                    raise InputError('Invalid input: ' + str(string))

    def _is_command(self, string):
        return string in self.commands

    @staticmethod
    def _is_params(string):
        return string.startswith('-') or string.startswith('--')

    @staticmethod
    def _is_start_acronym(string):
        return string.startswith('*')

    @staticmethod
    def _is_end_acronym(string):
        return string.endswith('**')

    @staticmethod
    def _acceptable_id(string):
        if not string[0].isalpha():
            return False

        for c in string:
            if not c.isalnum() and not c == '_':
                return False
        return True

    def token(self):
        return self.__tokens.pop(0) if self.__tokens else None
