import csv
import re
import requests
import time
from bs4 import BeautifulSoup


dicts = {}
#u_choice = input("Введите имя препарата: ")
u_choice = 'Солпадеин'

class Tracker():

    def __init__(self, url='https://tabletki.ua'):
        self.url = url


    def make_link(self, u_choice):
        link = self.url + '/' + u_choice + '/'
        #print(link)
        return link


    def get_html(self, url):
        r = requests.get(url)
        #print(r.text)
        return r.text


    def get_consists(self):
        html = self.get_html(self.make_link(u_choice))
        soup = BeautifulSoup(html, "html.parser")
        names = soup.find_all('i')
        consists = soup.find_all('p')
        active_substance = {'active_substance': consists[0].text}
        helper_substance = {'helper_substance':  consists[1].text.replace(u'\xa0', ' ')}
        #print(active_substance, helper_substance)
        return active_substance, helper_substance

    def get_medicinal_form(self):
        html = self.get_html(self.make_link(u_choice))
        soup = BeautifulSoup(html, "html.parser")
        names = soup.find_all('i')
        consists = soup.find_all('p')
        medicinal_form = {'medicinal_form': consists[2].text.replace(u'\xa0', ' ') + consists[3].text.replace(u'\xa0', ' ')}
        print(medicinal_form)


    def get_pharm_prop(self):
        html = self.get_html(self.make_link(u_choice))
        soup = BeautifulSoup(html, "html.parser")
        names = soup.find_all('i')
        consists = soup.find_all('p')
        pharm_prop = {'pharm_prop': consists[5].text + consists[6].text,
                      'pharm_prop_kin': consists[7].text + consists[8].text + consists[9].text + consists[10].text}
        print(pharm_prop['pharm_prop_kin'])


    def eat_method(self):
        html = self.get_html(self.make_link(u_choice))
        soup = BeautifulSoup(html, "html.parser")
        list = []
        names = soup.find('div', class_='goog-trans-section')
        global all_el
        all_el = names.find_all(class_=None)
        for i in range(0,len(all_el)):
            if all_el[i] == soup.find('h2', id='Состав'):
                list.append(i)
            elif all_el[i] == soup.find('h2', id='Показания'):
                list.append(i)
            elif all_el[i] == soup.find('h2', id='Противопоказания'):
                list.append(i)
            elif all_el[i] == soup.find('h2', id='Способ_применения_и_дозы'):
                list.append(i)
            elif all_el[i] == soup.find('h2', id='Побочные_эффекты'):
                list.append(i)
        return list


    def get_msg_substance(self):
        # html = self.get_html(self.make_link(u_choice))
        # soup = BeautifulSoup(html, "html.parser")
        # names = soup.find('div', class_='goog-trans-section')
        # all_el = names.find_all(class_=False)
        list = self.eat_method()
        substance = list[0]
        indications = list[1]
        anti_indications = list[2]
        method_to_eat = list[3]
        affects = list[4]
        # list_substance =[]                                                                                #this part of code is for MSG about substance
        # z = substance
        # while z < (indications-1):
        #     z = z+1
        #     msg = all_el[z].text
        #     #print(msg)
        #     #time.sleep(1)
        #     if msg == 'діюча речовина:' or \
        #                     msg == 'допоміжні речовини:' or \
        #                     msg == 'допоміжні речовини: ' or \
        #                     msg == 'діючі речовини: ' or \
        #                     msg == 'діючі речовини:' or \
        #                     msg == 'Основні фізико-хімічні властивості:' or \
        #                     msg == 'Основні фізико-хімічні властивості: ' or \
        #                     msg == 'Абсорбція' or \
        #                     msg == 'Розподіл.' or \
        #                     msg =='Біотрансформація.' or \
        #                     msg == 'Виведення.':
        #         pass
        #     else:
        #         list_substance.append(msg+'\n')
        # print(list_substance)
        # msg_substance = []
        # for i in list_substance:
        #     if i not in msg_substance:
        #         msg_substance.append(i)
        # msg_substance = ''.join(msg_substance)
        # print(msg_substance)                                                                              #       end here


        list_indications = []
        x = indications -1
        while x < anti_indications -1:
            x = x+1
            msg1 = all_el[x].text
            list_indications.append(msg1 + '\n')

        msg_indications = []
        print(list_indications)






        #return msg_substance



track = Tracker()
track.get_msg_substance()



