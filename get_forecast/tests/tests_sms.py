"""
	A test class for our SMS module. It mostly verifies that our phone numbers are valid for the twilio API.

	Can be invoked from bash terminal with syntax similar to this example:

	cd /path/to/get_forecast
	python -m unittest discover "$(pwd)/tests" -p tests*.py
"""

import unittest
from lib.config import *
from lib import sms

class TestSms(unittest.TestCase):
	def setUp(self):
		with open(data_path) as json_file:
			self.data = json.load(json_file)

		self.to = "207-555-5555"
		self.from_number = self.data['FROM_NUMBER']

	def _check_key(self, key):
		no_exception = True
		try:
			exists = self.data[key]
		except KeyError:
			no_exception = False

		assert no_exception == True

	def test_clean_to_is_digit(self):
		""" Make sure our to number contains only digits """
		clean_to = sms._clean_phone_number(self.to)
		assert clean_to.isdigit()

	def test_clean_from_is_digit(self):
		""" Make sure our from number is all digits except for the first char """
		clean_from = sms._clean_phone_number(self.from_number, True)
		assert clean_from[1:].isdigit()

	def test_from_number_starts_with_plus(self):
		""" Ensure our from number begins with a + """
		clean_from = sms._clean_phone_number(self.from_number, True)
		assert clean_from.startswith("+")

	def test_auth_token_present(self):
		""" Make sure our twilio AUTH_TOKEN is present in data.json """
		return self._check_key('AUTH_TOKEN')

	def test_auth_token_not_empty(self):
		""" Ensure our AUTH_TOKEN has a value """
		assert self.data['AUTH_TOKEN'] != ''

	def test_account_sid_present(self):
		""" Verify ACCOUNT_SID is present in data.json """
		return self._check_key('ACCOUNT_SID')

	def test_account_sid_not_empty(self):
		""" Verify ACCOUNT_SID has a value """
		assert self.data['ACCOUNT_SID'] != ''

	def tearDown(self):
		pass