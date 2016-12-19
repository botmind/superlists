from django.test import TestCase
from unittest.mock import call, patch
import accounts #in order to override the send_mail function in accounts with a monkeypatched version
from accounts.models import Token

class SendLoginEmailViewTest(TestCase):

	def test_redirects_to_home_page(self):
		response = self.client.post('/accounts/send_login_email', data={'email': 'monkey@fatcat.org'})
		self.assertRedirects(response, '/')

	def test_creates_token_associated_with_email(self):
		self.client.post('/accounts/send_login_email', data={'email': 'monkey@fatcat.org'})
		token = Token.objects.first()
		self.assertEqual(token.email, 'monkey@fatcat.org')

	@patch('accounts.views.send_mail')
	def test_sends_link_to_login_using_token_uid(self, mock_send_mail):
		self.client.post('/accounts/send_login_email', data={'email': 'monkey@fatcat.org'})

		token = Token.objects.first()
		expected_url = 'http://testserver/accounts/login?token={uid}'.format(uid=token.uid)
		(subject, body, from_email, to_list), kwargs = mock_send_mail.call_args
		self.assertIn(expected_url, body)

	@patch('accounts.views.send_mail')
	def test_sends_mail_to_address_from_post(self, mock_send_mail):
		self.client.post('/accounts/send_login_email', data={'email': 'monkey@fatcat.org'})

		self.assertTrue(mock_send_mail.called) #check that the function was in fact called
		(subject, body, from_email, to_list), kwargs = mock_send_mail.call_args #gets all the arguments passed through to send_mail
		self.assertEqual(subject, 'Your login link for Wise Words')
		self.assertEqual(from_email, 'noreply@wisewords')
		self.assertEqual(to_list, ['monkey@fatcat.org'])

	def test_adds_success_message(self):
		response = self.client.post('/accounts/send_login_email', data={'email': 'monkey@fatcat.org'}, follow=True)

		message = list(response.context['messages'])[0] #must listify the messages context
		self.assertEqual(message.message, "Check your email.  We've sent you a link to log in.")
		self.assertEqual(message.tags, "success")

@patch('accounts.views.auth')
class LoginViewTest(TestCase):

	def test_redirects_to_home_page(self, mock_auth):
		response = self.client.get('/accounts/login?token=abcd123')
		self.assertRedirects(response, '/')

	def test_calls_auth_login_with_user_if_there_is_one(self, mock_auth):
		response = self.client.get('/accounts/login?token=abcd123')
		self.assertEqual(mock_auth.login.call_args, call(response.wsgi_request, mock_auth.authenticate.return_value))

	
	def test_calls_authenticate_with_uid_from_get_request(self, mock_auth):
		self.client.get('/accounts/login?token=abcd123')
		self.assertEqual(mock_auth.authenticate.call_args, call(uid='abcd123'))

	def test_does_not_login_if_user_is_not_authenticated(self, mock_auth):
		mock_auth.authenticate.return_value = None
		self.client.get('/accounts/login?token=abcd123')
		self.assertEqual(mock_auth.login.called, False)		




