from db import db
from flask import render_template, request, redirect, session, abort

def addtodb():
    group = request.form["group"]
    name = request.form["name"]
    if group == "1":
        if session["csrf_token"] != request.form["csrf_token"]:
            abort(403)
        db.session.execute("INSERT INTO Groups (name) VALUES (:name)", {"name":name})
        db.session.commit()
        return redirect("/")
    else:
        if session["csrf_token"] != request.form["csrf_token"]:
            abort(403)
        db.session.execute("INSERT INTO CombGroups (name) VALUES (:name)", {"name":name})
        db.session.commit()
        return redirect("/")

def addkanji():
    groups = db.session.execute("SELECT id, name FROM Groups").fetchall()
    return render_template("addkanji.html", groups=groups)

def addkanjitodb():
    group = request.form["group"]
    kanji = request.form["kanji"]
    meaning = request.form["meaning"]
    kun = request.form["kun"]
    ony = request.form["ony"]
    try:
        if session["csrf_token"] != request.form["csrf_token"]:
            abort(403)
        db.session.execute("INSERT INTO Kanji (kanji, group_id) VALUES (:kanji, :group_id)", {"kanji":kanji, "group_id":group})
        db.session.commit()
        kanji_id = db.session.execute("SELECT id FROM Kanji WHERE kanji=:kanji", {"kanji":kanji}).fetchone()
        kanji_id = kanji_id[0]
        meaningsql = "INSERT INTO Meaning (meaning, kanji_id) VALUES (:meaning, :kanji_id)"
        kunsql = "INSERT INTO Kunyomi (kun, kanji_id) VALUES (:kun, :kanji_id)"
        onsql = "INSERT INTO Onyomi (ony, kanji_id) VALUES (:ony, :kanji_id)"
        db.session.execute(onsql, {"ony":ony, "kanji_id":kanji_id})
        db.session.execute(kunsql, {"kun":kun, "kanji_id":kanji_id})
        db.session.execute(meaningsql, {"meaning":meaning, "kanji_id":kanji_id})
        db.session.commit()
        return redirect("/")
    except:
        return redirect("/")

def addmeaning():
    kanji = db.session.execute("SELECT id, kanji FROM Kanji").fetchall()
    return render_template("addmeaning.html", kanji=kanji)

def addmeaningtodb():
    addto = request.form.getlist("addto")
    kanji_id = request.form["kanji_id"]
    meaning = request.form["meaning"]
    kun = request.form["kun"]
    ony = request.form["ony"]
    if session["csrf_token"] != request.form["csrf_token"]:
        abort(403)
    if "M" in addto and len(meaning) > 0:
        meaningsql = "INSERT INTO Meaning (meaning, kanji_id) VALUES (:meaning, :kanji_id)"
        db.session.execute(meaningsql, {"meaning":meaning, "kanji_id":kanji_id})
        db.session.commit()
    if "K" in addto and len(kun) > 0:
        kunsql = "INSERT INTO Kunyomi (kun, kanji_id) VALUES (:kun, :kanji_id)"
        db.session.execute(kunsql, {"kun":kun, "kanji_id":kanji_id})
        db.session.commit()
    if "O" in addto and len(ony) > 0:
        onsql = "INSERT INTO Onyomi (ony, kanji_id) VALUES (:ony, :kanji_id)"
        db.session.execute(onsql, {"ony":ony, "kanji_id":kanji_id})
        db.session.commit()
    return redirect("/")