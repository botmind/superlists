from django.shortcuts import render, redirect
from lists.models import Quote

# Create your views here.
def home_page(request):
	if request.method == 'POST':
		Quote.objects.create(text=request.POST['quote_text'])
		return redirect('/')

	quotes = Quote.objects.all()
	return render(request, 'home.html', {'quotes': quotes})