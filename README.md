# Kanjiharjoittelusovellus

## Lopullinen sovellus
Sovellus on valmis. Kirjautumaton käyttäjä voi kerrata yksittäisiä Kanji-merkkejä, ja yhdistelmiä. Vastauksia ei tallenneta jos ei ole sisäänkirjautunut. Sisäänkirjautuneen käyttäjän vastaukset (oikein vai väärin) tallennetaan yksittäisiä merkkejä kerratessa, ja oikein vastattuja merkkejä voi kerrata satunnaisessa järjestyksessä (vain jos on vastannut oikein tarpeeksi moneen). Jos käyttäjä on ylläpitäjä, voi hän lisätä ryhmiä, merkkejä ja niiden lukutapoja ja myöskin yhdistelmiä. Hän voi myös poistaa yksittäisiä merkkejä, jolloin kaikki niiden lukutavat yms. poistetaan myös, ja yhdistelmiä.

## sovelluksen testaaminen Renderissä
https://kanjiharjoittelusovellus.onrender.com/

**HUOM**: Koska Renderin ilmainen postgres tietokanta on voimassa vain rajoitetun ajan, ellei sitä päivitetä, toimii tämä sovellus tällä hetkellä **2.11.2023** asti, mikäli en sitä muista ennen tuota päivämäärää päivittää.

Sovellusta pystyi ennen testaamaan herokussa, mutta heroku muuttui maksulliseksi, joten nyt on käytössä Render.

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


Näiden lisäksi sisäänkirjautunut käyttäjä voi kerrata merkkejä, joihin hän on vastannut oikein, satunnaisessa järjestyksessä (huom. vain yksittäisiä merkkejä).

Ylläpitäjän oikeuksia vaativia toimenpiteitä voi testata käyttäjällä "admin" (salasana "admin")


## Sovelluksen tarkoitus

Sovelluksen tarkoitus on toimia työkaluna japanin kielen kanji-merkkien kertaukseen.

-Sovelluksessa käyttäjä voi luoda tunnuksen ja kirjautua sisään. 

-Käyttäjä voi kerrata kanji-merkkien tarkoitusta ja lukutapoja (joita ovat japanilainen ja kiinalainen lukutapa), tehtävässä jossa näytetään merkki, ja kenttiin kirjoitetaan sen merkitys ja lukutavat.

-Merkit olisi ryhmitelty eri tehtäviin joissa jokaisessa on noin ~10 merkkiä. 

-Käyttäjä voi myös kerrata merkkejä, jotka hän on käynyt läpi, satunnaisessa järjestyksessä. 

-Käyttäjä pystyy myös kertaamaan kanji-merkkien yhdistelmistä muodostuvia sanoja, jolloin tehtävässä kenttään kirjoitetaan sanan lukutapa ja sen tarkoitus. 

-Käyttäjä pystyy näkemään tilastoja oikeista ja vääristä vastauksista. 

-Jos käyttäjä on ylläpitäjä, hän voi lisätä ja poistaa merkkejä, ja niiden lukutapoja tai yhdistelmiä.
