from django.urls import path, re_path

from products.views import UserProductHistoryView

from analytics.models import ObjectViewed

from .views import (
        AccountHomeView,
        AccountEmailActivateView,
        LoginAndSecurityView,
        UserNameUpdateView,
        UserPhoneNumberUpdateView
        )

app_name = 'carts'
urlpatterns = [
    path('', AccountHomeView.as_view(), name='home'),   #cbv means class based views. Look in views.py
    path('email/resend-activation/', AccountEmailActivateView.as_view(), name='resend-activation'),
    re_path(r'^email/confirm/(?P<key>[0-9A-Za-z]+)/$', AccountEmailActivateView.as_view(), name='email-activate'),
    path('login-security/', LoginAndSecurityView.as_view(), name='login-security'),
    path('login-security/update-name/', UserNameUpdateView.as_view(), name='update-name'),
    path('login-security/update-phone-number/', UserPhoneNumberUpdateView.as_view(), name='update-phone-number'),
    path('history/products/', UserProductHistoryView.as_view(), name='history-products'),
]