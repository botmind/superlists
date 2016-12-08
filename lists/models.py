from django.db import models
from django.core.urlresolvers import reverse

# Create your models here.
class Author(models.Model):
	
	def get_absolute_url(self):
		return reverse('view_quote', args=[self.id])

class Quote(models.Model):
	text = models.TextField(default='')
	author = models.ForeignKey(Author, default=None)

	def __str__(self):
		return self.text

	class Meta:
		ordering = ('id',)
		unique_together = ('author', 'text')

