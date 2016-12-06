from .base import FunctionalTest
from unittest import skip

class QuoteValidationTest(FunctionalTest):

	def test_cannot_add_empty_quotes(self):
		#user hits enter on empty input box
		self.browser.get(self.server_url)
		self.browser.find_element_by_id('id_new_quote').send_keys('\n')

		#home page refreshes; error message flashes: quotes cannot be blank
		error = self.browser.find_element_by_css_selector('.has-error')
		self.assertEqual(error.text, "You can't submit a quote with no text!")

		#user enters a quote; everything works
		self.browser.find_element_by_id('id_new_quote').send_keys('Quote 1\n')
		self.check_for_row_in_list_table('Quote 1')

		#user tries to submit empty box again
		self.browser.find_element_by_id('id_new_quote').send_keys('\n')

		#error message flashes again
		self.check_for_row_in_list_table('Quote 1')
		error = self.browser.find_element_by_css_selector('.has-error')
		self.assertEqual(error.text, "You can't submit a quote with no text!")

		#user fills in text to correct error
		self.browser.find_element_by_id('id_new_quote').send_keys('Quote 2\n')
		self.check_for_row_in_list_table('Quote 1')
		self.check_for_row_in_list_table('Quote 2')

