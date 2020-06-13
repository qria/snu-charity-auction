from django.http import HttpResponseRedirect
from django.shortcuts import render

from auction.models import Auction, User

from django.views.generic import TemplateView
from django.views.generic.edit import CreateView
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.urls import reverse_lazy
from django.utils import dateformat


def index(request):
    auctions = Auction.objects.all()
    context = {'auctions': auctions}
    return render(request, 'index.html', context=context)


class CreateUserForm(UserCreationForm): # 내장 회원가입 폼을 상속받아서 확장한다.
    email = forms.EmailField(required=True) # 이메일 필드 추가

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def save(self, commit=True): # 저장하는 부분 오버라이딩
        user = super(CreateUserForm, self).save(commit=False) # 본인의 부모를 호출해서 저장하겠다.
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user


class CreateUserView(CreateView): # generic view중에 CreateView를 상속받는다.
    template_name = 'join.html' # 템플릿은?
    form_class = CreateUserForm # 푸슨 폼 사용? >> 내장 회원가입 폼을 커스터마지징 한 것을 사용하는 경우
    # form_class = UserCreationForm >> 내장 회원가입 폼 사용하는 경우
    success_url = reverse_lazy('join_done')


class RegisteredView(TemplateView): # generic view중에 TemplateView를 상속받는다.
    template_name = 'join_done.html' # 템플릿은?


def create_auction_view(request):
    #if not request.user.is_admin:
     #   return render(request, 'no-authorization.html')

    return render(request, 'create-auction.html')


def create_auction(request):
    admin_id = request.user.id
    name = request.POST['name']
    contents = request.POST['contents']
    start_datetime = request.POST['start-datetime']
    end_datetime = request.POST['end-datetime']
    min_bid = request.POST['min-bid']
    max_bid = request.POST['max-bid']

    auction = Auction(
        admin_id=admin_id,
        name=name,
        contents=contents,
        start_datetime=start_datetime,
        end_datetime=end_datetime,
        min_bid=min_bid,
        max_bid=max_bid
    )
    auction.save()

    return HttpResponseRedirect('/')


def modify_auction_view(request, auction_id):
    if not request.user.is_admin:
        return render(request, 'no-authorization.html')

    auction = Auction.objects.get(id=auction_id)
    formatted_start_datetime = dateformat.format(auction.start_datetime, 'Y-m-d H:i:s')
    formatted_end_datetime = dateformat.format(auction.end_datetime, 'Y-m-d H:i:s')
    context = {'auction': auction, 'formatted_start_datetime': formatted_start_datetime,
               'formatted_end_datetime': formatted_end_datetime}
    return render(request, 'modify-auction.html', context=context)


def modify_auction(request):
    auction_id = request.POST['auction-id']
    name = request.POST['name']
    contents = request.POST['contents']
    start_datetime = request.POST['start-datetime']
    end_datetime = request.POST['end-datetime']
    min_bid = request.POST['min-bid']
    max_bid = request.POST['max-bid']

    auction = Auction.objects.get(id=auction_id)
    auction.name = name
    auction.contents = contents
    auction.start_datetime = start_datetime
    auction.end_datetime = end_datetime
    auction.min_bid = min_bid
    auction.max_bid = max_bid
    auction.save()

    return HttpResponseRedirect(f'/auction/detail/{auction_id}')
    
def delete_auction(request, auction_id):
    if not request.user.is_admin:
        return render(request, 'no-authorization.html')
        
    auction = Auction.objects.get(id=auction_id)
    auction.delete()
    return HttpResponseRedirect('/')
    


def auction_detail_view(request, auction_id):
    auction = Auction.objects.get(id=auction_id)
    formatted_start_datetime = dateformat.format(auction.start_datetime, 'Y-m-d H:i:s')
    formatted_end_datetime = dateformat.format(auction.end_datetime, 'Y-m-d H:i:s')
    context = {'auction': auction, 'formatted_start_datetime': formatted_start_datetime,
               'formatted_end_datetime': formatted_end_datetime}
    return render(request, 'auction-detail.html', context)
