import random

import requests
from celery import shared_task
from celery.utils.log import get_task_logger
from decouple import config

from affiliates.models import OTP

logger = get_task_logger(__name__)


@shared_task
def send_sms(phone_no, message):

    logger.info("Sending SMS to phone number {}".format(phone_no))

    authkey = config('MSG91_AUTH_KEY')
    sender = 'halanx'
    data = {
        'authkey': authkey,
        'mobiles': phone_no,
        'message': message,
        'sender': sender,
        'route': '4'
    }
    url = config('MSG91_API_URL')
    res = requests.post(url, data=data)

    logger.info("Sent SMS to phone number {} with response: {}".format(phone_no, res.text))


def generate_otp(phone_no, first_name):
    rand = random.randrange(1, 8999) + 1000
    message = "Hi {}! {} is your One Time Password(OTP) for Halanx Affiliate Login.".format(first_name, rand)
    otp, created = OTP.objects.get_or_create(phone_no=phone_no)
    otp.password = rand
    otp.save()

    send_sms(phone_no, message)
