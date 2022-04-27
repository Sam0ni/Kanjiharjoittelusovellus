from db import db
from flask import render_template, request, redirect, session

def readexercises():
    sql = "SELECT * FROM Groups"
    result = db.session.execute(sql)
    return result.fetchall()

def readexersiceskanji(id):
    kanjitsql = "SELECT id, kanji FROM Kanji WHERE group_id=:id"
    kanjitcom = db.session.execute(kanjitsql, {"id":id})
    return kanjitcom.fetchall()

def readresult():
    id = request.form["id"]
    groupid = request.form["groupid"]
    counter = request.form["counter"]
    read = request.form["meaning"]
    kun = request.form["kun-yomi"]
    on = request.form["on-yomi"]
    right = int(request.form["right"])
    meaningsql = "SELECT meaning FROM Meaning WHERE kanji_id=:id"
    meaningcom = db.session.execute(meaningsql, {"id":id})
    meaning = meaningcom.fetchall()
    kunyomisql = "SELECT kun FROM Kunyomi WHERE kanji_id=:id"
    onyomisql = "SELECT ony FROM Onyomi WHERE kanji_id=:id"
    kunyomicom = db.session.execute(kunyomisql, {"id":id})
    kunyomi = kunyomicom.fetchall()
    onyomicom = db.session.execute(onyomisql, {"id":id})
    onyomi = onyomicom.fetchall()
    readright = False
    kunright = False
    onright = False
    for i in meaning:
        if read == i[0]:
            readright = True
            break
    for i in kunyomi:
        if kun == i[0]:
            kunright = True
            break
    for i in onyomi:
        if on == i[0]:
            onright = True
            break
    if readright and kunright and onright:
        right += 1
        try:
            if session["userid"]:
                write_results(id, True, session["userid"])
        except:
            pass
        return render_template("correctanswers.html", meaning=meaning, kunyomi=kunyomi, onyomi=onyomi, counter=counter, groupid=groupid, right=right) 
    else:
        try:
            if session["userid"]:
                write_results(id, False, session["userid"])
        except:
            pass
        return render_template("notcorrectanswers.html", meaning=meaning[1], kunyomi=kunyomi, onyomi=onyomi, counter=counter, groupid=groupid, right=right, yread=read, ykun=kun, yon=on)

def write_results(id, result, userid):
    selectsql = "SELECT answer FROM Answers WHERE user_id=:userid AND kanji_id=:id"
    results = db.session.execute(selectsql, {"userid":userid, "id":id}).fetchone()
    if results == None:
        sql = "INSERT INTO Answers (user_id, kanji_id, answer) VALUES (:userid, :id, :result)"
        db.session.execute(sql, {"userid":userid, "id":id, "result":result})
        db.session.commit()
    else:
        if results[0]:
            return
        else:
            sql = "UPDATE Answers SET answer=:result WHERE user_id=:userid AND kanji_id=:id"
            db.session.execute(sql, {"userid":userid, "id":id, "result":result})
            db.session.commit()

def randomize(id):
    sql = "SELECT kanji_id FROM Answers WHERE answer=TRUE AND user_id=:userid"
    kanjilist = db.session.execute(sql, {"userid":id}).fetchall()
    return kanjilist

def get_kanji(id):
    sql = "SELECT kanji FROM Kanji WHERE id=:id"
    return db.session.execute(sql, {"id":id}).fetchone()

def next():
    counter = int(request.form["counter"])
    groupid = request.form["groupid"]
    right = int(request.form["right"])
    kanji = readexersiceskanji(groupid)
    kanji = kanji[counter:]
    counter += 1
    if len(kanji) > 0:
        return render_template("readingquestions.html", kanji=kanji, groupid=groupid, counter=counter, right=right)
    else:
        return render_template("status.html", counter=counter-1, right=right)
