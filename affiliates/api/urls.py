from django.conf.urls import url

from affiliates.api import views

urlpatterns = [
    url('^referrals/tenant/$', views.TenantReferralCreateView.as_view()),
    url('^tenant/referrals/(?P<pk>[0-9]+)/$', views.TenantReferralUpdateView.as_view()),
    url('^owner/referrals/(?P<pk>[0-9]+)/$', views.OwnerReferralUpdateView.as_view()),
]