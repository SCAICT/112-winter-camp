import sqlite3
from sqlite3 import Cursor,Connection
from typing import Literal
class DataBase:
    def __init__(self,db_path:str) -> None:
        self.db = db_path
    
    def __call__(self,func:function):
        def wrapper(*args,**kwargs):
            """
            執行查詢動作
            """
            conn = sqlite3.connect(self.db)
            cursor = conn.cursor()
            result = func(conn, cursor, *args, **kwargs)

            cursor.close()
            conn.close()

            return result
        return wrapper


Admin = DataBase("back-end/flask/database/admin.db")
Client = DataBase("back-end/flask/database/account.db")

# todo
@Client
def isUser(conn:Connection, cursor:Cursor,account:str) -> bool:
    """
    輸入帳號 查詢是否在資料庫裡面
    """
    return bool()

@Client
def userData(conn:Connection, cursor:Cursor,account:str) -> list:
    """
    輸入帳號 查詢此人輸入的資料
    """
    return list()

@Client
def updateUserData(conn:Connection, cursor:Cursor,account:str,newData:list) -> bool:
    """
    輸入帳號 上傳/更新 資料
    """
    return bool()

@Client
def signConsent(conn:Connection, cursor:Cursor,account:str,consentID:Literal[0, 1]) -> bool:
    """
    輸入帳號 簽署文件 文件會有 0和1
    """
    return bool()

@Client
def userPay(conn:Connection, cursor:Cursor,account:str) -> bool:
    """
    輸入帳號 表用戶已付錢
    """
    return bool()

@Client
def logStudent(conn:Connection, cursor:Cursor) -> None:
    """
    輸出student表
    """
    cursor.execute('SELECT * FROM DATA')
    # 获取查询结果
    results = cursor.fetchall()
    # 打印结果
    for row in results:
        userID = row[0] #使用者ID
        name = row[1] #姓名
        email = row[2] #電子郵件
        school = row[3] #學校
        department = row[4] #科系
        club = row[5] #社團
        password = row[6] #密碼
        phone = row[7] #電話
        sex = row[8] #性別
        ID = row[9] #身分證字號
        birthday = str(row[10]) #生日
        emergency = row[11] #緊急聯絡人
        emergencyRelation = row[12] #緊急聯絡人關係
        emergencyPhone = row[13] #緊急聯絡人電話
        size = row[14] #衣服尺寸
        eat = row[15] #葷素
        specialEat = row[16] #特殊飲食習慣
        specialDisease = row[17] #疾病
        islive = row[18] #是否住宿
        coupon = row[19] #團報優惠碼
        print("=====================================")
        print("使用者ID: "+userID)
        print("姓名: "+name)
        print("電子郵件: "+email)
        print("學校: "+school)
        print("科系: "+department)
        print("社團: "+club)
        print("密碼: "+password)
        print("電話: "+phone)
        print("性別: "+sex)
        print("身分證字號: "+ID)
        print("生日: "+birthday)
        print("緊急聯絡人: "+emergency)
        print("緊急聯絡人關係: "+emergencyRelation)
        print("緊急聯絡人電話: "+emergencyPhone)
        print("衣服尺寸: "+size)
        print("葷素: "+eat)
        print("特殊飲食習慣: "+specialEat)
        print("疾病: "+specialDisease)
        print("是否住宿: "+islive)
        print("團報優惠碼: "+coupon)


@Admin
def logAdmin(conn:Connection, cursor:Cursor) -> None:
    """
    輸出admin表
    """
    cursor.execute('SELECT * FROM DATA')
    results = cursor.fetchall()
    for r in results:
        print(r)


# logAdmin()
logStudent()
