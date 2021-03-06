from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.views.generic import TemplateView
from django.shortcuts import render

# Create your views here.

class SalesView(LoginRequiredMixin, TemplateView):
    template_name = "analytics/sales.html"

    def dispatch(self, *args, **kwargs):
        user = self.request.user
        if user.is_authenticated and not user.is_staff:
            return render(self.request, '401.html', {"username": user.full_name, "email": user.email})
        elif not user.is_authenticated:
            return render(self.request, '401.html', {})
        return super(SalesView, self).dispatch(*args, **kwargs)

    def get_context_data(self, *args, **kwargs):
        return super(SalesView, self).get_context_data(*args, **kwargs)