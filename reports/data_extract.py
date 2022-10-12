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
YEAR_START = 2004
YEAR_END = 2021
LIST_PATTERN = 'http://www.cikrf.ru/politparty/finance/svodn_otchet_%s.php'

YEARS = range(YEAR_END, YEAR_START, -1)

class DataExtractor:
    """Data extractor for EGE"""

    def __init__(self):
        pass

    def extract_catalog(self):
        f = open(CATALOG_FILE, 'w', encoding='utf8')
        keys = ['year', 'number', 'party_name', 'report_date', 'report_url', 'verify_url']
        s = ('\t'.join(keys)) + '\n'
        f.write(s)
        for year in YEARS:
            listurl = LIST_PATTERN % str(year)[2:]
            print (listurl)
            data = requests.get(listurl).text
            soup = BeautifulSoup(data)
            body = soup.find('table')#, attrs={'class': 'greyborders'})
            if body is None: continue
            rows = body.find('tbody').findAll('tr')
            n = 0
            for row in rows:
                n += 1
                if n == 1: continue
                cells = row.findAll('td')
                if len(cells) != 5:
                    print('Row %d not 5 cells' % (n))
                    continue
                item = [str(year),]
                item.append(cells[0].text.strip())
                print(cells[3])
                item.append(cells[1].text.strip())
                item.append(cells[2].text)
                cell = cells[3].find('a')
                item.append(cell['href'] if cell else "")
                cell = cells[4].find('a')
                item.append(cell['href'] if cell else "")
                print(item)
                s = ('\t'.join(item)).replace('\n', ' ') + '\n'
                f.write(s)
        f.close()


    def extract_all_raw(self):
        reader = csv.DictReader(open(CATALOG_FILE, 'r', encoding='utf8'), delimiter="\t")
        for item in reader:
            url = item['report_url']
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
#    ext.extract_all_raw()


