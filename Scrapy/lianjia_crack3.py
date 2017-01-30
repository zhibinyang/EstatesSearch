# -*- coding: UTF-8 -*-
import requests
import datetime
import os
post_params = {'channel':'ershoufang','city_id':'110000','limit_count':100,'limit_offset':0}
headers = {u'Content-Type': u'application/x-www-form-urlencoded; charset=UTF-8',
           u'Lianjia-App-Id':'201502021415',
           u'Lianjia-App-Secret':'2d65387bec568cd2ec228ee869a64856',
           u'Lianjia-Channel':'Android_uc'}
r = requests.post('https://moapi.lianjia.com/house/ershoufang/search',data=post_params,headers=headers)
r.encoding = 'utf-8'
print r.text
more_data = r.json()['data']['has_more_data']

base_url = '/Users/zbyang/PycharmProjects/EstatesSearch/data'
folder = datetime.date.today().strftime('%Y%m%d').__str__()
base_url = os.path.join(base_url,folder)
if not os.path.exists(base_url):
    os.mkdir(base_url)
# print folder.__str__()
i = 0
print more_data
while(more_data==1):
    post_params = {'channel':'ershoufang','city_id':'110000','limit_count':100,'limit_offset':i}
    headers = {u'Content-Type': u'application/x-www-form-urlencoded; charset=UTF-8',
               u'Lianjia-App-Id':'201502021415',
               u'Lianjia-App-Secret':'2d65387bec568cd2ec228ee869a64856',
               u'Lianjia-Channel':'Android_uc'}
    r = requests.post('https://moapi.lianjia.com/house/ershoufang/search',data=post_params,headers=headers)
    r.encoding = 'utf-8'
    more_data = r.json()['data']['has_more_data']
    i += 100
    f = open(os.path.join(base_url,i.__str__()) + '.json','w')
    #print r.text
    f.writelines(r.text)


