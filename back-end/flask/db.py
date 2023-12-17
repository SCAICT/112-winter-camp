import sqlite3

# 连接到数据库（如果不存在，则会创建一个新的数据库）
conn = sqlite3.connect('back-end/flask/account.db')

# 创建一个游标对象，用于执行 SQL 语句
cursor = conn.cursor()

# 执行查询
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


# 关闭游标和连接
cursor.close()
conn.close()
