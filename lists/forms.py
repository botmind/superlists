from django import forms
from lists.models import Quote
from django.core.exceptions import ValidationError

EMPTY_QUOTE_ERROR = "You can't submit a quote with no text!"
DUPLICATE_QUOTE_ERROR = "This quote already exists."

class QuoteForm(forms.models.ModelForm):

	class Meta:
		model = Quote
		fields = ('text',)
		widgets = {
			'text': forms.fields.TextInput(attrs={
				'placeholder': 'Enter a new quote',
				'class': 'form-control input-lg'
			})
		}
		error_messages = {
			'text': {'required': EMPTY_QUOTE_ERROR}
		}

	def save(self, for_author):
		self.instance.author = for_author #.instance is the db object that is currently being modified or created
		return super().save()

class ExistingAuthorQuoteForm(QuoteForm):
	
	def __init__(self, for_author, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.instance.author = for_author #link the object currently being modified to the author

	def validate_unique(self):
		try:
			self.instance.validate_unique()
		except ValidationError as e:
			e.error_dict = {'text': [DUPLICATE_QUOTE_ERROR]}
			self._update_errors(e)

	def save(self):
		return forms.models.ModelForm.save(self) #call the grandparent class save method (with no for_author, since this is already taken care of in init)