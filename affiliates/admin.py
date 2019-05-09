from django.contrib import admin

from affiliates.models import Affiliate


@admin.register(Affiliate)
class AffiliateAdmin(admin.ModelAdmin):
    list_display = ('id', 'name',)
