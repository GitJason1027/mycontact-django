from django.test import TestCase
import ABook.package.mysql_sql as ms
# Create your tests here.
if __name__=='__main__':
    # user = 123;
    # sql = "select tid,tname from itype where tid = '4'"
    # conn = ms.connect(host='localhost', user='ABook', passwd='abab', db='mycontact', port=3306, charset='utf8')
    # cur = conn.cursor()
    # cur.execute(sql)
    # data = cur.fetchall()
    # print(data)
    # print(len(data))
    # print(sql)
    i=4
    sql = "select tid,tname from itype where tid = '%s'" %i
    sql1 ="select * from itype"
    data_i = ms.select(sql1)
    print(data_i)
