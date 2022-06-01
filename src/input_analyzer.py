from datetime import datetime
from input_lexer import InputError


class InputAnalyzer:
    def __init__(self, parser):
        self.parser = parser
        self.dict_query = {
            'ACRONYM': 'default',
            'FULL_NAME': 'default',
            'SCOPE': 'default',
            'TIME': None
        }

        self.params_requested = {
            'ACRONYM': False,
            'FULL_NAME': False,
            'SCOPE': False,
            'TIME': False
        }

    def check_input(self):
        pull_token = True
        awaiting_params = False
        awaiting_star = True

        v = self.parser.token()
        if v is None:
            from setup import version
            print('AcronymPy version ' + str(version))
            return

        if v[0] != 'COMMAND':
            raise InputError('Write command first')
        self.dict_query['COMMAND'] = v[1]

        if self.dict_query['COMMAND'] == 'add':
            v = self.parser.token()
            if v[0] != 'START_STAR':
                raise InputError('Missing acronym')
            v = self.parser.token()
            if v[0] != 'ID':
                raise InputError('form is: <ACRONYM FULL_NAME>')
            self.dict_query['ACRONYM'] = v[1]

            v = self.parser.token()
            if v[0] != 'END_STARS':
                raise InputError('missing full name')
            v = self.parser.token()
            if v[0] != 'ID':
                raise InputError('form is: *ACRONYM FULL_NAME**')
            self.dict_query['FULL_NAME'] = v[1]

            awaiting_star = False
            awaiting_params = True

        while True:
            if pull_token:
                v = self.parser.token()
            else:
                pull_token = True

            if v is None:
                break

            if v[0] == 'COMMAND':
                raise InputError('Write only one command')

            if awaiting_star:
                if v[0] == 'START_STAR':
                    acronym = self.parser.token()
                    if acronym[0] == 'ID':
                        self.dict_query['ACRONYM'] = acronym[1]
                        self.params_requested['ACRONYM'] = True
                    else:
                        raise InputError('Expecting acronym, received ' + str(acronym[1]))

                elif v[0] == 'END_STARS':
                    full_name = self.parser.token()
                    if full_name[0] == 'ID':
                        self.dict_query['FULL_NAME'] = full_name[1]
                        self.params_requested['FULL_NAME'] = True
                    else:
                        raise InputError('Expecting full name, received ' + str(full_name[1]))

                else:
                    awaiting_star = False
                    awaiting_params = True

            if awaiting_params:
                if v[0] == 'PARAM':
                    if v[1] not in self.parser.params[self.dict_query['COMMAND']]:
                        raise InputError('parameter not acceptable for command')

                    if v[1] == '-s' or v[1] == '--scope':
                        if self.params_requested['SCOPE']:
                            raise InputError('symbol for scope already used')

                        if self.dict_query['COMMAND'] == 'show':
                            scope_name = self.parser.token()
                            if scope_name is None:
                                self.dict_query['SCOPE'] = '%'
                            elif scope_name[0] == 'ID':
                                self.dict_query['SCOPE'] = scope_name[1]
                            else:
                                pull_token = False
                                v = scope_name
                                self.dict_query['SCOPE'] = '%'

                        else:
                            param_name = self.parser.token()
                            if param_name[0] != 'ID':
                                raise InputError('expected name after parameter symbol')
                            self.dict_query['SCOPE'] = param_name[1]

                        self.params_requested['SCOPE'] = True

                    elif v[1] == '-t' or '--time':
                        self.dict_query['TIME'] = datetime.now()
                        self.params_requested['TIME'] = True

        self.dict_query = self.dict_query

        return True
