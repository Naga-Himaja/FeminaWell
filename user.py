import sqlite3
class User:
    def add_new_user(name, email, phno, dob, password):
        con = sqlite3.connect("FeminaDatabase.db")
        c = con.cursor()
        try:
            x = (name,  email, phno, dob, password)
            insert = """INSERT INTO User (Name,  Email, PhoneNo, DOB, Password) VALUES (?,?,?,?,?);"""
            c.execute(insert, x)
        finally:
            con.commit()
            c.close()
            con.close()
            
    def check_email_exists(email):
        con = sqlite3.connect("FeminaDatabase.db")
        c = con.cursor()
        try:
            sql_select_query = "select * from User where Email = ?;"
            c.execute(sql_select_query, (email,))
            record = c.fetchall()   
        finally:
            con.commit()
            c.close()
            con.close()
        if len(record) == 0:
            return False
        else:
            return True

    def get_user_details(email):
        con = sqlite3.connect("FeminaDatabase.db")
        c = con.cursor()
        try:
            sql_select_query = "select * from User where Email = ?;"
            c.execute(sql_select_query, (email,))
            record = c.fetchall()
        finally:
            con.commit()
            c.close()
            con.close()
        return record[0]
    
    def update_profile(name,  email, phno, dob, userid):
        con = sqlite3.connect("FeminaDatabase.db")
        c = con.cursor()
        try:
            x = (name,  email, phno, dob, userid)
            update = "UPDATE User SET Name = ?, Email = ?, PhoneNo = ?, DOB = ?, WHERE UserID = ?;"
            c.execute(update, x)
        finally:
            con.commit()
            c.close()
            con.close()
            
    def update_password(newpwd, userid):
        con = sqlite3.connect("FeminaDatabase.db")
        c = con.cursor()
        try:
            x = (newpwd, userid)
            update = "UPDATE User SET password = ?WHERE UserID = ?;"
            c.execute(update, x)
        finally:
            con.commit()
            c.close()
            con.close()

    def delete_acc_posts(userid):
        con = sqlite3.connect("FeminaDatabase.db")
        c = con.cursor()
        try:
            delete = "DELETE FROM ApprovePosts WHERE userid = ?;"
            c.execute(delete, (userid,))
        finally:
            con.commit()
            c.close()
            con.close()

    def delete_acc(postid):
        con = sqlite3.connect("FeminaDatabase.db")
        c = con.cursor()
        try:
            delete = "DELETE FROM User WHERE UserID = ?;"
            c.execute(delete, (postid,))
        finally:
            con.commit()
            c.close()
            con.close()