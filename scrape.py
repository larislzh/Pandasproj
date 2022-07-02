import csv
from datetime import datetime
import requests
from bs4 import BeautifulSoup

def get_url(position):
    """Generate a url from postion with filter of last 14 days and fulltime"""
    template = 'https://sg.indeed.com/jobs?q={}&sc=0kf%3Ajt(fulltime)%3B&fromage=14'
    url = template.format(position)
    return url

def get_record(card):
    atag = card.h2.a
    job_title = card.find('a').text
    job_url = 'https://sg.indeed.com' + atag.get('href')
    company = card.find('span', 'companyName').text.strip()
    location = card.find('div', 'companyLocation').text.strip()
    job_summary = card.find('div', 'job-snippet').text.strip().replace('\n', ' ').replace('\r', ' ')
    job_quali = soup2.find_all('ul')[-3].get_text().strip().replace('\n', ' ').replace('\r', ' ')
    day_scraped = datetime.today().strftime('%d-%m-%y')
    try:
        job_salary = card.find('div', class_ = 'attribute_snippet').text
        job_salary.split("</svg>")[-1]
    except AttributeError:
        job_salary = ''
        
    record = (job_title, company, location, day_scraped, job_summary, job_quali, job_salary, job_url)
    
    return record

def main(position):
    records = []
    url = get_url(position)
    
    #Extract the job data
    while True:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "lxml")
        cards = soup.find_all('div', class_ = 'slider_item')

        for card in cards:
            for urls in job_url:
                response2 = requests.get(job_url)
                soup2 = BeautifulSoup(response2.text, "lxml")
                job_summary = card.find('div', 'job-snippet').text.strip().replace('\n', ' ').replace('\r', ' ')
                
            record = get_record(card)
            records.append(record)
            
            
        try:
            url = 'https://sg.indeed.com' + soup.find('a', {'aria-label': 'Next'}).get('href')
        except AttributeError:
            break
            
        #Save the job data
    with open(f'{position}.csv', 'w', newline = '', encoding = 'utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['JobTitle', 'Company', 'Location', 'ExtractDate', 'Summary', 'Qualifications', 'Salary', 'JobUrl'])
        writer.writerows(records)
