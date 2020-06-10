from django.urls import path
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout', auth_views.LogoutView.as_view(next_page='/'), name='logout'),


    # temp
    path('auction/create', views.create_auction_view),
    path('api/auction', views.create_auction),
    path('item/detail', views.item_detail_view)
]