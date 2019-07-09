from django.conf import settings

from utility.environments import PRODUCTION

if settings.ENVIRONMENT == PRODUCTION:
    LEAD_MANAGEMENT_TOOL_BASE_URL = 'https://leads.halanx.com/'
else:
    LEAD_MANAGEMENT_TOOL_BASE_URL = 'http://127.0.0.1:8000/'

TENANT_REFERRAL_CREATE_LEAD_API_URL = LEAD_MANAGEMENT_TOOL_BASE_URL + 'api/leads/tenant/referrals/'
OWNER_REFERRAL_CREATE_LEAD_API_URL = LEAD_MANAGEMENT_TOOL_BASE_URL + 'api/leads/owner/referrals/'
