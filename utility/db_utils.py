from affiliates.models import AffiliateOrganisationTypeCategory, AffiliateOccupationCategory

AFFILIATE_ORGANISATION_TYPE_CATEGORIES = [
    'Education',
    'E-Commerce',
    'Local Business',
    'Entertainment',
    'Other'
]


AFFILIATE_OCCUPATION_CATEGORIES = [
    'Student',
    'Receptionist',
    'HR Manager'
]


def load_affiliate_organisation_type_categories():
    for category in AFFILIATE_ORGANISATION_TYPE_CATEGORIES:
        AffiliateOrganisationTypeCategory.objects.get_or_create(name=category)


def load_affiliate_occupation_categories():
    for category in AFFILIATE_OCCUPATION_CATEGORIES:
        AffiliateOccupationCategory.objects.get_or_create(name=category)
