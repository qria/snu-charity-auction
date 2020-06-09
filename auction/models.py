from datetime import datetime

from django.db import models


class Auction(models.Model):
    id = models.AutoField(primary_key=True)
    # admin_id
    name = models.CharField(max_length=255, null=False, blank=False)
    contents = models.TextField(null=False, blank=True)
    # images
    state = models.CharField(max_length=20, null=False, blank=False)
    start_datetime = models.DateTimeField(null=False, blank=False)
    end_datetime = models.DateTimeField(null=False, blank=False)
    min_bid = models.IntegerField(null=False)
    max_bid = models.IntegerField(null=False)
    winning_bid = models.IntegerField(null=True)
    # winning_user_id
    created_datetime = models.DateTimeField(default=datetime.now, null=False, blank=False)
    updated_datetime = models.DateTimeField(default=datetime.now, null=False, blank=False)


class AuctionHistory(models.Model):
    id = models.AutoField(primary_key=True)
    auction = models.ForeignKey(Auction, on_delete=models.PROTECT)
    # user_id
    bid = models.IntegerField(null=False)
    is_valid = models.BooleanField(null=False)
    created_datetime = models.DateTimeField(default=datetime.now, null=False, blank=False)