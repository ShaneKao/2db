# -*- coding: utf-8 -*-
__author__ = 'Shane_Kao'
import cx_Oracle
import cPickle as pickle
import os
os.environ["NLS_LANG"]=".AL32UTF8"
result = pickle.load(open("result", "r"))
dbname = 'PLMD3'
username = "lsrm"
pwd = "lsrm"
dsn=cx_Oracle.makedsn('172.21.130.250','1533','PLMD3')
db=cx_Oracle.connect(username,pwd,dsn)
cursor = db.cursor()
for i in result:
    i['text']=i['text'].encode('utf-8')
    cursor.execute("INSERT INTO test1 VALUES (:post_id,:url,:text)" ,i)
db.commit()


