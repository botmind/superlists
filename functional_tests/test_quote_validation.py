from .base import FunctionalTest
from unittest import skip

class ItemValidationTest(FunctionalTest):

	def test_cannot_add_empty_list_items(self):
		#user hits enter on empty input box

		#home page refreshes; error message flashes: list items cannot be blank

		#user enters a quote; everything works

		#user tries to submit empty box again

		#error message flashes again

		#user fills in text to correct error
		self.fail('write me!')


