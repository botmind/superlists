from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


class NewVisitorTest(LiveServerTestCase):

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
		self.browser.get(self.live_server_url)

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
		edith_list_url = self.browser.current_url
		self.assertRegex(edith_list_url, '/quotes/.+')

		self.check_for_row_in_list_table('I think, therefore I am.')

		# There is still a text box inviting her to add another quote. She
		# enters "Man is a rational animal."
		inputbox = self.browser.find_element_by_id('id_new_quote')
		inputbox.send_keys('Man is a rational animal.')
		inputbox.send_keys(Keys.ENTER)

		# The page updates again, and now shows both quotes
		self.check_for_row_in_list_table('I think, therefore I am.')
		self.check_for_row_in_list_table('Man is a rational animal.')

		# A new user, Francis, comes to the site.

		## We use a new session to make sure no information
		## from Edith is coming through from cookies, etc.

		self.browser.quit()
		self.browser = webdriver.Firefox()

		# Francis visits the home page.  There is no sign of Edith's quotes.
		self.browser.get(self.live_server_url)
		page_text = self.browser.find_element_by_tag_name('body').text
		self.assertNotIn('I think, therefore I am.', page_text)
		self.assertNotIn('Man is a rational animal.', page_text)

		#Francis enters a new quote.
		inputbox = self.browser.find_element_by_id('id_new_quote')
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

	def test_layout_and_styling(self):
		#visit the home page
		self.browser.get(self.live_server_url)
		self.browser.set_window_size(1024, 768)

		#input box is centred
		inputbox = self.browser.find_element_by_id('id_new_quote')
		self.assertAlmostEqual(inputbox.location['x'] + inputbox.size['width'] / 2, 512, delta=10)

		#enter a new quote
		inputbox.send_keys('A new quote\n')
		inputbox = self.browser.find_element_by_id('id_new_quote')
		self.assertAlmostEqual(inputbox.location['x'] + inputbox.size['width'] / 2, 512, delta=10)

