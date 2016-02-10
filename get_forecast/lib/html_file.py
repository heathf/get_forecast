"""
	The purpose of this class is to write the forecast results to an HTML file. It will default to a file on the current
	user's Desktop, that is named with the pattern: HTML_OUT-<datestring>.html

	NOTE: It uses a 3rd party module called HTML that should be in the lib/third_party_modules directory. I could have
	formatted the HTML myself, but this module has some nice features, and makes the class easily scalable.
"""

import datetime
import logging
import os
from config import *
from third_party_modules import HTML

logger = logging.getLogger('get_forecast.html_file')

class HtmlFile(object):
	_default_folder = os.path.join(os.environ['HOME'], 'Desktop')
	_default_name = "{}{}{}".format('HTML_OUT-', datetime.datetime.now().strftime("%m%d%Y%H%M%S"), ".html")

	def __init__(self, response):
		"""
		We need the response from the NWS api call as the constructor for the class

		:param response: (list) The NWS response
		:return: (None)
		"""
		self._response = response

	def __repr__(self):
		"""
		Define a format for our class so python can use it

		:return: (str) A formatted string representing our class
		"""
		return "{}(response={})".format(self.__class__, self._response)

	def write_html_file(self, path=os.path.join(_default_folder, _default_name)):
		"""
		This method will write the NWS data to an HTML file.

		:param path: (str) The path that should be used for the HTML file
		:return: (str) The path that was used for the HTML file
		"""
		logger.debug("In write_html_file and the path is set to {}".format(path))
		table_data = [[x['time_description'], x['temperature'], x['description']] for x in self._response]
		header_row = ["Timeframe", "Temperature", "Weather Description"]

		html = HTML.Table(table_data, header_row=header_row)

		try:
			html = "<center>\n<br />\n<h1>{} Weather Forecast</h1>\n{}\n</center>".format(
				self._response[0]['location'],
				str(html)
			)
		except KeyError:
			logger.error(location_key_err)
			raise Exception(location_key_err)

		with open(path, "w") as f:
			logger.info("Writing the following content to {}: {}".format(path, html))
			f.write(html)

		return path




