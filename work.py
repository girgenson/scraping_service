import requests
import codecs
from bs4 import BeautifulSoup as BS
import mysqlx

a = mysqlx.connection

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 5.1; rv:47.0) Gecko/20100101 Firefox/47.0',
           'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
           }


def work(url):
    jobs = []
    errors = []
    domain = 'https://www.work.ua'
    url = 'https://www.work.ua/ru/jobs-kyiv-python/'
    resp = requests.get(url, headers=headers)
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
                             })
        else:
            errors.append({'url': url, 'title': "Div doesn't exist"})
    else:
        errors.append({'url': url, 'title': "Page doesn't response"})
    return jobs, errors


def rabota(url):
    jobs = []
    errors = []
    domain = 'https://rabota.ua'
    # url = 'https://rabota.ua/zapros/python/'
    resp = requests.get(url, headers=headers)
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
                        content = tr.p.text
                        company = 'No name'
                        p = tr.find('p', attrs={'class': 'card-title'})
                        if p:
                            company = p.a.text
                        jobs.append({'title': title.text,
                                     'url': domain + href,
                                     'description': content,
                                     'company': company,
                                     })
            else:
                errors.append({'url': url, 'title': "Table doesn't exist"})
        else:
            errors.append({'url': url, 'title': "Page is empty"})
    else:
        errors.append({'url': url, 'title': "Page doesn't response"})
    return jobs, errors


def dou(url):
    jobs = []
    errors = []
    # domain = 'https://www.work.ua'
    resp = requests.get(url, headers=headers)
    if resp.status_code == 200:
        soup = BS(resp.content, 'html.parser')
        main_div = soup.find('div', id='pjax-job-list')
        if main_div:
            li_lst = main_div.find_all('div', attrs={'class': 'card card-hover card-visited wordwrap job-link'})
            for div in li_lst:
                if '__hot' not in div['class']:
                    title = div.find('a')
                    real_title = title['title']
                    href = title['href']
                    # href = title.find('title')
                    # cont = div.find('div', attrs={'class': 'sh-info'})
                    cont = div.find('p', attrs={'class': 'overflow text-muted add-top-sm add-bottom'})
                    content = cont.text

                    company = 'No name'
                    a = title.find('a', attrs={'class': 'company'})
                    if a:
                        company = a.text
                    jobs.append({'title': title.text,
                                 'url': href,
                                 # 'description': content,
                                 'company': company,
                                 })
        else:
            errors.append({'url': url, 'title': "Div doesn't exist"})
    else:
        errors.append({'url': url, 'title': "Page doesn't response"})
    return jobs, errors


if __name__ == '__main__':
    # url = 'https://rabota.ua/zapros/python'
    url = 'https://www.work.ua/ru/jobs-kyiv-python/'
    jobs, errors = dou(url)
    h = codecs.open('work.txt', 'w', 'utf-8')
    h.write(str(jobs))
    h.close()
    print(errors)
