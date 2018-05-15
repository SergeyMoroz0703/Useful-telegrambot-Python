import csv
import re
import requests
import time
from bs4 import BeautifulSoup

class Tracker():

    def __init__(self, url='https://coinmarketcap.com/all/views/all'):
        self.url = url

    def get_html(self, url):
        r = requests.get(url)
        #    print(r.text)
        return r.text

    def get_all_links(self, html):
        soup = BeautifulSoup(html, "html.parser")
        tds = soup.find('table', id='currencies-all').find_all('td', class_='currency-name')
        links = []
        for td in tds:
            a = td.find('a').get('href')
            links.append('https://coinmarketcap.com' + a)
        return links


    def get_html_data(self, html_links):
        soup = BeautifulSoup(html_links, "html.parser")
        try:
            name = soup.find('h1', class_='text-large').text.strip().replace(" ", "")
        except:
            name = ''
        try:
            price = soup.find('span', id='quote_price').text.strip()
        except:
            price = ''

        data = {'name': name.split('\n', 1)[1], 'price': price}
        print(data)
        return data


    def main_price(self):
        try:
            btc_price = (self.get_html_data(self.get_html('https://coinmarketcap.com/currencies/bitcoin/')))
            eth_price = (self.get_html_data(self.get_html('https://coinmarketcap.com/currencies/ethereum/')))
            btc_hash_price = (self.get_html_data(self.get_html('https://coinmarketcap.com/currencies/bitcoin-cash/')))
            return btc_price,eth_price,btc_hash_price
        except requests.exceptions.ConnectionError:
            print('Connection error, try again please')


    def search_price(self, u_choice):
        try:
            all_links = self.get_all_links(self.get_html(self.url))
            #u_choice = input('enter currency name')
            if u_choice == 'bytecoin':
                u_choice = 'bytecoin-bcn'
            if str('https://coinmarketcap.com/currencies/' + u_choice + '/') in all_links:
                try:
                    currency_page = self.get_html('https://coinmarketcap.com/currencies/' + u_choice + '/')
                    last_response = self.get_html_data(currency_page)
                    #time.sleep(1)
                    return last_response
                except requests.exceptions.ConnectionError:
                    print('Connection error, try again please')
            else:
                print('I dont know this cryptocurrency: ' + u_choice + '. Please, try again.')
                return None
        except requests.exceptions.ConnectionError:
            print('Connection error, try again please')
