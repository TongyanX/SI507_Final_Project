# -*- coding: utf-8 -*-
"""Request and Store of State Abbreviation Data"""

import json
from Database.dbOperation import Database
from SI507_Final_Project.settings import BASE_DIR

# Data Source:
# https://gist.githubusercontent.com/mshafrir/2646763/raw/8b0dbb93521f5d6889502305335104218454c2bf/states_hash.json
f_dir = BASE_DIR + '/BaseScripts/RawData/'
f_name = 'state_abbr.json'


def get_state_abbr_data():
    """Get State Abbreviations from JSON File"""
    with open(f_dir + f_name) as f:
        data_dict = json.loads(f.read())

    return data_dict


def state_abbr_table():
    """Initialize State Abbreviation Table"""
    t_name = 'State_Abbr'
    db_operator = Database()
    data_dict = get_state_abbr_data()
    data_dict['DC'] = 'District of Columbia'

    table_dict = dict(name=t_name,
                      column=[('StateAbbr', 'TEXT'),
                              ('StateName', 'TEXT')])
    db_operator.create_table(table_dict)

    db_operator.insert_data(list(data_dict.items()), t_name)


def main():
    """Main Function to Initialize State Abbreviation Table"""
    state_abbr_table()


if __name__ == '__main__':
    main()
