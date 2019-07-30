from rest_framework import serializers

from referrals.models import TenantReferral, HouseOwnerReferral


class TenantReferralSerializer(serializers.ModelSerializer):
    class Meta:
        model = TenantReferral
        fields = '__all__'
        read_only_fields = ('converted_at', 'status', 'affiliate')


class HouseOwnerReferralSerializer(serializers.ModelSerializer):
    class Meta:
        model = HouseOwnerReferral
        fields = '__all__'
        read_only_fields = ('converted_at')