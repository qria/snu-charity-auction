from django.http import HttpResponseRedirect
from django.shortcuts import render

from auction.models import Auction


def index(request):
    return render(request, 'index.html')


def create_auction_view(request):
    return render(request, 'create-auction.html')


def create_auction(request):
    name = request.POST['name']
    contents = request.POST['contents']
    start_datetime = request.POST['start-datetime']
    end_datetime = request.POST['end-datetime']
    min_bid = request.POST['min-bid']
    max_bid = request.POST['max-bid']

    auction = Auction(
        name=name,
        contents=contents,
        start_datetime=start_datetime,
        end_datetime=end_datetime,
        min_bid=min_bid,
        max_bid=max_bid
    )
    auction.save()

    return HttpResponseRedirect('/')
