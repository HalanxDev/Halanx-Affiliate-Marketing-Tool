from django.conf import settings
from django.db import models

from affiliates.utils import ORGANISATION_TYPE_CATEGORIES, AFFILIATE_OCCUPATION_CATEGORIES
from utility.random_utils import generate_random_code


class Organisation(models.Model):
    type = models.CharField(max_length=255, choices=ORGANISATION_TYPE_CATEGORIES, blank=True, null=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    address = models.TextField()

    def __str__(self):
        return self.name


class Affiliate(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='affiliate')
    phone_no = models.CharField(max_length=15, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    occupation = models.CharField(max_length=100, choices=AFFILIATE_OCCUPATION_CATEGORIES, blank=True, null=True)
    organisation = models.ForeignKey('Organisation', blank=True, null=True, on_delete=models.SET_NULL,
                                     related_name='affiliates')
    unique_code = models.TextField(max_length=100, blank=True, null=True)
    active = models.BooleanField(default=True)
    verified = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    # noinspection PyUnresolvedReferences
    def save(self, *args, **kwargs):
        if not self.pk:
            existing_codes = Affiliate.objects.values_list('unique_code', flat=True)
            self.unique_code = generate_random_code(initials=self.user.first_name.lower(), n=3,
                                                    existing_codes=existing_codes)
        super(Affiliate, self).save(*args, **kwargs)

    # noinspection PyUnresolvedReferences
    @property
    def name(self):
        return self.user.get_full_name()


class OTP(models.Model):
    phone_no = models.CharField(max_length=30)
    password = models.IntegerField(null=True, blank=True)
    timestamp = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.id)
