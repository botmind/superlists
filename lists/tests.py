from django.template.loader import render_to_string
from django.core.urlresolvers import resolve
from django.test import TestCase
from django.http import HttpRequest

from lists.views import home_page
from lists.models import Quote, Author

class HomePageTest(TestCase):

	def test_root_url_resolves_to_home_page_view(self):
		found = resolve('/')
		self.assertEqual(found.func, home_page)

	def test_home_page_returns_correct_html(self):
		request = HttpRequest()
		response = home_page(request)
		expected_html = render_to_string('home.html')
		self.assertEqual(response.content.decode(), expected_html) #make sure the HTML received in the response is identical to the template; decode converts the bytes into a string

class QuoteViewTest (TestCase):

	def test_uses_quote_template(self):
		response = self.client.get('/quotes/quote-list/')
		self.assertTemplateUsed(response, 'quotes.html')

	def test_displays_all_items(self):
		author = Author.objects.create()
		Quote.objects.create(text='quote 1', author=author)
		Quote.objects.create(text='quote 2', author=author)

		response = self.client.get('/quotes/quote-list/')

		self.assertContains(response, 'quote 1')
		self.assertContains(response, 'quote 2')

class AuthorAndQuoteModelTest(TestCase):
	
	def test_saving_and_retrieving_items(self):

		author = Author()
		author.save()

		first_quote = Quote()
		first_quote.text = "I am the alpha and the omega."
		first_quote.author = author
		first_quote.save()

		second_quote = Quote()
		second_quote.text = "I second that emotion."
		second_quote.author = author
		second_quote.save()

		saved_author = Author.objects.first()
		self.assertEqual(saved_author, author)

		saved_quotes = Quote.objects.all()
		self.assertEqual(saved_quotes.count(), 2)

		first_saved_quote = saved_quotes[0]
		second_saved_quote = saved_quotes[1]
		self.assertEqual(first_saved_quote.text, "I am the alpha and the omega.")
		self.assertEqual(first_saved_quote.author, author)
		self.assertEqual(second_saved_quote.text, "I second that emotion.")
		self.assertEqual(second_saved_quote.author, author)

class NewQuoteTest(TestCase):

	def test_saving_a_POST_request(self):
		self.client.post('/quotes/new', data={'quote_text': 'I think, therefore I am.'})

		self.assertEqual(Quote.objects.count(), 1)
		new_quote = Quote.objects.first()
		self.assertEqual('I think, therefore I am.', new_quote.text)

	def test_redirects_after_POST(self):
		response = self.client.post('/quotes/new', data={'quote_text': 'I think, therefore I am.'})
		self.assertRedirects(response, '/quotes/quote-list/')