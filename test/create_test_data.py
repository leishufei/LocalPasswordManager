#!usr/bin/env python3
# -*- coding: utf-8 -*-
# @Software : PyCharm
import sqlite3

from utils import DataProcessor

dp = DataProcessor()

con = sqlite3.connect("../pwd.db")
cur = con.cursor()

sheetnames = ['01_test1', '02_test2', '03_test3', '04_test4', '05_test5', '06_test6', '07_test7', '08_test8', '09_test9']

for sheetname in sheetnames:
    create_sql = f'''CREATE TABLE `{sheetname}`(id varchar(32) NOT NULL DEFAULT "", item varchar(50) NOT NULL DEFAULT "", username varchar(50) NOT NULL DEFAULT "", password varchar(50) NOT NULL DEFAULT "");'''
    cur.execute(create_sql)

for i, sheetname in enumerate(sheetnames, start=1):
    insert_sql = f'INSERT INTO `{sheetname}` (id,item,username,password) VALUES(?,?,?,?);'
    for row in range(1, 101):
        sheetname = sheetname.split('_')[-1]
        values = [
            f'{sheetname}_item{row}',
            f'{sheetname}_username{row}',
            f'{sheetname}_password{row}'
        ]
        values.insert(0, dp.hash({
            'item': values[0],
            'username': values[1],
            'password': values[2]
        }))
        values[2] = dp.encrypt(values[2])
        values[3] = dp.encrypt(values[3])
        print(values)
        cur.execute(insert_sql, tuple(values))
con.commit()
cur.close()
con.close()
