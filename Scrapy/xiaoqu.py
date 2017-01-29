# -*- coding: UTF-8 -*-
class xiaoqu:
    def __init__(self,name,district,year):
        self._name = name
        self._district = district
        self._year = year
    def setPrice(self,price):
        self._price = price
    def getPrice(self):
        return self._price
    def getName(self):
        return self._name
    def getDistrict(self):
        return self._district
    def getYear(self):
        return self._year
    def __str__(self):
        return self._name + ' ' + self._district + ' ' + self._year.__str__()
    def __unicode__(self):
        return self._name + ' ' + self._district + ' ' + self._year.__unicode__()