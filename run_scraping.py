import codecs
import os
import sys

from django.db import DatabaseError

proj = os.path.dirname(os.path.abspath('manage.py'))
sys.path.append(proj)
os.environ["DJANGO_SETTINGS_MODULE"] = "scraping_service.settings"

import django
django.setup()

from scraping.parsers import *
from scraping.models import Vacancy, City, Language, Error


parsers = ((work, 'https://www.work.ua/ru/jobs-kyiv-python/'),
           (dou, 'https://jobs.dou.ua/vacancies/?city=%D0%9A%D0%B8%D0%B5%D0%B2&category=Python'),
           (rabota, 'https://rabota.ua/zapros/python'),
           (djinni, 'https://djinni.co/jobs/?keywords=python+%D0%BA%D0%B8%D0%B5%D0%B2')
)

city = City.objects.filter(slug='kiev').first()
language = Language.objects.filter(slug='python').first()

jobs, errors = [], []
for func, url in parsers:
    j, e = func(url)
    jobs += j
    errors += e

for job in jobs:
    v = Vacancy(**job, city=city, language=language)
    try:
        v.save()
    except DatabaseError:
        pass

if errors:
    er = Error(data=errors).save()


#
# h = codecs.open('parsers.txt', 'w', 'utf-8')
# h.write(str(jobs))
# h.close()
