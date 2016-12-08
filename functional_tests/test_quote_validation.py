from .base import FunctionalTest

class QuoteValidationTest(FunctionalTest):

	def test_cannot_add_empty_quotes(self):
		#user hits enter on empty input box
		self.browser.get(self.server_url)
		self.get_quote_input_box().send_keys('\n')

		#home page refreshes; error message flashes: quotes cannot be blank
		error = self.browser.find_element_by_css_selector('.has-error')
		self.assertEqual(error.text, "You can't submit a quote with no text!")

		#user enters a quote; everything works
		self.get_quote_input_box().send_keys('Quote 1\n')
		self.check_for_row_in_list_table('Quote 1')

		#user tries to submit empty box again
		self.get_quote_input_box().send_keys('\n')

		#error message flashes again
		self.check_for_row_in_list_table('Quote 1')
		error = self.browser.find_element_by_css_selector('.has-error')
		self.assertEqual(error.text, "You can't submit a quote with no text!")

		#user fills in text to correct error
		self.get_quote_input_box().send_keys('Quote 2\n')
		self.check_for_row_in_list_table('Quote 1')
		self.check_for_row_in_list_table('Quote 2')

	def test_cannot_add_duplicate_quotes(self):
		#submit a new quote
		self.browser.get(self.server_url)
		self.get_quote_input_box().send_keys('Quote 1\n')
		self.check_for_row_in_list_table('Quote 1')

		#try to enter a duplicate quote
		self.get_quote_input_box().send_keys('Quote 1\n')

		#error message is displayed
		self.check_for_row_in_list_table('Quote 1')
		error = self.browser.find_element_by_css_selector('.has-error')
		self.assertEqual(error.text, "This quote already exists.")


