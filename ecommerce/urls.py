"""ecommerce URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static

from django.urls import path, re_path, include
from django.contrib import admin
from django.contrib.auth.views import LogoutView
from django.views.generic import TemplateView, RedirectView

from accounts.views import LoginView, RegisterView, GuestRegisterView, LoginAndSecurityView
from addresses.views import (
    AddressCreateView,
    AddressListView,
    address_remove,
    AddressUpdateView,
    checkout_address_create_view,
    checkout_address_reuse_view,
    )
from analytics.views import SalesView
from billing.views import payment_method_view, payment_method_createview
from carts.views import cart_detail_api_view
from marketing.views import MarketingPreferenceUpdateView, MailchimpWebhookView
from orders.views import LibraryView
# from products.views import ProductByView

from .views import HomePage, about_page, contact_page
urlpatterns = [
    path('', HomePage.as_view(), name='home'),
    path('about/', about_page, name='about'),
    path('accounts/', RedirectView.as_view(url='/account')),
    path('account/', include("accounts.urls", namespace='account')),
    path('accounts/', include("accounts.passwords.urls")),
    path('address/', RedirectView.as_view(url='/addresses')),
    path('addresses/', AddressListView.as_view(), name='addresses'),
    path('addresses/create/', AddressCreateView.as_view(), name='address-create'),
    re_path(r'^addresses/(?P<pk>\d+)/$', AddressUpdateView.as_view(), name='address-update'),
    re_path(r'^addresses/remove/(?P<pk>\d+)/$', address_remove, name='address-remove'),
    path('analytics/sales/', SalesView.as_view(), name='sales-analytics'),
    path('api/cart/', cart_detail_api_view, name='api-cart'),
    path('billing/payment-method/', payment_method_view, name='billing-payment-method'),
    path('billing/payment-method/create/', payment_method_createview, name='billing-payment-method-endpoint'),
    path('cart/', include("carts.urls", namespace='cart')),
    path('checkout/address/create', checkout_address_create_view, name='checkout_address_create'),
    path('checkout/address/reuse', checkout_address_reuse_view, name='checkout_address_reuse'),
    path('contact/', contact_page, name='contact'),
    path('library/', LibraryView.as_view(), name='library'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('orders/', include("orders.urls", namespace='orders')),
    path('products/', include("products.urls", namespace='products')),
    # re_path(r'^product_by/(?P<product_by>\D+)/$', ProductByView.as_view(), name='product_by'),
    path('register/', RegisterView.as_view(), name='register'),
    path('register/guest/', GuestRegisterView.as_view(), name='guest_register'),
    path('search/', include("search.urls", namespace='search')),
    path('settings/', RedirectView.as_view(url='/account')),
    re_path(r'^settings/email/$', MarketingPreferenceUpdateView.as_view(), name='marketing-pref'),
    re_path(r'^webhooks/mailchimp/$', MailchimpWebhookView.as_view(), name='webhooks-mailchimp'),
    path('admin/', admin.site.urls),
]

if settings.DEBUG:
    urlpatterns = urlpatterns + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns = urlpatterns + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)