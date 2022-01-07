from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.views.generic import ListView, DetailView, View
from django.shortcuts import render, redirect, get_object_or_404

from analytics.mixins import ObjectViewedMixin

from analytics.models import ObjectViewed
from carts.models import Cart
from .models import Product, ProductFile
from orders.models import ProductPurchase

# Create your views here.

class ProductFeaturedListView(ListView):
    template_name = "products/product_list.html"
    
    def get_queryset(self, *args, **kwargs):
        request = self.request
        return Product.objects.all().featured()


class ProductFeaturedDetailView(ObjectViewedMixin, DetailView):
    queryset = Product.objects.all().featured()
    template_name = "products/featured-detail.html"

    # def get_queryset(self, *args, **kwargs):
    #     request = self.request
    #     return Product.objects.featured()

class UserProductHistoryView(LoginRequiredMixin, ListView):
    template_name = "products/user-product-history.html"

    def get_context_data(self, *args, **kwargs):
        context = super(UserProductHistoryView, self).get_context_data(*args, **kwargs)
        cart_obj, new_obj = Cart.objects.new_or_get(self.request)
        context['cart'] = cart_obj
        return context

    def get_queryset(self, *args, **kwargs):
        request = self.request
        views = request.user.objectviewed_set.by_model(Product)
        if views.exists():
            return views
        else:
            return


class ProductListView(ListView):
	# queryset = Product.objects.all()
    template_name = "products/product_list.html"

	# def get_context_data(self, *args, **kwargs):
	# 	context = super(ProductListView, self).get_context_data(*args, **kwargs)
	# 	print(context)
	# 	return context
    def get_context_data(self, *args, **kwargs):
        context = super(ProductListView, self).get_context_data(*args, **kwargs)
        cart_obj, new_obj = Cart.objects.new_or_get(self.request)
        context['cart'] = cart_obj
        return context

    def get_queryset(self, *args, **kwargs):
        request = self.request
        return Product.objects.all()

class ProductByView(ListView):
    # queryset = Product.objects.all()
    template_name = "products/list.html"

    def get_context_data(self, *args, **kwargs):
        context = super(ProductByView, self).get_context_data(*args, **kwargs)
        cart_obj, new_obj = Cart.objects.new_or_get(self.request)
        context['cart'] = cart_obj
        return context

    def get_queryset(self, *args, **kwargs):
        request = self.request
        product_by = self.kwargs.get('product_by')
        return Product.objects.all().search(product_by)


class ProductDetailSlugView(ObjectViewedMixin, DetailView):
    queryset = Product.objects.all()
    template_name = "products/detail.html"

    def get_context_data(self, *args, **kwargs):
        context = super(ProductDetailSlugView, self).get_context_data(*args, **kwargs)
        cart_obj, new_obj = Cart.objects.new_or_get(self.request)
        context['cart'] = cart_obj
        return context

    def get_object(self, *args, **kwargs):
        request = self.request
        slug = self.kwargs.get('slug')
        #instance = get_object_or_404(Product, slug=slug, active=True)
        try:
            instance = Product.objects.get(slug=slug, active=True)
        except Product.DoesNotExist: 
            raise Http404("Not found..")
        except Product.MultipleObjectsReturned:
            qs = Product.objects.filter(slug=slug, active=True)
            instance = qs.first()
        except Product.DoesNotExist:
            raise Http404("Uhhmmm")
        return instance

import os
from django.conf import settings
from mimetypes import guess_type
from wsgiref.util import FileWrapper

class ProductDownloadView(View):
    def get(self, request, *args, **kwargs):
        slug = kwargs.get("slug")
        pk = kwargs.get("pk")
        downloads_qs = ProductFile.objects.filter(pk=pk, product__slug=slug)
        if downloads_qs.count() != 1:
            raise Http404("Download not found")
        download_obj = downloads_qs.first()
        
        #permission checks
        can_download = False
        user_ready = True
        if download_obj.user_required:
            if not request.user.is_authenticated:
                user_ready=False

        purchased_products = ProductPurchase.objects.none()
        if download_obj.free:
            can_download = True
        else:
            #not free
            purchased_products = ProductPurchase.objects.products_by_request(request)
            if download_obj.product in purchased_products:
                can_download = True
                user_ready = True

        if not can_download or not user_ready:
            messages.error(request, "You must purchase the item first to download")
            return redirect(download_obj.get_default_url())

        aws_filepath = download_obj.generate_download_url()
        return HttpResponseRedirect(aws_filepath)

        #When not using AWS use the below code and comment the AWS part above
        # file_root = settings.PROTECTED_ROOT
        # filepath = download_obj.file.path
        # final_filepath = os.path.join(file_root, filepath)  #where the file is stored
        # with open(final_filepath, 'rb') as f:
        #     wrapper = FileWrapper(f)
        #     mimetype = 'application/force-download'
        #     guessed_mimetype = guess_type(filepath)[0]  #basically looking for extention of the file
        #     if guessed_mimetype:
        #         mimetype = guessed_mimetype
        #     response = HttpResponse(wrapper, content_type=mimetype)
        #     response['Content-Disposition'] = "attachment;filename=%s" %(download_obj.name)
        #     response['X-SendFile'] = str(download_obj.name)
        # return response
    #return redirect(download_obj.get_default_url())    #will fix it later