from db import db

def readexersices():
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
        return True
    else:
        return False

