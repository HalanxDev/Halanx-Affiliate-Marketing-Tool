from django.conf.urls import url

from faqs import views

urlpatterns = [
    url(r'^$', views.index, name='faqs'),
]
