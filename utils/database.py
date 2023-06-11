#!usr/bin/env python3
# -*- coding: utf-8 -*-
# @Software : PyCharm
import sqlite3
from typing import List, Dict

from . import DataProcessor

dp = DataProcessor()


class Database:
    def __init__(self):
        self.db_path = './pwd.db'
        self.ret = None
        self.create_sql = 'CREATE TABLE `%s`(id varchar(32) NOT NULL DEFAULT "", item varchar(50) NOT NULL DEFAULT "", username varchar(50) NOT NULL DEFAULT "", password varchar(50) NOT NULL DEFAULT "");'
        self.insert_sql = "INSERT INTO `{sheet}` (id,item,username,password) VALUES(?,?,?,?);"
        self.query_sql_1 = "SELECT name FROM sqlite_master WHERE type='table' order BY name;"
        self.query_sql_2 = "SELECT item,username,password FROM `{sheet}`;"
        self.query_sql_3 = "SELECT item,username,password FROM `{sheet}` WHERE item LIKE '%%{keyword}%%';"
        self.update_sql = "UPDATE `{sheet}` SET {set_group} WHERE id='{ori_id}';"
        self.delete_sql = "DELETE FROM `{sheet}` WHERE id='{hash_id}';"
        self.delete_sheet_sql = "DROP TABLE IF EXISTS `{sheet}`;"

        self.connect()

    def connect(self) -> bool:
        self.connection = sqlite3.connect(self.db_path)
        if self.connection:
            self.cursor = self.connection.cursor()
            if self.cursor:
                return True
        self.ret = '数据库连接失败'
        return False

    def close(self) -> None:
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()

    def check(self) -> bool:
        self.ret = None
        if not self.connection or not self.cursor:
            self.ret = '数据库连接丢失'
            return False
        return True

    def insert(self, sheet: str, item: Dict) -> bool:
        if not self.check():
            return False

        hash_id = dp.hash(item)
        values = [hash_id, item['item'], dp.encrypt(item['username']), dp.encrypt(item['password'])]
        try:
            self.cursor.execute(self.insert_sql.format(sheet=sheet), values)
            self.connection.commit()
            return True
        except:
            self.ret = '插入失败'
            return False

    def query_sheet_list(self) -> List[str]:
        if not self.check():
            return []

        self.cursor.execute(self.query_sql_1)
        fetch_results = self.cursor.fetchall()
        sheet_list = [each[0] for each in fetch_results]
        return sheet_list

    def query_0(self) -> List[Dict]:
        fetch_results = self.cursor.fetchall()
        items = []
        for each in fetch_results:
            item = each[0]
            username = dp.decrypt(each[1])
            password = dp.decrypt(each[2])
            items.append({
                'item': item,
                'username': username,
                'password': password
            })
        return items

    def query_by_sheet(self, sheet: str) -> List[Dict]:
        if not self.check():
            return []

        self.cursor.execute(self.query_sql_2.format(sheet=sheet))
        return self.query_0()

    def query_by_sheet_and_keyword(self, sheet: str, keyword: str) -> List[Dict]:
        if not self.check():
            return []

        self.cursor.execute(self.query_sql_3.format(sheet=sheet, keyword=keyword))
        return self.query_0()

    def update(self, sheet: str, item: Dict) -> bool:
        if not self.check():
            return False

        ori_hash_id = dp.hash(item['originalItem'])
        new_hash_id = dp.hash(item['updatedItem'])

        set_group_list = [f"id='{new_hash_id}'"]
        for k, v in item['updatedItem'].items():
            if k in ['username', 'password']:
                v = dp.encrypt(v)
            set_group_list.append(f"{k}='{v}'")

        try:
            self.cursor.execute(self.update_sql.format(sheet=sheet, set_group=', '.join(set_group_list), ori_id=ori_hash_id))
            self.connection.commit()
            return True
        except:
            self.ret = "更新失败"
            return False

    def delete(self, sheet: str, items: List[Dict]) -> bool:
        for item in items:
            hash_id = dp.hash(item)
            self.cursor.execute(self.delete_sql.format(sheet=sheet, hash_id=hash_id))
            self.connection.commit()
        return True

    def create_sheet(self, sheet: str) -> bool:
        if not self.check():
            return False

        try:
            # 用 format 会崩
            self.cursor.execute(self.create_sql % sheet)
            self.connection.commit()
            return True
        except:
            self.ret = "创建失败"
            return False

    def delete_sheet(self, sheet_list: List[str]) -> bool:
        if not self.check():
            return False

        for sheet in sheet_list:
            self.cursor.execute(self.delete_sheet_sql.format(sheet=sheet))
            self.connection.commit()
        return True
