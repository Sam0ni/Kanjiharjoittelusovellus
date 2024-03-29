# this file is only used for initializing new database
# change this file's name to db.py or copy the code to the original db.py
# after initialization copy back the original db.py

from app import app
from flask_sqlalchemy import SQLAlchemy
from os import getenv
import re

app.config["SQLALCHEMY_DATABASE_URI"] = getenv("DATABASE_URL").replace("://", "ql://", 1)
db = SQLAlchemy(app)

db.session.execute("CREATE TABLE Groups (id SERIAL PRIMARY KEY, name TEXT)")
db.session.execute("CREATE TABLE Kanji (id SERIAL PRIMARY KEY, kanji VARCHAR UNIQUE, group_id INTEGER REFERENCES Groups)")
db.session.execute("CREATE TABLE Meaning (meaning TEXT, kanji_id INTEGER REFERENCES Kanji)")
db.session.execute("CREATE TABLE Kunyomi (kun TEXT, kanji_id INTEGER REFERENCES Kanji)")
db.session.execute("CREATE TABLE Onyomi (Ony TEXT, kanji_id INTEGER REFERENCES Kanji)")
db.session.execute("CREATE TABLE CombGroups (id SERIAL PRIMARY KEY, name TEXT)")
db.session.execute("CREATE TABLE COMBINATIONS (id SERIAL PRIMARY KEY, kanji VARCHAR UNIQUE, meaning TEXT, yomikata TEXT, group_id INTEGER REFERENCES CombGroups)")
db.session.execute("CREATE TABLE Users (id SERIAL PRIMARY KEY, username TEXT UNIQUE, password TEXT, admin BOOLEAN)")
db.session.execute("CREATE TABLE Answers (id SERIAL PRIMARY KEY, user_id INTEGER, kanji_id INTEGER, answer BOOLEAN)")
db.session.execute("INSERT INTO Groups (id, name) VALUES (1, 'ykkonen')")
db.session.execute("INSERT INTO Groups (id, name) VALUES (2, 'kakkonen')")
db.session.execute("INSERT INTO Kanji (kanji, group_id) VALUES ('日', 1)")
db.session.execute("INSERT INTO Kanji (kanji, group_id) VALUES ('月', 1)")
db.session.execute("INSERT INTO Kanji (kanji, group_id) VALUES ('水', 1)")
db.session.execute("INSERT INTO Kanji (kanji, group_id) VALUES ('火', 2)")
db.session.execute("INSERT INTO Kanji (kanji, group_id) VALUES ('金 ', 2)")
db.session.execute("INSERT INTO Meaning (meaning, kanji_id) VALUES ('päivä', 1)")
db.session.execute("INSERT INTO Meaning (meaning, kanji_id) VALUES ('aurinko', 1)")
db.session.execute("INSERT INTO Meaning (meaning, kanji_id) VALUES ('kuu', 2)")
db.session.execute("INSERT INTO Meaning (meaning, kanji_id) VALUES ('kuukausi', 2)")
db.session.execute("INSERT INTO Meaning (meaning, kanji_id) VALUES ('vesi', 3)")
db.session.execute("INSERT INTO Meaning (meaning, kanji_id) VALUES ('tuli', 4)")
db.session.execute("INSERT INTO Meaning (meaning, kanji_id) VALUES ('kulta', 5)")
db.session.execute("INSERT INTO Kunyomi (kun, kanji_id) VALUES ('hi', 1)")
db.session.execute("INSERT INTO Kunyomi (kun, kanji_id) VALUES ('bi', 1)")
db.session.execute("INSERT INTO Kunyomi (kun, kanji_id) VALUES ('tsuki', 2)")
db.session.execute("INSERT INTO Kunyomi (kun, kanji_id) VALUES ('mizu', 3)")
db.session.execute("INSERT INTO Kunyomi (kun, kanji_id) VALUES ('hi', 4)")
db.session.execute("INSERT INTO Kunyomi (kun, kanji_id) VALUES ('kane', 5)")
db.session.execute("INSERT INTO Onyomi (ony, kanji_id) VALUES ('nichi', 1)")
db.session.execute("INSERT INTO Onyomi (ony, kanji_id) VALUES ('ni', 1)")
db.session.execute("INSERT INTO Onyomi (ony, kanji_id) VALUES ('gatsu', 2)")
db.session.execute("INSERT INTO Onyomi (ony, kanji_id) VALUES ('getsu', 2)")
db.session.execute("INSERT INTO Onyomi (ony, kanji_id) VALUES ('sui', 3)")
db.session.execute("INSERT INTO Onyomi (ony, kanji_id) VALUES ('ka', 4)")
db.session.execute("INSERT INTO Onyomi (ony, kanji_id) VALUES ('kin', 5)")
db.session.execute("INSERT INTO CombGroups (id, name) VALUES (1, 'ykkonen')")
db.session.execute("INSERT INTO CombGroups (id, name) VALUES (2, 'kakkonen')")
db.session.execute("INSERT INTO COMBINATIONS (kanji, meaning, yomikata, group_id) VALUES ('日本', 'japani', 'nihon', 1)")
db.session.execute("INSERT INTO COMBINATIONS (kanji, meaning, yomikata, group_id) VALUES ('花火', 'ilotulite', 'hanabi', 1)")

db.session.commit()
