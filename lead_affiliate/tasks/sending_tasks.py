import json

import requests
from decouple import config

from referrals.utils import TENANT_LEAD_FIELDS_PRESENT_IN_TENANT_REFERRAL_FIELDS, SUCCESS, \
    OWNER_LEAD_FIELDS_PRESENT_IN_OWNER_REFERRAL_FIELDS, SOURCE_NAME, DATA, METADATA
from utility.response_utils import STATUS
from utility.url_constants import TENANT_REFERRAL_CREATE_LEAD_API_URL, OWNER_REFERRAL_CREATE_LEAD_API_URL, \
    TENANT_REFERRAL_BULK_CREATE_LEAD_API_URL, OWNER_REFERRAL_BULK_CREATE_LEAD_API_URL


def send_tenant_referral_to_lead_tool_to_generate_lead(referral, referral_lead_source_name=''):
    request_data = {SOURCE_NAME: referral_lead_source_name}
    data = {}
    for field in referral._meta.get_fields():
        if field.name in TENANT_LEAD_FIELDS_PRESENT_IN_TENANT_REFERRAL_FIELDS:
            data[field.name] = str(getattr(referral, field.name))

    data[METADATA] = {'referral_id': referral.id}
    request_data[DATA] = data
    req = requests.post(TENANT_REFERRAL_CREATE_LEAD_API_URL, data=json.dumps(request_data),
                        headers={'Content-type': 'application/json'},
                        timeout=5,
                        auth=(config('LEAD_TOOL_ADMIN_USERNAME'), config('LEAD_TOOL_ADMIN_PASSWORD')))

    if req.status_code == 200:
        if req.json()[STATUS] == SUCCESS:
            referral.lead_published = True
            referral.save()


def send_owner_referral_to_lead_tool_to_generate_lead(referral, referral_lead_source_name=''):
    request_data = {SOURCE_NAME: referral_lead_source_name}
    data = {}
    for field in referral._meta.get_fields():
        if field.name in OWNER_LEAD_FIELDS_PRESENT_IN_OWNER_REFERRAL_FIELDS:
            data[field.name] = str(getattr(referral, field.name))

    data[METADATA] = {'referral_id': referral.id}
    request_data[DATA] = data
    req = requests.post(OWNER_REFERRAL_CREATE_LEAD_API_URL, data=json.dumps(request_data),
                        headers={'Content-type': 'application/json'},
                        timeout=5,
                        auth=(config('LEAD_TOOL_ADMIN_USERNAME'), config('LEAD_TOOL_ADMIN_PASSWORD')))

    if req.status_code == 200:
        if req.json()[STATUS] == SUCCESS:
            referral.lead_published = True
            referral.save()


def send_tenant_csv_referral_to_lead_tool_to_generate_leads(tenant_referrals, referral_lead_source_name=''):
    request_data = {SOURCE_NAME: referral_lead_source_name}
    tenant_referral_detail_list = []

    for referral in tenant_referrals:
        data = {}
        for field in referral._meta.get_fields():
            if field.name in TENANT_LEAD_FIELDS_PRESENT_IN_TENANT_REFERRAL_FIELDS:
                data[field.name] = str(getattr(referral, field.name))

        data[METADATA] = {'referral_id': referral.id}
        tenant_referral_detail_list.append(data)

    request_data[DATA] = tenant_referral_detail_list
    req = requests.post(TENANT_REFERRAL_BULK_CREATE_LEAD_API_URL, data=json.dumps(request_data),
                        headers={'Content-type': 'application/json'},
                        timeout=30,
                        auth=(config('LEAD_TOOL_ADMIN_USERNAME'), config('LEAD_TOOL_ADMIN_PASSWORD')))
    print(req)
    response = req.json()
    print(response)
    for referral, referral_status in zip(tenant_referrals, response):
        if referral_status[STATUS] == SUCCESS:
            referral.lead_published = True
            referral.save()


def send_owner_csv_referral_to_lead_tool_to_generate_leads(owner_referrals, referral_lead_source_name=''):
    request_data = {SOURCE_NAME: referral_lead_source_name}

    owner_referral_detail_list = []

    for referral in owner_referrals:
        data = {}
        for field in referral._meta.get_fields():
            if field.name in OWNER_LEAD_FIELDS_PRESENT_IN_OWNER_REFERRAL_FIELDS:
                data[field.name] = str(getattr(referral, field.name))

        data[METADATA] = {'referral_id': referral.id}
        owner_referral_detail_list.append(data)

    request_data[DATA] = owner_referral_detail_list
    req = requests.post(OWNER_REFERRAL_BULK_CREATE_LEAD_API_URL, data=json.dumps(request_data),
                        headers={'Content-type': 'application/json'},
                        timeout=30,
                        auth=(config('LEAD_TOOL_ADMIN_USERNAME'), config('LEAD_TOOL_ADMIN_PASSWORD')))
    print(req)
    response = req.json()
    print(response)
    for referral, referral_status in zip(owner_referrals, response):
        if referral_status[STATUS] == SUCCESS:
            referral.lead_published = True
            referral.save()
