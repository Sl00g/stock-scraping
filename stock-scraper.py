from bs4 import BeautifulSoup as bs
import requests
import pandas as pd
import time

def makePages():
    start_url = 'https://www.centralcharts.com/'
    pages = []
    for i in range(1,5):
        end_url = 'en/price-list-ranking/ALL/desc/ts_20-us-tech-150--qc_2-daily-change?p='
        #this end_url is interchangable with other stock markets; this specific one is related to US' Tech150
        new_page = start_url+end_url+str(i)
        pages.append(new_page)
    return pages

def getListTD(stock): #creates a list of td elements corresponding to a certain stock
    return stock.find_all('td')

def scrape_data():
    #scrape info from other sites: intrinsic value, stock abbreviation
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
            stock_price = (float)(tdList[1].span.text.replace(',',''))
            stock_percent_change = tdList[2].span.text
            stock_volume = (int)(tdList[6].span.text.replace(',', ''))
            new_stock = [stock_name, stock_price, stock_percent_change, stock_volume]
            stocks.append(new_stock)
    #get stock link

    df = pd.DataFrame(stocks, columns=['Stock', 'Current Price', '%Change', '# of Shares'])
    #df.to_csv('stocks.csv')
    print('Successfully scraped information.')

    #should be able to carry out operations like:
    #find top performing stock of the day (most percent up)
    #sort by price
    #sort alphabetically
    #get intrinsic price
    #should introduce a watchlist; specific stocks to display

    #first, you should get user input, maybe amount of cash they want to invest
    #give them stocks that meet their cash price, include link
    print('How much cash do you plan to invest?')
    cash = (float)(input('$'))
    #might want to loop until you get an actual float, figure out later

    condition = df['Current Price'] <= cash
    df_cash = df[condition] #this formats dataframe so that it only includes stocks within cash range

    q = 0
    asc = [True, True, True, False]
    #this array makes it so that things can be sorted ascending or descending
    #the dataframe keeps track of all the filters, but I'm trying to find a way to display them. 
    #I'm also trying to find a way to reset them... 

    while q==0:
        print('Filter information: \n1. Alphabetically\n2. By Price\n3. By %Change\n4. Number of Shares\n5. Quit')
        filter = (int)(input())
        if(filter==1):
            df_cash = df_cash.sort_values(by="Stock", ascending=asc[0])
        elif(filter==2):
            df_cash = df_cash.sort_values(by="Current Price", ascending = asc[1])
        elif(filter==3):
            df_cash = df_cash.sort_values(by="%Change", ascending = asc[2])
        elif(filter==4):
            df_cash = df_cash.sort_values(by="# of Shares", ascending=asc[3])
        else:
            q = 1
            break
        asc[filter-1] = not asc[filter-1]
        print(df_cash + '\n')


    #until they quit, keep prompting them with options
    #idea: have a stock library for them to add for a watchlist

    #could also use some formatting prettiness; getting rid of numbers on the side, spacing out further
    #idea: maybe add a graph

        
    #idea: they should be able to search for a stock; ignore their available cash


if __name__ == '__main__':
    while True:
        scrape_data()
        time.sleep(3600) 
        #scrapes hourly
        #idea: keep it in a database; scrape daily, keep data on these stocks