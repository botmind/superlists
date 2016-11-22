from django.db import models

# Create your models here.
class Author(models.Model):
	pass

class Quote(models.Model):
	text = models.TextField(default='')
	author = models.ForeignKey(Author, default=None)

