import json

import requests
from decouple import config

from referrals.utils import TENANT_LEAD_FIELDS_PRESENT_IN_TENANT_REFERRAL_FIELDS, SUCCESS, \
    OWNER_LEAD_FIELDS_PRESENT_IN_OWNER_REFERRAL_FIELDS
from utility.response_utils import STATUS
from utility.url_constants import TENANT_REFERRAL_CREATE_LEAD_API_URL, OWNER_REFERRAL_CREATE_LEAD_API_URL


def send_tenant_referral_to_lead_tool_to_generate_lead(referral):
    data = {}
    for field in referral._meta.get_fields():
        if field.name in TENANT_LEAD_FIELDS_PRESENT_IN_TENANT_REFERRAL_FIELDS:
            data[field.name] = str(getattr(referral, field.name))

    req = requests.post(TENANT_REFERRAL_CREATE_LEAD_API_URL, data=json.dumps(data),
                        headers={'Content-type': 'application/json'},
                        timeout=5,
                        auth=(config('LEAD_TOOL_ADMIN_USERNAME'), config('LEAD_TOOL_ADMIN_PASSWORD')))

    if req.status_code == 200:
        if req.json()[STATUS] == SUCCESS:
            referral.lead_published = True
            referral.save()


def send_owner_referral_to_lead_tool_to_generate_lead(referral):
    data = {}
    for field in referral._meta.get_fields():
        if field.name in OWNER_LEAD_FIELDS_PRESENT_IN_OWNER_REFERRAL_FIELDS:
            data[field.name] = str(getattr(referral, field.name))

    req = requests.post(OWNER_REFERRAL_CREATE_LEAD_API_URL, data=json.dumps(data),
                        headers={'Content-type': 'application/json'},
                        timeout=5,
                        auth=(config('LEAD_TOOL_ADMIN_USERNAME'), config('LEAD_TOOL_ADMIN_PASSWORD')))

    if req.status_code == 200:
        if req.json()[STATUS] == SUCCESS:
            referral.lead_published = True
            referral.save()
