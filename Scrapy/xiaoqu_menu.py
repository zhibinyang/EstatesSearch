# -*- coding: UTF-8 -*-
import requests
from bs4 import BeautifulSoup
import xiaoqu
import config
import time
import re
import database
import sys
import datetime
import os
class xiaoqu_menu:
    def __init__(self,base_url,district,mode='web',base_path=None):
        self.district = district
        if mode=='web':
            url = base_url + district + '/'
            print "Base URL:",url
            if base_path:
                self.path = os.path.join(base_path, self.district)
            else:
                self.path = None
            headers = {'User-Agent':'Safari/537.11',
                        'Accept':'text/html;q=0.9,*/*;q=0.8',
                        'Accept-Charset':'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
                        'Accept-Encoding':'gzip',
                        }
            r = requests.get(url,headers=headers)
            r.encoding = 'utf-8'
            self.basic_parser(r)
            self.baseurl = url
        elif base_path:
            print "Local File District: ",self.district
            self.path = os.path.join(base_path,self.district)
        else:
            print "Parameter error"
            sys.exit(-2)

    def basic_parser(self,result):
        # Parsed total amount, menu and page amount
        bs = BeautifulSoup(result.text, "html.parser")
        try:
            num_div = bs.find_all('div',attrs={'class':"resultDes"})
            if len(num_div) != 1:
                raise RuntimeError("Xiaoqu amount in Menu is not unique")
            num_span = num_div[0].h2.span
            self.amount = int(num_span.text.strip())
        except Exception as e:
            self.amount = 0
            print bs.text.encode('utf-8')
            print e
            print "Xiaoqu amount structure changed, need to check this part"
            print "May Got Blocked, Exiting"
            sys.exit(1)
        try:
            xiaoqu_ul = bs.find_all('ul',attrs={'class':'listContent'})
            if len(xiaoqu_ul) != 1:
                raise RuntimeError("Xiaoqu list in Menu is not unique")
            self.xiaoqu_ul = xiaoqu_ul[0] # return BS node
        except Exception as e:
            print e
            print "Xiaoqu list structure changed, need to check this part"
        try:
            page_div = bs.find_all('div',attrs={'comp-module':'page'})
            page_string = page_div[0].attrs['page-data']
            self.total_page = eval(page_string)['totalPage']
        except Exception as e:
            self.total_page = 0
            print e
            print "Xiaoqu list page structure changed, need to check this part"

    def parser(self):
        result_vector = []
        db = database.DatabaseInsert()
        for i in range(self.total_page):
            print "Page",i+1
            url = self.baseurl + config.page_key + (i+1).__str__() + '/'
            print "Current URL:",url
            r = requests.get(url)
            r.encoding = 'utf-8'
            bs = BeautifulSoup(r.text, "html.parser")
            if self.path:
                if not os.path.exists(self.path):
                    os.mkdir(self.path)
                f = open(os.path.join(self.path,config.page_key + (i+1).__str__()), 'w')
                f.write(r.text.encode('utf-8'))
            xiaoqu_ul = bs.find_all('ul',attrs={'class':'listContent'})
            if len(xiaoqu_ul) != 1:
                raise RuntimeError("Xiaoqu list in Menu is not unique")
            xiaoqu_li_list = xiaoqu_ul[0].find_all('li', attrs={'class': 'clear xiaoquListItem'})
            for xiaoqu_li in xiaoqu_li_list:
                try:
                    xq = self.xiaoqu_basic_parser(xiaoqu_li)
                    self.xiaoqu_price_parser(xiaoqu_li,xq)
                    #db.insert('xiaoqu', ['xiaoqu', 'district', 'year', 'price','date'], [xq.getName(), xq.getDistrict(), xq.getYear(), xq.getPrice(),datetime.date.today()])
                    # print xq.getName(),xq.getDistrict(),xq.getYear(),xq.getPrice()
                except Exception as e:
                    print e
                #print xiaoqu_li
            time.sleep(5)
    def local_parser(self):
        result_vector = []
        db = database.DatabaseInsert()
        if not os.path.exists(self.path):
            os.mkdir(self.path)
        for file in os.listdir(self.path):
            f = open(file,'r')
            bs = BeautifulSoup(f, "html.parser")
            xiaoqu_ul = bs.find_all('ul',attrs={'class':'listContent'})
            if len(xiaoqu_ul) != 1:
                raise RuntimeError("Xiaoqu list in Menu is not unique")
            xiaoqu_li_list = xiaoqu_ul[0].find_all('li', attrs={'class': 'clear xiaoquListItem'})
            for xiaoqu_li in xiaoqu_li_list:
                try:
                    xq = self.xiaoqu_basic_parser(xiaoqu_li)
                    self.xiaoqu_price_parser(xiaoqu_li,xq)
                    db.insert('xiaoqu', ['xiaoqu', 'district', 'year', 'price','date'], [xq.getName(), xq.getDistrict(), xq.getYear(), xq.getPrice(),datetime.date.today()])
                    # print xq.getName(),xq.getDistrict(),xq.getYear(),xq.getPrice()
                except Exception as e:
                    print e
                #print xiaoqu_li
            time.sleep(1)
    def xiaoqu_basic_parser(self,xiaoqu_bs):
        # Get xiaoqu Title
        title_div = xiaoqu_bs.find_all('div',attrs={'class':'title'})
        if len(title_div) != 1:
            raise RuntimeError("More than one Xiaoqu Title")
        xiaoqu_title = title_div[0].text.strip()

        # Get xiaoqu District
        district_a = xiaoqu_bs.find_all('a',attrs={'class':'district'})
        if len(district_a) != 1:
            raise  RuntimeError("More than one Xiaoqu Discrict")
        xiaoqu_district = district_a[0].text.strip()
        if xiaoqu_district != config.district_list[self.district]:
            raise RuntimeError("Wrong Xiaoqu District")
        year_div = xiaoqu_bs.find_all('div',attrs={'class':'positionInfo'})
        if len(year_div) != 1:
            raise  RuntimeError("More than one Xiaoqu Year Div")
        xiaoqu_year_vec = re.findall(u'.*?(\d{4})年建成.*?',year_div[0].text,re.MULTILINE)
        if len(xiaoqu_year_vec) == 1:
            xiaoqu_year = int(xiaoqu_year_vec[0])
        else:
            xiaoqu_year = -1
        xq = xiaoqu.xiaoqu(name=xiaoqu_title,district=xiaoqu_district,year=xiaoqu_year)
        return xq
    def xiaoqu_price_parser(self,xiaoqu_bs,xq):
        price_div = xiaoqu_bs.find_all('div',attrs={'class':'totalPrice'})
        if len(price_div) != 1:
            raise RuntimeError("More than one Xiaoqu Price")
        price_text = price_div[0].span.text
        if re.match('\d{1,}',price_text):
            xiaoqu_price = int(price_text)
        else:
            xiaoqu_price = -1
        xq.setPrice(xiaoqu_price)
        #print re.sub(r'\d{4}')

if __name__ == '__main__':
    xq = xiaoqu_menu(config.xiaoqu_url,'dongcheng','web','/Users/zyang2/PycharmProjects/EstatesSearch/data')
    xq.parser()
