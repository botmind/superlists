from django.shortcuts import render, redirect
from django.core.exceptions import ValidationError
from lists.models import Quote, Author
from lists.forms import QuoteForm

# Create your views here.
def home_page(request):
	return render(request, 'home.html', {'form': QuoteForm()})

def view_quote(request, author_id):
	author = Author.objects.get(id=author_id) #retrieve the author using the id passed in as part of the URL
	form = QuoteForm()
	if request.method == 'POST':
		form = QuoteForm(data=request.POST)
		if form.is_valid():
			Quote.objects.create(text=request.POST['text'], author=author)
			return redirect(author) #gets '/quotes/%d/' % (author.id) using the get_absolute_url fn in the Author model
	return render(request, 'quotes.html', {'author': author, 'form': form})

def new_quote(request):
	form = QuoteForm(data=request.POST)
	if form.is_valid():
		author = Author.objects.create()
		Quote.objects.create(text=request.POST['text'], author=author)
		return redirect(author) #gets '/quotes/%d/' % (author.id) using the get_absolute_url fn in the Author model
	else:
		return render(request, 'home.html', {'form': form})