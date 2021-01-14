from django.shortcuts import render
from scraping.models import Vacancy


def home_view(request):
    qs = Vacancy.objects.all()
    return render(request, 'scraping/home.html', {'object_list': qs})
