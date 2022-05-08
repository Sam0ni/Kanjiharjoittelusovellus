from db import db
from flask import render_template, request, redirect, session

def combinationexercises():
    sql = "SELECT * FROM CombGroups"
    result = db.session.execute(sql)
    return result.fetchall()

def combexercisekanji(id):
    kanjitsql = "SELECT id, kanji FROM Combinations WHERE group_id=:id"
    kanjitcom = db.session.execute(kanjitsql, {"id":id})
    return kanjitcom.fetchall()

def combinationresult():
    id = request.form["id"]
    groupid = request.form["groupid"]
    counter = request.form["counter"]
    right = int(request.form["right"])
    read = request.form["meaning"]
    yomikata = request.form["read"]
    sql = "SELECT meaning, yomikata FROM Combinations WHERE id=:id"
    sqlcom = db.session.execute(sql, {"id":id})
    results = sqlcom.fetchone()
    readright = False
    meaningright = False
    if results[0] == read.lower():
        meaningright = True
    if results[1] == yomikata.lower():
        readright = True
    if readright and meaningright:
        right += 1
        return render_template("combcorrectanswers.html", counter=counter, groupid=groupid, right=right) 
    else:
        return render_template("combnotcorrectanswers.html", results=results, counter=counter, groupid=groupid, right=right, yread=read, yyomikata=yomikata)

def combnext():
    counter = int(request.form["counter"])
    groupid = request.form["groupid"]
    right = int(request.form["right"])
    kanji = combexercisekanji(groupid)
    kanji = kanji[counter:]
    counter += 1
    if len(kanji) > 0:
        return render_template("combinationquestions.html", kanji=kanji, groupid=groupid, counter=counter, right=right)
    else:
        return render_template("status.html", counter=counter-1, right=right)
