from app import app
from flask import render_template, request, redirect, session
import exercises
import users
from random import shuffle, randint, Random


@app.route("/")
def index():
    try:
        if session["userid"]:
            username = users.get_username(session["userid"])
        return render_template("index.html", username=username)
    except:
        username = 0
        return render_template("index.html", username=username)

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
    id = request.form["id"]
    groupid = request.form["groupid"]
    counter = request.form["counter"]
    read = request.form["meaning"]
    kun = request.form["kun-yomi"]
    on = request.form["on-yomi"]
    right = int(request.form["right"])
    results = exercises.readresult(id, read, kun, on)
    if results[0]:
        right += 1
        try:
            if session["userid"]:
                print("vehnäinenkosto")
                exercises.write_results(id, True, session["userid"])
        except:
            pass
        return render_template("correctanswers.html", meaning=results[1], kunyomi=results[2], onyomi=results[3], counter=counter, groupid=groupid, right=right) 
    else:
        try:
            if session["userid"]:
                exercises.write_results(id, False, session["userid"])
        except:
            pass
        return render_template("notcorrectanswers.html", meaning=results[1], kunyomi=results[2], onyomi=results[3], counter=counter, groupid=groupid, right=right, yread=read, ykun=kun, yon=on)

@app.route("/next", methods=["POST"])
def next():
    counter = int(request.form["counter"])
    groupid = request.form["groupid"]
    right = int(request.form["right"])
    kanji = exercises.readexersiceskanji(groupid)
    kanji = kanji[counter:]
    counter += 1
    if len(kanji) > 0:
        return render_template("readingquestions.html", kanji=kanji, groupid=groupid, counter=counter, right=right)
    else:
        return render_template("status.html", counter=counter-1, right=right)

@app.route("/combinationexercise")
def combinations():
    allexercises = exercises.combinationexercises()
    return render_template("combinationexercises.html", exercises=allexercises)

@app.route("/combinationexercise/<int:id>")
def combinationexercise(id):
    kanji = exercises.combexercisekanji(id)
    return render_template("combinationquestions.html", kanji=kanji, groupid=id, counter=1, right=0)

@app.route("/combinationresult", methods=["POST"])
def combinationresult():
    id = request.form["id"]
    groupid = request.form["groupid"]
    counter = request.form["counter"]
    right = int(request.form["right"])
    read = request.form["meaning"]
    yomikata = request.form["read"]
    results = exercises.combinationresult(id, read, yomikata)
    if results[0]:
        right += 1
        return render_template("combcorrectanswers.html", counter=counter, groupid=groupid, right=right) 
    else:
        return render_template("combnotcorrectanswers.html", results=results[1], counter=counter, groupid=groupid, right=right, yread=read, yyomikata=yomikata)

@app.route("/combnext", methods=["POST"])
def combnext():
    counter = int(request.form["counter"])
    groupid = request.form["groupid"]
    right = int(request.form["right"])
    kanji = exercises.combexercisekanji(groupid)
    kanji = kanji[counter:]
    counter += 1
    if len(kanji) > 0:
        return render_template("combinationquestions.html", kanji=kanji, groupid=groupid, counter=counter, right=right)
    else:
        return render_template("status.html", counter=counter-1, right=right)


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
        userid = users.get_userid(username)
        session["userid"] = userid
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
        userid = users.get_userid(username)
        session["userid"] = userid
        return redirect("/")
    else:
        return render_template("register.html", error=True)

@app.route("/logout")
def logout():
    del session["userid"]
    return redirect("/")

@app.route("/randomize")
def randomize():
    id = str(session["userid"])
    kanji = exercises.randomize(id)
    seed = randint(1, 100)
    Random(seed).shuffle(kanji)
    kanji_id = kanji[0][0]
    currentkanji = exercises.get_kanji(kanji_id)
    if len(kanji) < 2:
        return render_template("randomizeerror.html")
    else:
        return render_template("randomquestions.html", kanji=currentkanji, kanji_id=kanji_id, counter=1, right=0, seed=seed)

@app.route("/randomresults", methods=["POST"])
def randomresult():
    id = request.form["id"]
    counter = request.form["counter"]
    read = request.form["meaning"]
    kun = request.form["kun-yomi"]
    on = request.form["on-yomi"]
    right = int(request.form["right"])
    seed = request.form["seed"]
    results = exercises.readresult(id, read, kun, on)
    if results[0]:
        right += 1
        return render_template("randomcorrectanswers.html", meaning=results[1], kunyomi=results[2], onyomi=results[3], counter=counter, right=right, seed=seed) 
    else:
        return render_template("randomnotcorrectanswers.html", meaning=results[1], kunyomi=results[2], onyomi=results[3], counter=counter, right=right, yread=read, ykun=kun, yon=on, seed=seed)

@app.route("/randomnext", methods=["POST"])
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