from django.conf import settings
from django.core.validators import RegexValidator
from django.urls import reverse
from django.db import models
from django.db.models.signals import post_save, pre_save

from accounts.models import GuestUser
User = settings.AUTH_USER_MODEL
# Create your models here.

import stripe
STRIPE_SECRET_KEY = getattr(settings, "STRIPE_SECRET_KEY")
stripe.api_key = STRIPE_SECRET_KEY



class BillingProfileManager(models.Manager):
    def new_or_get(self, request):
        user = request.user
        created = False
        obj = None
        guest_email_id = request.session.get('guest_email_id')
        if user.is_authenticated:
            'logged in user checkout; remember payment stuff'
            obj, created = self.model.objects.get_or_create(user=user, email=user.email)

        elif guest_email_id is not None:
            'guest user checkout; auto reloads payment stuff'
            guest_user_obj = GuestUser.objects.get(id=guest_email_id)
            obj, created = self.model.objects.get_or_create(full_name=guest_user_obj.full_name, email=guest_user_obj.email, phone_number=guest_user_obj.phone_number)

        else:
            pass
        return obj, created

class BillingProfile(models.Model):
    user = models.OneToOneField(User, blank=True, null=True, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=255, null=True, blank=True)
    email = models.EmailField()
    phone_regex = RegexValidator(regex=r'^\+?1?\d{1,10}$', message="Phone number must be entered in the format: '+91 9999999999'. Up to 10 digits allowed.")
    phone_number = models.CharField(validators=[phone_regex], max_length=10, blank=True, null=True) # validators should be a list
    active = models.BooleanField(default=True)
    update = models.DateTimeField(auto_now=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    customer_id = models.CharField(max_length=150, null=True, blank=True)

    objects = BillingProfileManager()

    def __str__(self):
        return self.email

    def charge(self, order_obj, card=None):
        return Charge.objects.do(self, order_obj, card)

    def get_cards(self):
        return self.card_set.all()

    def get_payment_method_url(self):
        return reverse("billing-payment-method")

    @property
    def has_card(self): #instance.has_card
        card_qs = self.get_cards()
        return card_qs.exists() # True or False

    @property
    def default_card(self):
        default_cards = self.get_cards().filter(active=True, default=True)
        if default_cards.exists():
            return default_cards.first()
        return None
    
    def set_cards_inactive(self):
        card_qs = self.get_cards()
        card_qs.update(active=False)
        return card_qs.filter(active=True).count()

def billing_profile_created_receiver(sender, instance, *args, **kwargs):
    if not instance.customer_id and instance.email:
        print("ACTUAL API REQUEST: Send to stripe/braintree")
        customer = stripe.Customer.create(
                email = instance.email
            )
        instance.customer_id = customer.id

pre_save.connect(billing_profile_created_receiver, sender=BillingProfile)


def user_created_receiver(sender, instance, created, *args, **kwargs):
    if created and instance.email:
        BillingProfile.objects.get_or_create(user=instance, email=instance.email)

post_save.connect(user_created_receiver, sender=User)


#INDIAN TEST CARD - 4000 0035 6000 0008
class CardManager(models.Manager):
    def all(self, *args, **kwargs):
        return self.get_queryset().filter(active=True)
    def add_new(self, billing_profile, token):
        if token:
            card_response = stripe.Customer.create_source(
                billing_profile.customer_id,
                source=token,
            )
            new_card = self.model(
                    billing_profile = billing_profile,
                    stripe_id = card_response.id,
                    brand = card_response.brand,
                    country = card_response.country,
                    exp_month = card_response.exp_month,
                    exp_year = card_response.exp_year,
                    last4 = card_response.last4,
                )
            new_card.save()
            return new_card
        return None

class Card(models.Model):
    billing_profile = models.ForeignKey(BillingProfile, on_delete=models.CASCADE)
    stripe_id = models.CharField(max_length=150)
    brand = models.CharField(max_length=120, null=True, blank=True)
    country = models.CharField(max_length=20, null=True, blank=True)
    exp_month = models.IntegerField(null=True, blank=True)
    exp_year = models.IntegerField(null=True, blank=True)
    last4 = models.CharField(max_length=4, null=True, blank=True)
    default = models.BooleanField(default=True)
    active = models.BooleanField(default=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    objects = CardManager()

    def __str__(self):
        return f"{self.brand} {self.last4}"

def new_card_post_save_receiver(sender, instance, created, *args, **kwargs):
    if instance.default:
        billing_profile = instance.billing_profile
        qs = Card.objects.filter(billing_profile=billing_profile).exclude(pk=instance.pk)
        qs.update(default=False)

post_save.connect(new_card_post_save_receiver, sender=Card)

class ChargeManager(models.Manager):
    def do(self, billing_profile, order_obj, card=None):
        card_obj = card
        if card_obj is None:
            cards = billing_profile.card_set.filter(default=True)
            if cards.exists():
                card_obj = cards.first()
        if card_obj is None:
            return False, "No card available!"

        charge = stripe.Charge.create(
            amount=int(order_obj.total * 100),
            currency="inr",
            customer = billing_profile.customer_id,
            source=card_obj.stripe_id,
            metadata={"order_id": order_obj.order_id},
        )
        new_charge_obj = self.model(
                billing_profile = billing_profile,
                stripe_id = charge.id,
                paid = charge.paid,
                refunded = charge.refunded,
                outcome = charge.outcome,
                outcome_type = charge.outcome['type'],
                seller_message = charge.outcome.get('seller_message'),
                risk_level = charge.outcome.get('risk_level'),
            )
        new_charge_obj.save()
        return new_charge_obj.paid, new_charge_obj.seller_message


class Charge(models.Model):
    billing_profile = models.ForeignKey(BillingProfile, on_delete=models.CASCADE)
    stripe_id = models.CharField(max_length=150)
    paid = models.BooleanField(default=False)
    refunded = models.BooleanField(default=False)
    outcome = models.TextField(null=True, blank=True)
    outcome_type = models.CharField(max_length=150, null=True, blank=True)
    seller_message = models.CharField(max_length=150, null=True, blank=True)
    risk_level = models.CharField(max_length=150, null=True, blank=True)

    objects = ChargeManager()
