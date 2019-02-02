import sqlite3

insert_user_q = 'insert into contacts(name,email,mobile,city) values(?,?,?,?);'
update_user_by_name_q = 'update contacts set email=?,mobile=?,city=? where name=?;'
update_user_by_email_q = 'update contacts set name=?,mobile=?,city=? where email=?;'
update_user_by_mobile_q = 'update contacts set name=?,email=?,city=? where mobile=?;'
delete_user_by_name_q = 'delete from contacts where name=?;'
delete_user_by_email_q = 'delete from contacts where email=?;'
get_user_by_name_q = 'select email,mobile,city from contacts where name=?;'
get_user_by_name_with_page_q = 'select email,mobile,city from contacts where name=? limit ? offset ?';
get_user_by_email_with_page_q = 'select name, mobile,city from contacts where email=? limit ? offset ?;'
get_user_by_email_q = 'select name,mobile,city from contacts where email=?;'
get_all_users_with_page_q = 'select name,email,mobile,city from contacts limit ? offset ?;'
get_all_users_q = 'select name,email,mobile,city from contacts;'
get_password_q = 'select passwd from credentials where uname=?;'

connection = None

def get_connection():
    global connection
    if connection is None:
        connection = sqlite3.connect('contacts.db')
    return connection

def insert_user(name,email,mobile,city):
    conn = get_connection()
    try:
        conn.execute(insert_user_q,(name,email,mobile,city))
        conn.commit()
    except sqlite3.IntegrityError:
        return False
    return True


def get_user_by_name(name,limit=None,offset=None):
    conn = get_connection()
    if limit is None and offset is None:
        cursor = conn.execute(get_user_by_name_q,(name,))
    else:
        cursor = conn.execute(get_user_by_name_with_page_q,(name,limit,offset))
    ret = []
    for row in cursor:
        ret1 = {}
        ret1['name'] = name
        ret1['email'] = row[0]
        ret1['mobile'] = row[1]
        ret1['city'] = row[2]
        ret.append(ret1)
    return ret

def get_user_by_email(email,limit=None,offset=None):
    conn = get_connection()
    if limit is None and offset is None:
        cursor = conn.execute(get_user_by_email_q,(email,))
    else:
        cursor = conn.execute(get_user_by_email_with_page_q,(email,limit,offset))
        #print('cursor called with',email,pageno,offset)
    ret = []
    for row in cursor:
        ret1 = {}
        ret1['name'] = row[0]
        ret1['email'] = email
        ret1['mobile'] = row[1]
        ret1['city'] = row[2]
        ret.append(ret1)
    return ret

def update_user_by_name(name,email,mobile,city):
    conn = get_connection()
    conn.execute(update_user_by_name_q,(email,mobile,city,name))
    conn.commit()
    return get_user_by_name(name)

def update_user_by_email(email, name, mobile, city):
    conn = get_connection()
    conn.execute(update_user_by_email_q,(email,mobile,city,name))
    conn.commit()
    return get_user_by_email(email)

def delete_user_by_name(name):
    conn = get_connection()
    conn.execute(delete_user_by_name_q,(name,))
    conn.commit()

def delete_user_by_email(email):
    conn = get_connection()
    conn.execute(delete_user_by_email_q,(email,))
    conn.commit()

def get_all_users(limit=None,offset=None):
    conn = get_connection()
    if limit is None and offset is None:
        cursor = conn.execute(get_all_users_q)
    else:
        cursor = conn.execute(get_all_users_with_page_q,(limit,offset))
    ret = []
    for row in cursor:
        ret1 = {}
        ret1['name'] = row[0]
        ret1['email'] = row[1]
        ret1['mobile'] = row[2]
        ret1['city'] = row[3]
        ret.append(ret1)
    return ret

def get_password(name):
    conn = get_connection()
    cursor = conn.execute(get_password_q,(name,))
    for row in cursor:
        res = row[0]
    return  res

