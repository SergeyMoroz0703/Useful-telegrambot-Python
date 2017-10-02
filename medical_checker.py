import csv
import re
import requests
import time
from bs4 import BeautifulSoup
import sys
import psycopg2
from learn_env.sergeyGit.config import DB_PWD, new_bad_list


class Tracker():

    def __init__(self, url='https://tabletki.ua'):
        self.url = url


    def make_link(self, u_choice):
        link = self.url + '/' + u_choice + '/'
        #print(link)
        return link


    def check_is_exist(self, u_choice):
        soup = BeautifulSoup(self.get_html(self.make_link(u_choice)), "html.parser")
        check = soup.find_all('div', class_='goog-trans-section')
        if check:
            print('True')
            return True
        else:
            print('False')
            return False


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
            elif all_el[i] == soup.find('h2', id='Передозировка'):
                list.append(i)
            elif all_el[i] == soup.find('h2', id='Побочные_эффекты'):
                list.append(i)
            else:
                pass
        image_obj = soup.find('div', class_='swiper-wrapper')
        try:
            image_link = 'http:' + image_obj.find('img').get('src')
            obj_list = [list, image_link]
        except AttributeError:
            print('Not image for this pharmacy')
            obj_list = [list, 'no_image_links']
        return obj_list


    def get_msg_substance(self, list):
        substance = list[0]
        indications = list[1]
        anti_indications = list[2]
        method_to_eat = list[3]
        overdose = list[4]
        try:
            affects = list[5]
        except:
            affects = list[4]
        list_substance =[]                                              #this part of code is for MSG about substance
        z = substance
        while z < (indications-1):
            z = z+1
            msg = all_el[z].text
            if msg in new_bad_list:
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
        #print(list_indications)
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
            if msg2 in new_bad_list:
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
        while v < overdose -1:
            v = v+1
            msg3 = all_el[v].text
            if msg3 in new_bad_list:
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



        list_overdose = []
        v = overdose -1
        while v < affects - 1:
            v = v+1
            msg = all_el[v].text
            if msg in new_bad_list:
                pass
            else:
                list_overdose.append(msg+'\n')
        msg_overdose = []
        for i in list_overdose:
            if i not in msg_overdose:
                msg_overdose.append(i)
        msg_overdose = ''.join(msg_overdose)




        list_affects = []
        b = affects -1
        while b < len(all_el) -13: #len(all_el) -2:
            b = b+1
            msg4 = all_el[b].text
            if msg4 in new_bad_list:
                pass
            else:
                list_affects.append(msg4+'\n')
        #print(list_affects)
        msg_affects = []
        for i in list_affects:
            if i not in msg_affects:
                msg_affects.append(i)
        msg_affects = ''.join(msg_affects)
        #print(msg_affects)
        result_dict = {
            'substance':msg_substance,
            'indications': msg_indications,
            'anti_indications': msg_anti_indications,
            'method_eat': msg_meth_eat,
            'affects': msg_affects,
            'overdose': msg_overdose
        }

        return result_dict


    def check_exist_database(self, u_choice):
        try:
            con = psycopg2.connect(host='localhost', user='sergeymoroz', password=DB_PWD, database='test1')
        except Exception as e:
            print(e)
        C = con.cursor()
        C.execute("select name from pharm1 where name = '{name}'".format(name=u_choice))
        if len(C.fetchall()) > 0:
            return True
        else:
            return False


    def get_db_data(self, u_choice):
        try:
            con = psycopg2.connect(host='localhost', user='sergeymoroz', password=DB_PWD, database='test1')
        except Exception as e:
            print(e)
        C = con.cursor()
        # C.execute("select name from pharm1 where name = '{name}'".format(name=u_choice))
        C.execute(
                "select substance, indications, anti_indications, method_eat, affects, imagelink from pharm1 where name = '{name}'".format(
                    name=u_choice))
        rows = C.fetchone()
        return rows


    def get_msg_bot(self, u_choice):
        if self.check_exist_database(u_choice) == True:
            print('Connecting to database')
            rows = self.get_db_data(u_choice)
            msg_substance = rows[0]
            msg_indications = rows[1]
            msg_antiindications = rows[2]
            msg_method_eat = rows[3]
            msg_affects = rows[4]
            image_link = rows[5]
            rows_msg = {
                'substance':rows[0],
                'indications':rows[1],
                'anti_indications':rows[2],
                'method_eat':rows[3],
                'affects':rows[4],
                'imagelink':rows[5],
            }
            return rows_msg
        else:
            obj_list = self.eat_method(self.get_html(self.make_link(u_choice)))
            try:
                list = obj_list[0]
                print(obj_list)
            except:
                print('Не корректное название препарата')
            image_link = obj_list[1]
            msg = self.get_msg_substance(list)
            msg_substance = msg['substance']
            msg_indications = msg['indications']
            msg_antiindications = msg['anti_indications']
            msg_method_eat = msg['method_eat']
            msg_affects = msg['affects']
            msg_overdose = msg['overdose']

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
      imagelink) VALUES ('{pharm_name}', '{substances}', '{indicat}', '{anti_ind}', '{meth_eat}', '{affect}', '{image}') returning id, name""".format(
                                                  pharm_name=u_choice,
                                                  substances=str(msg['substance']),
                                                  indicat=str(msg['indications']),
                                                  anti_ind=str(msg['anti_indications']),
                                                  meth_eat=str(msg['method_eat']),
                                                  affect=str(msg['affects']),
                                                  image=image_link))
            con.commit()
            rowss = C.fetchall()
            print(rowss)


            return msg



# track = Tracker()
# track.check_is_exist('Виагра')



