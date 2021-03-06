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
    return render_template("addkanji.html", groups=groups, error=False, success=False)

def addkanjitodb():
    try:
        group = request.form["group"]
    except:
        groups = db.session.execute("SELECT id, name FROM Groups").fetchall()
        return render_template("addkanji.html", groups=groups, error=True, success=False)
    kanji = request.form["kanji"]
    meaning = request.form["meaning"]
    kun = request.form["kun"]
    ony = request.form["ony"]
    if len(kanji) == 0 or len(meaning) == 0:
        groups = db.session.execute("SELECT id, name FROM Groups").fetchall()
        return render_template("addkanji.html", groups=groups, error=True, success=False)
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
        groups = db.session.execute("SELECT id, name FROM Groups").fetchall()
        return render_template("addkanji.html", groups=groups, error=False, success=True)
    except:
        groups = db.session.execute("SELECT id, name FROM Groups").fetchall()
        return render_template("addkanji.html", groups=groups, error=True, success=False)

def addmeaning():
    kanji = db.session.execute("SELECT id, kanji FROM Kanji").fetchall()
    return render_template("addmeaning.html", kanji=kanji, success=False, error=False)

def addmeaningtodb():
    addto = request.form.getlist("addto")
    kanji_id = request.form["kanji_id"]
    meaning = request.form["meaning"]
    kun = request.form["kun"]
    ony = request.form["ony"]
    success = False
    error = False
    if session["csrf_token"] != request.form["csrf_token"]:
        abort(403)
    if ("M" in addto and len(meaning) == 0) or ("K" in addto and len(kun) == 0) or ("O" in addto and len(ony) == 0):
        error = True
        kanji = db.session.execute("SELECT id, kanji FROM Kanji").fetchall()
        return render_template("addmeaning.html", kanji=kanji, success=success, error=error)
    if "M" in addto and len(meaning) > 0:
        meaningsql = "INSERT INTO Meaning (meaning, kanji_id) VALUES (:meaning, :kanji_id)"
        db.session.execute(meaningsql, {"meaning":meaning, "kanji_id":kanji_id})
        db.session.commit()
        success = True
    if "K" in addto and len(kun) > 0:
        kunsql = "INSERT INTO Kunyomi (kun, kanji_id) VALUES (:kun, :kanji_id)"
        db.session.execute(kunsql, {"kun":kun, "kanji_id":kanji_id})
        db.session.commit()
        success = True
    if "O" in addto and len(ony) > 0:
        onsql = "INSERT INTO Onyomi (ony, kanji_id) VALUES (:ony, :kanji_id)"
        db.session.execute(onsql, {"ony":ony, "kanji_id":kanji_id})
        db.session.commit()
        success = True
    kanji = db.session.execute("SELECT id, kanji FROM Kanji").fetchall()
    return render_template("addmeaning.html", kanji=kanji, success=success, error=error)

def remove():
    kanji = db.session.execute("SELECT id, kanji FROM Kanji").fetchall()
    return render_template("remove.html", kanji=kanji, success=False)

def removefromdb():
    if session["csrf_token"] != request.form["csrf_token"]:
        abort(403)
    kanji_id = request.form["kanji_id"]
    meaningsql = "DELETE FROM Meaning WHERE kanji_id=:id"
    kunsql = "DELETE FROM Kunyomi WHERE kanji_id=:id"
    onsql = "DELETE FROM Onyomi WHERE kanji_id=:id"
    sql = "DELETE FROM Kanji WHERE id=:id"
    db.session.execute(meaningsql, {"id":kanji_id})
    db.session.execute(kunsql, {"id":kanji_id})
    db.session.execute(onsql, {"id":kanji_id})
    db.session.execute(sql, {"id":kanji_id})
    db.session.commit()
    kanji = db.session.execute("SELECT id, kanji FROM Kanji").fetchall()
    return render_template("remove.html", kanji=kanji, success=True)

def addcomb():
    groups = db.session.execute("SELECT id, name FROM CombGroups").fetchall()
    return render_template("addcomb.html", groups=groups, error=False, success=False)

def addcombtodb():
    try:
        group = request.form["group"]
    except:
        groups = db.session.execute("SELECT id, name FROM CombGroups").fetchall()
        return render_template("addcomb.html", groups=groups, error=True, success=False)
    kanji = request.form["kanji"]
    meaning = request.form["meaning"]
    yomikata = request.form["yomikata"]
    if len(kanji) == 0 or len(meaning) == 0:
        groups = db.session.execute("SELECT id, name FROM CombGroups").fetchall()
        return render_template("addcomb.html", groups=groups, error=True, success=False)
    try:
        if session["csrf_token"] != request.form["csrf_token"]:
            abort(403)
        db.session.execute("INSERT INTO COMBINATIONS (kanji, meaning, yomikata, group_id) VALUES (:kanji, :meaning, :yomikata, :group_id)", {"kanji":kanji, "meaning":meaning, "yomikata":yomikata, "group_id":group})
        db.session.commit()
        groups = db.session.execute("SELECT id, name FROM CombGroups").fetchall()
        return render_template("addcomb.html", groups=groups, error=False, success=True)
    except:
        groups = db.session.execute("SELECT id, name FROM CombGroups").fetchall()
        return render_template("addcomb.html", groups=groups, error=True, success=False)

def removecomb():
    kanji = db.session.execute("SELECT id, kanji FROM COMBINATIONS").fetchall()
    return render_template("removecomb.html", kanji=kanji, success=False)

def removecombdb():
    if session["csrf_token"] != request.form["csrf_token"]:
        abort(403)
    kanji_id = request.form["kanji_id"]
    sql = "DELETE FROM COMBINATIONS WHERE id=:id"
    db.session.execute(sql, {"id":kanji_id})
    db.session.commit()
    kanji = db.session.execute("SELECT id, kanji FROM COMBINATIONS").fetchall()
    return render_template("removecomb.html", kanji=kanji, success=True)