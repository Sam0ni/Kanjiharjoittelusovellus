from app import app
from flask import render_template, request, redirect, session
import exercises
import users
import combinations
import randomizeexer
import addtodb
from random import shuffle, randint, Random


@app.route("/")
def index():
    try:
        admin = users.check_admin(session["username"])
        return render_template("index.html", admin=admin)
    except:
        return render_template("index.html", admin=False)

@app.route("/readexercises")
def readexercises():
    allexercises = exercises.readexercises()
    return render_template("readingexercises.html", exercises=allexercises, error = False)

@app.route("/readexercise/<int:id>")
def readexercise(id):
    kanji = exercises.readexersiceskanji(id)
    if len(kanji) == 0:
        allexercises = exercises.readexercises()
        return render_template("readingexercises.html", exercises=allexercises, error = True)
    return render_template("readingquestions.html", kanji=kanji, groupid=id, counter=1, right=0)

@app.route("/readresult", methods=["POST"])
def readresult():
    return exercises.readresult()

@app.route("/next", methods=["POST"])
def next():
    return exercises.next()

@app.route("/combinationexercise")
def combinationsexercises():
    allexercises = combinations.combinationexercises()
    return render_template("combinationexercises.html", exercises=allexercises, error=False)

@app.route("/combinationexercise/<int:id>")
def combinationexercise(id):
    kanji = combinations.combexercisekanji(id)
    if len(kanji) == 0:
        allexercises = combinations.combinationexercises()
        return render_template("combinationexercises.html", exercises=allexercises, error = True)
    return render_template("combinationquestions.html", kanji=kanji, groupid=id, counter=1, right=0)

@app.route("/combinationresult", methods=["POST"])
def combinationresult():
    return combinations.combinationresult()

@app.route("/combnext", methods=["POST"])
def combnext():
    return combinations.combnext()

@app.route("/addpage")
def addpage():
    if users.check_admin(session["username"]):
        return render_template("addpage.html")
    else:
        return render_template("notallowed.html")

@app.route("/addgroup")
def addgroup():
    if users.check_admin(session["username"]):
        return render_template("addgroup.html")
    else:
        return render_template("notallowed.html")

@app.route("/addtodb", methods=["POST"])
def addgrouptodb():
    if users.check_admin(session["username"]):
        return addtodb.addtodb()
    else:
        return render_template("notallowed.html")

@app.route("/addkanji")
def addkanji1():
    if users.check_admin(session["username"]):
        return addtodb.addkanji()
    else:
        return render_template("notallowed.html")

@app.route("/addkanjitodb", methods=["POST"])
def addkanjitodb1():
    if users.check_admin(session["username"]):
        return addtodb.addkanjitodb()
    else:
        return render_template("notallowed.html")

@app.route("/addmeaning")
def addmeaning1():
    if users.check_admin(session["username"]):
        return addtodb.addmeaning()
    else:
        return render_template("notallowed.html")

@app.route("/addmeaningtodb", methods=["POST"])
def addmeaningtodb1():
    if users.check_admin(session["username"]):
        return addtodb.addmeaningtodb()
    else:
        return render_template("notallowed.html")


@app.route("/loginpage")
def loginpage():
    return render_template("login.html", error=False)

@app.route("/checklogin", methods=["POST"])
def checklogin():
    username = request.form["username"]
    password = request.form["password"]
    if users.login(username, password):
        return redirect("/")
    else:
        return render_template("login.html", error=True)

@app.route("/registerpage")
def registerpage():
    return render_template("register.html", error=False)

@app.route("/checkregister", methods=["POST"])
def checkregister():
    username = request.form["username"]
    password = request.form["password"]
    if users.register(username, password):
        return redirect("/")
    else:
        return render_template("register.html", error=True)

@app.route("/logout")
def logout():
    users.logout()
    return redirect("/")

@app.route("/randomize")
def randomize():
    return randomizeexer.randomize()

@app.route("/randomresults", methods=["POST"])
def randomresult():
    return randomizeexer.readresult()

@app.route("/randomnext", methods=["POST"])
def randomnext():
    return randomizeexer.randomnext()

@app.route("/remove")
def remove():
    return addtodb.remove()

@app.route("/removefromdb", methods=["POST"])
def removefromdb():
    return addtodb.removefromdb()