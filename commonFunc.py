# -*- coding: utf-8 -*-
"""Common Functions Including Cache and Database"""

import json
import sqlite3

db_name = 'database/National_University.db'
cache_dir = 'cache_files/'


def load_cache(f_name, data_type='dict'):
    """Load Cache File"""
    try:
        with open(cache_dir + f_name) as f:
            cache_data = json.loads(f.read())
        return cache_data
    except FileNotFoundError:
        if data_type == 'list':
            return []
        elif data_type == 'dict':
            return {}
        else:
            return None


def save_cache(cache_dict, f_name):
    """Save Cache File"""
    with open(cache_dir + f_name, 'w') as f:
        f.write(json.dumps(cache_dict, indent=4))


def create_table(table_dict):
    """Create Table to Store Data"""
    # Database Connection
    con = sqlite3.connect(db_name)
    cur = con.cursor()

    t_name = table_dict['name']

    statement = 'DROP TABLE IF EXISTS {}'.format(t_name)
    cur.execute(statement)

    col_list = table_dict['column']
    col_name = [col[0] for col in col_list]
    col_type = [col[1] for col in col_list]
    statement = 'CREATE TABLE IF NOT EXISTS {} ('.format(t_name)
    for i in range(len(col_list)):
        statement += '\'{}\' {}, '.format(col_name[i], col_type[i])

    if 'key' in table_dict:
        key = table_dict['key']
        statement += 'PRIMARY KEY(\'{}\'))'.format(key)
    else:
        statement = statement[:-2] + ')'

    cur.execute(statement)
    con.commit()
    cur.close()
    con.close()


def insert_data(data_list, t_name):
    """Insert Data Tuples to a Given Table"""
    # Database Connection
    con = sqlite3.connect(db_name)
    cur = con.cursor()

    statement = 'INSERT INTO {} VALUES ('.format(t_name)
    statement += '?, ' * len(data_list[0])
    statement = statement[:-2] + ')'

    for data in data_list:
        cur.execute(statement, data)

    con.commit()
    cur.close()
    con.close()


def check_table(t_name):
    """Check If a Table Exists"""
    # Database Connection
    con = sqlite3.connect(db_name)
    cur = con.cursor()

    statement = 'SELECT name FROM sqlite_master WHERE type = \'table\' AND name = \'{}\''.format(t_name)
    cur.execute(statement)

    if cur.fetchone() is not None:
        return True
    else:
        return False
