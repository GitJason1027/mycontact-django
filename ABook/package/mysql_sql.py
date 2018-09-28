from django.db import connection, transaction

def select(sql):
    try:
        cursor = connection.cursor()
        # Data retrieval operation - no commit required
        cursor.execute(sql)
        row = cursor.fetchall()  # fetchone()返回一条记录,fetchall()返回所有记录
        cursor.close()
        return row
    except:
        print("mysql_sql.py function select goes wrong:")
        print(sql)
    else: pass

def selectToDic_iuser(sql):
    try:
        cursor = connection.cursor()
        # Data retrieval operation - no commit required
        cursor.execute(sql)
        data = cursor.fetchall()  # fetchone()返回一条记录,fetchall()返回所有记录
        cursor.close()
        dicData = []
        for row in data:
            result = {}
            result['uid'] = row[0]
            result['uname'] = row[1]
            result['uphone'] = row[2]
            result['upwd'] = row[3]
            result['uimgsrc'] = row[4]
            result['unew'] = row[5]
            dicData.append(result)
        return dicData
    except:
        print("mysql_sql.py function selectToDic_iuser goes wrong:")
        print(sql)
    else: pass

def selectToDic_contact(sql):
    try:
        cursor = connection.cursor()
        # Data retrieval operation - no commit required
        cursor.execute(sql)
        data = cursor.fetchall()  # fetchone()返回一条记录,fetchall()返回所有记录
        cursor.close()
        dicData = []
        for row in data:
            result = {}
            result['cid'] = row[0]
            result['cname'] = row[1]
            result['cphone'] = row[2]
            result['tid'] = row[3]
            result['cgender'] = row[4]
            result['cemail'] = row[5]
            result['cnote'] = row[6]
            result['picnum'] = int(row[0])%5
            dicData.append(result)
        return dicData
    except:
        print("mysql_sql.py function selectToDic_contact goes wrong:")
        print(sql)
    else: pass

def table_perform(sql):
    try:
        cursor = connection.cursor()
        # Data modifying operation - commit required
        cursor.execute(sql)
        transaction.commit()
        cursor.close()
    except:
        print("mysql_sql.py function table_perform goes wrong:")
        print(sql)
    else:pass
