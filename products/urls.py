from django.urls import path, re_path

from .views import (
        ProductByView,
        ProductListView,
        ProductDetailSlugView,
        ProductDownloadView,
        )

app_name = 'products'
urlpatterns = [
    path('', ProductListView.as_view(), name='list'),	#cbv means class based views. Look in views.py
    re_path(r'^product_by/(?P<product_by>\D+)/$', ProductByView.as_view(), name='product_by'),
    re_path(r'^(?P<slug>[\w-]+)/$', ProductDetailSlugView.as_view(), name='detail'),
    re_path(r'^(?P<slug>[\w-]+)/(?P<pk>\d+)/$', ProductDownloadView.as_view(), name='download'),
]