import sqlite3
from sqlite3 import Cursor,Connection
from typing import Literal

class DataBase:
    def __init__(self,db_path:str) -> None:
        self.db = db_path
    
    def __call__(self,func):
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
def isUserMail(conn:Connection, cursor:Cursor,mail:str) -> bool: #用email查用戶是否存在
    cursor.execute(f"SELECT * FROM DATA WHERE email = '{mail}'")
    results = cursor.fetchall()
    if bool(results) == True:
        return bool(results),results[0][0]
    else:
        return bool(results),None

print(isUserMail(mail="j097023855212@gmail.com"))

@Client
def isUserPhone(conn:Connection, cursor:Cursor,phone:str) -> tuple:
    cursor.execute(f"SELECT * FROM DATA WHERE phone = '{phone}'")
    results = cursor.fetchall()
    if bool(results) == True:
        return bool(results),results[0][0]
    else:
        return bool(results),None

@Client
def isUserID(conn:Connection, cursor:Cursor,UserID:str) -> bool:
    cursor.execute(f"SELECT * FROM DATA WHERE UserID = '{UserID}'")
    results = cursor.fetchall()
    if bool(results) == True:
        return bool(results)
    else:
        return bool(results)
    

@Client
def getUserData(conn:Connection, cursor:Cursor,UserID:str) -> list: 
    """
    用userID查用戶資料
    """
    cursor.execute(f"SELECT * FROM DATA WHERE UserID = '{UserID}'")
    results = cursor.fetchall()
    return list(results)

@Client
def getUserLastStep(conn:Connection, cursor:Cursor,UserID:str) -> list: 
    """
    用userID查詢lastStep所需資料
    """
    # coupon,isPaid,consentID,maintenance
    cursor.execute(f"SELECT coupon,isPaid,consentID,maintenance FROM DATA WHERE UserID = '{UserID}'")
    results = cursor.fetchall()
    return list(results)


@Client
def createUser(conn:Connection, cursor:Cursor,Data:list) -> bool: #創建用戶
    if isUserMail(Data[2])[0] == True:
        return False
    if isUserPhone(Data[7])[0] == True:
        return False

    cursor.execute(f"INSERT INTO DATA VALUES {tuple(Data)}")
    conn.commit()
    return True


# print(createUser(['123456','賴甲玉','a123456786@gmail.com','國立臺灣大學','資訊工程學系','資訊工程學系學會','123456','0912345658','男','A123456789','20000101','賴乙玉','父子','0912345678','S','葷','無','無','True','123456','1620000000','False','0101010101101010101']))

@Client
def deleteUserData(conn:Connection, cursor:Cursor,UserID:str) -> bool:
    if isUserID(UserID) == False:
        return False
    else:
        cursor.execute(f"DELETE FROM DATA WHERE UserID = '{UserID}'")
        conn.commit()
        return True
    


@Client
def updateUserData(conn:Connection, cursor:Cursor,UserID:str,Data:list) -> bool:
    if deleteUserData(UserID):
        if createUser(Data):
            return True
        else:
            return False
    else:
        return False
    
# print(updateUserData('123456',['123456','賴屏玉','a123456786@gmail.com','國立臺灣大大學','資訊工程學系','資訊工程學系學會','123456','0912345658','男','A123456789','20000101','賴乙玉','父子','0912345678','S','葷','無','無','True','123456','1620000000','False']))


@Client
def signConsent(conn:Connection, cursor:Cursor,userID:str,consentID:Literal[0, 1]) -> bool:
    cursor.execute(f"UPDATE DATA SET consentID = {consentID} WHERE UserID = '{userID}'")
    conn.commit()
    return True


@Client
def getStudentData(conn:Connection, cursor:Cursor,userID:str) -> list:
    """
    透過uuid get姓名、手機、家長姓名、家長手機
    """
    cursor.execute(f"SELECT name,phone,emergencyContact,emergencyPhone FROM DATA WHERE UserID = '{userID}'")
    results = cursor.fetchall()
    return list(results[0])

@Client
def isPasswordCorrect(conn:Connection , cursor:Cursor,userID:str,password:str) -> bool:
    cursor.execute(f"SELECT password FROM DATA WHERE UserID = '{userID}'")
    results = cursor.fetchall()
    if results[0][0] == password:
        return True
    else:
        return False


@Client
def userPay(conn:Connection, cursor:Cursor,userID:str) -> bool:
    cursor.execute(f"UPDATE DATA SET isPaid = True WHERE UserID = '{userID}'")
    conn.commit()
    return True


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
        timestamp = row[20] #時間戳
        isPaid = row[21] #是否付款
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
        print("時間戳: "+str(timestamp))
        print("是否付款: "+str(isPaid))


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
# logStudent()
