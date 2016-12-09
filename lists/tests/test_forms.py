from django.test import TestCase
from lists.forms import (QuoteForm, EMPTY_QUOTE_ERROR, DUPLICATE_QUOTE_ERROR, ExistingAuthorQuoteForm)
from lists.models import Author, Quote

class QuoteFormTest(TestCase):

	def test_form_quote_input_has_placeholder_and_css_classes(self):
		form = QuoteForm()
		self.assertIn('placeholder="Enter a new quote"', form.as_p())
		self.assertIn('class="form-control input-lg"', form.as_p())

	def test_form_validation_for_blank_quotes(self):
		form = QuoteForm(data={'text':''})
		self.assertFalse(form.is_valid()) #populates error attribute with a dict mapping names of fields of model to errors for those fields
		self.assertEqual(form.errors['text'], [EMPTY_QUOTE_ERROR])

	def test_form_save_handles_saving_to_an_author(self):
		author = Author.objects.create()
		form = QuoteForm(data={'text': 'Quote1'})
		new_quote = form.save(for_author=author)
		self.assertEqual(new_quote, Quote.objects.first())
		self.assertEqual(new_quote.text, 'Quote1')
		self.assertEqual(new_quote.author, author)

class ExistingAuthorQuoteFormTest(TestCase):

	def test_form_renders_quote_text_input(self):
		author = Author.objects.create()
		form = ExistingAuthorQuoteForm(for_author=author)
		self.assertIn('placeholder="Enter a new quote"', form.as_p())

	def test_form_validation_for_blank_quotes(self):
		author = Author.objects.create()
		form = ExistingAuthorQuoteForm(for_author=author, data={'text':''})
		self.assertFalse(form.is_valid())
		self.assertEqual(form.errors['text'], [EMPTY_QUOTE_ERROR])

	def test_form_validation_for_duplicate_items(self):
		author = Author.objects.create()
		Quote.objects.create(author=author, text='no dupes')
		form = ExistingAuthorQuoteForm(for_author=author, data={'text': 'no dupes'})
		self.assertFalse(form.is_valid())
		self.assertEqual(form.errors['text'], [DUPLICATE_QUOTE_ERROR])

	def test_form_save(self):
		author = Author.objects.create()
		form = ExistingAuthorQuoteForm(for_author=author, data={'text': 'quote'})
		new_quote = form.save()
		self.assertEqual(new_quote, Quote.objects.all()[0])
