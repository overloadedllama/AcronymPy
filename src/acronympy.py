import os
import sys

from db_handler import DBHandler
from executor import Executor
from input_analyzer import InputAnalyzer
from input_lexer import InputLexer


def runapp():
    parser = InputLexer()
    parser.create_token_stream()

    analyzer = InputAnalyzer(parser)
    if analyzer.check_input() is None:
        return

    script_dir = os.path.dirname(sys.argv[0])
    config_file_path = script_dir + os.sep + 'config_file_path'

    with open(config_file_path, 'r') as f:
        path = f.readline()

    db_handler = DBHandler(config_file=path)
    db_handler.init_connection()

    executor = Executor(db_handler)
    executor.execute_query(analyzer.dict_query, analyzer.params_requested)

    db_handler.close()
