from datetime import timedelta
from django.conf import settings
from django.contrib.auth.models import (
    AbstractBaseUser, BaseUserManager
)

from django.core.mail import send_mail
from django.core.validators import RegexValidator
from django.db import models
from django.db.models import Q
from django.db.models.signals import pre_save, post_save
from django.template.loader import get_template
from django.urls import reverse
from django.utils import timezone

from ecommerce.utils import random_string_generator, unique_key_generator


DEFAULT_ACTIVATION_DAYS = getattr(settings, 'DEFAULT_ACTIVATION_DAYS', 7)

#Custom User Manager
class UserManager(BaseUserManager):
    def create_user(self, email, full_name=None, password=None, phone_number=None, is_active=True, is_staff=False, is_admin=False):
        if not email:
            raise ValueError("Users must have an email address!")
        if not password:
            raise ValueError("Users must have a password!!")

        user_obj = self.model(
            email = self.normalize_email(email),
            full_name = full_name,
            phone_number = phone_number
        )
        user_obj.set_password(password) #change user password too
        user_obj.staff = is_staff
        user_obj.admin = is_admin
        user_obj.is_active = is_active
        user_obj.save(using=self._db)
        return user_obj

    def create_staffuser(self, email, full_name=None, phone_number=None, password=None):
        user = self.create_user(
            email,
            full_name = full_name,
            phone_number = phone_number,
            password = password,
            is_staff = True
        )
        return user

    def create_superuser(self, email, full_name=None, phone_number=None, password=None):
        user = self.create_user(
            email,
            full_name = full_name,
            phone_number = phone_number,
            password = password,
            is_staff = True,
            is_admin = True
        )
        return user

#Custom User class
class User(AbstractBaseUser):
    email = models.EmailField(max_length=255, unique=True)
    full_name = models.CharField(max_length=255)
    phone_regex = RegexValidator(regex=r'^\+?1?\d{1,10}$', message="Phone number must be entered in the format: '+91 9999999999'. Up to 10 digits allowed.")
    phone_number = models.CharField(validators=[phone_regex], max_length=10) # validators should be a list
    is_active = models.BooleanField(default=True) #can login
    staff = models.BooleanField(default=False) #staff user non superuser
    admin = models.BooleanField(default=False) #superuser
    timestamp = models.DateTimeField(auto_now_add=True)
    #confirm_email = models.BooleanField(default=False)
    #confirm_date = models.DateTimeField(default=False)

    USERNAME_FIELD = 'email'    #no longer using username
    #USERNAME_FIELD and password are required by default
    REQUIRED_FIELDS = ['full_name', 'phone_number']

    objects = UserManager()
    
    def __str__(self):
        return self.email
    
    def get_full_name(self):
        if self.full_name:
            return self.full_name
        return self.email
    
    def get_short_name(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        if self.is_admin:
            return True
        return self.staff
    
    @property
    def is_admin(self):
        return self.admin

    # @property
    # def is_active(self):
    #     return self.active

class EmailActivationQuerySet(models.query.QuerySet):
    def confirmable(self):
        now = timezone.now()
        start_range = now - timedelta(days=DEFAULT_ACTIVATION_DAYS)
        #does my object have a timestamp in here
        end_range = now
        return self.filter(
                activated = False,
                forced_expired = False
            ).filter(
                timestamp__gt=start_range,
                timestamp__lte=end_range
            )


class EmailActivationManager(models.Manager):
    def get_queryset(self):
        return EmailActivationQuerySet(self.model, using=self._db)

    def confirmable(self):
        return self.get_queryset().confirmable()

    def email_exists(self, email):
        return self.get_queryset().filter(Q(email=email) | Q(user__email=email)).filter(activated=False)

class EmailActivation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    email = models.EmailField()
    key = models.CharField(max_length=120, null=True, blank=True)
    activated = models.BooleanField(default=False)
    forced_expired = models.BooleanField(default=False)
    expires = models.IntegerField(default=7)# 7 Days
    timestamp = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)

    objects = EmailActivationManager()

    def __str__(self):
        return self.email

    def can_activate(self):
        qs = EmailActivation.objects.filter(pk=self.pk).confirmable() #only return 1 object
        if qs.exists():
            return True
        return False

    def activate(self):
        if self.can_activate():
            user = self.user
            user.is_active = True
            user.save()
            self.activated = True
            self.save()
            return True
        return False


    def regenerate(self):
        self.key = None
        self.save()
        if self.key is not None:
            return True
        return False

    def send_activation(self):
        if not self.activated and not self.forced_expired:
            if self.key:
                base_url = getattr(settings, 'BASE_URL', 'https://eshoppers.herokuapp.com')
                key_path = reverse("account:email-activate", kwargs={'key': self.key}) # change this to use reverse
                path = "{base}{path}".format(base=base_url, path=key_path)
                context = {
                    'path': path,
                    'email': self.email
                }
                
                txt_ = get_template("registration/emails/verify.txt").render(context)
                html_ = get_template("registration/emails/verify.html").render(context)
                subject = "Email Verification"
                from_email = settings.DEFAULT_FROM_EMAIL
                recipient_list = [self.email]
                sent_mail = send_mail(
                            subject,
                            txt_,
                            from_email,
                            recipient_list,
                            html_message=html_,
                            fail_silently=False,
                    )
                return sent_mail
        return False

def pre_save_email_activation(sender, instance, *args, **kwargs):
    if not instance.activated and not instance.forced_expired:
        if not instance.key:
            instance.key = unique_key_generator(instance)

pre_save.connect(pre_save_email_activation, sender=EmailActivation)

#Sending activation mails through post save signal
def post_save_user_create_receiver(sender, instance, created, *args, **kwargs):
    if created:
        obj = EmailActivation.objects.create(user=instance, email=instance.email)
        obj.send_activation()

post_save.connect(post_save_user_create_receiver, sender=User)

class GuestUser(models.Model):
    full_name = models.CharField(max_length=255)
    email = models.EmailField()
    phone_regex = RegexValidator(regex=r'^\+?1?\d{1,10}$', message="Phone number must be entered in the format: '+91 9999999999'. Up to 10 digits allowed.")
    phone_number = models.CharField(validators=[phone_regex], max_length=10) # validators should be a list
    active = models.BooleanField(default=True)
    update = models.DateTimeField(auto_now=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email