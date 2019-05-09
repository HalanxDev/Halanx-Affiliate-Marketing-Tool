from django.contrib.auth import logout, authenticate, login, get_user_model
from django.contrib.auth.decorators import user_passes_test, login_required
from django.contrib.auth.models import AnonymousUser
from django.contrib.sites.shortcuts import get_current_site
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.views.decorators.http import require_http_methods

from affiliates.models import Affiliate
from affiliates.tokens import account_activation_token
from affiliates.utils import send_account_verification_email
from utility.random_utils import generate_random_code

LOGIN_URL = '/login/'

User = get_user_model()


def is_affiliate(user):
    return Affiliate.objects.filter(user=user).count()


affiliate_login_test = user_passes_test(is_affiliate, login_url=LOGIN_URL)


def affiliate_login_required(view):
    decorated_view = login_required(affiliate_login_test(view), login_url=LOGIN_URL)
    return decorated_view


def logout_view(request):
    logout(request)
    request.session.flush()
    request.user = AnonymousUser
    return HttpResponseRedirect(reverse(home_page))


def login_view(request):
    error_msg = None
    logout(request)
    if request.POST:
        email, password = request.POST['email'], request.POST['password']
        user = authenticate(username=email, password=password)
        if user is not None:
            if is_affiliate(user):
                if user.is_active:
                    login(request, user)
                    next_page = request.GET.get('next')
                    if next_page:
                        return HttpResponseRedirect(next_page)
                    else:
                        return HttpResponseRedirect(reverse(home_page))
            else:
                error_msg = 'You are not an Affiliate.'
        else:
            error_msg = 'Either the email ID or the password is incorrect!'
    return render(request, 'login.html', {'error': error_msg})


@require_http_methods(['GET', 'POST'])
def register_view(request):
    if request.method == 'GET':
        return render(request, 'register.html')
    elif request.method == 'POST':
        data = request.POST
        email = data.get('email')

        if User.objects.filter(email=email).exists():
            return JsonResponse({'error': "User with this email already exists."}, status=500)

        first_name = data.get('first_name')
        last_name = data.get('last_name')
        password = data.get('password')
        phone_no = data.get('phone_no')
        username = generate_random_code(initials=first_name.lower(), n=3, alphabets=False,
                                        existing_codes=User.objects.values_list('username', flat=True))
        try:
            user = User.objects.create(username=username, first_name=first_name, last_name=last_name,
                                       email=email, password=password)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

        Affiliate.objects.create(user=user, phone_no=phone_no)

        # address = data.get('address')
        # occupation = data.get('occupation')
        # organisation_type = data.get('organisation_type')
        # organisation_name = data.get('organisation_name')
        # organisation_address = data.get('organisation_address')
        #
        # organisation = Organisation.objects.get_or_create(type=organisation_type, name=organisation_name,
        #                                                   address=organisation_address)
        # affiliate.organisation = organisation
        # affiliate.save()

        # send account verification link
        current_site = get_current_site(request)
        message = render_to_string('account_activation_email.html', {
            'user': user,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': account_activation_token.make_token(user),
        })
        send_account_verification_email(user.email, message)

        return redirect('account_activation_sent')


def account_activation_sent(request):
    return render(request, 'account_activation_sent.html')


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.affiliate.verified = True
        user.save()
        login(request, user)
        return redirect('home_page')
    else:
        return render(request, 'account_activation_invalid.html')


@require_http_methods(['GET'])
def home_page(request):
    return render(request, 'home.html')
