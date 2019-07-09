TENANT_REFERRAL = "tenant"
HOUSE_OWNER_REFERRAL = "house_owner"


GenderChoices = (
    ("male", "Male"),
    ("female", "Female"),
    ("other", "Other"),
)


GIRLS = 'girls'
BOYS = 'boys'
FAMILY = 'family'

HouseAccomodationAllowedCategories = (
    (GIRLS, 'Girls'),
    (BOYS, 'Boys'),
    (FAMILY, 'Family')
)

FLAT = 'flat'
PRIVATE_ROOM = 'private'
SHARED_ROOM = 'shared'

HouseAccomodationTypeCategories = (
    (SHARED_ROOM, 'Shared rooms'),
    (PRIVATE_ROOM, 'Private rooms'),
    (FLAT, 'Entire house'),
)

APARTMENT = 'apartment'
INDEPENDENT = 'independent'
VILLA = 'villa'

HouseTypeCategories = (
    (APARTMENT, 'Apartment'),
    (INDEPENDENT, 'Independent House'),
    (VILLA, 'Villa'),
)

PENDING = 'pending'
SUCCESS = 'success'
CANCELLED = 'cancelled'

ReferralStatusChoices = (
    (PENDING, 'Pending'),
    (SUCCESS, 'Success'),
    (CANCELLED, 'Cancelled'),
)

DASHBOARD_FORM_SOURCE = 'Dashboard Form'
DASHBOARD_BULK_UPLOAD_SOURCE = 'Dashboard File Upload'
WEBSITE_ENQUIRY_SOURCE = 'Website Enquiry'
WEBSITE_LOGIN_SOURCE = 'Website Login'

ReferralSourceChoices = (
    (DASHBOARD_FORM_SOURCE, DASHBOARD_FORM_SOURCE),
    (DASHBOARD_BULK_UPLOAD_SOURCE, DASHBOARD_BULK_UPLOAD_SOURCE),
    (WEBSITE_ENQUIRY_SOURCE, WEBSITE_ENQUIRY_SOURCE),
    (WEBSITE_LOGIN_SOURCE, WEBSITE_LOGIN_SOURCE),
)

TENANT_LEAD_FIELDS_PRESENT_IN_TENANT_REFERRAL_FIELDS = ('name', 'gender', 'phone_no', 'email',  'accomodation_for')
OWNER_LEAD_FIELDS_PRESENT_IN_OWNER_REFERRAL_FIELDS = ('name', 'gender', 'phone_no', 'email')
