#coding=utf-8
import json,mysql.connector as ms

def TableToJson(sql):
    jsonData = []
    try:
        conn = ms.connect(host='localhost',user='ABook',passwd='abab',db='address_book',port=3306,charset = 'utf8')
        cur = conn.cursor()
        #sql = "select * from person;"
        cur.execute(sql)
        data = cur.fetchall()
        cur.close()
        conn.close()

        for row in data:
            result = {}
            result['name'] = row[0]
            result['age'] = row[1]
            result['birthday'] = str(row[2])
            result['gender'] = row[3]
            jsonData.append(result)

    except:
        print("something goes wrong")
    else:
        jsonDatar = json.dumps(jsonData,ensure_ascii=False)
        jsonDatar = jsonDatar[1:len(jsonDatar)-1]
        return jsonDatar


if __name__=='__main__':
    data = TableToJson("select * from person;")
    print(data)

