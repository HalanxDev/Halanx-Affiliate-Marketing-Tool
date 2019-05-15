from django.conf import settings
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from common.models import AddressDetail
from utility.random_utils import generate_random_code


class AffiliateOccupationCategory(models.Model):
    name = models.CharField(max_length=500, blank=True, null=True)

    def __str__(self):
        return self.name


class AffiliateOrganisationTypeCategory(models.Model):
    name = models.CharField(max_length=500, blank=True, null=True)

    def __str__(self):
        return self.name


class Affiliate(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='affiliate')
    phone_no = models.CharField(max_length=15, blank=True, null=True)
    occupation = models.ForeignKey('AffiliateOccupationCategory', blank=True, null=True, on_delete=models.SET_NULL,
                                   related_name='affiliates')
    unique_code = models.CharField(max_length=100, blank=True, null=True)
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


class AffiliateOrganisation(models.Model):
    affiliate = models.OneToOneField('Affiliate', on_delete=models.CASCADE, related_name='organisation')
    type = models.ForeignKey('AffiliateOrganisationTypeCategory', blank=True, null=True, on_delete=models.SET_NULL,
                             related_name='organisations')
    name = models.CharField(max_length=255, blank=True, null=True)
    website = models.CharField(max_length=500, blank=True, null=True)

    def __str__(self):
        return str(self.name)


class AffiliateAddress(AddressDetail):
    affiliate = models.OneToOneField('Affiliate', on_delete=models.CASCADE, related_name='address')


class AffiliateOrganisationAddress(AddressDetail):
    organisation = models.OneToOneField('AffiliateOrganisation', on_delete=models.CASCADE, related_name='address')


class OTP(models.Model):
    phone_no = models.CharField(max_length=30)
    password = models.IntegerField(null=True, blank=True)
    timestamp = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.id)


# noinspection PyUnusedLocal
@receiver(post_save, sender=Affiliate)
def affiliate_post_save_hook(sender, instance, created, **kwargs):
    if created:
        AffiliateOrganisation(affiliate=instance).save()
        AffiliateAddress(affiliate=instance).save()
        super(Affiliate, instance).save()


# noinspection PyUnusedLocal
@receiver(post_save, sender=AffiliateOrganisation)
def organisation_post_save_hook(sender, instance, created, **kwargs):
    if created:
        AffiliateOrganisationAddress(organisation=instance).save()
        super(AffiliateOrganisation, instance).save()
