from db import db

def readexercises():
    sql = "SELECT * FROM Groups"
    result = db.session.execute(sql)
    return result.fetchall()

def readexersiceskanji(id):
    kanjitsql = "SELECT id, kanji FROM Kanji WHERE group_id=:id"
    kanjitcom = db.session.execute(kanjitsql, {"id":id})
    return kanjitcom.fetchall()

def readresult(id, read, kun, on):
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
        return (True, meaning, kunyomi, onyomi)
    else:
        return (False, meaning, kunyomi, onyomi)

def combinationexercises():
    sql = "SELECT * FROM CombGroups"
    result = db.session.execute(sql)
    return result.fetchall()

def combexercisekanji(id):
    kanjitsql = "SELECT id, kanji FROM Combinations WHERE group_id=:id"
    kanjitcom = db.session.execute(kanjitsql, {"id":id})
    return kanjitcom.fetchall()

def combinationresult(id, read, yomikata):
    sql = "SELECT meaning, yomikata FROM Combinations WHERE id=:id"
    sqlcom = db.session.execute(sql, {"id":id})
    results = sqlcom.fetchone()
    readright = False
    meaningright = False
    if results[0] == read:
        meaningright = True
    if results[1] == yomikata:
        readright = True
    if readright and meaningright:
        return (True, results)
    else:
        return (False, results)