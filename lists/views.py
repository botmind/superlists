from django.shortcuts import render, redirect
from django.core.exceptions import ValidationError
from lists.models import Quote, Author

# Create your views here.
def home_page(request):
	return render(request, 'home.html')

def view_quote(request, author_id):
	author = Author.objects.get(id=author_id) #retrieve the author using the id
	return render(request, 'quotes.html', {'author': author})

def new_quote(request):
	author = Author.objects.create()
	quote = Quote(text=request.POST['quote_text'], author=author)
	try:
		quote.full_clean()
		quote.save() #only save the quote if it passes all validations
	except ValidationError:
		author.delete() #if the quote does not pass the validation tests, remove the extraneous author
		error = "You can't submit a quote with no text!"
		return render(request, 'home.html', {"error": error})
	return redirect('/quotes/%d/' % (author.id))

def add_quote(request, author_id):
	author = Author.objects.get(id=author_id)
	Quote.objects.create(text=request.POST['quote_text'], author=author)
	return redirect('/quotes/%d/' % (author.id))