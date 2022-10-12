#!/usr/bin/env python
# coding: utf8
"""
Data extractor (cikrf.ru) party reports
"""
import csv
import json
import os, os.path
from urllib.parse import urljoin
from bs4 import BeautifulSoup, BeautifulStoneSoup
import time
import requests
BASE_URL = 'http://cikrf.ru'

CATALOG_FILE = 'data/datasets.csv'
YEARS = ['2005', '2006', '2007', '2008', '2009', '2010', '2011', '2012', '2013', '2014', '2015', '2016', '2017', '2018', '2019', '2020']
LIST_PATTERN = 'http://www.cikrf.ru/politparty/finance/%s/'


class DataExtractor:
    """Data extractor for EGE"""

    def __init__(self):
        pass

    def extract_catalog(self):
        f = open(CATALOG_FILE, 'w', encoding='utf8')
        keys = ['year', 'category_name', 'category_url', 'name', 'url']
        s = ('\t'.join(keys)) + '\n'
        f.write(s)
        for year in YEARS:
            listurl = LIST_PATTERN % year
            print (listurl)
            data = requests.get(listurl).text
            soup = BeautifulSoup(data)
            body = soup.find('div', attrs={'class': 'content_body'}).find('ul')
            if body is None: continue
            lis = body.findAll('li')
            catname = u'Сведения о поступлении и расходовании средств политических партий за %s год' % year
            for li in lis:
                ufile = li.find('a')
                name = ufile.string
                weburl = urljoin(BASE_URL, ufile['href'])
                r = [year, catname, listurl, name, weburl]
                print(name, weburl)
                s = ('\t'.join(r))+ '\n'
                f.write(s)
        f.close()


    def extract_all_raw(self):
        reader = csv.DictReader(open(CATALOG_FILE, 'r', encoding='utf8'), delimiter="\t")
        for item in reader:
            url = item['url']
            filename = url.rsplit('/')[-1]
            filepath = 'data/raw/'
            if not os.path.exists(filepath + filename):
                f = open(filepath + filename, 'wb')
                f.write(requests.get(url).content)
                print('Downloaded', url)
            else:
                print('Skipped', url)


if __name__ == "__main__":
    ext = DataExtractor()
    ext.extract_catalog()
    ext.extract_all_raw()


