from .base import FunctionalTest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

class NewVisitorTest(FunctionalTest):

	def test_can_start_a_list_for_one_user(self):
		# Edith has heard about a cool new online app with famous quotes. She goes
		# to check out its homepage
		self.browser.get(self.server_url)

		# She notices the page title and header mention wise words
		self.assertIn('Wise Words', self.browser.title)
		header_text = self.browser.find_element_by_tag_name('h1').text
		self.assertIn('Wise Words', header_text)
		

		# She is invited to enter a new quotation straight away
		inputbox = self.get_quote_input_box()
		self.assertEqual(inputbox.get_attribute('placeholder'), 'Enter a new quote')

		# She types "I think, therefore I am." into a text box
		inputbox.send_keys('I think, therefore I am.')

		# When she hits enter, the page updates, and now the page lists
		# "I think, therefore I am."" as a new quote.
		inputbox.send_keys(Keys.ENTER)
		edith_list_url = self.browser.current_url
		self.assertRegex(edith_list_url, '/quotes/.+')

		self.check_for_row_in_list_table('I think, therefore I am.')

		# There is still a text box inviting her to add another quote. She
		# enters "Man is a rational animal."
		inputbox = self.get_quote_input_box()
		inputbox.send_keys('Man is a rational animal.')
		inputbox.send_keys(Keys.ENTER)

		# The page updates again, and now shows both quotes
		self.check_for_row_in_list_table('I think, therefore I am.')
		self.check_for_row_in_list_table('Man is a rational animal.')

	def test_multiple_users_can_start_lists_at_different_urls(self):
		#Edith enters a new quote

		self.browser.get(self.server_url)
		inputbox = self.get_quote_input_box()
		inputbox.send_keys('I think, therefore I am.\n')
		self.check_for_row_in_list_table('I think, therefore I am.')

		#her list has a unique URL

		edith_list_url = self.browser.current_url
		self.assertRegex(edith_list_url, '/quotes/.+')

		# A new user, Francis, comes to the site.

		## We use a new session to make sure no information
		## from Edith is coming through from cookies, etc.

		self.browser.quit()
		self.browser = webdriver.Firefox()

		# Francis visits the home page.  There is no sign of Edith's quotes.
		self.browser.get(self.server_url)
		page_text = self.browser.find_element_by_tag_name('body').text
		self.assertNotIn('I think, therefore I am.', page_text)
		self.assertNotIn('Man is a rational animal.', page_text)

		#Francis enters a new quote.
		inputbox = self.get_quote_input_box()
		inputbox.send_keys('The pen is mightier than the sword.')
		inputbox.send_keys(Keys.ENTER)

		#Francis gets his own unique URL
		francis_list_url = self.browser.current_url
		self.assertRegex(francis_list_url, '/quotes/.+')
		self.assertNotEqual(francis_list_url, edith_list_url)

		#There is no trace of Edith's quotes
		page_text = self.browser.find_element_by_tag_name('body').text
		self.assertNotIn('I think, therefore I am.', page_text)
		self.assertIn('The pen is mightier than the sword.', page_text)

		#Satisfied, they both go to sleep