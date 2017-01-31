# -*- coding: UTF-8 -*-
import requests
import datetime
import os
from bs4 import BeautifulSoup
import codecs
import re
base_url = '/Users/zyang2/PycharmProjects/EstatesSearch/data/5i5j'
folder = datetime.date.today().strftime('%Y%m%d').__str__()
if not os.path.exists(os.path.join(base_url,folder)):
    os.mkdir(os.path.join(base_url,folder))
base_url = os.path.join(base_url,folder)
i = 1


headers = {u'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_2) AppleWebKit/602.3.12 (KHTML, like Gecko) Version/10.0.2 Safari/602.3.12',
           u'Connection':'keep-alive',
           u'Referer':'http://m.5i5j.com/bj/ershoufang',
           u'X-Requested-With':'XMLHttpRequest',
           u'Accept':'text/html, */*; q=0.01'}
more_data = True
str_vec = []
while(more_data):
    get_params = {'page':i,'pathInfo':''}
    r = requests.get('http://m.5i5j.com/bj/ershoufang/getlist',params=get_params,headers=headers)
    r.encoding = 'utf-8'
    #print r.text
    more_data = False
    if re.search('-- list --',r.text):
        more_data = True
    str_vec.append(r.text)
    if more_data == False or i % 1000 == 999:
        f = codecs.open(os.path.join(base_url, i.__str__()) + '.html', 'w','utf-8')
        f.writelines(str_vec)
        str_vec = []
        f.close()
    if i % 10 == 9:
        print i
    i += 1
    #print type(r.text)


#
# bs = BeautifulSoup(r.text,"html.parser")
# li_list = bs.find_all('li')
#
#
# # Pick Squre and Price per squre
# for li_item in li_list:
#     [p1,p2] = li_item.find('div',attrs={'class':'list_jiage'}).find_all('p')
#     print p1.text
#     print p2.text