from django.template.loader import render_to_string
from django.core.urlresolvers import resolve
from django.test import TestCase
from django.http import HttpRequest

from lists.views import home_page
from lists.models import Quote

class HomePageTest(TestCase):

	def test_root_url_resolves_to_home_page_view(self):
		found = resolve('/')
		self.assertEqual(found.func, home_page)

	def test_home_page_returns_correct_html(self):
		request = HttpRequest()
		response = home_page(request)
		expected_html = render_to_string('home.html')
		self.assertEqual(response.content.decode(), expected_html) #make sure the HTML received in the response is identical to the template; decode converts the bytes into a string

	def test_home_page_can_save_a_POST_request(self):
		request = HttpRequest()
		request.method = 'POST'
		request.POST['quote_text'] = 'I think, therefore I am.'

		response = home_page(request)

		self.assertIn('I think, therefore I am.', response.content.decode())
		expected_html = render_to_string('home.html', {'new_quote_text': 'I think, therefore I am.'})
		self.assertEqual(response.content.decode(), expected_html)

class QuoteModelTest(TestCase):
	
	def test_saving_and_retrieving_items(self):

		first_quote = Quote()
		first_quote.text = "I am the alpha and the omega."
		first_quote.save()

		second_quote = Quote()
		second_quote.text = "I second that emotion."
		second_quote.save()

		saved_quotes = Quote.objects.all()
		self.assertEqual(saved_quotes.count(), 2)

		first_saved_quote = saved_quotes[0]
		second_saved_quote = saved_quotes[1]
		self.assertEqual(first_saved_quote.text, "I am the alpha and the omega.")
		self.assertEqual(second_saved_quote.text, "I second that emotion.")