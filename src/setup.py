#!/usr/bin/env python3

import os
from configparser import ConfigParser
from db_handler import DBHandler

version = 1.0

packages = ['pypika', 'mysql-connector-python', 'mysql-connector']


def install_packages():
    for p in packages:
        print(p)
        os.system('pip install ' + p)


def create_config_file(file_name):
    config_file = file_name
    parser = ConfigParser()

    parser.add_section('mysql')
    user = input('Enter your username: ')
    passwd = input('Enter your password: ')
    host = input('Enter the host name: ')

    parser['mysql'] = {
        'user': user,
        'password': passwd,
        'database': 'AcronymDB',
        'host': host,
        'auth_plugin': 'mysql_native_password'
    }

    with open(config_file, 'w') as fw:
        parser.write(fw)


if __name__ == '__main__':
    install_packages()
    config_file_path = os.path.abspath(os.path.curdir + os.sep + '..') + os.sep + 'config.ini'

    if not input(f'Write database info in "{config_file_path}"? (y/n) ').lower().startswith('y'):
        config_file_path = input('Enter config file name: ')

    with open('config_file_path', 'x') as f:
        f.write(config_file_path)

    create_config_file(config_file_path)
    DBHandler.create_db(config_file_path)

    print('Setup finished. Exiting...')
