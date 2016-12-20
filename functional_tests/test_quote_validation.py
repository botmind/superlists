from .base import FunctionalTest

class QuoteValidationTest(FunctionalTest):

	def get_error_element(self):
		return self.browser.find_element_by_css_selector('.has-error')

	def test_cannot_add_empty_quotes(self):
		#user hits enter on empty input box
		self.browser.get(self.server_url)
		self.get_quote_input_box().send_keys('\n')

		#the browser intercepts the request, and does not load the quote page
		self.assertNotIn('Quote 1', self.browser.find_element_by_tag_name('body').text)

		#user enters a quote; everything works
		self.get_quote_input_box().send_keys('Quote 1\n')
		self.check_for_row_in_list_table('Quote 1')

		#user tries to submit empty box again
		self.get_quote_input_box().send_keys('\n')

		#browser prevents this again
		self.check_for_row_in_list_table('Quote 1')
		rows = self.browser.find_elements_by_css_selector('#id_quote_table tr')
		self.assertEqual(len(rows), 1)

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
		error = self.get_error_element()
		self.assertEqual(error.text, "This quote already exists.")

	def test_error_messages_cleared_on_input(self):
		#start a quote and cause a validation error
		self.browser.get(self.server_url)
		self.get_quote_input_box().send_keys('quote\n')
		self.check_for_row_in_list_table('quote')
		self.get_quote_input_box().send_keys('quote\n')

		error = self.get_error_element()
		self.assertTrue(error.is_displayed())

		#start typing in the input to clear the error
		self.get_quote_input_box().send_keys('a')

		#the error message instantly disappears
		error = self.get_error_element()
		self.assertFalse(error.is_displayed())

	def test_error_messages_cleared_on_click_in(self):
		#start a quote and cause a validation error
		self.browser.get(self.server_url)
		self.get_quote_input_box().send_keys('quote\n')
		self.check_for_row_in_list_table('quote')
		self.get_quote_input_box().send_keys('quote\n')

		error = self.get_error_element()
		self.assertTrue(error.is_displayed())

		#click into the input to clear the error
		self.get_quote_input_box().click()

		#the error message instantly disappears
		error = self.get_error_element()
		self.assertFalse(error.is_displayed())


