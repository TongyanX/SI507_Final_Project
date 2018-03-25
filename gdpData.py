# -*- coding: utf-8 -*-
"""Request and Store of GDP State Data"""

import csv
from commonFunc import create_table, insert_data, check_table

# Data Source:
# https://www.bea.gov/iTable/iTable.cfm?reqid=70&step=1&isuri=1&acrdn=2#reqid=70&step=4&isuri=1&7003=200&7001=1200&7002=1&7090=70
f_name = 'raw_data/GDP_by_state.csv'


def get_gdp_data():
    """Get GDP Data by State from CSV File"""
    with open(f_name) as f:
        data_list = list(csv.reader(f))[4:57]

    column_name = data_list[0][1:]
    column_name = [column_name[0]] + ['Y' + str(year) for year in column_name[1:]]
    column_data = [data[1:] for data in data_list[1:]]
    return column_name, column_data


def gdp_state_table():
    """Initialize GDP State Table"""
    t_name = 'GDP_State'
    column_name, column_data = get_gdp_data()

    if not check_table(t_name):
        column_list = ['TEXT'] + ['INT'] * (len(column_name) - 1)

        table_dict = dict(name=t_name,
                          column=list(zip(column_name, column_list)),
                          key=column_name[0]
                          )
        create_table(table_dict)

    insert_data([tuple(row) for row in column_data], t_name)


def main():
    """Main Function to Initialize GDP State Table"""
    gdp_state_table()


if __name__ == '__main__':
    main()
