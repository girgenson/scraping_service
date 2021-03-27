import codecs
import os
import sys

proj = os.path.dirname(os.path.abspath('manage.py'))
sys.path.append(proj)
os.environ["DJANGO_SETTINGS_MODULE"] = "scraping_service.settings"

import django
django.setup()

from scraping.parsers import *
from scraping.models import Vacancy, City, Language


parsers = ((work, 'https://www.work.ua/ru/jobs-kyiv-python/'),
           (dou, 'https://jobs.dou.ua/vacancies/?city=%D0%9A%D0%B8%D0%B5%D0%B2&category=Python'),
           (rabota, 'https://rabota.ua/zapros/python'),
           (djinni, 'https://djinni.co/jobs/?keywords=python+%D0%BA%D0%B8%D0%B5%D0%B2')
)

city = City.objects.filter(slug='kiev')
jobs, errors = [], []
for func, url in parsers:
    j, e = func(url)
    jobs += j
    errors += e

h = codecs.open('parsers.txt', 'w', 'utf-8')
h.write(str(jobs))
h.close()
