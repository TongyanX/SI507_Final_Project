# -*- coding: utf-8 -*-
"""Request and Store of National University Data"""

import requests
from bs4 import BeautifulSoup
from BaseScripts.classDef import NationalUniversity
from BaseScripts.CacheFile.cache import *
from Database.dbOperation import Database

agent = {'User-Agent': 'Chrome/59.0.3071.115'}


def get_national_university_data(univ_url):
    """Request National University Data through US News Website"""
    base_url = 'https://www.usnews.com'

    resp = requests.get(base_url + univ_url, headers=agent)
    soup = BeautifulSoup(resp.text, 'html.parser')

    map_chunk = soup.find('section', attrs={'class': 'hero-stats-widget-map'})
    address = map_chunk.find('p').find('strong').text.strip()
    info_list = soup.find_all('div', attrs={'class': 'block-looser'})[1].find_all('ul')
    stats_list = soup.find('section', attrs={'class': 'hero-stats-widget-stats'}).find('ul').find_all('strong')
    salary_chunk = soup.find_all('div', attrs={'class': 'block-looser'})[4].find('span', attrs={'class': 'text-strong'})

    life_resp = requests.get(base_url + univ_url + '/student-life', headers=agent)
    life_soup = BeautifulSoup(life_resp.text, 'html.parser')
    life_chunk = life_soup.find('div', attrs={'id': 'StudentBody'})
    gender_chunk = life_chunk.find('span', attrs={'data-test-id': 'v_percent'})

    academic_resp = requests.get(base_url + univ_url + '/academics', headers=agent)
    academic_soup = BeautifulSoup(academic_resp.text, 'html.parser')
    faculty_chunk = academic_soup.find('div', attrs={'data-field-id': 'vStudentFacultyRatio'})

    found_year = info_list[1].find('span', attrs={'class': 'heading-small'}).text
    if found_year == 'N/A':
        found_year = None
    else:
        found_year = int(found_year)

    endowment = info_list[5].find('span', attrs={'class': 'heading-small'}).text
    endowment = endowment.replace('$', '').replace(' +', '').strip()
    if endowment == 'N/A':
        endowment = None
    else:
        endowment_list = endowment.split()
        if len(endowment_list) == 1:
            endowment = float(endowment.replace(',', '')) / 1000
        elif endowment_list[1] == 'billion':
            endowment = float(endowment_list[0]) * 1000
        else:
            endowment = float(endowment_list[0])

    median_salary = salary_chunk.text.replace('*', '').strip() if salary_chunk is not None else None
    if median_salary is not None:
        median_salary = int(median_salary.replace('$', '').replace(',', ''))

    student_faculty = faculty_chunk.find('p').find('span', attrs={'class': 'text-strong'}).text.strip()
    if student_faculty == 'N/A':
        student_faculty = None
    else:
        student_faculty = int(student_faculty.split(':')[0])

    tuition_in_state = stats_list[0].text.split()[0]
    if tuition_in_state == 'N/A':
        tuition_in_state = None
    else:
        tuition_in_state = int(tuition_in_state.replace('$', '').replace(',', ''))

    female = gender_chunk.text if gender_chunk is not None else None
    if female is not None:
        female = float(female.replace('%', '')) / 100

    univ_dict = dict(name=soup.find('h1', attrs={'class': 'hero-heading'}).text.strip().replace('1', ''),
                     ranking=soup.find('strong').text.strip().split()[0].replace("#", "").replace('-', ' - '),
                     state=address.rsplit(', ', 1)[1],
                     city=address.rsplit(', ', 1)[0],
                     type=info_list[0].find('span', attrs={'class': 'heading-small'}).text.split(', ')[0],
                     found_year=found_year,
                     endowment=endowment,
                     median_salary=median_salary,
                     student_faculty=student_faculty,
                     female=female,
                     tuition_in_state=tuition_in_state)

    if univ_dict['type'] == 'Public':
        tuition_out_state = stats_list[1].text.split()[0]
        enrollment = stats_list[3].text
    else:
        tuition_out_state = stats_list[0].text.split()[0]
        enrollment = stats_list[2].text

    if tuition_out_state == 'N/A':
        tuition_out_state = None
    else:
        tuition_out_state = int(tuition_out_state.replace('$', '').replace(',', ''))

    if enrollment == 'N/A':
        enrollment = None
    else:
        enrollment = int(enrollment.replace(',', ''))

    univ_dict.update(dict(tuition_out_state=tuition_out_state,
                          enrollment=enrollment))

    return univ_dict


def get_national_university_page(page):
    """Request National University Page through US News Website"""
    base_url = 'https://www.usnews.com'
    page_url = '/best-colleges/rankings/national-universities?_mode=table&_page=' + str(page)

    resp = requests.get(base_url + page_url, headers=agent)
    soup = BeautifulSoup(resp.text, 'html.parser')

    table_chunk = soup.find('tbody', attrs={'data-js-id': 'items'})
    univ_list = table_chunk.find_all('tr', attrs={'data-view': 'colleges-search-results-table-row'})

    output_list = []
    for univ_chunk in univ_list:
        univ_url = univ_chunk.find('a')['href']
        output_list.append(get_national_university_data(univ_url))

    return output_list


def get_all_national_university():
    """Request All National University Info through US News Website"""
    f_name = 'national_university_info.json'

    data_list = load_cache(f_name, data_type='list')
    if len(data_list) == 0:
        print('Request National University Info through Website...')
        for page in range(1, 17):
            data_list += get_national_university_page(page)
        save_cache(data_list, f_name)
    else:
        print('Get National University Info from Cache File...')

    nu_obj_list = [NationalUniversity(data_dict=data_dict) for data_dict in data_list]
    return nu_obj_list


def national_university_table():
    """Initialize National University Table"""
    t_name = 'National_University'
    db_operator = Database()

    table_dict = dict(name=t_name,
                      column=[('ID', 'INT'),
                              ('Name', 'TEXT'),
                              ('Ranking', 'TEXT'),
                              ('State', 'TEXT'),
                              ('City', 'TEXT'),
                              ('Type', 'TEXT'),
                              ('FoundYear', 'TEXT'),
                              ('Endowment(M)', 'REAL'),
                              ('TuitionAndFeesInState', 'INT'),
                              ('TuitionAndFeesOutOfState', 'INT'),
                              ('Enrollment', 'INT'),
                              ('MedianStartingSalary', 'INT'),
                              ('StudentFacultyRatio', 'INT'),
                              ('FemalePercentage', 'REAL'),
                              ('Latitude', 'INT'),
                              ('Longitude', 'INT')],
                      key='ID')
    db_operator.create_table(table_dict)

    data_list = []
    for (i, nu_obj) in enumerate(get_all_national_university()):
        data_list.append((i + 1, nu_obj.name, nu_obj.ranking, nu_obj.state, nu_obj.city,
                          nu_obj.type, nu_obj.found_year, nu_obj.endowment, nu_obj.tuition_in_state,
                          nu_obj.tuition_out_state, nu_obj.enrollment, nu_obj.median_salary,
                          nu_obj.student_faculty, nu_obj.female, nu_obj.lat, nu_obj.lng))
    db_operator.insert_data(data_list, t_name)


def main():
    """Main Function to Initialize National University Table"""
    national_university_table()


if __name__ == '__main__':
    main()
