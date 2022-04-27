from app import app
from flask import render_template, request, redirect, session
import exercises
import users
import combinations
import randomizeexer
from random import shuffle, randint, Random


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/readexercises")
def readexercises():
    allexercises = exercises.readexercises()
    return render_template("readingexercises.html", exercises=allexercises)

@app.route("/readexercise/<int:id>")
def readexercise(id):
    kanji = exercises.readexersiceskanji(id)
    return render_template("readingquestions.html", kanji=kanji, groupid=id, counter=1, right=0)

@app.route("/readresult", methods=["POST"])
def readresult():
    return exercises.readresult()

@app.route("/next", methods=["POST"])
def next():
    return exercises.next()

@app.route("/combinationexercise")
def combinations():
    allexercises = combinations.combinationexercises()
    return render_template("combinationexercises.html", exercises=allexercises)

@app.route("/combinationexercise/<int:id>")
def combinationexercise(id):
    kanji = combinations.combexercisekanji(id)
    return render_template("combinationquestions.html", kanji=kanji, groupid=id, counter=1, right=0)

@app.route("/combinationresult", methods=["POST"])
def combinationresult():
    return combinations.combinationresult()

@app.route("/combnext", methods=["POST"])
def combnext():
    return combinations.combnext()


# add functions not finished
    @app.route("/addgroup")
    def addgroup():
        return render_template("addgroup.html")

    @app.route("/addtodb", methods=["POST"])
    def addtodb():
        group = request.form["group"]
        name = request.form["name"]
        if group == "1":
            db.session.execute("INSERT INTO Groups (name) VALUES (':name')", {"name":name})
            db.session.commit()
            return redirect("/")
        else:
            db.session.execute("INSERT INTO CombGroups (name) VALUES (':name')", {"name":name})

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