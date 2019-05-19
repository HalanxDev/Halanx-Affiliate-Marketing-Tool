from django.conf.urls import url
from django.contrib.auth import views as auth_views

from affiliates import views

urlpatterns = [
    url(r'^$', views.home_page, name='home_page'),
    url(r'^login/$', views.login_view, name='login'),
    url(r'^logout/$', views.logout_view, name='logout'),
    url(r'^register/$', views.register_view, name='register'),
    url(r'^password/$', views.change_password_view, name='change_password'),
    url(r'^account_activation_sent/$', views.account_activation_sent, name='account_activation_sent'),
    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        views.activate, name='activate'),

    url(r'^password_reset/$', views.CustomPasswordResetView.as_view(), name='password_reset'),
    url(r'^password_reset/done/$', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    url(r'^reset/done/$', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),

    url(r'^dashboard/$', views.dashboard_view, name='dashboard'),
    url(r'^profile/$', views.profile_view, name='profile'),
    url(r'^earnings/$', views.earnings_view, name='earnings'),

    url(r'^referrals/upload/$', views.referral_upload_view, name='referral_upload'),
    url(r'^referrals/upload/csv/$', views.referral_upload_csv_view, name='referral_upload_csv'),
    url(r'^referrals/list/$', views.referral_list_view, name='referral_list'),

    url(r'^tools/qrcode/$', views.qrcode_request_view, name='qrcode_request'),

    url(r'^widgets/data.js', views.test_view),
]
