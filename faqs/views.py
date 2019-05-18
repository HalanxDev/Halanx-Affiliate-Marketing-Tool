from django.shortcuts import render

from faqs.models import Topic


def index(request):
    topics = Topic.objects.all()
    return render(request, 'index.html', {'topics': topics})
