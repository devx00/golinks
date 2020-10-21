from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import models, transaction
from django.http.response import Http404
from django.urls import resolve, get_resolver
from django.utils.translation import gettext_lazy as _

slug_blacklist = [ "auth", "home", "links", "users" ]

def slug_validator(slug):
    """Make sure slug doesnt match any existing paths."""
    # This is really not ideal. But it is the easiest way I have found 
    # to dynamically check for a conflict.
    if slug.lower() in slug_blacklist:
        raise ValidationError(
            _('Slug \'%(slug)s\' conflicts with existing path.'),
            params={'slug': slug},
        )


class Link(models.Model):
    slug = models.SlugField(db_index=True, unique=True, validators=[slug_validator])
    # Using 2048 for max_length because its a url shortener
    # and 2048 seems to be a commonly cited maximum length for URLS
    # in a few common applications.
    url = models.URLField(max_length=2048)
    created_at = models.DateTimeField(auto_now_add=True)
    click_count = models.IntegerField(default=0)
    owner = models.ForeignKey('auth.User', related_name='links', on_delete=models.CASCADE, null=True, default=None)

    @transaction.atomic
    def increment_clicks(self, count=1):
        self.click_count += count
        self.save()
    
