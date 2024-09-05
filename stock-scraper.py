from bs4 import BeautifulSoup as bs
import requests
import pandas as pd

start_url = 'https://www.centralcharts.com/'
pages = []
for i in range(5):
    end_url = 'en/price-list-ranking/ALL/desc/ts_19-us-nasdaq-stocks--qc_3-previous-close-change?p='
    #this end_url is interchangable with other stock markets; this specific one is related to NASDAQ
    new_page = start_url+end_url+str(i)
    pages.append(new_page)

stocks = [] #looking for: name, price, percent change from previous, volume (i.e. total # shares)
for page in pages:
    page_html = requests.get(page).text
    soup = bs(page_html, 'lxml') #lxml is our specific parser in this occassion; works with broken html
