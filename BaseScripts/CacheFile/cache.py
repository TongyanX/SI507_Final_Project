# -*- coding: utf-8 -*-
"""Common Functions Including Cache and Database"""

import json
from SI507_Final_Project.settings import BASE_DIR

cache_dir = BASE_DIR + '/BaseScripts/CacheFile/'


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
