from datetime import datetime

from dateutil.relativedelta import relativedelta
from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils import timezone

from affiliates.models import AffiliateMonthlyReport
from referrals.utils import GenderChoices, HouseAccomodationAllowedCategories, HouseAccomodationTypeCategories, \
    ReferralStatusChoices, PENDING, ReferralSourceChoices, HouseTypeCategories, SUCCESS


class Referral(models.Model):
    name = models.CharField(max_length=500, blank=True, null=True)
    phone_no = models.CharField(max_length=20, blank=True, null=True)
    gender = models.CharField(max_length=20, choices=GenderChoices, blank=True, null=True)
    email = models.CharField(max_length=500, blank=True, null=True)
    status = models.CharField(max_length=50, choices=ReferralStatusChoices, default=PENDING)
    source = models.CharField(max_length=500, choices=ReferralSourceChoices, blank=True, null=True)

    timestamp = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    converted_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        abstract = True

    def __str__(self):
        return self.name


class TenantReferral(Referral):
    affiliate = models.ForeignKey('affiliates.Affiliate', blank=True, null=True, on_delete=models.SET_NULL,
                                  related_name='tenant_referrals')
    preferred_location = models.TextField(blank=True, null=True)
    expected_rent = models.FloatField(default=0, blank=True, null=True)
    expected_movein_date = models.DateField(blank=True, null=True)
    accomodation_for = models.CharField(max_length=25, choices=HouseAccomodationAllowedCategories,
                                        blank=True, null=True)
    accomodation_type = models.CharField(max_length=20, choices=HouseAccomodationTypeCategories, blank=True, null=True)


class HouseOwnerReferral(Referral):
    affiliate = models.ForeignKey('affiliates.Affiliate', blank=True, null=True, on_delete=models.SET_NULL,
                                  related_name='house_owner_referrals')
    house_address = models.TextField(blank=True, null=True)
    house_type = models.CharField(max_length=20, blank=True, null=True, choices=HouseTypeCategories)
    bhk_count = models.PositiveIntegerField(default=1, blank=True, null=True)


def update_monthly_report_balance(affiliate):
    monthly_reports = list(AffiliateMonthlyReport.objects.filter(affiliate=affiliate))

    for idx, monthly_report in enumerate(monthly_reports):
        if idx == 0:
            monthly_report.start_balance = 0
            monthly_report.end_balance = monthly_report.earning
        else:
            monthly_report.start_balance = monthly_reports[idx - 1].end_balance
            monthly_report.end_balance = monthly_report.start_balance + monthly_report.earning
        monthly_report.save()


# noinspection PyUnusedLocal
@receiver(pre_save, sender=TenantReferral)
def tenant_referral_pre_save_hook(sender, instance, **kwargs):
    old_tenant_referral = TenantReferral.objects.filter(id=instance.id).first()
    if not old_tenant_referral:
        return

    if old_tenant_referral.status == PENDING and instance.status == SUCCESS:
        if instance.affiliate:
            affiliate = instance.affiliate

            month = instance.converted_at.month
            year = instance.converted_at.year
            start_date = timezone.make_aware(datetime(year, month, 1))
            end_date = start_date + relativedelta(months=+1, seconds=-1)

            current_monthly_report, _ = AffiliateMonthlyReport.objects.get_or_create(affiliate=affiliate,
                                                                                     start_date=start_date,
                                                                                     end_date=end_date)

            current_monthly_report.tenant_conversion_count = (TenantReferral
                                                              .objects.filter(affiliate=affiliate, status=SUCCESS,
                                                                              converted_at__gte=
                                                                              current_monthly_report.start_date,
                                                                              converted_at__lte=
                                                                              current_monthly_report.end_date).count()
                                                              + 1)

            current_monthly_report.save()

            update_monthly_report_balance(affiliate)


# noinspection PyUnusedLocal
@receiver(pre_save, sender=HouseOwnerReferral)
def house_owner_referral_pre_save_hook(sender, instance, **kwargs):
    old_house_owner_referral = HouseOwnerReferral.objects.filter(id=instance.id).first()
    if not old_house_owner_referral:
        return

    if old_house_owner_referral.status == PENDING and instance.status == SUCCESS:
        if instance.affiliate:
            affiliate = instance.affiliate

            month = instance.converted_at.month
            year = instance.converted_at.year
            start_date = datetime(year, month, 1)
            end_date = start_date + relativedelta(months=+1, seconds=-1)

            current_monthly_report, _ = AffiliateMonthlyReport.objects.get_or_create(affiliate=affiliate,
                                                                                     start_date=start_date,
                                                                                     end_date=end_date)

            current_monthly_report.tenant_conversion_count = (HouseOwnerReferral
                                                              .objects.filter(affiliate=affiliate, status=SUCCESS,
                                                                              converted_at__gte=
                                                                              current_monthly_report.start_date,
                                                                              converted_at__lte=
                                                                              current_monthly_report.end_date).count()
                                                              + 1)

            current_monthly_report.save()

            update_monthly_report_balance(affiliate)
