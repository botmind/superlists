import re
from django.core import mail

from .base import FunctionalTest

TEST_EMAIL = 'monkey@fatcat.org'
SUBJECT = 'Your login link for Wise Words'

class LoginTest(FunctionalTest):

	def test_can_get_email_link_to_log_in(self):
		#visit site and enter email to login
		self.browser.get(self.server_url)
		self.browser.find_element_by_name('email').send_keys(TEST_EMAIL + '\n')

		#message is displayed, saying than email has been sent
		body = self.browser.find_element_by_tag_name('body')
		self.assertIn('Check your email', body.text)

		#user checks email and finds login message
		email = mail.outbox[0]
		self.assertIn(TEST_EMAIL, email.to)
		self.assertEqual(email.subject, SUBJECT)

		#the email contains a url
		self.assertIn('Use this link to log in', email.body)
		url_search = re.search(r'http://.+/.+$', email.body)
		if not url_search:
			self.fail('Could not find url in email body:\n{}'.format(email.body))
		url = url_search.group(0)
		self.assertIn(self.server_url, url)

		#user clicks the url
		self.browser.get(url)

		#user is logged in
		self.assert_logged_in(email=TEST_EMAIL)

		#now user logs out
		self.browser.find_element_by_link_text('Log out').click()

		#user is logged out
		self.assert_logged_out(email=TEST_EMAIL)