from decouple import config
from sendgrid import sendgrid
from sendgrid.helpers.mail import Mail

ORGANISATION_TYPE_CATEGORIES = []

AFFILIATE_OCCUPATION_CATEGORIES = []


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
