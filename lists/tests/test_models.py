from django.test import TestCase
from django.core.exceptions import ValidationError
from lists.models import Quote, Author


class QuoteModelTest(TestCase):
	
	def test_default_text(self):
		quote = Quote()
		self.assertEqual(quote.text, '')

	def test_quote_is_related_to_author(self):
		author = Author.objects.create()
		quote = Quote()
		quote.author = author
		quote.save()
		self.assertIn(quote, author.quote_set.all())

	def test_cannot_save_empty_quotes(self):
		author = Author.objects.create()
		quote = Quote.objects.create(author=author, text='')
		with self.assertRaises(ValidationError):
			quote.save()
			quote.full_clean()

	def test_duplicate_quotes_are_invalid(self):
		author = Author.objects.create()
		Quote.objects.create(author=author, text="q1")
		with self.assertRaises(ValidationError):
			quote = Quote(author=author, text="q1")
			quote.full_clean()

	def test_can_save_same_quote_to_different_authors(self):
		author1 = Author.objects.create()
		author2 = Author.objects.create()
		Quote.objects.create(author=author1, text="q1")
		quote = Quote(author=author2, text="q1")
		quote.full_clean() #should not raise error

	def test_quote_ordering(self):
		author1 = Author.objects.create()
		quote1 = Quote.objects.create(author=author1, text="q1")
		quote2 = Quote.objects.create(author=author1, text="q2")
		quote3 = Quote.objects.create(author=author1, text="q3")
		self.assertEqual(list(Quote.objects.all()), [quote1, quote2, quote3]) #have to convert queryset to list or comparison will not work

	def test_string_representation(self):
		quote = Quote(text='some text')
		self.assertEqual(str(quote), 'some text')

class AuthorModelTest(TestCase):

	def test_get_absolute_url(self):
		author = Author.objects.create()
		self.assertEqual(author.get_absolute_url(), '/quotes/%d/' % (author.id))