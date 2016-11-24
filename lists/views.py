from django.shortcuts import render, redirect
from lists.models import Quote, Author

# Create your views here.
def home_page(request):
	return render(request, 'home.html')

def view_quote(request, author_id):
	author = Author.objects.get(id=author_id) #retrieve the author using the id
	return render(request, 'quotes.html', {'author': author})

def new_quote(request):
	author = Author.objects.create()
	Quote.objects.create(text=request.POST['quote_text'], author=author)
	return redirect('/quotes/%d/' % (author.id))

def add_quote(request, author_id):
	author = Author.objects.get(id=author_id)
	Quote.objects.create(text=request.POST['quote_text'], author=author)
	return redirect('/quotes/%d/' % (author.id))