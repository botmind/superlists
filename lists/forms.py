from django import forms
from lists.models import Quote

EMPTY_QUOTE_ERROR = "You can't submit a quote with no text!"

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
