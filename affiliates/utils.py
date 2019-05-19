from datetime import datetime

from dateutil.relativedelta import relativedelta
from decouple import config
from django.utils import timezone
from sendgrid import sendgrid
from sendgrid.helpers.mail import Mail

from utility.random_utils import generate_random_code


def get_picture_upload_path(instance, filename):
    return "affiliates/{}/pictures/{}-{}".format(instance.affiliate.id, generate_random_code(n=5),
                                                 filename.split('/')[-1])


def get_thumbnail_upload_path(instance, filename):
    return "affiliates/{}/thumbnail/{}-{}".format(instance.affiliate.id, generate_random_code(n=5),
                                                  filename.split('/')[-1])


def get_referral_csv_upload_path(instance, filename):
    return "affiliates/{}/referral-uploads/{}_{}".format(instance.id, timezone.now().strftime("%Y_%m_%d_%H_%M_%S"),
                                                         filename)


default_profile_pic_url = "https://d28fujbigzf56k.cloudfront.net/static/img/nopic.jpg"
default_profile_pic_thumbnail_url = "https://d28fujbigzf56k.cloudfront.net/static/img/nopic_small.jpg"

DEFAULT_TENANT_CONVERSION_COMMISSION = 100
DEFAULT_HOUSE_OWNER_CONVERSION_COMMISSION = 1000


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


def update_monthly_report_start_balance(affiliate):
    monthly_reports = list(affiliate.monthly_reports.all())
    for idx, monthly_report in enumerate(monthly_reports):
        if idx == 0:
            monthly_report.start_balance = 0
        else:
            monthly_report.start_balance = monthly_reports[idx - 1].end_balance
        monthly_report.save()


def get_or_create_monthly_report(affiliate, month, year):
    start_date = datetime(year, month, 1)
    end_date = start_date + relativedelta(months=+1, seconds=-1)

    from affiliates.models import AffiliateMonthlyReport
    monthly_report, _ = AffiliateMonthlyReport.objects.get_or_create(affiliate=affiliate, start_date=start_date,
                                                                     end_date=end_date)
    return monthly_report
