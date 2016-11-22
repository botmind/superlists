from django.shortcuts import render, redirect
from lists.models import Quote, Author

# Create your views here.
def home_page(request):
	return render(request, 'home.html')

def view_quote(request):
	quotes = Quote.objects.all()
	return render(request, 'quotes.html', {'quotes': quotes})

def new_quote(request):
	author = Author.objects.create()
	Quote.objects.create(text=request.POST['quote_text'], author=author)
	return redirect('/quotes/quote-list/')