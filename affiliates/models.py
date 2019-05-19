from django.conf import settings
from django.core.files.base import ContentFile
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.html import format_html

from affiliates.utils import default_profile_pic_url, \
    default_profile_pic_thumbnail_url, get_picture_upload_path, get_thumbnail_upload_path, \
    DEFAULT_TENANT_CONVERSION_COMMISSION, DEFAULT_HOUSE_OWNER_CONVERSION_COMMISSION
from common.models import AddressDetail, BankDetail, Wallet
from common.utils import PENDING, PaymentStatusCategories, PAID
from utility.image_utils import compress_image
from utility.random_utils import generate_random_code


class Affiliate(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='affiliate')
    phone_no = models.CharField(max_length=15, blank=True, null=True)
    occupation = models.ForeignKey('AffiliateOccupationCategory', blank=True, null=True, on_delete=models.SET_NULL,
                                   related_name='affiliates')
    unique_code = models.CharField(max_length=100, blank=True, null=True, unique=True)
    profile_pic_url = models.CharField(max_length=500, blank=True, null=True, default=default_profile_pic_url)
    profile_pic_thumbnail_url = models.CharField(max_length=500, blank=True, null=True,
                                                 default=default_profile_pic_thumbnail_url)

    tenant_conversion_commission = models.FloatField(default=DEFAULT_TENANT_CONVERSION_COMMISSION)
    house_owner_conversion_commission = models.FloatField(default=DEFAULT_HOUSE_OWNER_CONVERSION_COMMISSION)

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

    def get_profile_pic_html(self):
        return format_html('<img src="{}" width="50" height="50" />'.format(self.profile_pic_url))

    get_profile_pic_html.short_description = 'Profile Pic'
    get_profile_pic_html.allow_tags = True


class AffiliateAddress(AddressDetail):
    affiliate = models.OneToOneField('Affiliate', on_delete=models.CASCADE, related_name='address')


class AffiliateBankDetail(BankDetail):
    affiliate = models.OneToOneField('Affiliate', on_delete=models.CASCADE, related_name='bank_detail')


class AffiliateOccupationCategory(models.Model):
    name = models.CharField(max_length=500, blank=True, null=True)

    class Meta:
        verbose_name_plural = "Affiliate occupation categories"

    def __str__(self):
        return self.name


class AffiliateOrganisationTypeCategory(models.Model):
    name = models.CharField(max_length=500, blank=True, null=True)

    class Meta:
        verbose_name_plural = "Affiliate organisation type categories"

    def __str__(self):
        return self.name


class AffiliateOrganisation(models.Model):
    affiliate = models.OneToOneField('Affiliate', on_delete=models.CASCADE, related_name='organisation')
    type = models.ForeignKey('AffiliateOrganisationTypeCategory', blank=True, null=True, on_delete=models.SET_NULL,
                             related_name='organisations')
    name = models.CharField(max_length=255, blank=True, null=True)
    website = models.CharField(max_length=500, blank=True, null=True)

    def __str__(self):
        return str(self.name)


class AffiliateOrganisationAddress(AddressDetail):
    organisation = models.OneToOneField('AffiliateOrganisation', on_delete=models.CASCADE, related_name='address')


class AffiliatePicture(models.Model):
    affiliate = models.ForeignKey('Affiliate', on_delete=models.SET_NULL, null=True, related_name='pictures')
    image = models.ImageField(upload_to=get_picture_upload_path, null=True, blank=True)
    thumbnail = models.ImageField(upload_to=get_thumbnail_upload_path, null=True, blank=True)
    is_profile_pic = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return str(self.affiliate.name)

    def save(self, *args, **kwargs):
        if not self.pk:
            temp_name, output, thumbnail = compress_image(self.image, quality=90, _create_thumbnail=True)
            self.image.save(temp_name, content=ContentFile(output.getvalue()), save=False)
            self.thumbnail.save(temp_name, content=ContentFile(thumbnail.getvalue()), save=False)

        if self.is_deleted and self.is_profile_pic:
            self.is_profile_pic = False
            self.affiliate.profile_pic_url = default_profile_pic_url
            self.affiliate.profile_pic_thumbnail_url = default_profile_pic_thumbnail_url
            self.affiliate.save()
        super(AffiliatePicture, self).save(*args, **kwargs)


class AffiliateMonthlyReport(models.Model):
    affiliate = models.ForeignKey('Affiliate', on_delete=models.SET_NULL, null=True, related_name='monthly_reports')
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()

    earning = models.FloatField(default=0)
    tenant_conversion_count = models.IntegerField(default=0)
    house_owner_conversion_count = models.IntegerField(default=0)

    start_balance = models.FloatField(default=0)
    end_balance = models.FloatField(default=0)

    class Meta:
        ordering = ('start_date', )

    def __str__(self):
        return str(self.id)

    def save(self, *args, **kwargs):
        self.earning = (self.affiliate.tenant_conversion_commission * self.tenant_conversion_count +
                        self.affiliate.house_owner_conversion_commission * self.house_owner_conversion_count)
        super(AffiliateMonthlyReport, self).save(*args, **kwargs)


class AffiliateWallet(Wallet):
    affiliate = models.OneToOneField('Affiliate', on_delete=models.PROTECT, related_name='wallet')

    def __str__(self):
        return str(self.affiliate.name)


class AffiliatePayment(models.Model):
    wallet = models.ForeignKey('AffiliateWallet', on_delete=models.SET_NULL, null=True, related_name='payments')
    amount = models.FloatField(default=0)
    description = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=30, default=PENDING, choices=PaymentStatusCategories)
    due_date = models.DateTimeField(blank=True, null=True)
    paid_on = models.DateTimeField(blank=True, null=True)

    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.id)


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
        AffiliateBankDetail(affiliate=instance).save()
        AffiliateWallet(affiliate=instance).save()
        super(Affiliate, instance).save()


# noinspection PyUnusedLocal
@receiver(post_save, sender=AffiliateOrganisation)
def organisation_post_save_hook(sender, instance, created, **kwargs):
    if created:
        AffiliateOrganisationAddress(organisation=instance).save()
        super(AffiliateOrganisation, instance).save()


# noinspection PyUnusedLocal
@receiver(post_save, sender=AffiliatePicture)
def affiliate_picture_post_save_task(sender, instance, *args, **kwargs):
    if instance.is_profile_pic:
        instance.affiliate.profile_pic_url = instance.image.url
        instance.affiliate.profile_pic_thumbnail_url = instance.thumbnail.url
        instance.affiliate.save()
        last_profile_pic = instance.affiliate.pictures.filter(is_profile_pic=True).exclude(id=instance.id).first()
        if last_profile_pic:
            last_profile_pic.is_profile_pic = False
            super(AffiliatePicture, last_profile_pic).save()


# noinspection PyUnusedLocal
@receiver(post_save, sender=AffiliateMonthlyReport)
def affiliate_payment_post_save_hook(sender, instance, created, **kwargs):
    wallet = instance.affiliate.wallet
    wallet.credit = sum(monthly_report.earning for monthly_report in instance.affiliate.monthly_reports.all())
    wallet.save()


# noinspection PyUnusedLocal
@receiver(post_save, sender=AffiliatePayment)
def affiliate_payment_post_save_hook(sender, instance, created, **kwargs):
    wallet = instance.wallet
    wallet.debit = sum(payment.amount for payment in wallet.payments.filter(status=PAID))
    wallet.pending_withdrawal = sum(payment.amount for payment in wallet.payments.filter(status=PENDING))
    wallet.save()
