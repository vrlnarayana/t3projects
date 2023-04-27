import sqlite3

def sqlite_conn():
    con = sqlite3.connect('db/turiyatree.db')
    return con

def readdata(yourname):
    con = sqlite_conn()
    cursor = con.cursor()
    stmt = "SELECT user,password FROM applogin where user='"+yourname+"';"
    user = cursor.execute(stmt).fetchall()
    if user:
        ret = user
    else:
        ret = None
    return ret


#authenticate with name,passcode not empty and passcode matching
def authenticate(yourname, yourpass):
    if yourname:  # display blocks below if yourname is not empty
        if yourpass:  # display blocks below if yourpass is not empty
            ret = readdata(yourname)
            if ret:
                if ret[0][1] == yourpass:
                # if yourpass == 'MIT@123': #display blocks below if yourpass is not equal to hashed code
                    return 'authenticated'
                else:
                    return "Enter matching name/passcode"
            else:
                return "User does not exist"

        else:
            return "Enter passcode"
    else:
        return "Enter your name & passcode"
