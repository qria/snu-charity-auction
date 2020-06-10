from datetime import datetime

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    """Custom user model with email auth and admin support"""

    # whether or not they are admin from this site
    # Not to be confused with `is_staff`, which indicates login capability of
    # the django-admin interface. Not sure we should remove one.
    is_admin = models.BooleanField(default=False)

    # email must be unique & non-null when used as a username
    email = models.EmailField(_('email address'), unique=True)

    USERNAME_FIELD = 'email'
    # email must not exist in required fields when used as username
    REQUIRED_FIELDS = ['username']


class Auction(models.Model):
    id = models.AutoField(primary_key=True)
    admin_id = models.ForeignKey(User, on_delete=models.PROTECT, related_name='admin_auction_set')
    name = models.CharField(max_length=255, null=False, blank=False)
    contents = models.TextField(null=False, blank=True)
    # images
    state = models.CharField(max_length=20, null=False, blank=False)
    start_datetime = models.DateTimeField(null=False, blank=False)
    end_datetime = models.DateTimeField(null=False, blank=False)
    min_bid = models.IntegerField(null=False)
    max_bid = models.IntegerField(null=False)
    winning_bid = models.IntegerField(null=True)
    winning_user_id = models.ForeignKey(User, on_delete=models.PROTECT, related_name='won_auction_set')
    created_datetime = models.DateTimeField(default=datetime.now, null=False, blank=False)
    updated_datetime = models.DateTimeField(default=datetime.now, null=False, blank=False)


class AuctionHistory(models.Model):
    id = models.AutoField(primary_key=True)
    auction = models.ForeignKey(Auction, on_delete=models.PROTECT)
    user_id = models.ForeignKey(User, on_delete=models.PROTECT)
    bid = models.IntegerField(null=False)
    is_valid = models.BooleanField(null=False)
    created_datetime = models.DateTimeField(default=datetime.now, null=False, blank=False)
