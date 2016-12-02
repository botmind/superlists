from .base import FunctionalTest

class LayoutAndStylingTest(FunctionalTest):

	def test_layout_and_styling(self):
		#visit the home page
		self.browser.get(self.server_url)
		self.browser.set_window_size(1024, 768)

		#input box is centred
		inputbox = self.browser.find_element_by_id('id_new_quote')
		self.assertAlmostEqual(inputbox.location['x'] + inputbox.size['width'] / 2, 512, delta=10)

		#enter a new quote
		inputbox.send_keys('A new quote\n')
		inputbox = self.browser.find_element_by_id('id_new_quote')
		self.assertAlmostEqual(inputbox.location['x'] + inputbox.size['width'] / 2, 512, delta=10)