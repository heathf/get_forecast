"""
	This project will retrieve NWS weather information for the Lander area. The data can be used in several ways:

	-t or --text - Send the weather data as a text message to the specified phone number
	-f or --file - Sends the output to an HTML file on the user's Desktop
	default      - Prints the weather data to the console

	There is also the ability to specify which city to retrieve results for, however that city must exist in
	cities.json. This option can be used with this argument:

	-c --city

	NOTES:
		- It uses a Twilio developer account to send the SMS. This isn't ideal, and isn't something I would do in a
		normal situation where a script is being distributed, but it seemed suitable for this scenario.
"""

import argparse
import logging
import sys
from lib.config import *
from lib import sms
from lib import weather
from lib import html_file

def _convert_msg(msg, sms=False):
	"""
	We want the output to be formatted differently depending on whether or not we're printing to the console, or sending
	a text message. So this func just does that formatting for us

	:param msg: (dict) This should be a dict containing our weather data
	:param city: (str) The city that the forecast corresponds to
	:param sms: (bool) True if we're sending the msg via SMS, False otherwise
	:return: (str) The formatted message string
	"""
	try:
		msg_string = "{} Weather\n".format(msg[0]['location'])
	except KeyError:
		raise Exception(location_key_err)

	desc = 'short_description' if sms else 'description'

	for x in msg:
		msg_string += "{}:\n\t{} degrees\n\t{}\n".format(
			x['time_description'],
			x['temperature'],
			x[desc]
		)

	return msg_string

def set_logger():
	"""
	Sets up a logger to use within the utility for troubleshooting and trackability. This logger should be used in the
	other modules as well as main, but child loggers should be used in the other modules. It will log messages to the
	/logs/get_forecast.log file.

	:return: (logging.Logger) The Logger object to use to log messages
	"""
	logger = logging.getLogger('get_forecast')
	logger.setLevel(logging.DEBUG)

	log_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "logs", "get_forecast.log")
	file_handler = logging.FileHandler(log_path)
	file_handler.setLevel(logging.DEBUG)

	formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
	file_handler.setFormatter(formatter)

	logger.addHandler(file_handler)

	return logger

def main(city="lander", sms_to=None, out_file=False):
	"""
	This main function will output our NWS weather results to the console, a Text message or an HTML file. If
	``sms_to`` is not null, it will attempt to send the SMS to the specified number. If ``out_file`` is present
	it will write the results to an HTML file on the Desktop. If neither ``sms_to`` or ``out_file`` is present,
	the results will be written to the console.

	It should be noted that only ``sms_to`` OR ``out_file`` can be present but not both.

	:param sms_to: (str) This should be a phone number, but passed as a string
	:return: (None) The message will be sent appropriately but no return value
	"""
	logger = set_logger()
	logger.debug("**********************    Script Started    **********************")

	if sms_to and out_file:
		err_msg = "You can pass ``sms_to`` OR ``out_file``, but not both"
		logger.error(err_msg)
		raise Exception(err_msg)

	weather_request = weather.WeatherRequest(city)
	response = weather_request.get_weather_request()

	logger.debug("Received the following response from the NWS call: {}".format(response))

	if sms_to:
		logger.info("Sending SMS message to the following number: {}".format(sms_to))
		sms.send_sms(sms_to, _convert_msg(response, True))
	elif out_file:
		html = html_file.HtmlFile(response)
		logger.info("Writing NWS data to HTML file")
		output_file = html.write_html_file()
		print "The HTML file has been written to: {}".format(output_file)
	else:
		logger.info("Sending NWS data to console")
		print(_convert_msg(response))

if __name__ == "__main__":
	choices = cities_data.keys() + [c.capitalize() for c in cities_data.keys()]
	parser = argparse.ArgumentParser()

	parser.add_argument(
		'-t',
		'--text',
		dest='Text',
		help='Use this option to send the weather data as a text message to the specified phone number'
	)

	parser.add_argument(
		'-c',
		'--city',
		dest='City',
		choices=choices,
		help='Use this argument to specify the city to retrieve weather for. The city must exist in cities.json'
	)

	parser.add_argument(
		'-f',
		'--file',
		dest='File',
		action='store_true',
		help='Use this switch parameter to output the weather results to an HTML file on the Desktop'
	)

	args = parser.parse_args()
	city = args.City.lower() if args.City else "lander"

	"""
	We're checking args here and in main. A little redundant, but if this is converted to a package at some point, it
	may come in handy if main is called as a method.
	"""
	if args.File and args.Text:
		print "You can pass --file (-f) or --text (-t) but not both"
		sys.exit(1)

	if args.Text:
		main(city, sms_to=args.Text)
	elif args.File:
		main(city, out_file=True)
	else:
		main(city)

	sys.exit(0)