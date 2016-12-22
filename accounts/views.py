from django.shortcuts import redirect
from django.core.mail import send_mail
from django.contrib import auth, messages
from accounts.models import Token
from django.core.urlresolvers import reverse

# Create your views here.
def send_login_email(request):
	email = request.POST['email']
	token = Token.objects.create(email=email)
	url = request.build_absolute_uri(
		reverse('login') + '?token={uid}'.format(uid=str(token.uid))
	)
	message_body = 'Use this link to log in:\n\n{url}'.format(url=url)
	send_mail('Your login link for Wise Words', message_body, 'noreply@wisewords', [email], fail_silently=False)
	messages.success(request, "Check your email.  We've sent you a link to log in.")
	return redirect('/')

def login(request):
	user = auth.authenticate(uid=request.GET.get('token'))
	if user:
		auth.login(request, user)
	return redirect('/')

# def logout(request):
# 	auth.logout(request)
# 	return redirect('/')