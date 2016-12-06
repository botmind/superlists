from django.test import TestCase
from lists.models import Quote, Author


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