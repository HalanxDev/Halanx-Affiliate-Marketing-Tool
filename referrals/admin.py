from django.contrib import admin

from referrals.models import TenantReferral, HouseOwnerReferral


@admin.register(TenantReferral)
class TenantReferralAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'phone_no', 'affiliate', 'preferred_location')


@admin.register(HouseOwnerReferral)
class HouseOwnerReferralAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'phone_no', 'affiliate', 'house_address')
