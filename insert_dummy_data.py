from vernam_cipher import encrypt
from helpers import generate_key, generate_salt

import sqlite3

con = sqlite3.connect("db/database.db")

def insert_student(details):

    cur = con.cursor()
    cur.execute(f"INSERT INTO students (username, first_name, surname, password, salt, key, year_group) VALUES (?, ?, ?, ?, ?, ?, ?)", details)
    con.commit()
    cur.close()
    
def insert_teacher(details):
    cur = con.cursor()
    cur.execute(f"INSERT INTO teachers (username, first_name, surname, password, salt, key) VALUES (?, ?, ?, ?, ?, ?)", details)
    con.commit()
    cur.close()

fname = input("first name: ")
sname = input("surname: ")
username = input("username: ")

password = input("password: ")
salt = generate_salt()
hash_pw = str(hash(password + salt))
key = generate_key(len(hash_pw))
encrypted_pw = encrypt(hash_pw, key)

type = input("student (s) or teacher (t): ")

# details = {
#     "username": username,
#     "fname": fname,
#     "sname": sname,
#     "password": encrypted_pw,
#     "salt": salt,
#     "key": key
# }

details = [(username), (fname), (sname), (encrypted_pw), (salt), (key)]

if type == "s":
    # insert into student table
    year_group = int(input("year group: "))
    details.append(year_group)
    insert_student(details)

elif type == "t":
    # insert into teacher table
    insert_teacher(details)

