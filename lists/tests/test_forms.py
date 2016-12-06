from django.test import TestCase
from lists.forms import QuoteForm, EMPTY_QUOTE_ERROR

class QuoteFormTest(TestCase):

	def test_form_quote_input_has_placeholder_and_css_classes(self):
		form = QuoteForm()
		self.assertIn('placeholder="Enter a new quote"', form.as_p())
		self.assertIn('class="form-control input-lg"', form.as_p())

	def test_form_validation_for_blank_quotes(self):
		form = QuoteForm(data={'text':''})
		self.assertFalse(form.is_valid()) #populates error attribute with a dict mapping names of fields of model to errors for those fields
		self.assertEqual(form.errors['text'], [EMPTY_QUOTE_ERROR])