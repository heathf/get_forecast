"""
	A simple test class to make sure our Forecast class is returning non null values. Most of the tests just check for
	empty strings or the length of the returned value, although we also ensure the json is property formatted from our
	request.

	Can be invoked from bash terminal with syntax similar to this example:

	cd /path/to/get_forecast
	python -m unittest discover "$(pwd)/tests" -p tests*.py
"""

import json
import unittest
from lib import forecast
from lib.third_party_modules import requests
from lib.config import *

class TestForecast(unittest.TestCase):
	def setUp(self):
		city = "lander"

		lat = cities_data[city]['lat']
		lon = cities_data[city]['lon']

		self.test_url = "http://forecast.weather.gov/MapClick.php?lat={}&lon={}&FcstType=json".format(lat, lon)

		self.periods = 5
		self.req = requests.get(self.test_url)
		self.f = forecast.Forecast(self.req.json())
		self.custom_forecast = self.f.get_custom_forecast(self.periods)

	def test_temperature(self):
		""" Just making sure we don't have an empty string """
		assert self.custom_forecast[0] != None

	def test_description(self):
		""" Just making sure we don't have an empty string """
		assert self.f.description != ''

	def test_short_description(self):
		""" Just making sure we don't have an empty string """
		assert self.f.short_description != ''

	def test_timespan(self):
		""" Making sure our time_span tuple has values as well """
		assert self.f.time_span[0][0] != '' and self.f.time_span[1][0] != ''

	def test_custom_forecast(self):
		""" Make sure our forecast has the same len as our periods """
		assert len(self.custom_forecast) == self.periods

	def test_json_format(self):
		""" Test our json to make sure it's valid """
		try:
			json.loads(self.req.text)
			valid_json = True
		except ValueError, e:
			valid_json = False

		assert valid_json == True

	def tearDown(self):
		pass
