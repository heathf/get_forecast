"""
	A simple module for sending sms messages.

	NOTE: It uses twillio which is a non-standard module that needs to be in setup.py.  Normally I wouldn't use a dev
	account for a project that is being distributed, but for this scenario it seemed appropriate
"""

import logging
from config import *
from twilio.rest import TwilioRestClient

logger = logging.getLogger('get_forecast.sms')

def _get_twilio_info():
	"""
	Reads the values from our data.json file.  This should be used as a private module level function, since (at least
	currently) data.json only contains twilio related information.

	:return: (dict) A dict that has our twilio info within it
	"""
	with open(data_path) as json_file:
		data = json.load(json_file)

	return data

def _clean_phone_number(phone_number, from_number=False):
	"""
	A simple function that cleans up phone numbers. If someone passes in a number that begins with a ``1``, or contains
	(), it strips them. It also ensures that a ``from`` number begins with a + which twilio requires

	:param phone_number: (str) The phone number to clean
	:param from_number: (bool) If this is a ``from`` twilio number, it needs to be handled specially
	:return: (str) The clean phone number
	"""
	logger.debug("In _clean_phone_number and initial number is {}".format(phone_number))
	phone_number = phone_number if not phone_number.startswith("1") else phone_number[1:]
	phone_number = phone_number.replace("-","").replace("(", "").replace(")", "")

	if from_number:
		phone_number = "{}{}".format("+", phone_number) if not phone_number.startswith("+") else phone_number

	logger.debug("In _clean_phone_number and cleaned phone number is {}".format(phone_number))
	return phone_number

def send_sms(send_to, msg_body, send_from=None):
	"""
	Will send a text message to the specified number

	:param send_to: (str) The phone number to send the SMS to. (Shouldn't begin with a 1)
	:param msg_body: (str) The text of the message to send
	:param send_from: (str) The number to send from. This defaults to my twilio dev number
	:return: (None)
	"""
	data = _get_twilio_info()

	try:
		ACCOUNT_SID = data['ACCOUNT_SID']
		AUTH_TOKEN = data['AUTH_TOKEN']
		send_from = send_from if send_from else data['FROM_NUMBER']
	except KeyError:
		err_msg = "send_sms caught a key error for ACCOUNT_SID, AUTH_TOKEN or FROM_NUMBER in data.json"
		logger.error(err_msg)
		raise Exception(err_msg)

	send_from = _clean_phone_number(send_from, True)
	send_to = _clean_phone_number(send_to)

	logger.debug("Sending an SMS message from {} to {} with body:\n{}".format(send_from, send_to, msg_body))

	client = TwilioRestClient(ACCOUNT_SID, AUTH_TOKEN)
	client.messages.create(to=send_to, from_=send_from, body=msg_body)