from flask import Flask
from flask import redirect, render_template, request, session
from flask_sqlalchemy import SQLAlchemy
from os import getenv

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = getenv("DATABASE_URL")
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
    return render_template("readingquestions.html", kanjit=kanjit, groupid=id, counter=1)

@app.route("/readresult", methods=["POST"])
def readresult():
    id = request.form["id"]
    groupid = request.form["groupid"]
    counter = request.form["counter"]
    read = request.form["meaning"]
    kun = request.form["kun-yomi"]
    on = request.form["on-yomi"]
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
        return render_template("correctanswers.html", meaning=meaning, kunyomi=kunyomi, onyomi=onyomi, counter=counter, groupid=groupid) 
    else:
        return render_template("notcorrectanswers.html", meaning=meaning, kunyomi=kunyomi, onyomi=onyomi, counter=counter, groupid=groupid)

@app.route("/next", methods=["POST"])
def next():
    counter = int(request.form["counter"])
    groupid = request.form["groupid"]
    kanjitsql = "SELECT id, kanji FROM Kanji WHERE group_id=:id"
    kanjitcom = db.session.execute(kanjitsql, {"id":groupid})
    kanjit = kanjitcom.fetchall()
    kanjit = kanjit[counter:]
    counter += 1
    if len(kanjit) > 0:
        return render_template("readingquestions.html", kanjit=kanjit, groupid=groupid, counter=counter)
    else:
        return render_template("status.html")

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
    return render_template("combinationquestions.html", kanjit=kanjit, groupid=id, counter=1)

@app.route("/combinationresult", methods=["POST"])
def combinationresult():
    id = request.form["id"]
    groupid = request.form["groupid"]
    counter = request.form["counter"]
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
        return render_template("combcorrectanswers.html", counter=counter, groupid=groupid) 
    else:
        return render_template("combnotcorrectanswers.html", results=results, counter=counter, groupid=groupid)

@app.route("/combnext", methods=["POST"])
def combnext():
    counter = int(request.form["counter"])
    groupid = request.form["groupid"]
    kanjitsql = "SELECT id, kanji FROM Combinations WHERE group_id=:id"
    kanjitcom = db.session.execute(kanjitsql, {"id":groupid})
    kanjit = kanjitcom.fetchall()
    kanjit = kanjit[counter:]
    counter += 1
    if len(kanjit) > 0:
        return render_template("combinationquestions.html", kanjit=kanjit, groupid=groupid, counter=counter)
    else:
        return render_template("status.html")