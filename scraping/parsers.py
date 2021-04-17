import requests

from bs4 import BeautifulSoup as BS
from random import choice


__all__ = ('work', 'rabota', 'dou', 'djinni')


headers = [{'User-Agent': 'Mozilla/5.0 (Windows NT 5.1; rv:47.0) Gecko/20100101 Firefox/47.0',
           'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'},
           {'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 12_2 like Mac OS X) '
                          'AppleWebKit/605.1.15 (KHTML, like Gecko) Version/12.1 Mobile/15E148 Safari/604.1',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'},
           {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:68.9) Gecko/20100101 Goanna/4.4 '
                          'Firefox/68.9 PaleMoon/28.8.3',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'},
           ]


def work(url, city=None, language=None):
    jobs = []
    errors = []
    domain = 'https://www.work.ua'
    # url = 'https://www.work.ua/ru/jobs-kyiv-python/'
    if url:
        resp = requests.get(url, headers=choice(headers))
        if resp.status_code == 200:
            soup = BS(resp.content, 'html.parser')
            main_div = soup.find('div', id='pjax-job-list')
            if main_div:
                div_lst = main_div.find_all('div', attrs={'class': 'job-link'})
                for div in div_lst:
                    title = div.find('h2')
                    href = title.a['href']
                    content = div.p.text
                    company = 'No name'
                    logo = div.find('img')
                    if logo:
                        company = logo['alt']
                    jobs.append({'title': title.text,
                                 'url': domain + href,
                                 'description': content,
                                 'company': company,
                                 'city_id': city,
                                 'language_id': language,
                                 })
            else:
                errors.append({'url': url, 'title': "Div doesn't exist"})
        else:
            errors.append({'url': url, 'title': "Page doesn't response"})
    return jobs, errors


def rabota(url, city=None, language=None):
    jobs = []
    errors = []
    domain = 'https://rabota.ua'
    # url = 'https://rabota.ua/zapros/python/'
    if url:
        resp = requests.get(url, headers=choice(headers))
        if resp.status_code == 200:
            soup = BS(resp.content, 'html.parser')
            new_jobs = soup.find('span', attrs={'class': 'fd-beefy-craftsmen'})
            if not new_jobs:
                table = soup.find('table', id='ctl00_content_vacancyList_gridList')
                if table:
                    tr_list = table.find_all('tr', attrs={'id': True})
                    for tr in tr_list:
                        div = tr.find('div', attrs={'class': 'card-body'})
                        if div:
                            title = div.find('h2', attrs={'class': 'card-title'})
                            href = title.a['href']
                            content = div.find('div', attrs={'class': 'card-description'}).text
                            company = 'No name'
                            p = tr.find('a', attrs={'class': 'company-profile-name'})
                            if p:
                                company = p.get('title')
                            jobs.append({'title': title.text,
                                         'url': domain + href,
                                         'description': content,
                                         'company': company,
                                         'city_id': city,
                                         'language_id': language,
                                         })
                else:
                    errors.append({'url': url, 'title': "Table doesn't exist"})
            else:
                errors.append({'url': url, 'title': "Page is empty"})
        else:
            errors.append({'url': url, 'title': "Page doesn't response"})
    return jobs, errors


def dou(url, city=None, language=None):
    jobs = []
    errors = []
    if url:
        resp = requests.get(url, headers=choice(headers))
        if resp.status_code == 200:
            soup = BS(resp.content, 'html.parser')
            main_div = soup.find('div', id='vacancyListId')
            if main_div:
                li_lst = main_div.find_all('li', attrs={'class': 'l-vacancy'})
                for li in li_lst:
                    if '__hot' not in li['class']:
                        title = li.find('div', attrs={'class': 'title'})
                        href = title.a['href']
                        cont = li.find('div', attrs={'class': 'sh-info'})
                        content = cont.text
                        company = 'No name'
                        a = title.find('a', attrs={'class': 'company'})
                        if a:
                            company = a.text
                        jobs.append({'title': title.text,
                                     'url': href,
                                     'description': content,
                                     'company': company,
                                     'city_id': city,
                                     'language_id': language,
                                     })
            else:
                errors.append({'url': url, 'title': "Div doesn't exist"})
        else:
            errors.append({'url': url, 'title': "Page doesn't response"})
    return jobs, errors


def djinni(url, city=None, language=None):
    jobs = []
    errors = []
    domain = 'https://djinni.co'
    if url:
        resp = requests.get(url, headers=choice(headers))
        if resp.status_code == 200:
            soup = BS(resp.content, 'html.parser')
            main_ul = soup.find('ul', attrs={'class': 'list-jobs'})
            if main_ul:
                li_lst = main_ul.find_all('li', attrs={'class': 'list-jobs__item'})
                for li in li_lst:
                    title = li.find('div', attrs={'class': 'list-jobs__title'})
                    href = title.a['href']
                    cont = li.find('div', attrs={'class': 'list-jobs__description'})
                    content = cont.text
                    company = 'No name'
                    comp = li.find('div', attrs={'class': 'list-jobs__details__info'})
                    if comp:
                        company = comp.text
                        jobs.append({'title': title.text,
                                     'url': domain + href,
                                     'description': content,
                                     'company': company,
                                     'city_id': city,
                                     'language_id': language,
                                     })
            else:
                    errors.append({'url': url, 'title': "Ul doesn't exist"})
        else:
            errors.append({'url': url, 'title': "Page doesn't response"})
    return jobs, errors
