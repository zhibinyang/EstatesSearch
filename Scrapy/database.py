# -*- coding: UTF-8 -*-

import pymysql
import db_config
import re
import datetime
class DatabaseInsert():
    def __init__(self):
        self._conn = pymysql.connect(host=db_config.MySQLServer, user=db_config.User, passwd = db_config.Passwd, db=db_config.db,charset="utf8")
        self._cur = self._conn.cursor()
    def __delete__(self, instance):
        self._cur.close()
        self._conn.close()
    def _execute(self, command):
        self._cur.execute(command)
        return self._cur.fetchall()
    def insert(self, table, items, values):
        #values = map(lambda x:x==None and 'NULL' or str(x), values) # Convert all the None data to NULL
        if isinstance(items,list):
            part1 = ','.join('`{0}`'.format(key) for key in items)
        elif isinstance(items, str):
            part1 = items
        elif isinstance(items, None):
            part1 = 'NULL'
        else:
            raise RuntimeError('Invalid type for Insertion Items')
        if isinstance(values, list):
            print values
            part2 = u','.join(u'\'{0}\''.format(key) for key in values)
            part2 = re.sub('\'NULL\'', 'NULL', part2, flags=re.IGNORECASE)
        elif isinstance(values, str):
            part2 = values
        elif isinstance(values, None):
            part2 = 'NULL'
        else:
            raise RuntimeError('Invalid type for Insertion Values')
        self._execute('INSERT IGNORE INTO `' + table + '`(' + part1 + ')VALUES(' + part2 + ');')
        self._conn.commit()

if __name__ == '__main__':
    db = DatabaseInsert()
    db.insert('xiaoqu',['xiaoqu','district','year','price','date'],[u'惠新里',u'朝阳',1980,60000,datetime.date.today()])