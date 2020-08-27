# db3.py
import pymysql

# 데이터 베이스에 접속하는 함수
def get_connection() :
    conn = pymysql.connect(host='127.0.0.10', user='root',
            password='1234', db='covid12', charset='utf8')
    if conn:
        print('디비 접속 완료')
    return conn

def get_kosdaq_list() :
    conn = get_connection()
    cursor = conn.cursor()

    sql = ''' SELECT * FROM covid12.kosdaq order by date  '''
    cursor.execute(sql)
    result = cursor.fetchall()

    temp_list = []
    for row in result:
        temp_dic = {}
        temp_dic['date'] = row[0]
        temp_dic['endprice'] = row[1]
        temp_dic['diff'] = row[2]
        temp_dic['tradingvolume'] = row[3]
        temp_list.append(temp_dic)
    conn.close()
    return temp_list  

def get_jinbiotech_list() :
    conn = get_connection()
    cursor = conn.cursor()

    sql = ''' SELECT * FROM covid12.jinbiotech order by date  '''
    cursor.execute(sql)
    result = cursor.fetchall()

    temp_list = []
    for row in result:
        temp_dic = {}
        temp_dic['date'] = row[0]
        temp_dic['endprice'] = row[1]
        temp_dic['diff'] = row[2]
        temp_dic['tradingvolume'] = row[3]
        temp_list.append(temp_dic)
    conn.close()
    return temp_list  

def worldcity(no):
    conn = get_connection()
    cursor = conn.cursor()
    sql = '''SELECT * FROM worldcity where No = %s'''
    cursor.execute(sql,no)
    result = cursor.fetchone()
    temp_dic = {}
    temp_dic['No'] = result[0]
    temp_dic['Code'] = result[1]
    temp_dic['Name'] = result[2]
    temp_dic['GNP'] = result[3]
    temp_dic['Population'] = result[4]
    conn.close()
    return temp_dic

def member(no) :
    conn = get_connection()
    cursor = conn.cursor()

    sql = '''SELECT * FROM member where userNo = %s'''
    cursor.execute(sql, no)
    result = cursor.fetchone()
    if result:
        temp_dic = {}
        temp_dic['userNo'] = result[0]
        temp_dic['userID'] = result[1]
        temp_dic['userName'] = result[2]
        temp_dic['pwd'] = result[3]
        conn.close()
        return temp_dic
    else:
        conn.close()
        return 0

def search_worldcity_list(name):
    conn = get_connection()
    cursor = conn.cursor()
    sql = '''SELECT * FROM worldCity where Name like %s'''
    name = '%'+name+'%'
    cursor.execute(sql, name)
    result = cursor.fetchall()
    temp_list = []
    for row in result :
        temp_dic = {}
        temp_dic['No'] = row[0]
        temp_dic['Code'] = row[1]
        temp_dic['Name'] = row[2]
        temp_dic['GNP'] = row[3]
        temp_dic['Population'] = row[4]
        temp_list.append(temp_dic)
    
    conn.close()
    return temp_list

# 회원추가
def worldcity_add(Code, Name, GNP, Population):
    conn = get_connection()
    cursor = conn.cursor()
    sql = '''
            INSERT INTO worldcity
                (Code, Name, GNP, Population)
                values (%s, %s, %s, %s)
            '''
    cursor.execute(sql, (Code, Name, GNP, Population))
    conn.commit()
    conn.close()

def member_add(userID, userName, pwd):
    conn = get_connection()
    cursor = conn.cursor()
    sql = '''INSERT INTO member (userID, userName, pwd) values (%s, %s, %s)'''
    cursor.execute(sql, (userID, userName, pwd))
    conn.commit()
    conn.close()



def get_worldcity_list() :
    conn = get_connection()
    cursor = conn.cursor()

    sql = ''' SELECT * FROM worldcity  '''
    cursor.execute(sql)
    result = cursor.fetchall()

    temp_list = []
    for row in result:
        temp_dic = {}
        temp_dic['No'] = row[0]
        temp_dic['Code'] = row[1]
        temp_dic['Name'] = row[2]
        temp_dic['GNP'] = row[3]
        temp_dic['Population'] = row[4]
        temp_list.append(temp_dic)
    conn.close()
    return temp_list  

def worldcity_delete(worldcity_no):
    # 데이타베이스 접속함수 호출
    conn = get_connection()
    # 작업변수 생성
    cursor = conn.cursor()
    sql = '''Delete from worldcity where no = %s'''    
    cursor.execute(sql, (worldcity_no))
    conn.commit()
    conn.close()

def worldcity_update(c_no, c_gnp, c_population):
    # 데이타베이스 접속함수 호출
    conn = get_connection()
    # 작업변수 생성
    cursor = conn.cursor()
    # 레코드 수정 sql 구문 
    sql = '''update worldcity set GNP=%s,Population=%s where No=%s'''
    cursor.execute(sql, (c_gnp, c_population, c_no))
    conn.commit()
    conn.close()

def member_update(c_no, c_id, c_pwd):
    # 데이타베이스 접속함수 호출
    conn = get_connection()
    # 작업변수 생성
    cursor = conn.cursor()
    # 레코드 수정 sql 구문 
    sql = '''update member set userID=%s,pwd=%s where userNo=%s'''
    cursor.execute(sql, (c_id, c_pwd, c_no))
    conn.commit()
    conn.close()


# userId, pwd 데이타 값 확인 함수 
def login_result(userID, pwd):

    conn = get_connection()
    cursor = conn.cursor()

    sql = '''SELECT * FROM covid12.member WHERE userID=%s AND pwd=%s'''
    cursor.execute(sql,(userID,pwd))
    login_result = cursor.fetchone()

    if login_result:
        return True
    else:
        return False

