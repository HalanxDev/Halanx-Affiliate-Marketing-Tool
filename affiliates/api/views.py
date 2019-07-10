from rest_framework import status
from rest_framework.generics import CreateAPIView, get_object_or_404
from rest_framework.response import Response

from affiliates.api.serializers import TenantReferralSerializer
from affiliates.models import Affiliate
from referrals.models import TenantReferral
from referrals.tasks.tasks_affiliate_lead_management import send_tenant_referral_to_lead_tool_to_generate_lead


class TenantReferralCreateView(CreateAPIView):
    serializer_class = TenantReferralSerializer
    queryset = TenantReferral.objects.all()

    def create(self, request, *args, **kwargs):
        affiliate_code = request.data.get('affiliate_code')
        affiliate = get_object_or_404(Affiliate, unique_code=affiliate_code)
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            tenant_referral = serializer.save(affiliate=affiliate)
            # send referral details to lead tool
            try:
                send_tenant_referral_to_lead_tool_to_generate_lead(tenant_referral)
            except Exception as E:
                print(E)

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

