"""
	Houses a simple WeatherRequest class that contains info related to our NWS requests. It works in conjunction with
	the forecast.Forecast class, although they are not formally related. At least in theory, we may want to get multiple
	forecasts from the same WeatherRequest.

	NOTE: I could have used the urllib2 module for making the requests, but the requests module has an elegant interface
	that I prefer, and it seemed popular enough to include in the project. If the scope of the project were to grow, the
	advantage of using it, would potentially increase.
 """

import forecast
import logging
from config import *
import requests

logger = logging.getLogger('get_forecast.weather')

class WeatherRequest(object):
	def __init__(self, city):
		"""
		We need a city name as a constructor. We convert to lowercase to match our json

		:param city: (str) The name of a city to obtain (which needs to be present in cities.json)
		:return: (None)
		"""
		self.city = city.lower()
		self.missing_city = Exception("Unable to locate the following city in cities.json: {}".format(city))
		self.max_periods_exceeded = Exception("Enter a lower number for periods. Max value = 13")

	def __repr__(self):
		"""
		Define a format for our class so python can use it

		:return: (str) A formatted string representing our class
		"""
		return "{}(city={})".format(self.__class__, self.city)

	@property
	def url(self):
		"""
		Returns a url suitable for calling the NWS api for the weather data. Note that it pulls the ``city`` attrib's
		info from cities.json which needs to be present in the resources dir

		:return: (str) A string containing the url with the proper lat and lon for our city
		"""
		try:
			lat = cities_data[self.city]['lat']
			lon = cities_data[self.city]['lon']
		except KeyError:
			logger.error(self.missing_city.message)
			raise self.missing_city

		formatted_url = "http://forecast.weather.gov/MapClick.php?lat={}&lon={}&FcstType=json".format(lat, lon)
		logger.debug("weather.WeatherRequest.url = {}".format(formatted_url))
		return formatted_url

	def get_weather_request(self, periods=4):
		"""
		Sends a request for the weather data and returns it using our Forecast class. The ``periods`` param must be
		lower than 14, because we only retrieve 13 items from NWS.

		:param periods: (int) The number of time periods to retrieve. Must be lower than 14
		:return: (forecast.Forecast) The Forecast object containing our parsed weather data
		"""
		if periods > 13:
			logger.error(self.max_periods_exceeded)
			raise self.max_periods_exceeded

		req = requests.get(self.url)
		f = forecast.Forecast(req.json())
		logger.debug("Calling get_custom_forecast for {} periods".format(periods))
		custom_forecast = f.get_custom_forecast(periods)

		return custom_forecast