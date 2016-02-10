"""
	A class that converts our NWS json data into a friendlier format, and filters out the stuff we don't care about. If
	additional NWS data is required, or features related to that data, they would be added here.
"""

import logging

logger = logging.getLogger('get_forecast.forecast')

class Forecast(object):
	def __init__(self, json_data):
		"""
		We want the NWS json response passed into the constructor, which we'll parse into properties

		:param json_data: The json response from NWS
		:return: (None)
		"""
		self._json_data = json_data

	def __repr__(self):
		"""
		Define a format for our class so python can use it

		:return: (str) A formatted string representing our class
		"""
		return "{}(json_data={})".format(self.__class__, str(self._json_data))

	@property
	def temperature(self):
		try:
			return self._json_data['data']['temperature']
		except KeyError:
			logger.error("Hit KeyError with keys ['data']['temperature']")
			raise

	@property
	def description(self):
		try:
			return self._json_data['data']['text']
		except KeyError:
			logger.error("Hit KeyError with keys ['data']['text']")
			raise

	@property
	def short_description(self):
		try:
			return self._json_data['data']['weather']
		except KeyError:
			logger.error("Hit KeyError with keys ['data']['weather']")
			raise

	@property
	def location(self):
		try:
			return self._json_data['location']
		except KeyError:
			logger.error("Hit KeyError with keys ['location']")
			raise

	@property
	def time_span(self):
		try:
			return (self._json_data['time']['startValidTime'], self._json_data['time']['startPeriodName'])
		except KeyError:
			logger.error("Hit KeyError with key ['time'] or one if its children")
			raise

	def get_custom_forecast(self, periods):
		"""
		This method returns a list of dicts that have a value for each property on our class that corresponds to one
		another. In other words, the first temperature is in the same dict as the first description etc, because those
		values are related to one another by the time period.

		:param periods: (int) The number of time periods to retrieve. (ie Tonight, Tomorrow)
		:return: (list) A list of dicts
		"""
		custom_forecasts = []
		for i in range(periods):
			temp_d = {
				'description': self.description[i],
				'time_description': self.time_span[1][i],
				'short_description': self.short_description[i],
				'location': self.location['areaDescription'],
				'temperature': self.temperature[i]
			}

			custom_forecasts.append(temp_d)

		return custom_forecasts
