from django.shortcuts import render
from django.shortcuts import HttpResponse
from django.shortcuts import redirect
import ABook.package.mysql_sql as ms
import os
import re


# Create your views here.

def login(request):

    print("function login")
    error_msg = ""
    if request.method == "POST":
        phone = request.POST.get('phone', None)
        pwd = request.POST.get('pwd', None)
        sql_user = "SELECT * FROM IUser WHERE Uphone = '%s' AND Upwd= '%s'" % (phone, pwd)
        data = ms.selectToDic_iuser(sql_user)
        if data:
            uname = data[0]['uname']
            uimgsrc = data[0]['uimgsrc']
            uid = data[0]['uid']
            unew = data[0]['unew']

            # 更新unew=0；
            if str(unew) == '1':
                print("unew===111")
                sql_new = "update IUser set unew = 0 where uid = '%s'" % uid
                ms.table_perform(sql_new)
            else:
                pass

            # 选择用户下的所有联系人
            sql_contact = "SELECT * FROM Contact where uid = '%s' ORDER BY CONVERT(cname USING gbk)" % uid
            row = ms.selectToDic_contact(sql_contact)

            # 以下的新建联系人卡片中的类别
            sql_newcontact_type = "select tid,tname from IType where uid = '%s' order by tid" % uid
            newtype_msg = ms.select(sql_newcontact_type)

            # 以下是联系人卡片中的类别
            type_msg = ()
            if row:
                for i in row:
                    sql = "select tid,tname from IType where tid = '%s'" % i['tid']
                    data_i = ms.select(sql)
                    i['tid'] = data_i[0][1]

                sql2 = "select tid,tname from IType where uid = '%s' order by tid" % (uid)
                data_i2 = ms.select(sql2)
                type_msg = data_i2
            else:
                pass
            return render(request, 'home.html',
                          {'name_msg': uname, 'imgsrc_msg': uimgsrc, 'id_msg': uid, 'row_msg': row,
                           'newtype_msg': newtype_msg, 'type_msg': type_msg, 'new_msg': unew})
        else:
            error_msg = "用户名或密码错误"
    return render(request, 'login.html', {'error_msg': error_msg})


def signup(request):
    print("function signup")
    error_msg = ""
    name = ""
    phone = ""
    defaultImgSrc = "static/sources/user_img/default.png"

    pattern = re.compile(r"[ !\"#$%&'()*+,\-./:;<=>?@[\\\]^_`{|}~]")
    if request.method == "POST":
        name = request.POST.get('name', None)
        phone = request.POST.get('phone', None)
        pwd = request.POST.get('pwd', None)
        obj = request.FILES.get('file')
        data_phone = ms.select("SELECT * FROM IUser WHERE uphone='%s'" % phone)
        data_name = ms.select("SELECT * FROM IUser WHERE uname='%s'" % name)

        if name == "":
            error_msg = "用户名不可为空"
        elif phone == "":
            error_msg = "电话号码不可为空"
        elif pwd == "":
            error_msg = "密码不可为空"
        elif data_name:
            error_msg = "用户名已注册"
        elif data_phone:
            error_msg = "手机号已注册"
        elif phone.isdigit() == False:
            error_msg = "请输入正确的手机号"
            phone = ""
        elif pattern.findall(name):
            error_msg = "用户名不可包含特殊字符"
            name = ""
        elif pattern.findall(pwd):
            error_msg = "密码不可包含特殊字符"
        else:
            file_path = ""
            if obj:
                objName = obj.name
                objsp = objName.split('.')
                fileName = phone + "." + objsp[1]
                file_path = os.path.join('static/sources/user_img/', fileName)
                f = open(file_path, mode="wb")
                for i in obj.chunks():
                    f.write(i)
                f.close()
            else:
                file_path = defaultImgSrc
            sql_user = "INSERT INTO IUser(uname,uphone,upwd,uimgsrc,unew) VALUE('%s','%s','%s','%s',1)" % (
            name, phone, pwd, file_path)
            print(sql_user)
            ms.table_perform(sql_user)

            uid = ms.select("select uid from IUser where uphone='%s'" % phone)
            print("uid")
            print(uid)
            sql_type_init = "INSERT INTO IType(uid,tname,tnote) value('%s','%s','%s')" % (
            uid[0][0], '未分组', '以下联系人未设置类别')
            print(sql_type_init)
            ms.table_perform(sql_type_init)
            error_msg = "注册成功"
            return render(request, 'login.html', {'error_msg': error_msg, "phone_msg": phone})
    else:
        pass
    return render(request, 'signup.html', {'error_msg': error_msg, "name_msg": name, "phone_msg": phone})


def home(request, nid):
    msg = backtohome(nid)
    return render(request, 'home.html', msg)


def usermanage(request, nid):
    uid = nid
    error_msg = ""
    msg = {}
    sql_user_init = "SELECT * FROM IUser WHERE uid = '%s'" % uid
    data_init = ms.selectToDic_iuser(sql_user_init)
    if data_init:
        uphone_init = data_init[0]['uphone']
        uname_init = data_init[0]['uname']
        uimgsrc_init = data_init[0]['uimgsrc']
    msg_init = {'name_msg': uname_init, 'imgsrc_msg': uimgsrc_init, 'id_msg': uid, 'phone_msg': uphone_init}

    if request.method == "POST":
        uname = request.POST.get('uname')
        upwd = request.POST.get('upwd')
        upwd_rapid = request.POST.get('upwd_rapid')
        uphone = request.POST.get('uphone')
        obj = request.FILES.get('file')

        data_name = ms.select("SELECT * FROM IUser WHERE uname='%s'" % uname)
        print(data_name)
        check_id = 0
        if (len(data_name) != 0):
            check_id = data_name[0][0]
        sql = ""
        if (len(data_name) != 0) and (check_id != int(uid)):
            error_msg = '用户名已经被注册'
            msg_init['error_msg'] = error_msg
            return render(request, 'user_manage.html', msg_init)
        elif (upwd != upwd_rapid):
            print("#2")
            error_msg = '两次输入的密码不相同'
            msg_init['error_msg'] = error_msg
            return render(request, 'user_manage.html', msg_init)
        elif (uname == "") and (upwd != ""):
            print("#3")
            sql = "update IUser set upwd='%s' where uid = '%s'" % (upwd, uid)
            # 文件update
            file_path = ""
            if obj:
                objName = obj.name
                objsp = objName.split('.')
                fileName = uphone + "." + objsp[1]
                file_path = os.path.join('static/sources/user_img/', fileName)
                f = open(file_path, mode="wb")
                for i in obj.chunks():
                    f.write(i)
                f.close()
                sql_update = "update IUser set uimgsrc = '%s' where uid='%s'" % (file_path, uid)
                print(sql_update)
                ms.table_perform(sql_update)
            else:
                pass

        elif (uname != "") and (upwd == ""):
            print("#4")
            sql = "update IUser set uname='%s' where uid = '%s'" % (uname, uid)

            # 文件update
            file_path = ""
            if obj:
                objName = obj.name
                objsp = objName.split('.')
                fileName = uphone + "." + objsp[1]
                file_path = os.path.join('static/sources/user_img/', fileName)
                f = open(file_path, mode="wb")
                for i in obj.chunks():
                    f.write(i)
                f.close()
                sql_update = "update IUser set uimgsrc = '%s' where uid='%s'" % (file_path, uid)
                print(sql_update)
                ms.table_perform(sql_update)
            else:
                pass
        elif (upwd == "") and (uname == ""):
            print("#5")
            # 文件update
            file_path = ""
            if obj:
                objName = obj.name
                objsp = objName.split('.')
                fileName = uphone + "." + objsp[1]
                file_path = os.path.join('static/sources/user_img/', fileName)
                f = open(file_path, mode="wb")
                for i in obj.chunks():
                    f.write(i)
                f.close()
                sql_update = "update iuser set uimgsrc = '%s' where uid='%s'" % (file_path, uid)
                print(sql_update)
                ms.table_perform(sql_update)
            else:
                pass
        else:
            print("#6")
            sql = "update iuser set uname='%s',upwd='%s' where uid = '%s'" % (uname, upwd, uid)

        print(sql)
        ms.table_perform(sql)
        sql_user = "SELECT * FROM IUser WHERE uid = '%s'" % uid
        data = ms.selectToDic_iuser(sql_user)
        if data:
            uphone = data[0]['uphone']
            uname = data[0]['uname']
            uimgsrc = data[0]['uimgsrc']
            uid = data[0]['uid']
        msg = {'name_msg': uname, 'imgsrc_msg': uimgsrc, 'id_msg': uid, 'phone_msg': uphone}
        msg['success_msg'] = "修改成功"
        return render(request, 'user_manage.html', msg)
    else:
        sql_user = "SELECT * FROM IUser WHERE uid = '%s'" % uid
        data = ms.selectToDic_iuser(sql_user)
        if data:
            uphone = data[0]['uphone']
            uname = data[0]['uname']
            uimgsrc = data[0]['uimgsrc']
            uid = data[0]['uid']
        msg = {'name_msg': uname, 'imgsrc_msg': uimgsrc, 'id_msg': uid, 'phone_msg': uphone}
        return render(request, 'user_manage.html', msg)
    return HttpResponse("def usermanage ")


def contactAdd(request, nid):
    print("function contactAdd")
    uid = nid
    if request.method == "POST":
        cname = request.POST.get('name', None)
        cphone = request.POST.get('phone', None)
        tid = request.POST.get('type', None)
        newtype = request.POST.get('newtype', None)
        cgender = request.POST.get('gender', None)
        cemail = request.POST.get('email', None)
        cnote = request.POST.get('note', None)
        print(cname, cphone, tid, cgender, cemail, cnote, nid)

        if tid == "new":
            sql_newtype = "insert into IType(uid,tname,tnote) value('%s','%s','%s')" % (uid, newtype, '无')
            ms.table_perform(sql_newtype)
            sql_select_tid = "select max(tid) from IType where uid = '%s'" % uid
            tid = ms.select(sql_select_tid)[0][0]
        else:
            pass

        sql_insert = "INSERT INTO Contact(cname,cphone,tid,cgender,cemail,cnote,uid) VALUE('%s','%s','%s','%s','%s','%s','%s')" % (
        cname, cphone, tid, cgender, cemail, cnote, uid)
        ms.table_perform(sql_insert)

        msg = backtohome(nid)
        return render(request, 'home.html', msg)
    else:
        pass
    return render(request, 'home.html')


def contactEdit(request):
    print("function contactEdit")
    if request.method == "POST":
        id = request.POST.get('id', None)
        sp = id.split('-')
        uid = sp[0]
        cid = sp[1]

        if request.POST.get('submit_edit'):
            cname = request.POST.get('name', None)
            cphone = request.POST.get('phone', None)
            tid = request.POST.get('type', None)
            newtype = request.POST.get('newtype', None)
            cgender = request.POST.get('gender', None)
            cemail = request.POST.get('email', None)
            cnote = request.POST.get('note', None)

            if tid == "new":
                sql_newtype = "insert into IType(uid,tname,tnote) value('%s','%s','%s')" % (uid, newtype, '无')
                ms.table_perform(sql_newtype)
                sql_select_tid = "select max(tid) from IType where uid = '%s'" % uid
                tid = ms.select(sql_select_tid)[0][0]
            else:
                pass

            sql_update = "UPDATE Contact SET cname='%s',cphone='%s',tid='%s',cgender='%s',cemail='%s',cnote='%s' WHERE cid='%s'" % (
            cname, cphone, tid, cgender, cemail, cnote, cid)
            print(sql_update)
            ms.table_perform(sql_update)
        # 非submit_edit的请求按钮，就是删除按钮
        else:
            sql_delete = "DELETE FROM Contact WHERE cid ='%s'" % cid
            ms.table_perform(sql_delete)

        msg = backtohome(uid)
        return render(request, 'home.html', msg)
    else:
        print("contactEdit is not POST method")
    return render(request, 'home.html')


def contactSearch(request, nid):
    print("function contactSearch")
    uid = nid
    if request.method == "POST":
        stype = request.POST.get('searchtype')
        sinfo = request.POST.get('searchinfo')
        sql = ""
        if stype == "姓名":
            sql = "SELECT * FROM Contact WHERE uid='%s'" % uid + " and cname LIKE '%" + "%s" % sinfo + "%'"
        elif stype == "性别":
            sql = "SELECT * FROM Contact WHERE uid='%s'" % uid + " and cgender LIKE '%" + "%s" % sinfo + "%'"
        elif stype == "类别":
            sql = "SELECT * FROM Contact WHERE uid='%s'" % uid + " and tid in(select tid from itype where tname like '%" + "%s" % sinfo + "%')"
        elif stype == "手机号":
            sql = "SELECT * FROM Contact WHERE uid='%s'" % uid + " and cphone LIKE '%" + "%s" % sinfo + "%'"
        else:
            print("search error type")

        sql = sql + " ORDER BY CONVERT(cname USING gbk)"

        # 返回home
        sql_userinfo = "SELECT * FROM IUser WHERE uid = '%s'" % uid
        data = ms.selectToDic_iuser(sql_userinfo)

        if data:
            uname = data[0]['uname']
            uimgsrc = data[0]['uimgsrc']
            uid = data[0]['uid']
            row = ms.selectToDic_contact(sql)
            print(sql)
            print(row)
            if row:
                search_msg = "以下是对" + stype + "为'" + sinfo + "'的搜索结果"
            else:
                search_msg = "没有找到结果"
            # ----
            # 以下是联系人卡片中的类别
            type_msg = []
            if row:
                for i in row:
                    print(i)
                    sql = "select tid,tname from IType where tid = '%s'" % i['tid']
                    data_i = ms.select(sql)
                    print(data_i)
                    i['tid'] = data_i[0][1]
                sql2 = "select tid,tname from IType where uid = '%s' order by tid" % (uid)
                data_i2 = ms.select(sql2)
                type_msg = data_i2
            else:
                pass
            # ----

            return render(request, 'home_search.html',
                          {'name_msg': uname, 'imgsrc_msg': uimgsrc, 'id_msg': uid, 'row_msg': row,
                           'type_msg': type_msg, 'search_msg': search_msg})
        else:
            print("cotactEdit sql data 为空")
    else:
        pass
    return HttpResponse("contactSearch error")


def contactType(request, nid):
    uid = nid
    msg = backtohome(uid)
    msg.pop('newtype_msg')
    sql_type = "select tid,tname,tnote from IType where uid = '%s' order by tid" % uid
    type_tag = ms.select(sql_type)
    type_edit_tag = []
    for i in type_tag:
        type_edit_tag.append(i)
    type_edit_tag.pop(0)
    msg['type_tag'] = type_tag
    msg['type_edit_tag'] = type_edit_tag
    return render(request, 'home_type.html', msg)


def selectedType(request, nid):
    sp = nid.split('_')
    uid = sp[0]
    tid = sp[1]

    msg = backtohome(uid)

    msg.pop('newtype_msg')
    sql_type = "select tid,tname,tnote from IType where uid = '%s' order by tid" % uid
    type_tag = ms.select(sql_type)
    type_edit_tag = []
    for i in type_tag:
        type_edit_tag.append(i)
    type_edit_tag.pop(0)
    msg['type_tag'] = type_tag
    msg['type_edit_tag'] = type_edit_tag

    sql_contact = "SELECT * FROM Contact where uid = '%s' and tid = '%s' ORDER BY CONVERT(cname USING gbk)" % (uid, tid)
    row = ms.selectToDic_contact(sql_contact)
    if row:
        for i in row:
            sql = "select tid,tname from IType where tid = '%s'" % i['tid']
            data_i = ms.select(sql)
            i['tid'] = data_i[0][1]
    else:
        pass
    msg['row_msg'] = row
    return render(request, 'home_type.html', msg)


def edittype(request, nid):
    uid = nid
    tid = request.POST.get('type')
    tname = request.POST.get('typename')
    tnote = request.POST.get('note_' + tid)

    if request.POST.get('submit_edit'):
        print('submit_edit')
        if tnote == "":
            tnote = '无'
        else:
            pass

        if tid == "new":
            sql_newtype = "insert into IType(uid,tname,tnote) value('%s','%s','%s')" % (uid, tname, tnote)
            ms.table_perform(sql_newtype)
        else:
            sql_upadte = "UPDATE IType SET tname = '%s',tnote = '%s' WHERE tid = '%s' " % (tname, tnote, tid)
            ms.table_perform(sql_upadte)
    else:
        print('submit_delete')
        sql_nogroup = "select tid from IType where uid = '%s' order by tid" % uid
        typedata = ms.select(sql_nogroup)
        sql_contact_upadte = "update Contact set tid='%s' where tid = '%s'" % (typedata[0][0], tid)
        ms.table_perform(sql_contact_upadte)
        sql_delete = "delete from IType where tid='%s'" % tid
        ms.table_perform(sql_delete)
    # 返回类别页面
    msg = backtohome(uid)
    msg.pop('newtype_msg')
    sql_type = "select tid,tname,tnote from IType where uid = '%s' order by tid" % uid
    type_tag = ms.select(sql_type)
    type_edit_tag = []
    for i in type_tag:
        type_edit_tag.append(i)
    type_edit_tag.pop(0)
    msg['type_tag'] = type_tag
    msg['type_edit_tag'] = type_edit_tag
    return render(request, 'home_type.html', msg)


def deleteuser(request):
    uid = request.POST.get('uid_delete')
    sql = "SET FOREIGN_KEY_CHECKS = 0;delete from IUser where uid='%s';SET FOREIGN_KEY_CHECKS = 1;" % uid
    ms.table_perform(sql)
    return render(request, 'login.html')


def backtohome(uid):
    sql_user = "SELECT * FROM IUser WHERE uid = '%s'" % uid
    data = ms.selectToDic_iuser(sql_user)
    if data:
        uname = data[0]['uname']
        uimgsrc = data[0]['uimgsrc']
        uid = data[0]['uid']

        # 选择用户下的所有联系人
        sql_contact = "SELECT * FROM Contact where uid = '%s' ORDER BY CONVERT(cname USING gbk)" % uid
        row = ms.selectToDic_contact(sql_contact)

        # 以下的新建联系人卡片中的类别
        sql_newcontact_type = "select tid,tname from IType where uid = '%s' order by tid" % uid
        newtype_msg = ms.select(sql_newcontact_type)

        # 以下是联系人卡片中的类别
        type_msg = []
        if row:
            for i in row:
                sql = "select tid,tname from IType where tid = '%s'" % i['tid']
                data_i = ms.select(sql)
                print(sql)
                print(data_i)
                i['tid'] = data_i[0][1]
            sql2 = "select tid,tname from IType where uid = '%s' order by tid" % (uid)
            data_i2 = ms.select(sql2)
            type_msg = data_i2
        else:
            pass

        ret = {'name_msg': uname, 'imgsrc_msg': uimgsrc, 'id_msg': uid, 'row_msg': row, 'newtype_msg': newtype_msg,
               'type_msg': type_msg}
    return ret
