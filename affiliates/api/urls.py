from django.conf.urls import url

from affiliates.api import views

urlpatterns = [
    url('^referrals/tenant/$', views.TenantReferralCreateView.as_view()),
]