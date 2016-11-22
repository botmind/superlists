from django.shortcuts import render, redirect
from lists.models import Quote

# Create your views here.
def home_page(request):
	return render(request, 'home.html')

def view_quote(request):
	quotes = Quote.objects.all()
	return render(request, 'quotes.html', {'quotes': quotes})

def new_quote(request):
	Quote.objects.create(text=request.POST['quote_text'])
	return redirect('/quotes/quote-list/')