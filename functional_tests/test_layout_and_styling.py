from .base import FunctionalTest

class LayoutAndStylingTest(FunctionalTest):

	def test_layout_and_styling(self):
		#visit the home page
		self.browser.get(self.server_url)
		self.browser.set_window_size(1024, 768)

		#input box is centred
		inputbox = self.get_quote_input_box()
		self.assertAlmostEqual(inputbox.location['x'] + inputbox.size['width'] / 2, 512, delta=10)

		#enter a new quote
		inputbox.send_keys('A new quote\n')
		inputbox = self.get_quote_input_box()
		self.assertAlmostEqual(inputbox.location['x'] + inputbox.size['width'] / 2, 512, delta=10)