from decouple import config
from sendgrid import sendgrid
from sendgrid.helpers.mail import Mail

from utility.random_utils import generate_random_code


# noinspection PyUnusedLocal
def get_affiliate_qr_code_upload_path(instance, filename):
    return "qrcode/{}/{}.png".format(instance.user.id, generate_random_code(n=5))


def get_picture_upload_path(instance, filename):
    return "affiliates/{}/pictures/{}-{}".format(instance.affiliate.id, generate_random_code(n=5),
                                                 filename.split('/')[-1])


def get_thumbnail_upload_path(instance, filename):
    return "affiliates/{}/thumbnail/{}-{}".format(instance.affiliate.id, generate_random_code(n=5),
                                                  filename.split('/')[-1])


default_profile_pic_url = "https://d28fujbigzf56k.cloudfront.net/static/img/nopic.jpg"
default_profile_pic_thumbnail_url = "https://d28fujbigzf56k.cloudfront.net/static/img/nopic_small.jpg"


def send_account_verification_email(email, message):
    sg = sendgrid.SendGridAPIClient(api_key=config("SENDGRID_API_KEY"))
    mail = Mail(
        from_email='Halanx <support@halanx.com>',
        to_emails=email,
        subject="Activate Your Halanx Affiliate Account",
        html_content=message)
    try:
        sg.send(mail)
    except Exception as e:
        print(e)


def send_password_reset_email(email, message):
    sg = sendgrid.SendGridAPIClient(api_key=config("SENDGRID_API_KEY"))
    mail = Mail(
        from_email='Halanx <support@halanx.com>',
        to_emails=email,
        subject="Halanx Affiliate Account Password Reset",
        html_content=message)
    try:
        sg.send(mail)
    except Exception as e:
        print(e)
