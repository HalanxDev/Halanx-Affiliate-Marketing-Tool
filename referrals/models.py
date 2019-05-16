from django.db import models

from referrals.utils import GenderChoices, HouseAccomodationAllowedCategories, HouseAccomodationTypeCategories, \
    ReferralStatusChoices, PENDING, ReferralSourceChoices


class Referral(models.Model):
    name = models.CharField(max_length=500, blank=True, null=True)
    phone_no = models.CharField(max_length=20, blank=True, null=True)
    gender = models.CharField(max_length=20, choices=GenderChoices, blank=True, null=True)
    email = models.CharField(max_length=500, blank=True, null=True)
    timestamp = models.DateTimeField(auto_created=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=50, choices=ReferralStatusChoices, default=PENDING)
    source = models.CharField(max_length=500, choices=ReferralSourceChoices, blank=True, null=True)

    class Meta:
        abstract = True

    def __str__(self):
        return self.name


class TenantReferral(Referral):
    affiliate = models.ForeignKey('affiliates.Affiliate', blank=True, null=True, on_delete=models.SET_NULL,
                                  related_name='tenant_referrals')
    preferred_location = models.TextField(blank=True, null=True)
    expected_rent = models.FloatField(default=0)
    expected_movein_date = models.DateField(blank=True, null=True)
    accomodation_for = models.CharField(max_length=25, choices=HouseAccomodationAllowedCategories,
                                        blank=True, null=True)
    accomodation_type = models.CharField(max_length=20, choices=HouseAccomodationTypeCategories)


class HouseOwnerReferral(Referral):
    affiliate = models.ForeignKey('affiliates.Affiliate', blank=True, null=True, on_delete=models.SET_NULL,
                                  related_name='house_owner_referrals')
    house_address = models.TextField(blank=True, null=True)
    bhk_count = models.PositiveIntegerField(default=1, blank=True, null=True)
