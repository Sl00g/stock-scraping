from bs4 import BeautifulSoup as bs
import requests
import pandas as pd

def makePages(): #can modify this later so that you are using a user inputted url
    start_url = 'https://www.centralcharts.com/'
    pages = []
    for i in range(1,2):
        end_url = 'en/price-list-ranking/ALL/desc/ts_19-us-nasdaq-stocks--qc_3-previous-close-change?p='
        #this end_url is interchangable with other stock markets; this specific one is related to NASDAQ
        new_page = start_url+end_url+str(i)
        pages.append(new_page)
    return pages

def getListTD(stock): #creates a list of td elements corresponding to a certain stock
    return stock.find_all('td')

pages = makePages()
stocks = [] #looking for: name, price, percent change from previous, volume (i.e. total # shares)
for page in pages:
    page_html = requests.get(page).text
    soup = bs(page_html, 'lxml') #lxml is our specific parser in this occassion; works with broken html
    table = soup.find('table', class_ = 'tabMini tabQuotes').tbody #there is a tr element in the table head, we don't want that
    stocks_html = table.find_all('tr')
    for stock in stocks_html:
        tdList = getListTD(stock)
        stock_name = tdList[0].a.text
        stock_price = tdList[1].span.text
        stock_percent_change = tdList[2].span.text
        stock_volume = tdList[6].span.text
        new_stock = [stock_name, stock_price, stock_percent_change, stock_volume]
        stocks.append(new_stock)

df = pd.DataFrame(stocks, columns=['Stock', 'Current Price', '%Change', '# of Shares'])
df.to_csv('stocks.csv')
print('Created csv!')
