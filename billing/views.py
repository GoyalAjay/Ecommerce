from django.conf import settings
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect
from django.utils.http import is_safe_url
from .models import BillingProfile, Card
import stripe


STRIPE_SECRET_KEY = getattr(settings, "STRIPE_SECRET_KEY", "sk_test_51HI8gRIEBArkPqGJIk1s959NCXVDOnfZGEEjwxlrbjKXmAVrNPAC7F6KgTvVKPmfzdcigjsMvxPeoaHoDtzyNeBI00vjqLP3nZ")
STRIPE_PUB_KEY = getattr(settings, "STRIPE_PUB_KEY", "pk_test_51HI8gRIEBArkPqGJIBLnImqYPJPOmVAE1sBrqsjydTRv68E7GUv5YktcFMKakoKdtP3EFMbQuCKSlKUJiuexC7vH004bebxOR3")
stripe.api_key = STRIPE_SECRET_KEY

def payment_method_view(request):
    billing_profile, billing_profile_created = BillingProfile.objects.new_or_get(request)
    if not billing_profile:
        return redirect('/cart')

    next_url=None
    next_ = request.GET.get('next')
    if is_safe_url(next_, request.get_host()):
        next_url = next_
    return render(request, 'billing/payment-method.html', {"publish_key": STRIPE_PUB_KEY, "next_url": next_url})


def payment_method_createview(request):
    if request.method == 'POST' and request.is_ajax():
        billing_profile, billing_profile_created = BillingProfile.objects.new_or_get(request)
        if not billing_profile:
            return HttpResponse({"message": "Cannot find this user"}, status_code=401)

        token = request.POST.get("token")
        if token is not None:
            new_card_obj = Card.objects.add_new(billing_profile, token)
        return JsonResponse({"message": "Success! Your card has been added."})
    return HttpResponse("error", status_code=401)
