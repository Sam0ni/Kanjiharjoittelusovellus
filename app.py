from flask import Flask
from flask import redirect, render_template, request, session
from flask_sqlalchemy import SQLAlchemy
import os
import re

uri = os.getenv("DATABASE_URL")  # or other relevant config var
if uri.startswith("postgres://"):
    uri = uri.replace("postgres://", "postgresql://")

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = uri
#app.config["SQLALCHEMY_DATABASE_URI"] = getenv("DATABASE_URL")
db = SQLAlchemy(app)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/readexercises")
def readexercises():
    sql = "SELECT * FROM Groups"
    result = db.session.execute(sql)
    exercises = result.fetchall()
    return render_template("readingexercises.html", exercises=exercises)

@app.route("/readexercise/<int:id>")
def readexercise(id):
    kanjitsql = "SELECT id, kanji FROM Kanji WHERE group_id=:id"
    kanjitcom = db.session.execute(kanjitsql, {"id":id})
    kanjit = kanjitcom.fetchall()
    return render_template("readingquestions.html", kanjit=kanjit, groupid=id, counter=1, oikein=0)

@app.route("/readresult", methods=["POST"])
def readresult():
    id = request.form["id"]
    groupid = request.form["groupid"]
    counter = request.form["counter"]
    read = request.form["meaning"]
    kun = request.form["kun-yomi"]
    on = request.form["on-yomi"]
    oikein = int(request.form["oikein"])
    meaningsql = "SELECT meaning FROM Meaning WHERE kanji_id=:id"
    meaningcom = db.session.execute(meaningsql, {"id":id})
    meaning = meaningcom.fetchall()
    kunyomisql = "SELECT kun FROM Kunyomi WHERE kanji_id=:id"
    onyomisql = "SELECT ony FROM Onyomi WHERE kanji_id=:id"
    kunyomicom = db.session.execute(kunyomisql, {"id":id})
    kunyomi = kunyomicom.fetchall()
    onyomicom = db.session.execute(onyomisql, {"id":id})
    onyomi = onyomicom.fetchall()
    readoikein = False
    kunoikein = False
    onoikein = False
    for i in meaning:
        if read == i[0]:
            readoikein = True
            break
    for i in kunyomi:
        if kun == i[0]:
            kunoikein = True
            break
    for i in onyomi:
        if on == i[0]:
            onoikein = True
            break
    if kunoikein and onoikein and readoikein:
        oikein += 1
        return render_template("correctanswers.html", meaning=meaning, kunyomi=kunyomi, onyomi=onyomi, counter=counter, groupid=groupid, oikein=oikein) 
    else:
        return render_template("notcorrectanswers.html", meaning=meaning, kunyomi=kunyomi, onyomi=onyomi, counter=counter, groupid=groupid, oikein=oikein)

@app.route("/next", methods=["POST"])
def next():
    counter = int(request.form["counter"])
    groupid = request.form["groupid"]
    oikein = int(request.form["oikein"])
    kanjitsql = "SELECT id, kanji FROM Kanji WHERE group_id=:id"
    kanjitcom = db.session.execute(kanjitsql, {"id":groupid})
    kanjit = kanjitcom.fetchall()
    kanjit = kanjit[counter:]
    counter += 1
    if len(kanjit) > 0:
        return render_template("readingquestions.html", kanjit=kanjit, groupid=groupid, counter=counter, oikein=oikein)
    else:
        return render_template("status.html", counter=counter-1, oikein=oikein)

@app.route("/combinationexercise")
def combinations():
    sql = "SELECT * FROM CombGroups"
    result = db.session.execute(sql)
    exercises = result.fetchall()
    return render_template("combinationexercises.html", exercises=exercises)

@app.route("/combinationexercise/<int:id>")
def combinationexercise(id):
    kanjitsql = "SELECT id, kanji FROM Combinations WHERE group_id=:id"
    kanjitcom = db.session.execute(kanjitsql, {"id":id})
    kanjit = kanjitcom.fetchall()
    return render_template("combinationquestions.html", kanjit=kanjit, groupid=id, counter=1, oikein=0)

@app.route("/combinationresult", methods=["POST"])
def combinationresult():
    id = request.form["id"]
    groupid = request.form["groupid"]
    counter = request.form["counter"]
    oikein = int(request.form["oikein"])
    read = request.form["meaning"]
    yomikata = request.form["read"]
    sql = "SELECT meaning, yomikata FROM Combinations WHERE id=:id"
    sqlcom = db.session.execute(sql, {"id":id})
    results = sqlcom.fetchone()
    readoikein = False
    meaningoikein = False
    if results[0] == read:
        meaningoikein = True
    if results[1] == yomikata:
        readoikein = True
    if readoikein and meaningoikein:
        oikein += 1
        return render_template("combcorrectanswers.html", counter=counter, groupid=groupid, oikein=oikein) 
    else:
        return render_template("combnotcorrectanswers.html", results=results, counter=counter, groupid=groupid, oikein=oikein)

@app.route("/combnext", methods=["POST"])
def combnext():
    counter = int(request.form["counter"])
    groupid = request.form["groupid"]
    oikein = int(request.form["oikein"])
    kanjitsql = "SELECT id, kanji FROM Combinations WHERE group_id=:id"
    kanjitcom = db.session.execute(kanjitsql, {"id":groupid})
    kanjit = kanjitcom.fetchall()
    kanjit = kanjit[counter:]
    counter += 1
    if len(kanjit) > 0:
        return render_template("combinationquestions.html", kanjit=kanjit, groupid=groupid, counter=counter, oikein=oikein)
    else:
        return render_template("status.html", counter=counter-1, oikein=oikein)

#TESTI
@app.route("/createtables")
def createtables():
    db.create_all()
    sql =   ["CREATE TABLE Groups (id SERIAL PRIMARY KEY, name TEXT)",
            "CREATE TABLE Kanji (id SERIAL PRIMARY KEY, kanji VARCHAR, group_id INTEGER REFERENCES Groups)",
            "CREATE TABLE Meaning (meaning TEXT, kanji_id INTEGER REFERENCES Kanji)",
            "CREATE TABLE Kunyomi (kun TEXT, kanji_id INTEGER REFERENCES Kanji)",
            "CREATE TABLE Onyomi (Ony TEXT, kanji_id INTEGER REFERENCES Kanji)",
            "CREATE TABLE CombGroups (id SERIAL PRIMARY KEY, name TEXT)",
            "CREATE TABLE COMBINATIONS (id SERIAL PRIMARY KEY, kanji VARCHAR, meaning TEXT, yomikata TEXT, group_id INTEGER REFERENCES CombGroups)",
            "INSERT INTO Groups (id, name) VALUES (1, 'ykkonen')",
            "INSERT INTO Groups (id, name) VALUES (2, 'kakkonen')",
            "INSERT INTO Kanji (kanji, group_id) VALUES ('日', 1)",
            "INSERT INTO Kanji (kanji, group_id) VALUES ('月', 1)",
            "INSERT INTO Meaning (meaning, kanji_id) VALUES ('päivä', 1)",
            "INSERT INTO Meaning (meaning, kanji_id) VALUES ('aurinko', 1)",
            "INSERT INTO Meaning (meaning, kanji_id) VALUES ('kuu', 2)",
            "INSERT INTO Meaning (meaning, kanji_id) VALUES ('kuukausi', 2)",
            "INSERT INTO Kunyomi (kun, kanji_id) VALUES ('hi', 1)",
            "INSERT INTO Kunyomi (kun, kanji_id) VALUES ('bi', 1)",
            "INSERT INTO Kunyomi (kun, kanji_id) VALUES ('tsuki', 2)",
            "INSERT INTO Onyomi (ony, kanji_id) VALUES ('nichi', 1)",
            "INSERT INTO Onyomi (ony, kanji_id) VALUES ('ni', 1)",
            "INSERT INTO Onyomi (ony, kanji_id) VALUES ('gatsu', 2)",
            "INSERT INTO Onyomi (ony, kanji_id) VALUES ('getsu', 2)",
            "INSERT INTO CombGroups (id, name) VALUES (2, 'ykkonen')",
            "INSERT INTO CombGroups (id, name) VALUES (1, 'kakkonen')",
            "INSERT INTO COMBINATIONS (kanji, meaning, yomikata, group_id) VALUES ('日本', 'japani', 'nihon', 1)",
            "INSERT INTO COMBINATIONS (kanji, meaning, yomikata, group_id) VALUES ('花火', 'ilotulite', 'hanabi', 1)"]
    for i in sql:
        db.session.execute(i)
    db.session.commit()
    return redirect("/")




@app.route("/addgroup")
def addgroup():
    return render_template("addgroup.html")

@app.route("/addtodb", methods=["POST"])
def addtodb():
    ryhma = request.form["ryhma"]
    name = request.form["name"]
    if ryhma == "1":
        db.session.execute("INSERT INTO Groups (name) VALUES (':name')", {"name":name})
        db.session.commit()
        return redirect("/")
    else:
        db.session.execute("INSERT INTO CombGroups (name) VALUES (':name')", {"name":name})