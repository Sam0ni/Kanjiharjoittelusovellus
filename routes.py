from app import app
from flask import render_template, request
import exercises


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/readexercises")
def readexercises():
    allexercises = exercises.readexercises()
    return render_template("readingexercises.html", exercises=allexercises)

@app.route("/readexercise/<int:id>")
def readexercise(id):
    kanjit = exercises.readexersiceskanji(id)
    return render_template("readingquestions.html", kanjit=kanjit, groupid=id, counter=1, oikein=0)

@app.route("/readresult", methods=["POST"])
def readresult():
    id = request.form["id"]
    groupid = request.form["groupid"]
    counter = request.form["counter"]
    read = request.form["meaning"]
    kun = request.form["kun-yomi"]
    on = request.form["on-yomi"]
    right = int(request.form["oikein"])
    results = exercises.readresult(id, read, kun, on)
    if results[0]:
        right += 1
        return render_template("correctanswers.html", meaning=results[1], kunyomi=results[2], onyomi=results[3], counter=counter, groupid=groupid, oikein=right) 
    else:
        return render_template("notcorrectanswers.html", meaning=results[1], kunyomi=results[2], onyomi=results[3], counter=counter, groupid=groupid, oikein=right, yread=read, ykun=kun, yon=on)

@app.route("/next", methods=["POST"])
def next():
    counter = int(request.form["counter"])
    groupid = request.form["groupid"]
    oikein = int(request.form["oikein"])
    kanjit = exercises.readexersiceskanji(groupid)
    kanjit = kanjit[counter:]
    counter += 1
    if len(kanjit) > 0:
        return render_template("readingquestions.html", kanjit=kanjit, groupid=groupid, counter=counter, oikein=oikein)
    else:
        return render_template("status.html", counter=counter-1, oikein=oikein)

@app.route("/combinationexercise")
def combinations():
    allexercises = exercises.combinationexercises()
    return render_template("combinationexercises.html", exercises=allexercises)

@app.route("/combinationexercise/<int:id>")
def combinationexercise(id):
    kanji = exercises.combexercisekanji(id)
    return render_template("combinationquestions.html", kanjit=kanji, groupid=id, counter=1, oikein=0)

@app.route("/combinationresult", methods=["POST"])
def combinationresult():
    id = request.form["id"]
    groupid = request.form["groupid"]
    counter = request.form["counter"]
    oikein = int(request.form["oikein"])
    read = request.form["meaning"]
    yomikata = request.form["read"]
    results = exercises.combinationresult(id, read, yomikata)
    if results[0]:
        oikein += 1
        return render_template("combcorrectanswers.html", counter=counter, groupid=groupid, oikein=oikein) 
    else:
        return render_template("combnotcorrectanswers.html", results=results[1], counter=counter, groupid=groupid, oikein=oikein, yread=read, yyomikata=yomikata)

@app.route("/combnext", methods=["POST"])
def combnext():
    counter = int(request.form["counter"])
    groupid = request.form["groupid"]
    oikein = int(request.form["oikein"])
    kanjit = exercises.combexercisekanji(groupid)
    kanjit = kanjit[counter:]
    counter += 1
    if len(kanjit) > 0:
        return render_template("combinationquestions.html", kanjit=kanjit, groupid=groupid, counter=counter, oikein=oikein)
    else:
        return render_template("status.html", counter=counter-1, oikein=oikein)



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