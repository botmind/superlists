from django.db import models
import uuid
from django.contrib import auth

auth.signals.user_logged_in.disconnect(auth.models.update_last_login) #updates the last_login property; without this, django errors out that this field does not exist.

class User(models.Model):
	email = models.EmailField(primary_key=True)
	REQUIRED_FIELDS = ()
	USERNAME_FIELD = 'email'

	is_anonymous = False
	is_authenticated = True

class Token(models.Model):
	email = models.EmailField()
	uid = models.CharField(default=uuid.uuid4, max_length=40)