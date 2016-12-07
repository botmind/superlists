from django.test import TestCase
from lists.forms import QuoteForm, EMPTY_QUOTE_ERROR
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