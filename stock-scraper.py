from bs4 import BeautifulSoup as bs
import requests
import pandas as pd

start_url = 'https://www.centralcharts.com/'
pages = []
for page in range(5):
    end_url = 'en/price-list-ranking/ALL/desc/ts_19-us-nasdaq-stocks--qc_3-previous-close-change?p='
    new_page = start_url+end_url+str(page)
    pages.append(new_page)



