from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView

from analytics.mixins import ObjectViewedMixin
from .forms import ContactForm
from carts.models import Cart
from products.models import Product
from analytics.models import ObjectViewed

class HomePage(ListView):
    template_name = "home_page.html"

    def get_context_data(self, *args, **kwargs):
        context = super(HomePage, self).get_context_data(*args, **kwargs)
        cart_obj, new_obj = Cart.objects.new_or_get(self.request)
        context['title'] = "Hello World!"
        context['content'] = "Welcome to the homepage."
        request = self.request
        if request.user.is_authenticated:
        	context['cart'] = cart_obj
        return context

    def get_queryset(self, *args, **kwargs):
        request = self.request
        if request.user.is_authenticated:
            views = self.request.user.objectviewed_set.by_model(Product)
            if views.exists():
                return views
            else:
                return
        return False
        

def about_page(request):
	context = {
		"title":"About Page",
		"content":"Welcome to the about.",
	}
	return render(request, "home_page.html", context)

def contact_page(request):
	contact_form = ContactForm(request.POST or None)
	context = {
		"title":"Contact Us",
		"form":contact_form,
	}
	if contact_form.is_valid():
		print(contact_form.cleaned_data)
		if request.is_ajax():
			return JsonResponse({"message": "Thank you. We'll be contacting you soon"})
	
	if contact_form.errors:
		errors = contact_form.errors.as_json()
		if request.is_ajax():
			return HttpResponse(errors, status=400, content_type='application/json')
	return render(request, "contact/view.html", context)