import csv
import re
import requests
import time
from bs4 import BeautifulSoup
import sys
import psycopg2
from learn_env.sergeyGit.config import DB_PWD


#u_choice = 'Нафтизин'

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


    def eat_method(self, html):
        #html = self.get_html(self.make_link(u_choice))
        soup = BeautifulSoup(html, "html.parser")
        list = []
        names = soup.find('div', class_='goog-trans-section')
        global all_el
        try:
            all_el = names.find_all(class_=None)
        except AttributeError:
            print('Не корректное название лекарства')
            return False
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

        image_obj = soup.find('div', class_='swiper-wrapper')
        image_link = 'http:' + image_obj.find('img').get('src')
        obj_list = [list, image_link]
        return obj_list


    def get_msg_substance(self, list):
        substance = list[0]
        indications = list[1]
        anti_indications = list[2]
        method_to_eat = list[3]
        affects = list[4]
        list_substance =[]                                              #this part of code is for MSG about substance
        z = substance
        while z < (indications-1):
            z = z+1
            msg = all_el[z].text
            if msg == 'діюча речовина:' or \
                            msg == 'допоміжні речовини:' or \
                            msg == 'допоміжні речовини: ' or \
                            msg == 'діючі речовини: ' or \
                            msg == 'діючі речовини:' or \
                            msg == 'Основні фізико-хімічні властивості:' or \
                            msg == 'Основні фізико-хімічні властивості: ' or \
                            msg == 'Абсорбція' or \
                            msg == 'Розподіл.' or \
                            msg =='Біотрансформація.' or \
                            msg == '®' or \
                            msg == '® ' or \
                            msg == 'In vitro' or \
                            msg == 'In vitro ' or \
                            msg == 'Виведення.':
                pass
            else:
                list_substance.append(msg+'\n')
        #print(list_substance)
        msg_substance = []
        for i in list_substance:
            if i not in msg_substance:
                msg_substance.append(i)
        msg_substance = ''.join(msg_substance)
        #print(msg_substance)                                                                         #       end here


        list_indications = []                                           # this part of code for MSG about indications
        x = indications -1
        while x < anti_indications -1:
            x = x+1
            msg1 = all_el[x].text
            list_indications.append(msg1 + '\n')
        msg_indications = []
        for i in list_indications:
            if i not in msg_indications:
                msg_indications.append(i)
        msg_indications = ''.join(msg_indications)
        #print(msg_indications)                                                    #end here


        list_anti_indications = []                                 # this part of code for MSG about antiindications
        c = anti_indications -1
        while c < method_to_eat -1:
            c = c+1
            msg2 = all_el[c].text
            if msg2 == 'Спричинена вмістом парацетамолу:' or \
                            msg2 == 'Спричинена вмістом кодеїну: ' or \
                            msg2 == 'Спричинена вмістом кофеїну: ' or \
                            msg2 == 'Здатність впливати на швидкість реакції при керуванні автотранспортом або ' \
                                    'іншими механізмами.' or \
                            msg2 == 'Застосування у період вагітності або годування груддю.' or \
                            msg2 == 'Вагітність. ' or \
                            msg2 == 'Годування груддю. ' or \
                            msg2 == '®' or \
                            msg2 == 'Дослідження in vitro.' or \
                            msg2 == '® ' or \
                            msg2 == ' in vitro.' or \
                            msg2 == 'in vitro' or \
                            msg2 == 'Дослідження in vivo.' or \
                            msg2 == ' in vivo.' or \
                            msg2 == 'in vivo.' or \
                            msg2 == 'Підвищена чутливість до активної речовини або будь-якої з допоміжних' \
                                    ' речовин препарату.' or \
                            msg2 == '50' or \
                            msg2 == 'Втрата слуху.' or \
                            msg2 == 'Захворювання, що передаються статевим шляхом.' or \
                            msg2 == 'Вплив на кровотечі. ' or \
                            msg2 == '®' or \
                            msg2 == 'Вплив на зір. ':

               pass
            else:
                list_anti_indications.append(msg2+'\n')
        #print(list_anti_indications)
        msg_anti_indications = []
        for i in list_anti_indications:
            if i not in msg_anti_indications:
                msg_anti_indications.append(i)
        msg_anti_indications = ''.join(msg_anti_indications)
        #print(msg_anti_indications)                                                     # end here


        list_meth_eat = []
        v = method_to_eat -1
        while v < affects -1:
            v = v+1
            msg3 = all_el[v].text
            if msg3 == 'Дорослі:' or \
                msg3 == 'Дорослі: ' or \
                msg3 == 'Діти. ' or \
                msg3 == 'Діти.' or \
                msg3 == 'Симптоми передозування парацетамолом.' or \
                msg3 == 'Діти' or \
                msg3 == 'Симптоми передозування кофеїном. ' or \
                msg3 == 'Спосіб введення.' or \
                msg3 == '®' or \
                msg3 == '® ' or \
                msg3 == '®\xa0' or \
                msg3 == 'Симптоми передозування кодеїном.':
                pass
            else:
                list_meth_eat.append(msg3+'\n')
        #print(list_meth_eat)
        msg_meth_eat = []
        for i in list_meth_eat:
            if i not in msg_meth_eat:
                msg_meth_eat.append(i)
        msg_meth_eat = ''.join(msg_meth_eat)
        #print(msg_meth_eat)

        list_affects = []
        b = affects -1
        while b < len(all_el) -13: #len(all_el) -2:
            b = b+1
            msg4 = all_el[b].text
            if msg4 == 'З боку кровоносної та лімфатичної системи:' or \
                msg4 == 'З боку імунної системи:' or \
                msg4 == 'З боку шкіри та підшкірної тканини:' or \
                msg4 == 'Порушення з боку гепатобіліарної системи:' or \
                msg4 == 'З боку центральної нервової системи:' or \
                msg4 == 'Психічні порушення:' or \
                msg4 == 'З боку серця:' or \
                msg4 == 'З боку нирок і сечовидільної системи' or \
                msg4 == 'Інші:' or \
                msg4 == 'Порушення з боку органів дихання, грудної клітини та середостіння:' or \
                msg4 == '® ' or \
                msg4 == 'з боку нервової системи' or \
                msg4 == 'З боку дихальної системи, органів грудної клітки та середостіння:' or \
                msg4 == 'з боку серцево-судинної системи' or \
                msg4 == 'З боку травного тракту:':
                pass
            else:
                list_affects.append(msg4+'\n')
        msg_affects = []
        for i in list_affects:
            if i not in msg_affects:
                msg_affects.append(i)
        msg_affects = ''.join(msg_affects)
        #print(msg_affects)
        result_dict = {
            'substance':msg_substance,
            'indications': msg_indications,
            'anti_indications': msg_indications,
            'method_eat': msg_meth_eat,
            'affects': msg_affects
        }

        return result_dict


    def get_msg_bot(self, u_choice):

        obj_list = self.eat_method(self.get_html(self.make_link(u_choice)))
        try:
            list = obj_list[0]
        except:
            print('Не корректное название препарата')
        image_link = obj_list[1]
        print(image_link)
        msg = self.get_msg_substance(list)
        print(msg['substance'])
        try:
            con = psycopg2.connect(host='localhost', user='sergeymoroz', password=DB_PWD, database='test1')
        except Exception as e:
            print(e)
        C = con.cursor()
        C.execute("""insert into pharm1 (name,
 substance,
  indications,
   anti_indications,
    method_eat,
     affects,
      imagelink) VALUES ('{pharm_name}', '{substances}', '{indicat}', '{anti_ind}', '{meth_eat}', '{affect}', '{image}') returning id, affects""".format(
                                                  pharm_name=u_choice,
                                                  substances=str(msg['substance']),
                                                  indicat=str(msg['anti_indications']),
                                                  anti_ind=str(msg['anti_indications']),
                                                  meth_eat=str(msg['method_eat']),
                                                  affect=str(msg['affects']),
                                                  image=image_link))
        con.commit()
        rows = C.fetchall()
        print(rows)

track = Tracker()
track.get_msg_bot('Виагра')
# if track.eat_method() == False:
#     print('False')
# print(track.eat_method()[3])


