from datetime import datetime

from django.utils import timezone


def get_number(field_str):
    try:
        return int(field_str)
    except ValueError:
        try:
            return float(field_str)
        except ValueError:
            return None


def get_datetime(raw_date):
    if raw_date in [None, '']:
        return None
    for fmt in ('%Y-%m-%d', '%Y-%m-%d %H:%M:%S'):
        try:
            return timezone.make_aware(datetime.strptime(raw_date, fmt), timezone.get_default_timezone())
        except ValueError:
            pass
    raise ValueError('no valid date format found')
