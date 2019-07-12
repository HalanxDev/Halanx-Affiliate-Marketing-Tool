from django.http import JsonResponse
from rest_framework import status
from rest_framework.authentication import BasicAuthentication
from rest_framework.generics import CreateAPIView, get_object_or_404, UpdateAPIView
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response

from affiliates.api.serializers import TenantReferralSerializer
from affiliates.models import Affiliate
from referrals.models import TenantReferral
# from referrals.tasks.tasks_affiliate_lead_management import send_tenant_referral_to_lead_tool_to_generate_lead
from referrals.utils import AFFILIATE_QR, DATA, METADATA, SUCCESS, TASK_TYPE, UPDATE_TENANT_LEAD_ACTIVITY_STATUS
from utility.response_utils import STATUS, ERROR


class TenantReferralCreateView(CreateAPIView):
    serializer_class = TenantReferralSerializer
    queryset = TenantReferral.objects.all()

    def create(self, request, *args, **kwargs):
        from lead_affiliate.tasks.sending_tasks import send_tenant_referral_to_lead_tool_to_generate_lead
        affiliate_code = request.data.get('affiliate_code')
        affiliate = get_object_or_404(Affiliate, unique_code=affiliate_code)
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            tenant_referral = serializer.save(affiliate=affiliate)
            # send referral details to lead tool
            try:
                send_tenant_referral_to_lead_tool_to_generate_lead(tenant_referral,
                                                                   referral_lead_source_name=AFFILIATE_QR)
            except Exception as E:
                print(E)

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TenantReferralUpdateView(UpdateAPIView):
    queryset = TenantReferral.objects.all()
    authentication_classes = (BasicAuthentication, )
    permission_classes = (IsAdminUser, )

    def patch(self, request, *args, **kwargs):
        if self.request.data[TASK_TYPE] == UPDATE_TENANT_LEAD_ACTIVITY_STATUS:
            try:
                instance = self.get_object()
                print('updating ', instance)
                instance.status = self.request.data[METADATA]['referral_status']
                instance.save()
                response_json = {STATUS: SUCCESS}
                return JsonResponse(response_json, status=200)
            except Exception as E:
                response_json = {STATUS: ERROR, 'message': str(E)}
                return JsonResponse(response_json, status=400)
