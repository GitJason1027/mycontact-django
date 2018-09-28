#coding=utf-8
import mysql.connector as ms

def TableToDic(sql):
    dicData = []
    try:
        conn = ms.connect(host='localhost',user='ABook',passwd='abab',db='address_book',port=3306,charset = 'utf8')
        cur = conn.cursor()
        #sql = "select * from person;"
        cur.execute(sql)
        data = cur.fetchall()
        cur.close()
        conn.close()
        print(data)
        print(data[0][0])
        for row in data:
            result = {}
            result['name'] = row[0]
            result['age'] = row[1]
            result['birthday'] = str(row[2])
            result['gender'] = row[3]
            dicData.append(result)
    except:
        print("something goes wrong")
    else:
        return dicData

if __name__=='__main__':
    data = TableToDic("select * from person")
    print(data)
    print(data[0]['age'])