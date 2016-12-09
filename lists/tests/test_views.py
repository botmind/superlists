from django.utils.html import escape
from django.template.loader import render_to_string
from django.core.urlresolvers import resolve
from django.test import TestCase
from django.http import HttpRequest

from lists.views import home_page
from lists.models import Quote, Author
from lists.forms import QuoteForm, EMPTY_QUOTE_ERROR

from unittest import skip

class HomePageTest(TestCase):

	def test_root_url_resolves_to_home_page_view(self):
		found = resolve('/')
		self.assertEqual(found.func, home_page)

	def test_home_page_returns_correct_html(self):
		request = HttpRequest()
		response = home_page(request)
		expected_html = render_to_string('home.html', {'form': QuoteForm()})
		#print(expected_html)
		self.assertEqual(response.content.decode(), expected_html) #make sure the HTML received in the response is identical to the template; decode converts the bytes into a string

	def test_home_page_uses_quote_form(self):
		response = self.client.get('/')
		self.assertIsInstance(response.context['form'], QuoteForm)

class QuoteViewTest (TestCase):

	def test_uses_quote_template(self):
		author = Author.objects.create()
		response = self.client.get('/quotes/%d/' % (author.id))
		self.assertTemplateUsed(response, 'quotes.html')

	def test_displays_only_quotes_for_that_author(self):
		correct_author = Author.objects.create()
		Quote.objects.create(text='quote 1', author=correct_author)
		Quote.objects.create(text='quote 2', author=correct_author)
		other_author = Author.objects.create()
		Quote.objects.create(text='other quotey', author=other_author)
		Quote.objects.create(text='other quoteyb', author=other_author)

		response = self.client.get('/quotes/%d/' % (correct_author.id))
		
		self.assertContains(response, 'quote 1')
		self.assertContains(response, 'quote 2')
		self.assertNotContains(response, 'other quotey')
		self.assertNotContains(response, 'other quoteyb')

	def test_passes_correct_author_to_template(self):
		other_author = Author.objects.create()
		correct_author = Author.objects.create()
		response = self.client.get('/quotes/%d/' % (correct_author.id))
		self.assertEqual(response.context['author'], correct_author)

	def test_can_save_a_POST_request_to_an_existing_list(self):
		other_author = Author.objects.create()
		correct_author = Author.objects.create()

		self.client.post('/quotes/%d/' % (correct_author.id), data={'text': 'A new quote for an existing author'})
		self.assertEqual(Quote.objects.count(), 1)
		new_quote = Quote.objects.first()
		self.assertEqual(new_quote.text, 'A new quote for an existing author')
		self.assertEqual(new_quote.author, correct_author)

	def test_POST_redirects_to_quote_view(self):
		other_author = Author.objects.create()
		correct_author = Author.objects.create()

		response = self.client.post('/quotes/%d/' % (correct_author.id), data={'text': 'A new quote for an existing author'})

		self.assertRedirects(response, '/quotes/%d/' % (correct_author.id))

	def post_invalid_input(self):
		author = Author.objects.create()
		return self.client.post('/quotes/%d/' % (author.id), data={'text': ''})

	def test_for_invalid_input_nothing_saved_to_db(self):
		self.post_invalid_input()
		self.assertEqual(Quote.objects.count(), 0)

	def test_for_invalid_input_renders_quote_template(self):
		response = self.post_invalid_input()
		self.assertEqual(response.status_code, 200)
		self.assertTemplateUsed(response, 'quotes.html')

	def test_for_invalid_input_passes_form_to_template(self):
		response = self.post_invalid_input()
		self.assertIsInstance(response.context['form'], QuoteForm)

	def test_for_invalid_input_shows_error_on_page(self):
		response = self.post_invalid_input()
		self.assertContains(response, escape(EMPTY_QUOTE_ERROR))

	@skip
	def test_duplicate_quote_validation_errors_display_on_quotes_page(self):
		author1 = Author.objects.create()
		quote1 = Quote.objects.create(author=author1, text='q1')
		response = self.client.post('/quotes/%d/' % (author1.id), data={'text': 'q1'})
		expected_error = escape("This quote already exists.")
		self.assertContains(response, expected_error)
		self.assertTemplateUsed(response, 'quotes.html')
		self.assertEqual(Quote.objects.all().count(), 1)


class NewQuoteTest(TestCase):

	def test_saving_a_POST_request(self):
		self.client.post('/quotes/new', data={'text': 'I think, therefore I am.'})

		self.assertEqual(Quote.objects.count(), 1)
		new_quote = Quote.objects.first()
		self.assertEqual('I think, therefore I am.', new_quote.text)

	def test_redirects_after_POST(self):
		response = self.client.post('/quotes/new', data={'text': 'I think, therefore I am.'})
		new_author = Author.objects.first()
		self.assertRedirects(response, '/quotes/%d/' % (new_author.id))

	def test_for_invalid_input_renders_home_template(self):
		response = self.client.post('/quotes/new', data={'text': ''})
		self.assertEqual(response.status_code, 200)
		self.assertTemplateUsed(response, 'home.html')

	def test_validation_errors_are_shown_on_home_page(self):
		response = self.client.post('/quotes/new', data={'text': ''})
		self.assertContains(response, escape(EMPTY_QUOTE_ERROR))

	def test_for_invalid_input_passes_form_to_template(self):
		response = self.client.post('/quotes/new', data={'text': ''})
		self.assertIsInstance(response.context['form'], QuoteForm)


	def test_invalid_quotes_arent_saved(self):
		self.client.post('/quotes/new', data={'text': ''})
		self.assertEqual(Author.objects.count(), 0)
		self.assertEqual(Quote.objects.count(), 0)