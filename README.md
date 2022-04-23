# Kanjiharjoittelusovellus

## Sovelluksen nykytilanne
Sovellukseen voi nyt kirjautua, ja läpikäytyjä merkkejä voi kerrata satunnaisessa järjestyksessä.
Sovelluksesta vielä puuttuu admin käyttjäjien toiminnot kuten merkkien lisääminen.

## sovelluksen testaaminen Herokussa
https://kanjiharjoittelusovellus.herokuapp.com/

lukutapa linkistä pääsee kertaamaan yksittäisiä kanji-merkkejä. Harjoitus 1:ssä on 3 merkkiä ja 2:ssa 2.

Tässä merkit ja niihin oikeat vastaukset (huom. "/" merkki tarkoittaa että kumpi vain käy, mutta ei molemmat):

Harjoitus 1:

日 merkitys: päivä/aurinko, kun-yomi: hi/bi, on-yomi: nichi/ni

月 merkitys: kuu/kuukausi, kun-yomi: tsuki, on-yomi: gatsu/getsu

水 merkitys: vesi, kun-yomi: mizu, on-yomi: sui

Harjoitus 2:

金 merkitys: kulta, kun-yomi: kane, on-yomi: kin

火 Merkitys: tuli, kun-yomi: hi, on-yomi: ka

sama yhdistelmä tehtävissä, mutta merkit ovat eri tietenkin:

日本 merkitys: japani lukutapa: nihon

花火 merkitys: ilotulite lukutapa: hanabi


Näiden lisäksi sisäänkirjautunut käyttäjä voi kerrata merkkejä, joihin hän on vastannut oikein, satunnaisessa järjestyksessä.



## Sovelluksen tarkoitus

Sovelluksen tarkoitus on toimia työkaluna japanin kielen kanji-merkkien kertaukseen.

-Sovelluksessa käyttäjä voi luoda tunnuksen ja kirjautua sisään. 

-Käyttäjä voi kerrata kanji-merkkien tarkoitusta ja lukutapoja (joita ovat japanilainen ja kiinalainen lukutapa), tehtävässä jossa näytetään merkki, ja kenttiin kirjoitetaan sen merkitys ja lukutavat.

-Merkit olisi ryhmitelty eri tehtäviin joissa jokaisessa on noin ~10 merkkiä. 

-Käyttäjä voi myös kerrata merkkejä, jotka hän on käynyt läpi, satunnaisessa järjestyksessä. 

-Käyttäjä pystyy myös kertaamaan kanji-merkkien yhdistelmistä muodostuvia sanoja, jolloin tehtävässä kenttään kirjoitetaan sanan lukutapa ja sen tarkoitus. 

-Käyttäjä pystyy näkemään tilastoja oikeista ja vääristä vastauksista. 

-Jos käyttäjä on ylläpitäjä, hän voi lisätä ja poistaa merkkejä, ja niiden lukutapoja tai yhdistelmiä.
