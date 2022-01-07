from django.contrib.auth import authenticate, login, get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.views.generic import CreateView, FormView, DetailView, View, UpdateView
from django.views.generic.edit import FormMixin
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.utils.http import is_safe_url
from django.utils.safestring import mark_safe

from ecommerce.mixins import NextUrlMixin, RequestFormAttachMixin
from .forms import LoginForm, RegisterForm, GuestForm, ReactivateEmailForm, UserNameChangeForm, UserPhoneNumberChangeForm
from .models import GuestUser, EmailActivation
from .signals import user_logged_in

# @login_required
# def account_home_view(request):
#     return render(request, "accounts/home.html", {})


class AccountHomeView(LoginRequiredMixin ,DetailView):
    template_name = 'accounts/home.html'
    
    def get_object(self):
        return self.request.user

class LoginAndSecurityView(LoginRequiredMixin ,DetailView):
    template_name = 'login_&_security.html'

    def get_object(self):
        return HttpResponseRedirect(reverse('account:login-security'))


class AccountEmailActivateView(FormMixin, View):
    success_url = '/login/'
    form_class = ReactivateEmailForm
    key = None
    def get(self, request, key=None, *args, **kwargs):
        self.key = key
        if key is not None:
            qs = EmailActivation.objects.filter(key__iexact=key)
            confirm_qs = qs.confirmable()
            if confirm_qs.count()==1:
                obj = confirm_qs.first()
                obj.activate()
                messages.success(request, "Your account has been activated. Please login.")
                return redirect("login")
            else:
                activated_qs = qs.filter(activated=True)
                if activated_qs.exists():
                    reset_link = reverse("password_reset")
                    msg = """Your email has already been confirmed.
                    Click <a href="{link}">here</a> if you forgot your password and want to reset it
                    """.format(link=reset_link)
                    messages.info(request, mark_safe(msg))
                    return redirect("login")
        context = {'form': self.get_form(), 'key':key}
        return render(request, 'registration/activation-error.html', context)

    def post(self, request, *args, **kwargs):
        #create a form to receive an email
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        msg = """Activation link sent, please check your email."""
        request = self.request
        messages.success(request, msg)
        email = form.cleaned_data.get('email')
        obj = EmailActivation.objects.email_exists(email).first()
        user = obj.user
        new_activation = EmailActivation.objects.create(user=user, email=email)
        new_activation.send_activation()
        return super(AccountEmailActivateView, self).form_valid(form)

    def form_invalid(self, form):
        context = {'form': form, 'key': self.key}
        return render(self.request, 'registration/activation-error.html', context)

class GuestRegisterView(NextUrlMixin, RequestFormAttachMixin, CreateView):
    form_class = GuestForm
    default_next = '/register/'

    def get_success_url(self):
        return self.get_next_url()

    def form_invalid(self, form):
        return redirect(self.default_next)

class LoginView(NextUrlMixin, RequestFormAttachMixin, FormView):
    form_class = LoginForm
    success_url = '/'
    template_name = 'accounts/login.html'
    default_next = '/'

    def form_valid(self, form):
        next_path = self.get_next_url()
        return redirect(next_path)

class RegisterView(RequestFormAttachMixin, CreateView):
    form_class = RegisterForm
    template_name = 'accounts/register.html'
    success_url="/login/"

class UserNameUpdateView(LoginRequiredMixin, UpdateView):
    form_class = UserNameChangeForm
    template_name = "accounts/detail-update-view.html"

    def get_object(self):
        return self.request.user

    def get_context_data(self, *args, **kwargs):
        context = super(UserNameUpdateView, self).get_context_data(*args, **kwargs)
        context['title'] = "Change Your Name"
        return context

    def get_success_url(self):
        return reverse("account:home")

class UserPhoneNumberUpdateView(LoginRequiredMixin, UpdateView):
    form_class = UserPhoneNumberChangeForm
    template_name = "accounts/detail-update-view.html"

    def get_object(self):
        return self.request.user

    def get_context_data(self, *args, **kwargs):
        context = super(UserPhoneNumberUpdateView, self).get_context_data(*args, **kwargs)
        context['title'] = "Change Your Phone Number"
        return context

    def get_success_url(self):
        return reverse("account:home")
