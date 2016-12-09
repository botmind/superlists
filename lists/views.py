from django.shortcuts import render, redirect
from django.core.exceptions import ValidationError
from lists.models import Quote, Author
from lists.forms import QuoteForm, ExistingAuthorQuoteForm

# Create your views here.
def home_page(request):
	return render(request, 'home.html', {'form': QuoteForm()})

def view_quote(request, author_id):
	author = Author.objects.get(id=author_id) #retrieve the author using the id passed in as part of the URL
	form = ExistingAuthorQuoteForm(for_author=author)
	if request.method == 'POST':
		form = ExistingAuthorQuoteForm(for_author=author, data=request.POST)
		if form.is_valid():
			form.save()
			return redirect(author) #gets '/quotes/%d/' % (author.id) using the get_absolute_url fn in the Author model
	return render(request, 'quotes.html', {'author': author, 'form': form})

def new_quote(request):
	form = QuoteForm(data=request.POST)
	if form.is_valid():
		author = Author.objects.create()
		form.save(for_author=author)
		return redirect(author) #gets '/quotes/%d/' % (author.id) using the get_absolute_url fn in the Author model
	else:
		return render(request, 'home.html', {'form': form})