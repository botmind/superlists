from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import unittest

class NewVisitorTest(unittest.TestCase):

	def setUp(self):
		self.browser = webdriver.Firefox()
		self.browser.implicitly_wait(3)

	def tearDown(self):
		self.browser.quit()

	def check_for_row_in_list_table(self, row_text):
		table = self.browser.find_element_by_id('id_quote_table')
		rows = table.find_elements_by_tag_name('tr')
		self.assertIn(row_text, [row.text for row in rows])

	def test_can_start_a_list_and_retrieve_it_later(self):
		# Edith has heard about a cool new online app with famous quotes. She goes
		# to check out its homepage
		self.browser.get('http://localhost:8000')

		# She notices the page title and header mention wise words
		self.assertIn('Wise Words', self.browser.title)
		header_text = self.browser.find_element_by_tag_name('h1').text
		self.assertIn('Wise Words', header_text)
		

		# She is invited to enter a new quotation straight away
		inputbox = self.browser.find_element_by_id('id_new_quote')
		self.assertEqual(inputbox.get_attribute('placeholder'), 'Enter a new quote')

		# She types "I think, therefore I am." into a text box
		inputbox.send_keys('I think, therefore I am.')

		# When she hits enter, the page updates, and now the page lists
		# "I think, therefore I am."" as a new quote.
		inputbox.send_keys(Keys.ENTER)

		self.check_for_row_in_list_table('I think, therefore I am.')

		# There is still a text box inviting her to add another quote. She
		# enters "Man is a rational animal."
		inputbox = self.browser.find_element_by_id('id_new_quote')
		inputbox.send_keys('Man is a rational animal.')
		inputbox.send_keys(Keys.ENTER)

		# The page updates again, and now shows both quotes
		self.check_for_row_in_list_table('I think, therefore I am.')
		self.check_for_row_in_list_table('Man is a rational animal.')

		# Edith wonders whether the site will remember her list. Then she sees
		# that the site has generated a unique URL for her -- there is some
		# explanatory text to that effect.

		# She visits that URL - her to-do list is still there.

		# Satisfied, she goes back to sleep
		self.fail('Finish the test!')

if __name__ == '__main__':
	unittest.main(warnings='ignore')