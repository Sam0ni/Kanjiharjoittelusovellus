from db import db
from flask import render_template, request, redirect, session
import exercises
from random import randint, Random


def randomize():
    id = str(session["userid"])
    kanji = exercises.randomize(id)
    seed = randint(1, 100)
    Random(seed).shuffle(kanji)
    if len(kanji) < 2 or kanji is None:
        return render_template("randomizeerror.html")
    kanji_id = kanji[0][0]
    currentkanji = exercises.get_kanji(kanji_id)   
    return render_template("randomquestions.html", kanji=currentkanji, kanji_id=kanji_id, counter=1, right=0, seed=seed)

def readresult():
    id = request.form["id"]
    counter = request.form["counter"]
    read = request.form["meaning"]
    kun = request.form["kun-yomi"]
    on = request.form["on-yomi"]
    right = int(request.form["right"])
    seed = request.form["seed"]
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
        return render_template("randomcorrectanswers.html", meaning=meaning, kunyomi=kunyomi, onyomi=onyomi, counter=counter, right=right, seed=seed) 
    else:
        return render_template("randomnotcorrectanswers.html", meaning=meaning, kunyomi=kunyomi, onyomi=onyomi, counter=counter, right=right, yread=read, ykun=kun, yon=on, seed=seed)

def randomnext():
    try:
        counter = int(request.form["counter"])
        right = int(request.form["right"])
        seed = int(request.form["seed"])
        id = str(session["userid"])
        kanji = exercises.randomize(id)
        Random(seed).shuffle(kanji)
        kanji = kanji[counter:]
        kanji_id = kanji[0][0]
        currentkanji = exercises.get_kanji(kanji_id)
        counter += 1
        if len(kanji) > 0:
            return render_template("randomquestions.html", kanji=currentkanji, kanji_id=kanji_id, counter=counter, right=right, seed=seed)
    except:
        return render_template("status.html", counter=counter, right=right)