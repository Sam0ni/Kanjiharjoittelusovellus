from db import db
from werkzeug.security import check_password_hash, generate_password_hash

def login(username, password):
    sql = "SELECT username, password FROM Users WHERE username=:username"
    results = db.session.execute(sql, {"username":username}).fetchone()
    if not results:
        return False
    else:
        hash_value = results.password
        if check_password_hash(hash_value, password):
            return True
        else:
            return False

def register(username, password):
    try:
        hash_val = generate_password_hash(password)
        sql = "INSERT INTO Users (username, password, admin) VALUES (:username, :password, False)"
        db.session.execute(sql, {"username":username, "password":hash_val})
        db.session.commit()
        return True
    except:
        return False

def get_username(id):
    sql = "SELECT username FROM Users WHERE id=:id"
    username = db.session.execute(sql, {"id":id}).fetchone()
    if username.username != None:
        return username.username
    else:
        return 0

def get_userid(username):
    sql = "SELECT id FROM Users WHERE username=:username"
    id = db.session.execute(sql, {"username":username}).fetchone()
    if id.id != None:
        return id.id
    else:
        return 0