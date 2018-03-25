# -*- coding: utf-8 -*-
"""Definition of Important Classes"""

import json
import requests
from secret_file import google_places_key
from commonFunc import load_cache, save_cache

# US lat-long range for checking locations of sites
us_lat_range = [19.50139, 64.85694]
us_lon_range = [-161.75583, -68.01197]


class NationalUniversity(object):
    """National University Class"""

    def __init__(self, name=None, ranking=None, state=None, city=None, univ_type=None,
                 found_year=None, endowment=None, tuition_in_state=None, tuition_out_state=None,
                 enrollment=None, median_salary=None, student_faculty=None, female=None, data_dict=None):
        if data_dict is not None:
            self.name = data_dict.get('name')
            self.ranking = data_dict.get('ranking')
            self.state = data_dict.get('state')
            self.city = data_dict.get('city')
            self.type = data_dict.get('type')
            self.found_year = data_dict.get('found_year')
            self.endowment = data_dict.get('endowment')
            self.tuition_in_state = data_dict.get('tuition_in_state')
            self.tuition_out_state = data_dict.get('tuition_out_state')
            self.enrollment = data_dict.get('enrollment')
            self.median_salary = data_dict.get('median_salary')
            self.student_faculty = data_dict.get('student_faculty')
            self.female = data_dict.get('female')

        else:
            self.name = name
            self.ranking = ranking
            self.state = state
            self.city = city
            self.type = univ_type
            self.found_year = found_year
            self.endowment = endowment
            self.tuition_in_state = tuition_in_state
            self.tuition_out_state = tuition_out_state
            self.enrollment = enrollment
            self.median_salary = median_salary
            self.student_faculty = student_faculty
            self.female = female

        gps_location = self.get_gps_info()
        self.lat = gps_location['lat']
        self.lng = gps_location['lng']

    def __str__(self):
        return '{} is a {} national university located in {}, {}.'.format(self.name, self.type, self.city, self.state)

    def request_gps_info(self, nation=False, state=False, city=False):
        """Request GPS Data Through Google Place API"""
        # Required url and parameters for requesting data
        base_url = 'https://maps.googleapis.com/maps/api/place/textsearch/json'
        detail_list = [self.name]
        if city is True:
            detail_list.append(self.city)
        if state is True:
            detail_list.append(self.state)
        if nation is True:
            detail_list.append('US')
        params = {'key': google_places_key,
                  'query': ', '.join(detail_list),
                  'types': 'school'}

        # Request the location data
        resp = requests.get(base_url, params=params)
        result = json.loads(resp.text)

        # Return a dictionary containing latitude and longitude data in string form
        if result['status'] == 'OK':
            if len(result['results']) == 1:
                location = result['results'][0]['geometry']['location']

                # Remove the mis-match locations returned by API which is not located in US
                if (location['lat'] >= us_lat_range[0]) and (location['lat'] <= us_lat_range[1]) and (
                            location['lng'] >= us_lon_range[0]) and (location['lng'] <= us_lon_range[1]):
                    return location
                else:
                    location = {'lat': None, 'lng': None}

            else:
                if nation is False:
                    location = self.request_gps_info(nation=True)
                else:
                    if state is False:
                        location = self.request_gps_info(nation=True, state=True)
                    else:
                        if city is False:
                            location = self.request_gps_info(nation=True, state=True, city=True)
                        else:
                            for each_result in result['result']:
                                location = each_result['geometry']['location']
                                if (location['lat'] >= us_lat_range[0]) and (location['lat'] <= us_lat_range[1]) and (
                                        location['lng'] >= us_lon_range[0]) and (location['lng'] <= us_lon_range[1]):
                                    return location
                            location = {'lat': None, 'lng': None}

            return location

        # Leave the data empty if it is not found or mis-found
        elif result['status'] == 'ZERO_RESULTS':
            print('Failed to request data <GPS Location of {}> from Google Place API'.format(self.name))
            location = {'lat': None, 'lng': None}
            return location

        # Return a signal when exceed the request limit
        else:
            print('API request limit is exceeded.')
            return None

    def get_gps_info(self):
        """Get GPS Data From API Or Cache File"""
        file_name = 'national_university_gps.json'
        cache_file = load_cache(file_name)

        # Get data from cache file
        if self.name in cache_file:
            print('Get <GPS Location of {}> from Cache File...'.format(self.name))

        # Request data from web page
        else:
            print('Request <GPS Location of {}> through Google Place API...'.format(self.name))
            location = self.request_gps_info()
            if location is not None:
                cache_file[self.name] = self.request_gps_info()
                save_cache(cache_file, file_name)
            else:
                return {'lat': None, 'lng': None}

        return cache_file[self.name]

#
# class StateGDP(object):
#     """State GDP Class"""
#     def __init__(self, area=None, data_dict=None):
#         if data_dict is not None:
#             for year in data_dict:
#                 if year[0] == 'Y':
#                     setattr(self, year.lower(), data_dict[year])
#             self.area = data_dict.get('Area')
#             if self.area is None:
#                 self.area = area
#
#         else:
#             self.area = area
#