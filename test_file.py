# -*- coding: utf-8 -*-
"""Request and Store of State Abbreviation Data"""

import unittest


class TestDataRequest(unittest.TestCase):
    def test_get_national_university_data(self):
        from universityData import get_national_university_data
        univ_dict = get_national_university_data('/best-colleges/university-of-michigan-9092')

        self.assertEqual(univ_dict.get('name'), 'University of Michigan--Ann Arbor')
        self.assertEqual(univ_dict.get('ranking'), '28')
        self.assertEqual(univ_dict.get('state'), 'MI')
        self.assertEqual(univ_dict.get('city'), 'Ann Arbor')
        self.assertEqual(univ_dict.get('type'), 'Public')
        self.assertEqual(univ_dict.get('found_year'), '1817')
        self.assertEqual(univ_dict.get('endowment'), 9600)
        self.assertEqual(univ_dict.get('tuition_in_state'), 14826)
        self.assertEqual(univ_dict.get('tuition_out_state'), 47476)
        self.assertEqual(univ_dict.get('enrollment'), 44718)
        self.assertEqual(univ_dict.get('median_salary'), 58400)
        self.assertEqual(univ_dict.get('student_faculty'), 15)
        self.assertEqual(univ_dict.get('female'), 0.502)

    def test_get_national_university_page(self):
        from universityData import get_national_university_page
        univ_list = get_national_university_page(1)

        self.assertEqual(len(univ_list), 20)
        self.assertIsInstance(univ_list[0], dict)
        self.assertEqual(univ_list[0].get('name'), 'Princeton University')
        self.assertEqual(univ_list[1].get('ranking'), '2')

    def test_get_gdp_data(self):
        from gdpData import get_gdp_data
        column_name, column_data = get_gdp_data()

        self.assertEqual(len(column_name), 21)
        self.assertEqual(column_name[0], 'Area')
        self.assertEqual(column_name[1], 'Y1997')
        self.assertEqual(column_name[-1], 'Y2016')
        self.assertEqual(column_data[2][0], 'Alaska')
        self.assertEqual(column_data[2][2], '24030')
        self.assertEqual(column_data[5][1], '1081444')

    def test_get_state_abbr_data(self):
        from stateAbbrData import get_state_abbr_data
        state_dict = get_state_abbr_data()

        self.assertEqual(state_dict['MI'], 'Michigan')
        self.assertEqual(state_dict['CA'], 'California')


class TestNationalUniversity(unittest.TestCase):
    def setUp(self):
        """Create Testing Objects"""
        from universityData import get_national_university_data
        univ_dict = get_national_university_data('/best-colleges/university-of-michigan-9092')
        from classDef import NationalUniversity
        self.nu_obj1 = NationalUniversity(data_dict=univ_dict)
        self.nu_obj2 = NationalUniversity(name='University of California--Los Angeles', city='Los Angeles', state='CA')

    def test_attr_1(self):
        """Test Object 1's Variables' Values"""
        self.assertEqual(self.nu_obj1.name, 'University of Michigan--Ann Arbor')
        self.assertEqual(self.nu_obj1.ranking, '28')
        self.assertEqual(self.nu_obj1.state, 'MI')
        self.assertEqual(self.nu_obj1.city, 'Ann Arbor')
        self.assertEqual(self.nu_obj1.type, 'Public')
        self.assertEqual(self.nu_obj1.found_year, '1817')
        self.assertEqual(self.nu_obj1.endowment, 9600)
        self.assertEqual(self.nu_obj1.tuition_in_state, 14826)
        self.assertEqual(self.nu_obj1.tuition_out_state, 47476)
        self.assertEqual(self.nu_obj1.enrollment, 44718)
        self.assertEqual(self.nu_obj1.median_salary, 58400)
        self.assertEqual(self.nu_obj1.student_faculty, 15)
        self.assertEqual(self.nu_obj1.female, 0.502)
        self.assertEqual(self.nu_obj1.lat, 42.2850942)
        self.assertEqual(self.nu_obj1.lng, -83.73855669999999)

    def test_attr_2(self):
        """Test Object 1's Variables' Values"""
        self.assertEqual(self.nu_obj2.name, 'University of California--Los Angeles')
        self.assertEqual(self.nu_obj2.state, 'CA')
        self.assertEqual(self.nu_obj2.city, 'Los Angeles')
        self.assertEqual(self.nu_obj2.lat, 34.054276)
        self.assertEqual(self.nu_obj2.lng, -118.255787)


# class TestStateGDP(unittest.TestCase):
#     def setUp(self):
#         """Create Testing Objects"""
#         from classDef import StateGDP
#         self.gdp_obj1 = StateGDP(data_dict=dict(Area='Test', Y2018=1000000))
#
#         from gdpData import get_gdp_data
#         column_name, column_data = get_gdp_data()
#         self.data_dict2 = dict(zip(column_name, column_data[23]))
#         self.gdp_obj2 = StateGDP(data_dict=self.data_dict2)
#
#     def test_attr(self):
#         self.assertTrue(hasattr(self.gdp_obj1, 'area'))
#         self.assertTrue(hasattr(self.gdp_obj1, 'y2018'))
#         self.assertEqual(self.gdp_obj1.area, 'Test')
#         self.assertEqual(self.gdp_obj1.y2018, 1000000)
#
#         self.assertTrue(hasattr(self.gdp_obj2, 'area'))
#         self.assertEqual(self.gdp_obj2.area, self.data_dict2['Area'])
#         for year in range(1997, 2017):
#             self.assertTrue(hasattr(self.gdp_obj2, 'y' + str(year)))
#             self.assertEqual(eval('self.gdp_obj2.y' + str(year)), self.data_dict2['Y' + str(year)])
#
#     def tearDown(self):
#         pass


class TestDatabase(unittest.TestCase):
    pass


if __name__ == '__main__':
    unittest.main()
