from django.contrib.auth.models import User
from django.db import models

# Create your models here.
class Link(models.Model):
    slug = models.SlugField(db_index=True, unique=True)
    # Using 2048 for max_length because its a url shortener
    # and 2048 seems to be a commonly cited maximum length for URLS
    # in a few common applications.
    url = models.URLField(max_length=2048)
    created_at = models.DateTimeField(auto_now_add=True)
    click_count = models.IntegerField(default=0)