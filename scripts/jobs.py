import re
import json
import requests
from bs4 import BeautifulSoup

def clean_html(raw_text):
    html_regex = re.compile('<.*?>')
    clean_text = re.sub(html_regex, '', raw_text)
    return clean_text

def print_company_header(company):
    print()
    print('-------------------------------------------------')
    print('--------- {} ----------'.format(company))
    print('-------------------------------------------------')

GREENHOUSE = 'https://boards.greenhouse.io/{}/jobs/{}'
GREENHOUSE_EMBED = 'https://boards.greenhouse.io/embed/job_app?token={}'
GREENHOUSE_API = 'https://api.greenhouse.io/v1/boards/{}/jobs'

LEVER_API = 'https://jobs.lever.co/{}'

KEYWORDS = ['Security', 'Privacy', 'Cybersecurity', 'Infosec', 'Red Team', 'Offensive']

def pinterest():
    COMPANY = 'pinterest'
    API = 'https://jobsapi-google.m-cloud.io/api/job/search?&pageSize=30&offset=0&companyName=companies%2F201fe4ec-50f6-4262-92bf-3f1779cdcc41&query=security&orderBy=relevance%20desc'

    res = requests.get(API)
    if res.status_code != 200:
        print('Something wrong: {}'.format(res.content))
        return

    res_json = res.json()
    f = open('./data/{}.md'.format(COMPANY), 'a+')
    
    for result in res_json['searchResults']:
        job_title = clean_html(result['summary']['job_title_snippet'])
        job_url = result['job']['url']
        
        text_to_write = '{} - {}\n\n'.format(job_title, job_url)
        f.write(text_to_write)
        print(text_to_write)

    f.close()
    return

def snap():
    COMPANY = 'snap'
    API = 'https://www.snap.com/api/jobs'

    res = requests.get(API)
    if res.status_code != 200:
        print('Something wrong: {}'.format(res.content))
        return

    listings = res.json()
    f = open('./data/{}.md'.format(COMPANY), 'a+')

    for job in listings['data']['Report_Entry']:
        if any(word in job['title'] for word in KEYWORDS):
            job_title = job['title']
            job_url = job['absolute_url']
            
            text_to_write = '{} - {}\n\n'.format(job_title, job_url)
            f.write(text_to_write)
            print(text_to_write)

    f.close()
    return

def block():
    COMPANY = 'block'
    API = 'https://careers.smartrecruiters.com/Square/?search=security'

    res = requests.get(API)
    if res.status_code != 200:
        print('Something wrong: {}'.format(res.content))
        return

    soup = BeautifulSoup(res.content, 'html5lib')
    raw_data = soup.find('ul', attrs = {'data-page':'0'}).contents

    f = open('./data/{}.md'.format(COMPANY), 'a+')

    for data in raw_data:
        job_title = data.find('h4').contents[0]
        job_url = data.find('a')['href']
        
        text_to_write = '{} - {}\n\n'.format(job_title, job_url)
        f.write(text_to_write)
        print(text_to_write)

    f.close()
    return

def twitter():
    COMPANY = 'twitter'
    API = 'https://careers.twitter.com/content/careers-twitter/en/roles.careers.search.json?q=security&location=careers-twitter%3Asr%2Foffice%2Fus%2Fwashington&location=careers-twitter%3Asr%2Foffice%2Fus%2Fsunnyvale&location=careers-twitter%3Asr%2Foffice%2Fus%2Fseattle&location=careers-twitter%3Asr%2Foffice%2Fus%2Fsan-jose&location=careers-twitter%3Asr%2Foffice%2Fus%2Fsan-francisco&location=careers-twitter%3Asr%2Foffice%2Fus%2Fsacramento&location=careers-twitter%3Asr%2Foffice%2Fus%2Fremote-us&location=careers-twitter%3Asr%2Foffice%2Fus%2Foakland&location=careers-twitter%3Asr%2Foffice%2Fus%2Fnew-york-city&location=careers-twitter%3Asr%2Foffice%2Fus%2Fmiami&location=careers-twitter%3Asr%2Foffice%2Fus%2Flos-angeles&location=careers-twitter%3Asr%2Foffice%2Fus%2Fhillsboro-dc&team=&offset=0&limit=50&sortBy=modified&asc=false'

    res = requests.get(API)
    if res.status_code != 200:
        print('Something wrong: {}'.format(res.content))
        return

    listings = res.json()
    f = open('./data/{}.md'.format(COMPANY), 'a+')

    for job in listings['results']:
        job_title = job['title']
        job_url = job['url']
        
        text_to_write = '{} - {}\n\n'.format(job_title, job_url)
        f.write(text_to_write)
        print(text_to_write)

    f.close()
    return

def uber():
    COMPANY = 'uber'
    API = 'https://www.uber.com/api/loadSearchJobsResults'
    JOB_URL = 'https://www.uber.com/global/en/careers/list/{}/'

    headers = {
        # Already added when you pass json=
        # 'Content-Type': 'application/json',
        'x-csrf-token': 'x',
    }

    params = {
        'localeCode': 'en',
    }

    json_data = {
        'params': {
            'location': [
                {
                    'country': 'USA',
                    'region': 'California',
                    'city': 'San Francisco',
                },
                {
                    'country': 'USA',
                    'region': 'California',
                    'city': 'Sunnyvale',
                },
                {
                    'country': 'USA',
                    'region': 'California',
                    'city': 'Los Angeles',
                },
                {
                    'country': 'USA',
                    'region': 'Washington',
                    'city': 'Seattle',
                },
                {
                    'country': 'USA',
                    'region': 'New York',
                    'city': 'New York',
                },
                {
                    'country': 'USA',
                    'region': 'Texas',
                    'city': 'Dallas',
                },
                {
                    'country': 'USA',
                    'region': 'District of Columbia',
                    'city': 'Washington',
                },
            ],
            'department': [
                'Engineering',
            ],
            'team': [
                'Security Engineer',
            ],
            'query': 'security',
        },
        'page': 0,
        'limit': 30,
    }

    res = requests.post(API, params=params, headers=headers, json=json_data)
    if res.status_code != 200:
        print('Something wrong: {}'.format(res.content))
        return

    listings = res.json()['data']['results']
    f = open('./data/{}.md'.format(COMPANY), 'a+')

    for job in listings:
        job_title = job['title']
        job_url = JOB_URL.format(job['id'])
        
        text_to_write = '{} - {}\n\n'.format(job_title, job_url)
        f.write(text_to_write)
        print(text_to_write)

    f.close()
    return

def servicenow():
    COMPANY = 'servicenow'
    API = 'https://careers.smartrecruiters.com/ServiceNow/?search=security'

    res = requests.get(API)
    if res.status_code != 200:
        print('Something wrong: {}'.format(res.content))
        return

    soup = BeautifulSoup(res.content, 'html5lib')
    raw_data = soup.find_all('li', attrs = {'class':'opening-job job column wide-7of16 medium-1of2'})

    f = open('./data/{}.md'.format(COMPANY), 'a+')

    for data in raw_data:
        job_title = data.find('h4').contents[0]
        job_url = data.find('a')['href']
        
        text_to_write = '{} - {}\n\n'.format(job_title, job_url)
        f.write(text_to_write)
        print(text_to_write)

    f.close()
    return

def spotify():
    COMPANY = 'spotify'
    API = 'https://api-dot-new-spotifyjobs-com.nw.r.appspot.com/wp-json/animal/v1/job/search?c=engineering'
    LISTING_URL = 'https://www.lifeatspotify.com/jobs/{}'

    res = requests.get(API)
    if res.status_code != 200:
        print('Something wrong: {}'.format(res.content))
        return

    listings = res.json()

    f = open('./data/{}.md'.format(COMPANY), 'a+')

    for job in listings['result']:
        if any(word in job['text'] for word in KEYWORDS):
            job_title = job['text']
            job_url = LISTING_URL.format(job['id'])
            
            text_to_write = '{} - {}\n\n'.format(job_title, job_url)
            f.write(text_to_write)
            print(text_to_write)

    f.close()
    return

# common API for companies using lever
def lever(company):
    API = LEVER_API.format(company)

    res = requests.get(API)
    if res.status_code != 200:
        print('Something wrong: {}'.format(res.content))
        return

    soup = BeautifulSoup(res.content, 'html5lib')
    raw_data = soup.find_all('div', attrs={'class': 'posting'})

    f = open('./data/{}.md'.format(company), 'a+')

    for data in raw_data:
        job_title = data.find('h5').contents[0]
        if any(word in job_title for word in KEYWORDS):
            job_title = data.find('h5').contents[0]
            job_url = data.find('a')['href']

            text_to_write = '{} - {}\n\n'.format(job_title, job_url)
            f.write(text_to_write)
            print(text_to_write)

    f.close()
    return

# common API for companies using greenhouse
def greenhouse(company):
    API = GREENHOUSE_API.format(company)

    res = requests.get(API)
    if res.status_code != 200:
        print('Something wrong: {}'.format(res.content))
        return

    listings = res.json()

    f = open('./data/{}.md'.format(company), 'a+')

    for job in listings['jobs']:
        if any(word in job['title'] for word in KEYWORDS):
            job_title = job['title']
            job_url = job['absolute_url']
            
            text_to_write = '{} - {}\n\n'.format(job_title, job_url)
            f.write(text_to_write)
            print(text_to_write)

    f.close()
    return

if __name__ == '__main__':
    misc_companies = [
        block,
        pinterest,
        servicenow,
        snap,
        spotify,
        twitter,
        uber,
    ]

    greenhouse_companies = [
        'airbnb', # greenhouse
        'airtable', # greenhouse
        'appian', # greenhouse
        # 'arcticwolf', # greenhouse
        'asana', # greenhouse
        'aurorainnovation', # greenhouse
        'benchling', # greenhouse
        'boxinc', # greenhouse
        'brex', # greenhouse
        'checkr', # greenhouse
        'chime', # greenhouse
        'cloudflare', # greenhouse
        'coinbase', # greenhouse
        'cruise', # greenhouse
        'databricks', # greenhouse
        'datadog', # greenhouse
        'doordash', # greenhouse
        'dropbox', # greenhouse
        'flexport', # greenhouse
        'grammarly', # greenhouse
        'gusto', # greenhouse
        'instacart', # greenhouse
        'lyft', # greenhouse
        'nuro', # greenhouse
        'praetorian', # greenhouse
        'qualtrics', # greenhouse
        'reddit', # greenhouse
        'retool', # greenhouse
        'rippling', # greenhouse
        'robinhood', # greenhouse
        'scaleai', # greenhouse
        'stripe', # greenhouse
    ]

    lever_companies = [
        'anduril', # lever
        'opendoor', # lever
        'plaid', # lever
        'netflix', # lever
        'verkada', # lever
    ]
    
    # miscellaneous
    for company in misc_companies:
        print_company_header(str(company.__name__))
        company()

    # lever
    for company in lever_companies:
        print_company_header(company)
        lever(company)

    # greenhouse
    for company in greenhouse_companies:
        print_company_header(company)
        greenhouse(company)
