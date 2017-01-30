import requests
from PIL import Image
from bs4 import BeautifulSoup
import hashlib
vect = []
for i in range(100000):
    r = requests.get('http://captcha.lianjia.com/human').json()
    #bs = BeautifulSoup(r.text,"html.parser")
    #image = bs.find("a", {"id": "logo"}).find("img")["src"]
    for image in r["images"].values():
        vect.append(image+'\n')
    if i%1000 == 999:
        print i
        f = open('/Users/zyang2/PycharmProjects/EstatesSearch/data/crack/' + i.__str__() + 'data' ,'a')
        f.writelines(vect)
        vect = []
        f.close()
#print vect
    #print r["images"].values()