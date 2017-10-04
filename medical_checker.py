import requests
from bs4 import BeautifulSoup
import psycopg2
from learn_env.sergeyGit.config import DB_PWD, new_bad_list


class Tracker():

    def __init__(self, url='https://tabletki.ua'):
        self.url = url


# Function make_link() returning link depend of u_choice (user choice) and of selr.url.
    def make_link(self, u_choice):
        link = self.url + '/' + u_choice + '/'
        return link


    def get_html(self, url):
        r = requests.get(url)
        return r.text


# div class='goog-trans-section' exist only in case when u_choice pills was founded in html.
# Function need to check is correct user input (u_choice) or not.
    def check_is_exist(self, u_choice):
        soup = BeautifulSoup(self.get_html(self.make_link(u_choice)), "html.parser")
        check = soup.find_all('div', class_='goog-trans-section')
        if check:
            print('True')
            return True
        else:
            print('False')
            return False


#Function get_main_list collects all elements with necessarry id's and search link with image, returning list
    def get_main_list(self, html):
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


#Function get_msg_substance find and returning all elements that apply to different group about piils (like substance,
#affects etc)
    def get_msgs_all(self, list):
        substance = list[0]         #getting indexes of all necessarry tags (like <h2>)
        indications = list[1]
        anti_indications = list[2]
        method_to_eat = list[3]
        overdose = list[4]
        try:
            affects = list[5]
        except:
            affects = list[4]
        list_substance =[]
        z = substance
        while z < (indications-1):
            z = z+1
            msg = all_el[z].text   #getting text from all elements between two tags (this text which mean all substance)
            if msg in new_bad_list: #here deleting are repetitive strings
                pass
            else:
                list_substance.append(msg.replace("'","")+'\n')

        msg_substance = []
        for i in list_substance:
            if i not in msg_substance:
                msg_substance.append(i)
        msg_substance = ''.join(msg_substance) # creating new unique message about substance of pill which user choose

        list_indications = []
        x = indications -1
        while x < anti_indications -1:
            x = x+1
            msg1 = all_el[x].text
            list_indications.append(msg1.replace("'","") + '\n')
        msg_indications = []
        for i in list_indications:
            if i not in msg_indications:
                msg_indications.append(i)
        msg_indications = ''.join(msg_indications)

        list_anti_indications = []
        c = anti_indications -1
        while c < method_to_eat -1:
            c = c+1
            msg2 = all_el[c].text
            if msg2 in new_bad_list:
               pass
            else:
                list_anti_indications.append(msg2.replace("'","")+'\n')
        msg_anti_indications = []
        for i in list_anti_indications:
            if i not in msg_anti_indications:
                msg_anti_indications.append(i)
        msg_anti_indications = ''.join(msg_anti_indications)

        list_meth_eat = []
        v = method_to_eat -1
        while v < overdose -1:
            v = v+1
            msg3 = all_el[v].text
            if msg3 in new_bad_list:
                pass
            else:
                list_meth_eat.append(msg3.replace("'","")+'\n')
        msg_meth_eat = []
        for i in list_meth_eat:
            if i not in msg_meth_eat:
                msg_meth_eat.append(i)
        msg_meth_eat = ''.join(msg_meth_eat)

        list_overdose = []
        v = overdose -1
        while v < affects - 1:
            v = v+1
            msg = all_el[v].text
            if msg in new_bad_list:
                pass
            else:
                list_overdose.append(msg.replace("'","")+'\n')
        msg_overdose = []
        for i in list_overdose:
            if i not in msg_overdose:
                msg_overdose.append(i)
        msg_overdose = ''.join(msg_overdose)

        list_affects = []
        b = affects -1
        while b < len(all_el) -13:
            b = b+1
            msg4 = all_el[b].text
            if msg4 in new_bad_list:
                pass
            else:
                list_affects.append(msg4.replace("'","")+'\n')
        msg_affects = []
        for i in list_affects:
            if i not in msg_affects:
                msg_affects.append(i)
        msg_affects = ''.join(msg_affects)
        result_dict = {                         #Creating dictionary with all messages about user choice
            'substance':msg_substance,
            'indications': msg_indications,
            'anti_indications': msg_anti_indications,
            'method_eat': msg_meth_eat,
            'affects': msg_affects,
            'overdose': msg_overdose
        }

        return result_dict


#Before start parsing the donor site, trying to search info in database (PostgeSQL).If exist - returning True
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


#Returning information from database about user choice (previously checking if exist)
    def get_db_data(self, u_choice):
        try:
            con = psycopg2.connect(host='localhost', user='sergeymoroz', password=DB_PWD, database='test1')
        except Exception as e:
            print(e)
        C = con.cursor()
        C.execute(
                "select substance, indications, anti_indications, method_eat, affects, imagelink from pharm1 "
                "where name = '{name}'".format(name=u_choice))
        rows = C.fetchone()
        return rows


#Here final message is formed. First checking if user choice exist in database, if yes - forming dictionary from
#database. If not - forming message dictionary from parsed message(get_msgs_all()) and added to database.
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
            print(rows_msg['substance'])
            return rows_msg
        else:
            obj_list = self.get_main_list(self.get_html(self.make_link(u_choice)))

            list = obj_list[0]
            print(obj_list)
            image_link = obj_list[1]
            msg = self.get_msgs_all(list)
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
            try:
                C.execute("""insert into pharm1 (name,
 substance,
  indications,
   anti_indications,
    method_eat,
     affects,
      imagelink) VALUES ('{pharm_name}', '{substances}', '{indicat}', '{anti_ind}', '{meth_eat}', '{affect}', '{image}') returning id, name, imagelink""".format(
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
            except psycopg2.ProgrammingError as e:
                print (e)
                print('Cant add to database')

            dict_to_return = {
                'substance': msg['substance'],
                'indications': msg['indications'],
                'anti_indications': msg['anti_indications'],
                'method_eat': msg['method_eat'],
                'affects': msg['affects'],
                'imagelink': image_link,
            }
            return dict_to_return


# track = Tracker()
# track.get_msg_bot('Омез')