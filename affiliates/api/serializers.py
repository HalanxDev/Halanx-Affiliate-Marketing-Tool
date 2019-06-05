from rest_framework import serializers

from referrals.models import TenantReferral


class TenantReferralSerializer(serializers.ModelSerializer):
    class Meta:
        model = TenantReferral
        fields = '__all__'
        read_only_fields = ('converted_at', 'status', 'affiliate')
