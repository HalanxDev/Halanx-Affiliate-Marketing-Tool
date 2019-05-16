from django.contrib import admin
from django.urls import reverse
from django.utils.safestring import mark_safe

from affiliates.models import Affiliate, AffiliateAddress, AffiliateOrganisation, AffiliateOrganisationAddress, \
    AffiliateOccupationCategory, AffiliateOrganisationTypeCategory, AffiliatePicture, AffiliateBankDetail


@admin.register(AffiliateOccupationCategory)
class AffiliateOccupationCategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', )


@admin.register(AffiliateOrganisationTypeCategory)
class AffiliateOrganisationTypeCategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', )


class AffiliateAddressInline(admin.StackedInline):
    model = AffiliateAddress


class AffiliateBankDetailInline(admin.StackedInline):
    model = AffiliateBankDetail


class AffiliateOrganisationInline(admin.StackedInline):
    model = AffiliateOrganisation
    fields = ('name', 'type', 'website', 'organisation_address',)
    readonly_fields = ('organisation_address',)

    # noinspection PyProtectedMember
    @staticmethod
    def organisation_address(instance):
        url = reverse('admin:%s_%s_change' % (
            instance._meta.app_label, instance._meta.model_name), args=[instance.pk])
        if instance.pk:
            return mark_safe(u'{address} <a href="{u}">Edit</a>'.format(address=instance.address, u=url))
        else:
            return ''


class AffiliateOrganisationAddressInline(admin.StackedInline):
    model = AffiliateOrganisationAddress


@admin.register(AffiliateOrganisation)
class AffiliateOrganisationAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'type', 'website', 'address')
    inlines = (
        AffiliateOrganisationAddressInline,
    )


class AffiliatePictureTabular(admin.TabularInline):
    model = AffiliatePicture
    extra = 0
    ordering = ('-timestamp',)


@admin.register(Affiliate)
class AffiliateAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'occupation', 'organisation_name', 'get_profile_pic_html', 'verified')
    readonly_fields = ('get_profile_pic_html',)
    inlines = (
        AffiliateAddressInline,
        AffiliateOrganisationInline,
        AffiliateBankDetailInline,
        AffiliatePictureTabular,
    )

    def get_inline_instances(self, request, obj=None):
        # Return no inlines when obj is being created
        if not obj:
            return []
        else:
            return super(AffiliateAdmin, self).get_inline_instances(request, obj)

    @staticmethod
    def organisation_name(obj):
        return obj.organisation.name
