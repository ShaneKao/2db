# -*- coding: utf-8 -*-
__author__ = 'Shane_Kao'
import pymssql
import cPickle as pickle
from dateutil import tz
db = "tp-bisapqc-v03"
user = "cmdb"
pwd = "cmdb#1234"
db = pymssql.connect(server=db, user=user, password=pwd, database='daniel_test')
cursor = db.cursor()
cursor.execute("CREATE TABLE test1 (post_id NVARCHAR(2000) , url NVARCHAR(2000), text NVARCHAR(2000))")
result = pickle.load(open("result", "r"))

def getColumnsSchema(TABLE_NAME):
    sqlcmd = """select column_name, DATA_TYPE
                 from information_schema.columns
                where table_name = N'%s'
                order by ORDINAL_POSITION asc""" % TABLE_NAME

    cursor.execute(sqlcmd)
    rows = cursor.fetchall()
    column_list = {}
    for row in rows:
        column_list[row[0]] = row[1]
    return column_list
COL_LIST = [x for x in result[0].keys()]
VALUE_LIST = []
for __idx in range(len(result)):
    tmp_val=[]
    for x in COL_LIST:
        if result[__idx].has_key(x):
            tmp_val.append(result[__idx][x])
        else:
            tmp_val.append('')
    VALUE_LIST.append(tmp_val)
def myInsert(TABLE_NAME, columns, values, col_schema):
    to_zone = tz.gettz('Asia/Taipei')
    sql_field = "[" + "],[".join(columns) + "]"
    sql_H_cmd = u"INSERT INTO [%s] (%s) VALUES " % (TABLE_NAME, sql_field)
    sql_R_cmd = ""
    for __rec in values:
        tmp_row = "("
        for __val in range(len(__rec)):
            if isinstance(__rec[__val], (unicode,str)):
                __rec[__val] = __rec[__val].replace("'","''")
            else:
                __rec[__val] = __rec[__val] if __rec[__val] is not None else ''

            __col_type = col_schema[columns[__val]]
            if __col_type == 'nvarchar':
                tmp_row = tmp_row + "N'%s' ," % __rec[__val]
            elif __col_type in ('varchar'):
                tmp_row = tmp_row + "'%s' ," % __rec[__val]
            elif __col_type in ('datetime'):
                if len(__rec[__val]) > 0:
                    __local_datetime = parser.parse(__rec[__val]).astimezone(to_zone).strftime('%Y/%m/%d %H:%M:%S')
                    tmp_row = tmp_row + "'%s' ," % __local_datetime
                else:
                    __local_datetime = ''
                    tmp_row = tmp_row + "Null ,"

            else:
                tmp_row = tmp_row + "'%s' ," % __rec[__val]

        tmp_row = tmp_row[:-1]+ ")"
        sql_R_cmd = sql_R_cmd + tmp_row + ","
    return u"%s %s" %  (sql_H_cmd ,sql_R_cmd[:-1])


col_schema = getColumnsSchema("test1")

__SQL_ins = myInsert("test1", columns=COL_LIST, values= VALUE_LIST, col_schema=col_schema)
try:
    cursor.execute(__SQL_ins.encode('utf-8'))
    db.commit()

except:
    print __SQL_ins
    raise
db.close()