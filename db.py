from app import app
from flask_sqlalchemy import SQLAlchemy
from os import getenv
import re

app.config["SQLALCHEMY_DATABASE_URI"] = getenv("DATABASE_URL").replace("://", "ql://", 1)
db = SQLAlchemy(app)

db.session.execute("INSERT INTO Groups (id, name) VALUES (1, 'ykkonen');
INSERT INTO Groups (id, name) VALUES (2, 'kakkonen');
INSERT INTO Kanji (kanji, group_id) VALUES ('日', 1);
INSERT INTO Kanji (kanji, group_id) VALUES ('月', 1);
INSERT INTO Kanji (kanji, group_id) VALUES ('水', 1);
INSERT INTO Kanji (kanji, group_id) VALUES ('火', 2);
INSERT INTO Kanji (kanji, group_id) VALUES ('金 ', 2);
INSERT INTO Meaning (meaning, kanji_id) VALUES ('päivä', 1);
INSERT INTO Meaning (meaning, kanji_id) VALUES ('aurinko', 1);
INSERT INTO Meaning (meaning, kanji_id) VALUES ('kuu', 2);
INSERT INTO Meaning (meaning, kanji_id) VALUES ('kuukausi', 2);
INSERT INTO Meaning (meaning, kanji_id) VALUES ('vesi', 3);
INSERT INTO Meaning (meaning, kanji_id) VALUES ('tuli', 4);
INSERT INTO Meaning (meaning, kanji_id) VALUES ('kulta', 5);
INSERT INTO Kunyomi (kun, kanji_id) VALUES ('hi', 1);
INSERT INTO Kunyomi (kun, kanji_id) VALUES ('bi', 1);
INSERT INTO Kunyomi (kun, kanji_id) VALUES ('tsuki', 2);
INSERT INTO Kunyomi (kun, kanji_id) VALUES ('mizu', 3);
INSERT INTO Kunyomi (kun, kanji_id) VALUES ('hi', 4);
INSERT INTO Kunyomi (kun, kanji_id) VALUES ('kane', 5);
INSERT INTO Onyomi (ony, kanji_id) VALUES ('nichi', 1);
INSERT INTO Onyomi (ony, kanji_id) VALUES ('ni', 1);
INSERT INTO Onyomi (ony, kanji_id) VALUES ('gatsu', 2);
INSERT INTO Onyomi (ony, kanji_id) VALUES ('getsu', 2);
INSERT INTO Onyomi (ony, kanji_id) VALUES ('sui', 3);
INSERT INTO Onyomi (ony, kanji_id) VALUES ('ka', 4);
INSERT INTO Onyomi (ony, kanji_id) VALUES ('kin', 5);
INSERT INTO CombGroups (id, name) VALUES (1, 'ykkonen');
INSERT INTO CombGroups (id, name) VALUES (2, 'kakkonen');
INSERT INTO COMBINATIONS (kanji, meaning, yomikata, group_id) VALUES ('日本', 'japani', 'nihon', 1);
INSERT INTO COMBINATIONS (kanji, meaning, yomikata, group_id) VALUES ('花火', 'ilotulite', 'hanabi', 1);")
db.session.commit()
