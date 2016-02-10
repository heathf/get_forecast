"""
	The purpose of this module is to house global type variables/functions, so we don't need to mess the global scope
	with variables.
"""

import json
import os

resources_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "resources")
data_path = os.path.join(resources_path, "data.json")
cities_path = os.path.join(resources_path, "cities.json")

#We use this in a couple different places, so we'll store it here
location_key_err = "Unable to locate ['location'] key in response"

with open(cities_path) as json_file:
	cities_data = json.load(json_file)