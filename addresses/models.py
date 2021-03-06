from django.db import models
from django.urls import reverse

from billing.models import BillingProfile

# Create your models here.


# ADDRESS_TYPES = (
#     ('billing', 'Billing'),
#     ('shipping', 'Shipping'),
# )
class Address(models.Model):
    billing_profile = models.ForeignKey(BillingProfile, on_delete=models.CASCADE)
    address_type = models.CharField(max_length=120, default='Shipping')#choices=ADDRESS_TYPES)
    address_line_1 = models.CharField(max_length=120)
    address_line_2 = models.CharField(max_length=120, null=True, blank=True)
    city = models.CharField(max_length=120)
    postal_code = models.CharField(max_length=120)
    state = models.CharField(max_length=120)
    country = models.CharField(max_length=120, default='India')

    def __str__(self):
        return str(self.billing_profile)

    def get_absolute_url(self):
        return reverse("address-update", kwargs={"pk": self.pk})

    def remove_address(self):
        return reverse("address-remove", kwargs={"pk": self.pk})

    def get_address(self):
        return "{line1}\n{line2}\n{city}-{postal}\n{state}\n{country}".format(
                line1 = self.address_line_1,
                line2 = self.address_line_2 or "",
                city = self.city,
                postal = self.postal_code,
                state = self.state,
                country = self.country
            )
