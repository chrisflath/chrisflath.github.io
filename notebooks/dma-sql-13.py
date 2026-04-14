# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "marimo",
#     "polars",
#     "duckdb",
#     "plotly",
# ]
# ///

import marimo

__generated_with = "0.13.0"
app = marimo.App(
    width="medium",
    app_title="DMA Session 13: Textanalyse",
)


@app.cell(hide_code=True)
def _():
    import marimo as mo
    return (mo,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        # Session 13: Textanalyse — Übungen

        Theorie und geführte Beispiele → **13-textanalyse-guide.py**

        **Aufgabentypen:**

        - 🟢 **Geführt**: Vollständige Lösung zum Nachvollziehen
        - 🟡 **Angepasst**: Teillösung zum Ergänzen (`???`)
        - 🔵 **Selbstständig**: Eigene Lösung schreiben
        - 🔴 **Debugging**: Fehler finden und beheben
        - ⭐ **Entdecken**: Offene Herausforderungen

        > **Hinweis:** 🟡-Aufgaben enthalten `???` als Platzhalter. Die Zelle zeigt einen SQL-Fehler, bis Sie die `???` durch die richtige Lösung ersetzen — das ist Absicht!

        **Drei Datensätze — steigende Komplexität:**

        | Datensatz | Sprache | Fokus |
        |-----------|---------|-------|
        | Produktbewertungen | Deutsch | String-Grundfunktionen, TRIM, REPLACE, LOWER |
        | McDonald's Reviews | Englisch | LIKE, Feature Engineering, Aspekt-Analyse |
        | UFO Sightings | Englisch | Regex, Tokenisierung, Text Mining |
        """
    )
    return


@app.cell
def _(mo):
    import polars as pl
    import plotly.express as px

    _warn = ""
    try:
        base = mo.notebook_location() / "public"
        produktbewertungen = pl.read_csv(str(base / "produktbewertungen.csv"))
        mcdonalds_reviews = pl.read_csv(str(base / "mcdonalds_reviews.csv"))
        ufo_sightings = pl.read_csv(str(base / "ufo_sightings.csv"))
    except Exception:
        produktbewertungen = pl.DataFrame({
            "id": list(range(1, 51)),
            "kategorie": [
                "Elektronik", "Elektronik", "Küche", "Sport", "Haushalt",
                "Garten", "Elektronik", "Küche", "Sport", "Haushalt",
                "Garten", "Elektronik", "Küche", "Sport", "Haushalt",
                "Garten", "Elektronik", "Küche", "Sport", "Haushalt",
                "Elektronik", "Küche", "Sport", "Garten", "Haushalt",
                "Elektronik", "Küche", "Sport", "Garten", "Haushalt",
                "Elektronik", "Küche", "Sport", "Garten", "Haushalt",
                "Elektronik", "Küche", "Sport", "Garten", "Haushalt",
                "Elektronik", "Küche", "Sport", "Garten", "Haushalt",
                "Elektronik", "Küche", "Sport", "Garten", "Haushalt",
            ],
            "sterne": [
                5, 2, 4, 1, 3, 5, 4, 1, 5, 2,
                3, 5, 2, 4, 1, 4, 3, 5, 2, 4,
                1, 5, 3, 4, 2, 5, 1, 4, 3, 2,
                4, 5, 1, 3, 5, 2, 4, 3, 1, 5,
                3, 2, 5, 4, 1, 4, 3, 2, 5, 1,
            ],
            "bewertung_text": [
                "Tolles Produkt, super Qualität!",
                "Leider  kaputt nach 2 Wochen.",
                " Sehr gutes Messer, hochwertig ",
                "Totaler Schrott!!",
                "Ganz okay für den Preis.",
                "Wunderbarer Rasenmäher, läuft leise und zuverlässig. Klare Kaufempfehlung!",
                "Gute Bildqualität, aber der Ton könnte besser sein.",
                "Die Pfanne klebt schon nach einer Woche!!  Sehr enttäuschend.",
                "SUPER Laufschuhe, perfekte Dämpfung und sehr bequem beim Joggen.",
                "Staubsauger hat wenig  Saugkraft, nicht empfehlenswert.",
                "Gartenschere liegt gut in der Hand. Schneidet sauber.",
                " Bluetooth-Kopfhörer mit erstklassigem Klang und langer Akkulaufzeit ",
                "Mixer funktioniert, aber ist extrem laut. Qualität mittelmäßig.",
                "Yogamatte rutscht nicht und ist angenehm dick. Sehr zufrieden!",
                "Bügeleisen tropft ständig. Schlechte Qualität für den Preis!!",
                "Hochbeet aus robustem Holz,  einfacher Aufbau. Empfehlenswert.",
                "Okay.",
                "Fantastisches Kochbuch mit vielen kreativen Rezepten. Toll für Anfänger und Fortgeschrittene!",
                "Tennisschläger ist viel zu schwer. Rückgabe!",
                "Guter Wäscheständer, stabil und platzsparend.",
                "Ladekabel  nach 3 Tagen defekt. Absoluter Schrott.",
                "Beste Salatschüssel die ich je hatte, perfekte Größe und schönes Design.",
                "Fußball hat gute Qualität, liegt gut in der Hand.",
                "Gießkanne ist praktisch, aber das Material wirkt billig.",
                "Mülleimer mit Sensor öffnet sich nicht immer zuverlässig. Na ja.",
                "Tolles Tablet, schnell und der Bildschirm ist gestochen scharf!",
                " Küchenmesser war stumpf bei Lieferung  ",
                "Fahrradhelm sitzt perfekt und sieht super aus. Top Qualität!",
                "Die Blumenerde ist hochwertig, Pflanzen wachsen prächtig.",
                "Handtücher fusseln stark nach dem Waschen. Enttäuschend.",
                "Webcam mit guter Auflösung, Mikrofon allerdings rauscht etwas.",
                "Toaster funktioniert einwandfrei, gleichmäßige Bräunung. Sehr empfehlenswert!",
                "Schlechtester Tischtennisschläger den ich je benutzt habe!!!",
                "Normales Vogelhäuschen, erfüllt seinen Zweck.",
                "Wunderbar weiche Bettwäsche, schläft sich herrlich. Premium Qualität!",
                "Maus  reagiert  manchmal  nicht. Sehr  ärgerlich.",
                "Kaffeemühle mahlt gleichmäßig und sieht schick aus. Gute Qualität.",
                "Wanderschuhe sind wasserdicht und bequem. Perfekt für lange Touren!",
                "Unkrautstecher ist nach einmaligem Gebrauch verbogen!",
                "Erstklassiger Ventilator, leise und kraftvoll. Besser als erwartet!",
                "Durchschnittliches Produkt, nicht schlecht aber auch nicht gut.",
                "Schneebesen verbiegt sich leicht. Qualität mangelhaft.",
                "Hervorragende Trinkflasche! Hält Getränke den ganzen Tag kalt. Super Qualität!!",
                "Gartenhandschuhe sind robust und angenehm zu tragen.",
                "Billig verarbeitet, Griff wackelt schon nach einer Woche.",
                "Die Powerbank lädt schnell und hat eine große Kapazität. Empfehlung!",
                "Nudelholz ist  zu  leicht, rollt nicht gleichmäßig.",
                "Schwimmbrille drückt am Nasensteg. Nicht komfortabel.",
                "Wunderschöner Blumentopf, tolle Farben und hochwertige Keramik!",
                "Absolut nutzlos! Funktioniert überhaupt nicht wie beschrieben!!",
            ],
        })
        mcdonalds_reviews = pl.DataFrame({
            "review_id": list(range(1, 51)),
            "rating": [
                1, 5, 2, 4, 3, 1, 5, 2, 4, 3,
                5, 1, 4, 2, 3, 5, 1, 4, 2, 3,
                4, 1, 5, 2, 3, 4, 1, 5, 2, 3,
                5, 1, 4, 2, 3, 5, 2, 4, 1, 3,
                4, 1, 5, 2, 3, 4, 2, 5, 1, 3,
            ],
            "store_name": [
                "Drive-Thru", "Airport", "City Center", "Mall", "Highway",
                "Drive-Thru", "City Center", "Airport", "Mall", "Highway",
                "Drive-Thru", "City Center", "Airport", "Mall", "Highway",
                "Mall", "Drive-Thru", "City Center", "Airport", "Highway",
                "Drive-Thru", "Airport", "Mall", "City Center", "Highway",
                "City Center", "Highway", "Drive-Thru", "Mall", "Airport",
                "Airport", "Drive-Thru", "City Center", "Highway", "Mall",
                "Mall", "City Center", "Drive-Thru", "Airport", "Highway",
                "Drive-Thru", "Mall", "Airport", "City Center", "Highway",
                "Airport", "Highway", "Mall", "Drive-Thru", "City Center",
            ],
            "review_text": [
                "Terrible food, cold fries and the burger was stale.",
                "Great burger and fresh fries, loved every bite!",
                "The food was bland and the nuggets were rubbery.",
                "Really enjoyed the Big Mac, food quality was above average.",
                "Average food, nothing special but edible.",
                "Got food poisoning from the chicken sandwich. Never again!",
                "Best fries I have ever had, crispy and perfectly salted.",
                "My burger was raw in the middle, absolutely disgusting food.",
                "The breakfast menu is fantastic, pancakes were fluffy and delicious.",
                "Coffee was lukewarm but the muffin was decent.",
                "Fresh salad with grilled chicken, surprisingly good for fast food!",
                "Found a hair in my burger. Completely unacceptable food quality.",
                "Kids loved the Happy Meal, good portions and tasty nuggets.",
                "Fries were soggy and cold, clearly been sitting there for hours.",
                "The food was okay, just your typical fast food experience.",
                "Excellent service, the staff was incredibly friendly and helpful!",
                "Worst service ever, the employee was rude and dismissive.",
                "Staff was friendly but a bit slow during the rush hour.",
                "The cashier got my order wrong twice. Terrible service.",
                "Service was fine, no complaints but nothing remarkable.",
                "Very quick service at the drive-thru, staff was polite.",
                "The staff ignored me for 10 minutes. Rude and unprofessional!",
                "Outstanding service, the manager came to check on us personally.",
                "Employee was helpful when I asked about allergens in the menu.",
                "Service took forever, had to wait 25 minutes for a simple order.",
                "Great value for the price, you get a lot of food for your money.",
                "Way too expensive for what you get. The prices keep going up!",
                "Good value meal deals, especially the combo offers.",
                "The price of a Big Mac is outrageous these days. Not cheap anymore.",
                "Reasonable prices for airport location, better value than expected.",
                "Happy hour deals are amazing, unbeatable value!",
                "Overpriced for such small portions. Not worth the money.",
                "The value menu is still affordable, good option on a budget.",
                "Prices have doubled but quality has dropped. Expensive for fast food!",
                "Decent price for a family meal, cheaper than cooking at home honestly.",
                "The restaurant was spotless, tables were clean and floors shiny.",
                "Disgusting! Dirty tables, filthy bathroom and trash everywhere.",
                "Very clean location, you can tell they take hygiene seriously.",
                "The dining area was dirty with sticky tables and old food on the floor.",
                "Clean kitchen visible from the counter, that is reassuring.",
                "Tables were clean but the bathroom needed serious attention.",
                "One of the cleanest fast food places I have been to, well maintained.",
                "Filthy restaurant, saw a cockroach near the drink station. Gross!",
                "Convenient location right off the highway, open late which is nice.",
                "Just a regular McDonald's, nothing great and nothing terrible.",
                "The new remodel looks modern, comfortable seating and good WiFi.",
                "Always reliable when traveling, you know exactly what you will get.",
                "Came here late at night, only option open. It was fine I suppose.",
            ],
        })
        ufo_sightings = pl.DataFrame({
            "datetime": [
                "2019-06-15", "2020-07-04", "2018-03-22", "2019-12-01", "2020-07-04",
                "2017-08-10", "2021-01-15", "2016-11-23", "2019-07-04", "2020-09-05",
                "2018-06-30", "2015-04-12", "2022-02-14", "2017-10-31", "2019-03-18",
                "2020-07-04", "2016-07-04", "2021-05-22", "2018-08-08", "2019-11-11",
                "2015-12-25", "2022-06-01", "2017-07-04", "2020-03-15", "2018-01-20",
                "2021-09-18", "2016-05-05", "2019-07-04", "2020-10-10", "2017-02-28",
                "2022-07-04", "2015-08-19", "2018-12-31", "2019-04-01", "2021-07-04",
                "2016-09-15", "2020-06-21", "2017-11-22", "2022-01-01", "2018-07-04",
                "2019-05-05", "2015-10-08", "2021-03-14", "2020-08-25", "2016-12-12",
                "2022-04-22", "2017-06-18", "2019-02-14", "2021-11-05", "2018-07-04",
            ],
            "state": [
                "CA", "TX", "NY", "FL", "AZ", "OH", "WA", "CA", "TX", "NY",
                "FL", "AZ", "OH", "WA", "CA", "TX", "NY", "FL", "OH", "AZ",
                "WA", "CA", "TX", "NY", "FL", "AZ", "OH", "CA", "WA", "TX",
                "NY", "FL", "CA", "AZ", "TX", "OH", "WA", "NY", "CA", "FL",
                "TX", "AZ", "OH", "WA", "CA", "NY", "FL", "TX", "AZ", "CA",
            ],
            "shape": [
                "light", "fireball", "triangle", "circle", "light",
                "disk", "sphere", "oval", "fireball", "changing",
                "triangle", "cigar", "light", "unknown", "circle",
                "fireball", "fireball", "sphere", "disk", "light",
                "triangle", "oval", "fireball", "changing", "cigar",
                "light", "circle", "fireball", "sphere", "unknown",
                "fireball", "disk", "light", "triangle", "fireball",
                "circle", "oval", "light", "sphere", "fireball",
                "changing", "disk", "triangle", "light", "cigar",
                "circle", "fireball", "sphere", "unknown", "fireball",
            ],
            "duration_text": [
                "5 minutes", "about 30 seconds", "2 hours", "~10 min", "3 minutes",
                "a few seconds", "15 minutes", "about 1 hour", "45 seconds", "~5 min",
                "10 minutes", "30 seconds", "about 20 minutes", "2-3 minutes", "1 hour",
                "~2 min", "several minutes", "about 15 seconds", "half an hour", "8 minutes",
                "a few minutes", "~45 seconds", "5-10 minutes", "about 3 minutes", "20 seconds",
                "1 minute", "roughly 10 min", "about 1 minute", "15 seconds", "~30 min",
                "3 minutes", "a few seconds", "several hours", "about 5 minutes", "2 minutes",
                "~20 seconds", "10-15 minutes", "about 2 hours", "45 seconds", "30 seconds",
                "7 minutes", "approximately 1 hour", "about 10 seconds", "~3 min", "25 minutes",
                "a couple minutes", "roughly 20 seconds", "about 5 min", "4 minutes", "~1 minute",
            ],
            "description": [
                "Bright white light hovering in the sky then disappeared south",
                "Orange fireball moving fast across the sky on July 4th heading east",
                "Large red triangle shaped object flying in zigzag pattern over the city",
                "Green circle stationary for 2 hours above the lake then vanished",
                "Two blue lights moving erratic changed direction suddenly toward north",
                "Silver disk hovering silently over the field then shot upward at incredible speed",
                "White sphere moving slowly from west to east across the night sky",
                "Oval shaped orange object stationary near the horizon for several minutes",
                "Bright orange fireball ascending fast on July 4th could have been fireworks",
                "Red and green changing lights hovering then moving north at high speed",
                "Three white triangle lights in formation flying south very slowly and silently",
                "Cigar shaped object with red lights on each end moving east steadily",
                "Single bright white light pulsing and hovering before disappearing instantly",
                "Unknown shape with orange glow seen moving erratic over the mountains at night",
                "Green circle with white halo hovering above the treeline then drifted west",
                "Multiple orange fireballs rising fast on July 4th near the fairgrounds",
                "Brilliant red fireball streaking across the sky on Independence Day heading north",
                "Blue and white sphere zigzag pattern across the sky then vanished behind clouds",
                "Metallic disk stationary above the highway reflecting sunlight for ten minutes",
                "Faint white light moving slowly east to west then abruptly stopped and disappeared",
                "Three red triangle lights hovering in formation before flying off to the south",
                "Large oval object with green and blue lights changing colors near the airport",
                "Orange fireball on July 4th moving west to east could be a flare or firework",
                "Bright white light changing shape and direction rapidly hovering then moving north",
                "Dark cigar shaped object with no lights moving silently south above the neighborhood",
                "Pulsing blue and white light hovering above the field for about one minute",
                "Small green circle moving fast from south to north then disappeared behind a hill",
                "Huge orange fireball on July 4th shooting straight up and then fading out",
                "White sphere hovering stationary then drifting slowly west over the mountains",
                "Strange shape with red and orange lights moving erratic over the plains at night",
                "Red and orange fireball on July 4th moving north very bright and silent",
                "Shiny silver disk seen hovering above the beach at sunset for several minutes",
                "Flickering white light moving in zigzag pattern disappeared heading south suddenly",
                "Red triangle with three lights at corners hovering above the parking lot silently",
                "Bright orange fireball on July 4th moving fast across sky before fading out east",
                "Green and white circle hovering low above the rooftops then accelerated north",
                "Oval object orange glow stationary above the lake changed color to red then vanished",
                "Single white light moving slowly east to west very high altitude no sound at all",
                "Glowing blue sphere appeared from nowhere hovering then shot off to the north instantly",
                "Orange fireball on July 4th moving south very slowly looked like a lantern or flare",
                "White and red changing lights moving erratic above the highway for seven minutes",
                "Small silver disk seen moving fast heading west no sound completely silent",
                "Three white lights triangle formation hovering then drifted slowly south over the city",
                "Bright green light pulsing and hovering above the forest then moved east quickly",
                "Long dark cigar shaped object with faint red lights moving north at high altitude",
                "Blue and green circle hovering stationary above the park then disappeared instantly",
                "Massive orange fireball seen on Fourth of July heading east over the stadium",
                "White sphere moving in zigzag pattern changed direction three times then vanished north",
                "Unknown object red and orange lights moving erratic above the desert at night",
                "Orange fireball on July 4th near the river very bright moving fast then faded out",
            ],
        })
        _warn = "warn"

    if _warn:
        mo.callout(mo.md("**Hinweis:** CSVs konnten nicht geladen werden. Es werden Beispieldaten verwendet."), kind="warn")

    mo.md(
        f"""
        **Geladen:** {len(produktbewertungen)} Produktbewertungen,
        {len(mcdonalds_reviews)} McDonald's Reviews,
        {len(ufo_sightings)} UFO Sightings
        """
    )
    return mcdonalds_reviews, mo, pl, produktbewertungen, px, ufo_sightings


# -----------------------------------------------------------------------
# Phase 1: Datenüberblick (Produktbewertungen)
# -----------------------------------------------------------------------


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ---

        ## Phase 1: Datenüberblick (Produktbewertungen)

        Wir starten mit einem kleinen, vertrauten Datensatz: 50 deutsche Produktbewertungen.
        Hier lernen wir die SQL-Werkzeuge kennen, bevor wir sie auf die großen Datensätze loslassen.
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ### 🟢 Aufgabe 13.1: Datenüberblick

        Wie viele Bewertungen gibt es pro Kategorie? Wie ist die durchschnittliche Sternebewertung?
        """
    )
    return


@app.cell
def _(mo, produktbewertungen):
    _df = mo.sql(
        f"""
        SELECT
            kategorie,
            COUNT(*) AS anzahl,
            ROUND(AVG(sterne), 2) AS avg_sterne,
            MIN(sterne) AS min_sterne,
            MAX(sterne) AS max_sterne
        FROM produktbewertungen
        GROUP BY kategorie
        ORDER BY avg_sterne DESC
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.accordion({"🔑 Musterlösung": mo.md("""
```sql
SELECT
    kategorie,
    COUNT(*) AS anzahl,
    ROUND(AVG(sterne), 2) AS avg_sterne,
    MIN(sterne) AS min_sterne,
    MAX(sterne) AS max_sterne
FROM produktbewertungen
GROUP BY kategorie
ORDER BY avg_sterne DESC
```
""")})
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ### 🟡 Aufgabe 13.2: LENGTH-Profiling

        Wie lang sind die Bewertungstexte? Gibt es Unterschiede nach Sternebewertung? Ergänzen Sie `???`:
        """
    )
    return


@app.cell
def _(mo, produktbewertungen):
    _df = mo.sql(
        f"""
        SELECT
            ??? AS sterne,
            ROUND(AVG(LENGTH(bewertung_text)), 0) AS avg_laenge,
            MIN(LENGTH(???)) AS min_laenge,
            MAX(LENGTH(???)) AS max_laenge,
            COUNT(*) AS anzahl
        FROM produktbewertungen
        GROUP BY ???
        ORDER BY ???
        -- Tipp: sterne, bewertung_text
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.accordion({"🔑 Musterlösung": mo.md("""
```sql
SELECT
    sterne,
    ROUND(AVG(LENGTH(bewertung_text)), 0) AS avg_laenge,
    MIN(LENGTH(bewertung_text)) AS min_laenge,
    MAX(LENGTH(bewertung_text)) AS max_laenge,
    COUNT(*) AS anzahl
FROM produktbewertungen
GROUP BY sterne
ORDER BY sterne
```
**Beobachtung:** Schreiben unzufriedene Kunden (1-2 Sterne) längere oder kürzere Texte als zufriedene?
""")})
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ### 🔵 Aufgabe 13.3: Lange Bewertungen finden

        Finden Sie alle Bewertungen mit mehr als 80 Zeichen. Zeigen Sie id, sterne, Textlänge und den Text.

        *Hinweis: `LENGTH(bewertung_text) > 80`*
        """
    )
    return


@app.cell
def _(mo, produktbewertungen):
    _df = mo.sql(
        f"""
        -- Ihre Lösung hier
        -- Erwartete Spalten: id, sterne, text_laenge, bewertung_text
        SELECT 'Schreiben Sie Ihre Abfrage hier' AS hinweis
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.accordion({"🔑 Musterlösung": mo.md("""
```sql
SELECT
    id,
    sterne,
    LENGTH(bewertung_text) AS text_laenge,
    bewertung_text
FROM produktbewertungen
WHERE LENGTH(bewertung_text) > 80
ORDER BY text_laenge DESC
```
""")})
    return


# -----------------------------------------------------------------------
# Phase 2: Textbereinigung (Produktbewertungen)
# -----------------------------------------------------------------------


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ---

        ## Phase 2: Textbereinigung (Produktbewertungen)

        Reale Textdaten sind selten sauber: führende Leerzeichen, doppelte Leerzeichen,
        inkonsistente Schreibweisen. SQL bietet `TRIM`, `REPLACE` und `LOWER` zur Bereinigung.
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ### 🟢 Aufgabe 13.4: TRIM — Unsichtbare Leerzeichen finden

        Finden Sie Bewertungen, bei denen der Text führende oder nachfolgende Leerzeichen hat.
        """
    )
    return


@app.cell
def _(mo, produktbewertungen):
    _df = mo.sql(
        f"""
        SELECT
            id,
            bewertung_text,
            TRIM(bewertung_text) AS getrimmt,
            LENGTH(bewertung_text) AS original_laenge,
            LENGTH(TRIM(bewertung_text)) AS trimmed_laenge,
            LENGTH(bewertung_text) - LENGTH(TRIM(bewertung_text)) AS entfernt
        FROM produktbewertungen
        WHERE bewertung_text != TRIM(bewertung_text)
        ORDER BY entfernt DESC
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.accordion({"🔑 Musterlösung": mo.md("""
```sql
SELECT
    id,
    bewertung_text,
    TRIM(bewertung_text) AS getrimmt,
    LENGTH(bewertung_text) AS original_laenge,
    LENGTH(TRIM(bewertung_text)) AS trimmed_laenge,
    LENGTH(bewertung_text) - LENGTH(TRIM(bewertung_text)) AS entfernt
FROM produktbewertungen
WHERE bewertung_text != TRIM(bewertung_text)
ORDER BY entfernt DESC
```
**Erklärung:** `TRIM()` entfernt Leerzeichen am Anfang und Ende. Die Differenz zeigt, wie viele Zeichen entfernt werden.
""")})
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ### 🟡 Aufgabe 13.5: REPLACE — Doppelte Leerzeichen entfernen

        Finden Sie Bewertungen mit doppelten Leerzeichen und ersetzen Sie diese. Ergänzen Sie `???`:
        """
    )
    return


@app.cell
def _(mo, produktbewertungen):
    _df = mo.sql(
        f"""
        SELECT
            id,
            bewertung_text,
            REPLACE(bewertung_text, ???, ???) AS bereinigt
        FROM produktbewertungen
        WHERE bewertung_text LIKE ???
        -- Tipp: REPLACE(text, '  ', ' '), LIKE '%  %'
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.accordion({"🔑 Musterlösung": mo.md("""
```sql
SELECT
    id,
    bewertung_text,
    REPLACE(bewertung_text, '  ', ' ') AS bereinigt
FROM produktbewertungen
WHERE bewertung_text LIKE '%  %'
```
**Erklärung:** `REPLACE(text, alt, neu)` braucht immer 3 Argumente: den Text, was ersetzt werden soll, und den Ersatz.
""")})
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ### 🔵 Aufgabe 13.6: LENGTH-REPLACE Trick — Ausrufezeichen zählen

        **Klausur-Pattern:** `LENGTH(text) - LENGTH(REPLACE(text, 'x', ''))` = Anzahl von 'x'

        Zählen Sie die Ausrufezeichen pro Bewertung und zeigen Sie die Top 10 emotionalsten Bewertungen.
        Berechnen Sie auch den Durchschnitt pro Sternebewertung.

        *Hinweis: `LENGTH(bewertung_text) - LENGTH(REPLACE(bewertung_text, '!', ''))` als `anzahl_ausrufezeichen`*
        """
    )
    return


@app.cell
def _(mo, produktbewertungen):
    _df = mo.sql(
        f"""
        -- Ihre Lösung hier
        -- Erwartete Spalten: id, sterne, bewertung_text, anzahl_ausrufezeichen
        -- Top 10 nach anzahl_ausrufezeichen DESC
        SELECT 'Schreiben Sie Ihre Abfrage hier' AS hinweis
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.accordion({"🔑 Musterlösung": mo.md("""
```sql
SELECT
    id, sterne, bewertung_text,
    LENGTH(bewertung_text) - LENGTH(REPLACE(bewertung_text, '!', ''))
        AS anzahl_ausrufezeichen
FROM produktbewertungen
WHERE LENGTH(bewertung_text) - LENGTH(REPLACE(bewertung_text, '!', '')) > 0
ORDER BY anzahl_ausrufezeichen DESC
LIMIT 10
```

**Bonus — Durchschnitt pro Sternebewertung:**
```sql
SELECT
    sterne,
    ROUND(AVG(
        LENGTH(bewertung_text) - LENGTH(REPLACE(bewertung_text, '!', ''))
    ), 2) AS avg_ausrufezeichen
FROM produktbewertungen
GROUP BY sterne
ORDER BY sterne
```
""")})
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ### 🔴 Aufgabe 13.7: Debugging — REPLACE mit falscher Argumentzahl

        Die folgende Abfrage soll doppelte Leerzeichen ersetzen. Sie hat einen Fehler!
        """
    )
    return


@app.cell
def _(mo, produktbewertungen):
    _df = mo.sql(
        f"""
        -- 🔴 Diese Abfrage hat einen Fehler — finden und beheben Sie ihn!
        SELECT
            id,
            REPLACE(bewertung_text, '  ') AS bereinigt
        FROM produktbewertungen
        WHERE bewertung_text LIKE '%  %'
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.accordion({"🔑 Lösung": mo.md("""
**Problem:** `REPLACE` braucht **3 Argumente**: text, alt, neu! Hier fehlt das 3. Argument (der Ersatzstring).

**Lösung:**
```sql
SELECT
    id,
    REPLACE(bewertung_text, '  ', ' ') AS bereinigt
FROM produktbewertungen
WHERE bewertung_text LIKE '%  %'
```
""")})
    return


# -----------------------------------------------------------------------
# Phase 3: LOWER & Pattern Matching (Produktbewertungen)
# -----------------------------------------------------------------------


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ---

        ## Phase 3: LOWER & Pattern Matching (Produktbewertungen)

        `LOWER()` normalisiert die Groß-/Kleinschreibung — unverzichtbar für Textsuche.
        Kombiniert mit `LIKE` können wir Muster in Freitext finden.
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ### 🟢 Aufgabe 13.8: LOWER-Normalisierung

        Finden Sie alle Bewertungen, die das Wort "qualität" enthalten (unabhängig von Groß-/Kleinschreibung).
        """
    )
    return


@app.cell
def _(mo, produktbewertungen):
    _df = mo.sql(
        f"""
        SELECT
            id, sterne, bewertung_text
        FROM produktbewertungen
        WHERE LOWER(bewertung_text) LIKE '%qualität%'
           OR LOWER(bewertung_text) LIKE '%hochwertig%'
        ORDER BY sterne DESC
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.accordion({"🔑 Musterlösung": mo.md("""
```sql
SELECT
    id, sterne, bewertung_text
FROM produktbewertungen
WHERE LOWER(bewertung_text) LIKE '%qualität%'
   OR LOWER(bewertung_text) LIKE '%hochwertig%'
ORDER BY sterne DESC
```
**Beobachtung:** "Qualität" wird sowohl positiv ("super Qualität") als auch negativ ("schlechte Qualität") verwendet!
""")})
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ### 🟡 Aufgabe 13.9: Positive vs. negative Wörter — CASE WHEN + LOWER + LIKE

        Klassifizieren Sie jede Bewertung als positiv, negativ oder neutral anhand von Schlüsselwörtern. Ergänzen Sie `???`:
        """
    )
    return


@app.cell
def _(mo, produktbewertungen):
    _df = mo.sql(
        f"""
        SELECT
            id, sterne, bewertung_text,
            CASE
                WHEN LOWER(bewertung_text) LIKE '%toll%'
                  OR LOWER(bewertung_text) LIKE '%super%'
                  OR LOWER(bewertung_text) LIKE '%perfekt%'
                  OR LOWER(bewertung_text) LIKE '%empfehl%'
                  THEN 'positiv'
                WHEN LOWER(bewertung_text) LIKE ???
                  OR LOWER(bewertung_text) LIKE ???
                  OR LOWER(bewertung_text) LIKE ???
                  THEN 'negativ'
                ELSE 'neutral'
            END AS sentiment
        FROM produktbewertungen
        ORDER BY sterne
        -- Tipp: '%schrott%', '%schlecht%', '%enttäusch%'
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.accordion({"🔑 Musterlösung": mo.md("""
```sql
SELECT
    id, sterne, bewertung_text,
    CASE
        WHEN LOWER(bewertung_text) LIKE '%toll%'
          OR LOWER(bewertung_text) LIKE '%super%'
          OR LOWER(bewertung_text) LIKE '%perfekt%'
          OR LOWER(bewertung_text) LIKE '%empfehl%'
          THEN 'positiv'
        WHEN LOWER(bewertung_text) LIKE '%schrott%'
          OR LOWER(bewertung_text) LIKE '%schlecht%'
          OR LOWER(bewertung_text) LIKE '%enttäusch%'
          THEN 'negativ'
        ELSE 'neutral'
    END AS sentiment
FROM produktbewertungen
ORDER BY sterne
```
""")})
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ### 🔵 Aufgabe 13.10: Eigene Wortliste — Sentiment pro Kategorie

        Erweitern Sie die Sentiment-Analyse: Zählen Sie positive und negative Bewertungen pro Kategorie.
        Definieren Sie eigene Wortlisten für positiv/negativ.

        *Hinweis: `CASE WHEN ... THEN 'positiv' ...`, dann `COUNT(*) FILTER (WHERE sentiment = 'positiv')` pro Kategorie*
        """
    )
    return


@app.cell
def _(mo, produktbewertungen):
    _df = mo.sql(
        f"""
        -- Ihre Lösung hier
        -- Erwartete Spalten: kategorie, anzahl_positiv, anzahl_negativ, anzahl_neutral
        SELECT 'Schreiben Sie Ihre Abfrage hier' AS hinweis
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.accordion({"🔑 Musterlösung": mo.md("""
```sql
WITH mit_sentiment AS (
    SELECT
        kategorie,
        CASE
            WHEN LOWER(bewertung_text) LIKE '%toll%'
              OR LOWER(bewertung_text) LIKE '%super%'
              OR LOWER(bewertung_text) LIKE '%perfekt%'
              OR LOWER(bewertung_text) LIKE '%empfehl%'
              OR LOWER(bewertung_text) LIKE '%wunderbar%'
              OR LOWER(bewertung_text) LIKE '%erstklassig%'
              OR LOWER(bewertung_text) LIKE '%hervorragend%'
              THEN 'positiv'
            WHEN LOWER(bewertung_text) LIKE '%schrott%'
              OR LOWER(bewertung_text) LIKE '%schlecht%'
              OR LOWER(bewertung_text) LIKE '%enttäusch%'
              OR LOWER(bewertung_text) LIKE '%kaputt%'
              OR LOWER(bewertung_text) LIKE '%defekt%'
              OR LOWER(bewertung_text) LIKE '%nutzlos%'
              THEN 'negativ'
            ELSE 'neutral'
        END AS sentiment
    FROM produktbewertungen
)
SELECT
    kategorie,
    COUNT(*) FILTER (WHERE sentiment = 'positiv') AS anzahl_positiv,
    COUNT(*) FILTER (WHERE sentiment = 'negativ') AS anzahl_negativ,
    COUNT(*) FILTER (WHERE sentiment = 'neutral') AS anzahl_neutral
FROM mit_sentiment
GROUP BY kategorie
ORDER BY anzahl_positiv DESC
```
""")})
    return


# -----------------------------------------------------------------------
# Phase 4: LIKE & Feature Engineering (McDonald's)
# -----------------------------------------------------------------------


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ---

        ## Phase 4: LIKE & Feature Engineering (McDonald's Reviews)

        Jetzt wechseln wir zu englischen McDonald's-Bewertungen.
        Mit `LIKE` und `CASE WHEN` extrahieren wir Aspekte und korrelieren sie mit Ratings.
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ### 🟢 Aufgabe 13.11: LIKE-Filterung — Food Reviews finden

        Finden Sie alle Reviews, die über das Essen sprechen.
        """
    )
    return


@app.cell
def _(mcdonalds_reviews, mo):
    _df = mo.sql(
        f"""
        SELECT review_id, rating, review_text
        FROM mcdonalds_reviews
        WHERE LOWER(review_text) LIKE '%food%'
           OR LOWER(review_text) LIKE '%burger%'
           OR LOWER(review_text) LIKE '%fries%'
        ORDER BY rating
        LIMIT 15
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.accordion({"🔑 Musterlösung": mo.md("""
```sql
SELECT review_id, rating, review_text
FROM mcdonalds_reviews
WHERE LOWER(review_text) LIKE '%food%'
   OR LOWER(review_text) LIKE '%burger%'
   OR LOWER(review_text) LIKE '%fries%'
ORDER BY rating
LIMIT 15
```
""")})
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ### 🟡 Aufgabe 13.12: CASE WHEN + LIKE — Feature Engineering

        Erzeugen Sie boolesche Feature-Spalten für: Food, Service, Speed, Cleanliness, Price.
        Ergänzen Sie die fehlenden `???` LIKE-Patterns:
        """
    )
    return


@app.cell
def _(mcdonalds_reviews, mo):
    _df = mo.sql(
        f"""
        SELECT
            review_id, rating,
            CASE WHEN LOWER(review_text) LIKE '%food%'
                      OR LOWER(review_text) LIKE '%burger%'
                      OR LOWER(review_text) LIKE '%fries%'
                      OR LOWER(review_text) LIKE '%nuggets%'
                 THEN 1 ELSE 0 END AS food,
            CASE WHEN LOWER(review_text) LIKE '%service%'
                      OR LOWER(review_text) LIKE '%staff%'
                      OR LOWER(review_text) LIKE '%rude%'
                      OR LOWER(review_text) LIKE '%friendly%'
                 THEN 1 ELSE 0 END AS service,
            CASE WHEN LOWER(review_text) LIKE ???
                      OR LOWER(review_text) LIKE ???
                      OR LOWER(review_text) LIKE ???
                 THEN 1 ELSE 0 END AS speed,
            CASE WHEN LOWER(review_text) LIKE ???
                      OR LOWER(review_text) LIKE ???
                 THEN 1 ELSE 0 END AS cleanliness,
            CASE WHEN LOWER(review_text) LIKE '%price%'
                      OR LOWER(review_text) LIKE '%expensive%'
                      OR LOWER(review_text) LIKE '%value%'
                 THEN 1 ELSE 0 END AS price
        FROM mcdonalds_reviews
        LIMIT 20
        -- Tipp speed: '%wait%', '%slow%', '%quick%'
        -- Tipp cleanliness: '%clean%', '%dirty%'
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.accordion({"🔑 Musterlösung": mo.md("""
```sql
SELECT
    review_id, rating,
    CASE WHEN LOWER(review_text) LIKE '%food%'
              OR LOWER(review_text) LIKE '%burger%'
              OR LOWER(review_text) LIKE '%fries%'
              OR LOWER(review_text) LIKE '%nuggets%'
         THEN 1 ELSE 0 END AS food,
    CASE WHEN LOWER(review_text) LIKE '%service%'
              OR LOWER(review_text) LIKE '%staff%'
              OR LOWER(review_text) LIKE '%rude%'
              OR LOWER(review_text) LIKE '%friendly%'
         THEN 1 ELSE 0 END AS service,
    CASE WHEN LOWER(review_text) LIKE '%wait%'
              OR LOWER(review_text) LIKE '%slow%'
              OR LOWER(review_text) LIKE '%quick%'
         THEN 1 ELSE 0 END AS speed,
    CASE WHEN LOWER(review_text) LIKE '%clean%'
              OR LOWER(review_text) LIKE '%dirty%'
         THEN 1 ELSE 0 END AS cleanliness,
    CASE WHEN LOWER(review_text) LIKE '%price%'
              OR LOWER(review_text) LIKE '%expensive%'
              OR LOWER(review_text) LIKE '%value%'
         THEN 1 ELSE 0 END AS price
FROM mcdonalds_reviews
LIMIT 20
```
""")})
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ### 🔵 Aufgabe 13.13: Aspekt-Rating Korrelation mit UNION ALL

        Welche Aspekte haben die höchsten / niedrigsten Durchschnittsbewertungen?
        Nutzen Sie `UNION ALL` um jeden Aspekt separat auszuwerten.

        *Hinweis: Für jeden Aspekt: `SELECT 'Aspekt' AS aspect, COUNT(*), ROUND(AVG(rating), 2) FROM ... WHERE ...`*
        """
    )
    return


@app.cell
def _(mcdonalds_reviews, mo):
    _df = mo.sql(
        f"""
        -- Ihre Lösung hier
        -- Erwartete Spalten: aspect, n, avg_rating
        -- 5 Zeilen (Food, Service, Speed, Cleanliness, Price)
        SELECT 'Schreiben Sie Ihre Abfrage hier' AS hinweis
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.accordion({"🔑 Musterlösung": mo.md("""
```sql
SELECT 'Food' AS aspect,
       COUNT(*) AS n,
       ROUND(AVG(rating), 2) AS avg_rating
FROM mcdonalds_reviews
WHERE LOWER(review_text) LIKE '%food%'
   OR LOWER(review_text) LIKE '%burger%'
   OR LOWER(review_text) LIKE '%fries%'
UNION ALL
SELECT 'Service', COUNT(*), ROUND(AVG(rating), 2)
FROM mcdonalds_reviews
WHERE LOWER(review_text) LIKE '%service%'
   OR LOWER(review_text) LIKE '%staff%'
   OR LOWER(review_text) LIKE '%rude%'
   OR LOWER(review_text) LIKE '%friendly%'
UNION ALL
SELECT 'Speed', COUNT(*), ROUND(AVG(rating), 2)
FROM mcdonalds_reviews
WHERE LOWER(review_text) LIKE '%wait%'
   OR LOWER(review_text) LIKE '%slow%'
   OR LOWER(review_text) LIKE '%quick%'
UNION ALL
SELECT 'Cleanliness', COUNT(*), ROUND(AVG(rating), 2)
FROM mcdonalds_reviews
WHERE LOWER(review_text) LIKE '%clean%'
   OR LOWER(review_text) LIKE '%dirty%'
   OR LOWER(review_text) LIKE '%filthy%'
UNION ALL
SELECT 'Price', COUNT(*), ROUND(AVG(rating), 2)
FROM mcdonalds_reviews
WHERE LOWER(review_text) LIKE '%price%'
   OR LOWER(review_text) LIKE '%expensive%'
   OR LOWER(review_text) LIKE '%value%'
ORDER BY avg_rating DESC
```
""")})
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ### 🔴 Aufgabe 13.14: Debugging — UNION ALL mit unterschiedlicher Spaltenanzahl

        Die folgende Abfrage soll Food- und Service-Aspekte vergleichen. Sie hat einen Fehler!
        """
    )
    return


@app.cell
def _(mcdonalds_reviews, mo):
    _df = mo.sql(
        f"""
        -- 🔴 Diese Abfrage hat einen Fehler — finden und beheben Sie ihn!
        SELECT 'Food' AS aspect,
               COUNT(*) AS n,
               ROUND(AVG(rating), 2) AS avg_rating
        FROM mcdonalds_reviews
        WHERE LOWER(review_text) LIKE '%food%'
        UNION ALL
        SELECT 'Service', COUNT(*)
        FROM mcdonalds_reviews
        WHERE LOWER(review_text) LIKE '%service%'
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.accordion({"🔑 Lösung": mo.md("""
**Problem:** Die beiden SELECT-Teile haben **unterschiedliche Spaltenanzahl**: der erste hat 3 Spalten (aspect, n, avg_rating), der zweite nur 2 (aspect, n). UNION ALL erfordert gleiche Spaltenanzahl!

**Lösung:**
```sql
SELECT 'Food' AS aspect,
       COUNT(*) AS n,
       ROUND(AVG(rating), 2) AS avg_rating
FROM mcdonalds_reviews
WHERE LOWER(review_text) LIKE '%food%'
UNION ALL
SELECT 'Service', COUNT(*), ROUND(AVG(rating), 2)
FROM mcdonalds_reviews
WHERE LOWER(review_text) LIKE '%service%'
```
""")})
    return


# -----------------------------------------------------------------------
# Phase 5: Aspekt-Analyse (McDonald's)
# -----------------------------------------------------------------------


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ---

        ## Phase 5: Aspekt-Analyse (McDonald's Reviews)

        Jetzt kombinieren wir Feature Engineering mit Aggregation und Visualisierung.
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ### 🟢 Aufgabe 13.15: Aspekte nach Rating-Tier mit FILTER

        Vergleichen Sie die Häufigkeit der Aspekte in positiven (4-5 Sterne) vs. negativen (1-2 Sterne) Reviews.
        """
    )
    return


@app.cell
def _(mcdonalds_reviews, mo):
    aspekt_analyse = mo.sql(
        f"""
        WITH features AS (
            SELECT
                review_id, rating,
                CASE WHEN LOWER(review_text) LIKE '%food%'
                          OR LOWER(review_text) LIKE '%burger%'
                          OR LOWER(review_text) LIKE '%fries%'
                          OR LOWER(review_text) LIKE '%nuggets%'
                     THEN 1 ELSE 0 END AS food,
                CASE WHEN LOWER(review_text) LIKE '%service%'
                          OR LOWER(review_text) LIKE '%staff%'
                          OR LOWER(review_text) LIKE '%rude%'
                          OR LOWER(review_text) LIKE '%friendly%'
                     THEN 1 ELSE 0 END AS service,
                CASE WHEN LOWER(review_text) LIKE '%clean%'
                          OR LOWER(review_text) LIKE '%dirty%'
                          OR LOWER(review_text) LIKE '%filthy%'
                     THEN 1 ELSE 0 END AS cleanliness,
                CASE WHEN LOWER(review_text) LIKE '%price%'
                          OR LOWER(review_text) LIKE '%expensive%'
                          OR LOWER(review_text) LIKE '%value%'
                     THEN 1 ELSE 0 END AS price
            FROM mcdonalds_reviews
        )
        SELECT
            'Food' AS aspect,
            SUM(food) FILTER (WHERE rating >= 4) AS positiv,
            SUM(food) FILTER (WHERE rating <= 2) AS negativ,
            SUM(food) AS gesamt
        FROM features
        UNION ALL
        SELECT 'Service',
            SUM(service) FILTER (WHERE rating >= 4),
            SUM(service) FILTER (WHERE rating <= 2),
            SUM(service)
        FROM features
        UNION ALL
        SELECT 'Cleanliness',
            SUM(cleanliness) FILTER (WHERE rating >= 4),
            SUM(cleanliness) FILTER (WHERE rating <= 2),
            SUM(cleanliness)
        FROM features
        UNION ALL
        SELECT 'Price',
            SUM(price) FILTER (WHERE rating >= 4),
            SUM(price) FILTER (WHERE rating <= 2),
            SUM(price)
        FROM features
        ORDER BY gesamt DESC
        """
    )
    return (aspekt_analyse,)


@app.cell
def _(aspekt_analyse, mcdonalds_reviews, px):
    fig_aspekt = px.bar(
        aspekt_analyse,
        x="aspect",
        y=["positiv", "negativ"],
        barmode="group",
        title=f"Aspekte: Positiv (4-5 Sterne) vs. Negativ (1-2 Sterne) (n={len(mcdonalds_reviews)})",
        labels={"aspect": "Aspekt", "value": "Anzahl", "variable": "Tier"},
        color_discrete_map={"positiv": "#2ecc71", "negativ": "#e74c3c"},
    )
    fig_aspekt.update_layout(height=400)
    fig_aspekt


@app.cell(hide_code=True)
def _(mo):
    mo.accordion({"🔑 Musterlösung": mo.md("""
```sql
WITH features AS (
    SELECT review_id, rating,
        CASE WHEN LOWER(review_text) LIKE '%food%' OR ... THEN 1 ELSE 0 END AS food,
        CASE WHEN LOWER(review_text) LIKE '%service%' OR ... THEN 1 ELSE 0 END AS service,
        ...
    FROM mcdonalds_reviews
)
SELECT 'Food' AS aspect,
    SUM(food) FILTER (WHERE rating >= 4) AS positiv,
    SUM(food) FILTER (WHERE rating <= 2) AS negativ,
    SUM(food) AS gesamt
FROM features
UNION ALL ...
```
**Pattern:** CTE mit Feature-Spalten, dann `SUM(...) FILTER (WHERE ...)` für bedingte Aggregation.
""")})
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ### 🟡 Aufgabe 13.16: Wörter nach Rating — Tokenisierung + FILTER

        Welche Wörter kommen häufiger in positiven vs. negativen Reviews vor? Ergänzen Sie `???`:
        """
    )
    return


@app.cell
def _(mcdonalds_reviews, mo):
    _df = mo.sql(
        f"""
        WITH stoppwoerter AS (
            SELECT UNNEST(['the','a','an','and','or','to','in','of','it','is',
                           'was','for','on','that','with','as','at','by','from',
                           'this','i','we','no','me','so','very','about','had',
                           'were','but','not','then','be']) AS wort
        ),
        woerter AS (
            SELECT
                rating,
                UNNEST(regexp_split_to_array(
                    LOWER(TRIM(review_text)), '[^a-z]+')) AS word
            FROM mcdonalds_reviews
        )
        SELECT
            word,
            COUNT(*) FILTER (WHERE rating >= ???) AS count_positiv,
            COUNT(*) FILTER (WHERE rating <= ???) AS count_negativ
        FROM woerter
        WHERE LENGTH(word) > 1
          AND word NOT IN (SELECT wort FROM stoppwoerter)
        GROUP BY word
        HAVING COUNT(*) >= 2
        ORDER BY ??? DESC
        LIMIT 20
        -- Tipp: rating >= 4, rating <= 2, count_positiv
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.accordion({"🔑 Musterlösung": mo.md("""
```sql
WITH stoppwoerter AS (
    SELECT UNNEST(['the','a','an','and','or','to','in','of','it','is',
                   'was','for','on','that','with','as','at','by','from',
                   'this','i','we','no','me','so','very','about','had',
                   'were','but','not','then','be']) AS wort
),
woerter AS (
    SELECT
        rating,
        UNNEST(regexp_split_to_array(
            LOWER(TRIM(review_text)), '[^a-z]+')) AS word
    FROM mcdonalds_reviews
)
SELECT
    word,
    COUNT(*) FILTER (WHERE rating >= 4) AS count_positiv,
    COUNT(*) FILTER (WHERE rating <= 2) AS count_negativ
FROM woerter
WHERE LENGTH(word) > 1
  AND word NOT IN (SELECT wort FROM stoppwoerter)
GROUP BY word
HAVING COUNT(*) >= 2
ORDER BY count_positiv DESC
LIMIT 20
```
""")})
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ### 🔵 Aufgabe 13.17: Sentiment-Score — positive minus negative Wörter

        Bauen Sie einen einfachen Sentiment-Score pro Rating-Stufe:
        Zählen Sie positive Wörter (great, fresh, delicious, friendly, clean, excellent, best, love)
        minus negative (terrible, cold, rude, slow, dirty, worst, wrong, disgusting).

        Korreliert der Score mit dem tatsächlichen Rating?

        *Hinweis: `CASE WHEN LOWER(review_text) LIKE '%great%' THEN 1 ELSE 0 END` für jedes Wort, dann summieren und von negativen subtrahieren.*
        """
    )
    return


@app.cell
def _(mcdonalds_reviews, mo):
    _df = mo.sql(
        f"""
        -- Ihre Lösung hier
        -- Erwartete Spalten: rating, avg_sentiment_score, anzahl
        -- Sortiert nach rating
        SELECT 'Schreiben Sie Ihre Abfrage hier' AS hinweis
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.accordion({"🔑 Musterlösung": mo.md("""
```sql
SELECT
    rating,
    ROUND(AVG(
        (CASE WHEN LOWER(review_text) LIKE '%great%' THEN 1 ELSE 0 END)
      + (CASE WHEN LOWER(review_text) LIKE '%fresh%' THEN 1 ELSE 0 END)
      + (CASE WHEN LOWER(review_text) LIKE '%delicious%' THEN 1 ELSE 0 END)
      + (CASE WHEN LOWER(review_text) LIKE '%friendly%' THEN 1 ELSE 0 END)
      + (CASE WHEN LOWER(review_text) LIKE '%clean%' THEN 1 ELSE 0 END)
      + (CASE WHEN LOWER(review_text) LIKE '%excellent%' THEN 1 ELSE 0 END)
      + (CASE WHEN LOWER(review_text) LIKE '%best%' THEN 1 ELSE 0 END)
      + (CASE WHEN LOWER(review_text) LIKE '%love%' THEN 1 ELSE 0 END)
      - (CASE WHEN LOWER(review_text) LIKE '%terrible%' THEN 1 ELSE 0 END)
      - (CASE WHEN LOWER(review_text) LIKE '%cold%' THEN 1 ELSE 0 END)
      - (CASE WHEN LOWER(review_text) LIKE '%rude%' THEN 1 ELSE 0 END)
      - (CASE WHEN LOWER(review_text) LIKE '%slow%' THEN 1 ELSE 0 END)
      - (CASE WHEN LOWER(review_text) LIKE '%dirty%' THEN 1 ELSE 0 END)
      - (CASE WHEN LOWER(review_text) LIKE '%worst%' THEN 1 ELSE 0 END)
      - (CASE WHEN LOWER(review_text) LIKE '%wrong%' THEN 1 ELSE 0 END)
      - (CASE WHEN LOWER(review_text) LIKE '%disgusting%' THEN 1 ELSE 0 END)
    ), 2) AS avg_sentiment_score,
    COUNT(*) AS anzahl
FROM mcdonalds_reviews
GROUP BY rating
ORDER BY rating
```
**Beobachtung:** Der Sentiment-Score sollte mit dem Rating steigen — je höher das Rating, desto mehr positive Wörter!
""")})
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ### 🔴 Aufgabe 13.18: Debugging — WHERE auf falscher CTE-Ebene

        Die folgende Abfrage soll nur Food-Reviews zeigen, aber der Filter greift nicht korrekt.
        """
    )
    return


@app.cell
def _(mcdonalds_reviews, mo):
    _df = mo.sql(
        f"""
        -- 🔴 Diese Abfrage hat einen Fehler — finden und beheben Sie ihn!
        WITH food_reviews AS (
            SELECT review_id, rating, review_text
            FROM mcdonalds_reviews
        )
        SELECT
            rating,
            COUNT(*) AS anzahl,
            ROUND(AVG(LENGTH(review_text)), 0) AS avg_laenge
        FROM food_reviews
        WHERE LOWER(review_text) LIKE '%food%'
           OR LOWER(review_text) LIKE '%burger%'
        GROUP BY rating
        HAVING anzahl > 0
        ORDER BY rating
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.accordion({"🔑 Lösung": mo.md("""
**Problem:** Die CTE `food_reviews` holt **alle** Reviews ohne Filter. Der Filter kommt erst in der äußeren Query. Das funktioniert zwar syntaktisch, aber der CTE-Name ist irreführend und das `HAVING anzahl > 0` ist überflüssig (COUNT ist immer > 0 wegen WHERE).

**Bessere Lösung — Filter in die CTE verschieben:**
```sql
WITH food_reviews AS (
    SELECT review_id, rating, review_text
    FROM mcdonalds_reviews
    WHERE LOWER(review_text) LIKE '%food%'
       OR LOWER(review_text) LIKE '%burger%'
)
SELECT
    rating,
    COUNT(*) AS anzahl,
    ROUND(AVG(LENGTH(review_text)), 0) AS avg_laenge
FROM food_reviews
GROUP BY rating
ORDER BY rating
```
**Merke:** Filter sollten so früh wie möglich angewendet werden (in der CTE, nicht erst in der äußeren Query). Das ist effizienter und lesbarer.
""")})
    return


# -----------------------------------------------------------------------
# Phase 6: Regex & Capture Groups (UFO)
# -----------------------------------------------------------------------


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ---

        ## Phase 6: Reguläre Ausdrücke & Capture Groups (UFO Sightings)

        Jetzt wird es wild: UFO-Augenzeugenberichte mit chaotischen Freitextfeldern.
        DuckDB bietet mächtige Regex-Funktionen: `regexp_extract`, `regexp_extract_all`, `regexp_matches`.
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ### 🟢 Aufgabe 13.19: regexp_extract — Dauer parsen mit Capture Groups

        Das `duration_text`-Feld ist chaotisch: "5 minutes", "about 30 seconds", "~10 min"...

        DuckDB kann mit **Capture Groups** Zahl UND Einheit extrahieren:
        `regexp_extract(text, '(\d+)\s*(minutes?|seconds?|hours?)', gruppe)`
        """
    )
    return


@app.cell
def _(mo, ufo_sightings):
    _df = mo.sql(
        f"""
        SELECT
            duration_text,
            regexp_extract(duration_text,
                '(\d+)\s*(seconds?|minutes?|mins?|hours?|hrs?)', 1)
                AS zahl,
            regexp_extract(duration_text,
                '(\d+)\s*(seconds?|minutes?|mins?|hours?|hrs?)', 2)
                AS einheit
        FROM ufo_sightings
        WHERE regexp_matches(duration_text,
                '\d+\s*(seconds?|minutes?|mins?|hours?|hrs?)')
        LIMIT 20
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.accordion({"🔑 Musterlösung": mo.md("""
```sql
SELECT
    duration_text,
    regexp_extract(duration_text,
        '(\\d+)\\s*(seconds?|minutes?|mins?|hours?|hrs?)', 1)
        AS zahl,
    regexp_extract(duration_text,
        '(\\d+)\\s*(seconds?|minutes?|mins?|hours?|hrs?)', 2)
        AS einheit
FROM ufo_sightings
WHERE regexp_matches(duration_text,
        '\\d+\\s*(seconds?|minutes?|mins?|hours?|hrs?)')
LIMIT 20
```
**Erklärung:** Gruppe 1 = die Zahl (`\\d+`), Gruppe 2 = die Einheit. Das `?` nach dem `s` macht das "s" optional (minute/minutes).
""")})
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ### 🟡 Aufgabe 13.20: regexp_extract_all — Farben aus UFO-Beschreibungen

        UFO-Beschreibungen erwähnen oft Farben. DuckDB kann mit `regexp_extract_all` **alle** Treffer als Liste finden.
        Ergänzen Sie `???`:
        """
    )
    return


@app.cell
def _(mo, ufo_sightings):
    _df = mo.sql(
        f"""
        SELECT
            UNNEST(regexp_extract_all(LOWER(description),
                '(???)')) AS farbe,
            COUNT(*) AS anzahl
        FROM ufo_sightings
        GROUP BY farbe
        ORDER BY anzahl DESC
        -- Tipp: 'red|orange|white|green|blue|yellow|silver'
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.accordion({"🔑 Musterlösung": mo.md("""
```sql
SELECT
    UNNEST(regexp_extract_all(LOWER(description),
        '(red|orange|white|green|blue|yellow|silver)')) AS farbe,
    COUNT(*) AS anzahl
FROM ufo_sightings
GROUP BY farbe
ORDER BY anzahl DESC
```
**Erklärung:** `regexp_extract_all` gibt eine Liste aller Treffer zurück. `UNNEST` wandelt die Liste in einzelne Zeilen um.
""")})
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ### 🔵 Aufgabe 13.21: Bewegungsmuster klassifizieren

        Klassifizieren Sie UFO-Bewegungen mit `regexp_matches` + `CASE WHEN`:
        - **Hovering**: "hover", "stationary"
        - **Erratic**: "zigzag", "erratic", "changed direction"
        - **Vanishing**: "disappear", "vanish"
        - **Moving**: "moving", "moved", "flew", "flying"

        *Hinweis: `CASE WHEN regexp_matches(LOWER(description), 'hover|stationary') THEN 'Hovering' ...`*
        """
    )
    return


@app.cell
def _(mo, ufo_sightings):
    _df = mo.sql(
        f"""
        -- Ihre Lösung hier
        -- Erwartete Spalten: bewegung, anzahl
        -- Sortiert nach anzahl DESC
        SELECT 'Schreiben Sie Ihre Abfrage hier' AS hinweis
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.accordion({"🔑 Musterlösung": mo.md("""
```sql
SELECT
    CASE
        WHEN regexp_matches(LOWER(description),
             'hover|stationary') THEN 'Hovering'
        WHEN regexp_matches(LOWER(description),
             'zigzag|erratic|changed direction') THEN 'Erratic'
        WHEN regexp_matches(LOWER(description),
             'disappear|vanish') THEN 'Vanishing'
        WHEN regexp_matches(LOWER(description),
             'moving|moved|flew|flying') THEN 'Moving'
        ELSE 'Unbekannt'
    END AS bewegung,
    COUNT(*) AS anzahl,
    ROUND(AVG(LENGTH(description)), 0) AS avg_beschreibungslaenge
FROM ufo_sightings
GROUP BY bewegung
ORDER BY anzahl DESC
```
""")})
    return


# -----------------------------------------------------------------------
# Phase 7: Tokenisierung & Text Mining (UFO)
# -----------------------------------------------------------------------


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ---

        ## Phase 7: Tokenisierung & Text Mining (UFO Sightings)

        Tokenisierung = Text in Wörter zerlegen. Mit `UNNEST(regexp_split_to_array(...))` und
        Stoppwort-Filterung extrahieren wir die informativsten Begriffe.
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ### 🟢 Aufgabe 13.22: Tokenisierung — Top 25 Wörter

        Zerlegen Sie alle UFO-Beschreibungen in Wörter und berechnen Sie die Top 25 Worthäufigkeiten.
        """
    )
    return


@app.cell
def _(mo, ufo_sightings):
    word_freq = mo.sql(
        f"""
        SELECT
            UNNEST(regexp_split_to_array(
                LOWER(TRIM(description)), '\s+')) AS word,
            COUNT(*) AS frequency
        FROM ufo_sightings
        GROUP BY word
        HAVING LENGTH(word) > 0
        ORDER BY frequency DESC
        LIMIT 25
        """
    )
    return (word_freq,)


@app.cell
def _(px, ufo_sightings, word_freq):
    fig_freq = px.bar(
        word_freq,
        y="word",
        x="frequency",
        orientation="h",
        title=f"Top 25 Words in UFO Sighting Descriptions (n={len(ufo_sightings)})",
        labels={"word": "Word", "frequency": "Frequency"},
        color="frequency",
        color_continuous_scale="Blues",
    )
    fig_freq.update_layout(yaxis=dict(autorange="reversed"), height=600)
    fig_freq


@app.cell(hide_code=True)
def _(mo):
    mo.accordion({"🔑 Musterlösung": mo.md("""
```sql
SELECT
    UNNEST(regexp_split_to_array(
        LOWER(TRIM(description)), '\\s+')) AS word,
    COUNT(*) AS frequency
FROM ufo_sightings
GROUP BY word
HAVING LENGTH(word) > 0
ORDER BY frequency DESC
LIMIT 25
```
**Beobachtung:** Die häufigsten Wörter sind Stoppwörter ("the", "and", "in"). Wir müssen diese filtern!
""")})
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ### 🟡 Aufgabe 13.23: Stoppwort-Filterung

        Filtern Sie Stoppwörter heraus und zeigen Sie die Top 30 informativen Wörter. Ergänzen Sie `???`:
        """
    )
    return


@app.cell
def _(mo, ufo_sightings):
    _df = mo.sql(
        f"""
        WITH stoppwoerter AS (
            SELECT UNNEST(['the','a','an','and','or','to','in','of','it','is',
                           'was','for','on','that','with','as','at','by','from',
                           'this','i','we','no','me','so','very','about','had',
                           'were','but','not','then','be']) AS wort
        ),
        woerter AS (
            SELECT
                UNNEST(regexp_split_to_array(
                    LOWER(TRIM(description)), '\s+')) AS word
            FROM ufo_sightings
        )
        SELECT word, COUNT(*) AS frequency
        FROM woerter
        WHERE LENGTH(word) > ???
          AND word NOT IN (SELECT ??? FROM stoppwoerter)
        GROUP BY word
        ORDER BY frequency DESC
        LIMIT 30
        -- Tipp: LENGTH(word) > 1, SELECT wort FROM stoppwoerter
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.accordion({"🔑 Musterlösung": mo.md("""
```sql
WITH stoppwoerter AS (
    SELECT UNNEST(['the','a','an','and','or','to','in','of','it','is',
                   'was','for','on','that','with','as','at','by','from',
                   'this','i','we','no','me','so','very','about','had',
                   'were','but','not','then','be']) AS wort
),
woerter AS (
    SELECT
        UNNEST(regexp_split_to_array(
            LOWER(TRIM(description)), '\\s+')) AS word
    FROM ufo_sightings
)
SELECT word, COUNT(*) AS frequency
FROM woerter
WHERE LENGTH(word) > 1
  AND word NOT IN (SELECT wort FROM stoppwoerter)
GROUP BY word
ORDER BY frequency DESC
LIMIT 30
```
**Pattern:** `WITH stoppwoerter -> Tokenisieren -> WHERE NOT IN -> GROUP BY`
""")})
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ### 🔵 Aufgabe 13.24: July 4th Spike — UFOs oder Feuerwerk?

        Gibt es einen Spike an UFO-Meldungen am 4. Juli (US Independence Day)?
        Vergleichen Sie die Shapes am 4. Juli vs. Rest des Jahres.

        *Hinweis: `EXTRACT(MONTH FROM CAST(datetime AS DATE))`, `EXTRACT(DAY FROM ...)`*

        *Bonus: Wie viele "fireball"-Sichtungen sind am 4. Juli vs. Rest des Jahres?*
        """
    )
    return


@app.cell
def _(mo, ufo_sightings):
    _df = mo.sql(
        f"""
        -- Ihre Lösung hier
        -- Variante 1: Sichtungen pro Monat
        -- Variante 2: Shapes am 4. Juli vs. Rest
        SELECT 'Schreiben Sie Ihre Abfrage hier' AS hinweis
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.accordion({"🔑 Musterlösung": mo.md("""
**Variante 1: Sichtungen pro Monat**
```sql
SELECT
    EXTRACT(MONTH FROM CAST(datetime AS DATE)) AS monat,
    COUNT(*) AS anzahl_sichtungen
FROM ufo_sightings
GROUP BY monat
ORDER BY monat
```

**Variante 2: Shapes am 4. Juli vs. Rest**
```sql
SELECT
    shape,
    COUNT(*) FILTER (WHERE EXTRACT(MONTH FROM CAST(datetime AS DATE)) = 7
                       AND EXTRACT(DAY FROM CAST(datetime AS DATE)) = 4)
        AS july_4th,
    COUNT(*) FILTER (WHERE NOT (EXTRACT(MONTH FROM CAST(datetime AS DATE)) = 7
                            AND EXTRACT(DAY FROM CAST(datetime AS DATE)) = 4))
        AS rest,
    COUNT(*) AS gesamt
FROM ufo_sightings
GROUP BY shape
ORDER BY july_4th DESC
```
**Beobachtung:** "Fireball" dominiert am 4. Juli — wahrscheinlich Feuerwerk!
""")})
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ### 🔴 Aufgabe 13.25: Debugging — Unescapte Sonderzeichen in Regex

        Die folgende Abfrage soll Zahlen aus dem Dauertext extrahieren. Sie hat einen Fehler!
        """
    )
    return


@app.cell
def _(mo, ufo_sightings):
    _df = mo.sql(
        f"""
        -- 🔴 Diese Abfrage hat einen Fehler — finden und beheben Sie ihn!
        SELECT
            duration_text,
            regexp_extract(duration_text, '(d+) (minutes?|seconds?)', 1) AS zahl
        FROM ufo_sightings
        LIMIT 15
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.accordion({"🔑 Lösung": mo.md(r"""
**Problem:** `d+` sucht nach einem oder mehreren Buchstaben "d" — es fehlt der Backslash! `\d+` ist die Regex-Syntax für "eine oder mehrere Ziffern".

Außerdem fehlt `\s*` zwischen Zahl und Einheit.

**Lösung:**
```sql
SELECT
    duration_text,
    regexp_extract(duration_text, '(\d+)\s*(minutes?|seconds?)', 1) AS zahl
FROM ufo_sightings
LIMIT 15
```
""")})
    return


# -----------------------------------------------------------------------
# Phase 8: Exploration
# -----------------------------------------------------------------------


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ---

        ## Phase 8: Exploration

        Offene Herausforderungen — kombinieren Sie die gelernten Techniken kreativ!

        **Tipp:** Vergleichen Sie Ihre Lösungen mit Ihrem Nachbarn — bei Textanalyse gibt es oft kreative Ansätze, an die man allein nicht denkt!
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ### ⭐ Aufgabe 13.26: German vs. English — Wortlängenvergleich

        Vergleichen Sie die durchschnittliche Wortlänge in deutschen Produktbewertungen vs. englischen McDonald's-Reviews.
        Deutsche Wörter sind bekanntlich länger — stimmt das auch hier?

        *Hinweis: Tokenisieren Sie beide Datensätze und berechnen Sie `AVG(LENGTH(word))` — nutzen Sie UNION ALL.*
        """
    )
    return


@app.cell
def _(mcdonalds_reviews, mo, produktbewertungen):
    _df = mo.sql(
        f"""
        -- Ihre Lösung hier
        -- Erwartete Spalten: sprache, avg_wortlaenge, anzahl_woerter
        SELECT 'Schreiben Sie Ihre Abfrage hier' AS hinweis
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.accordion({"🔑 Musterlösung": mo.md("""
```sql
SELECT
    'Deutsch' AS sprache,
    ROUND(AVG(LENGTH(word)), 2) AS avg_wortlaenge,
    COUNT(*) AS anzahl_woerter
FROM (
    SELECT UNNEST(regexp_split_to_array(
        LOWER(TRIM(bewertung_text)), '\\s+')) AS word
    FROM produktbewertungen
)
WHERE LENGTH(word) > 0

UNION ALL

SELECT
    'English',
    ROUND(AVG(LENGTH(word)), 2),
    COUNT(*)
FROM (
    SELECT UNNEST(regexp_split_to_array(
        LOWER(TRIM(review_text)), '\\s+')) AS word
    FROM mcdonalds_reviews
)
WHERE LENGTH(word) > 0
```
""")})
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ### ⭐ Aufgabe 13.27: Aspekt-Analyse Transfer — McDonald's-Pattern auf Produktbewertungen

        Übertragen Sie das Aspekt-basierte Feature-Engineering-Pattern von McDonald's auf die Produktbewertungen.
        Definieren Sie deutsche Aspekte: Qualität, Preis, Haltbarkeit, Komfort.
        Welcher Aspekt korreliert am stärksten mit der Sternebewertung?

        *Hinweis: CASE WHEN + LIKE mit deutschen Schlüsselwörtern, dann AVG(sterne) pro Aspekt.*
        """
    )
    return


@app.cell
def _(mo, produktbewertungen):
    _df = mo.sql(
        f"""
        -- Ihre Lösung hier
        -- Erwartete Spalten: aspekt, n, avg_sterne
        SELECT 'Schreiben Sie Ihre Abfrage hier' AS hinweis
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.accordion({"🔑 Musterlösung": mo.md("""
```sql
SELECT 'Qualität' AS aspekt,
       COUNT(*) AS n,
       ROUND(AVG(sterne), 2) AS avg_sterne
FROM produktbewertungen
WHERE LOWER(bewertung_text) LIKE '%qualität%'
   OR LOWER(bewertung_text) LIKE '%hochwertig%'
   OR LOWER(bewertung_text) LIKE '%erstklassig%'
UNION ALL
SELECT 'Preis', COUNT(*), ROUND(AVG(sterne), 2)
FROM produktbewertungen
WHERE LOWER(bewertung_text) LIKE '%preis%'
   OR LOWER(bewertung_text) LIKE '%billig%'
   OR LOWER(bewertung_text) LIKE '%günstig%'
UNION ALL
SELECT 'Haltbarkeit', COUNT(*), ROUND(AVG(sterne), 2)
FROM produktbewertungen
WHERE LOWER(bewertung_text) LIKE '%kaputt%'
   OR LOWER(bewertung_text) LIKE '%defekt%'
   OR LOWER(bewertung_text) LIKE '%woche%'
   OR LOWER(bewertung_text) LIKE '%haltbar%'
UNION ALL
SELECT 'Komfort', COUNT(*), ROUND(AVG(sterne), 2)
FROM produktbewertungen
WHERE LOWER(bewertung_text) LIKE '%bequem%'
   OR LOWER(bewertung_text) LIKE '%komfortabel%'
   OR LOWER(bewertung_text) LIKE '%angenehm%'
ORDER BY avg_sterne DESC
```
""")})
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ### ⭐ Aufgabe 13.28: Entity Extraction — US-Staaten in UFO-Beschreibungen

        Einige UFO-Beschreibungen erwähnen Orte. Vergleichen Sie die `state`-Spalte mit dem tatsächlichen
        Text: Werden bestimmte Städte oder Landmarks erwähnt? Welche Staaten haben die meisten Sichtungen?

        *Hinweis: `GROUP BY state`, oder versuchen Sie Ortsnamen im Text zu finden mit `regexp_extract_all`.*
        """
    )
    return


@app.cell
def _(mo, ufo_sightings):
    _df = mo.sql(
        f"""
        -- Ihre Lösung hier
        -- Idee 1: Sichtungen pro State
        -- Idee 2: Ortserwähnungen im Text extrahieren
        SELECT 'Schreiben Sie Ihre Abfrage hier' AS hinweis
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.accordion({"🔑 Musterlösung": mo.md("""
**Sichtungen pro State:**
```sql
SELECT
    state,
    COUNT(*) AS anzahl,
    ROUND(AVG(LENGTH(description)), 0) AS avg_beschreibungslaenge
FROM ufo_sightings
GROUP BY state
ORDER BY anzahl DESC
```

**Landmark-Erwähnungen:**
```sql
SELECT
    UNNEST(regexp_extract_all(LOWER(description),
        '(highway|airport|lake|city|beach|park|forest|mountains?|stadium|desert|river)')) AS ort,
    COUNT(*) AS anzahl
FROM ufo_sightings
GROUP BY ort
ORDER BY anzahl DESC
```
""")})
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ### ⭐ Aufgabe 13.29: Textlänge vs. Rating — Scatter Plot (McDonald's)

        Gibt es einen Zusammenhang zwischen Textlänge und Bewertung?
        Erstellen Sie einen Scatter Plot mit `px.scatter()`.

        *Hinweis: SQL-Query mit `LENGTH(review_text)` und `rating`, dann `px.scatter()`*
        """
    )
    return


@app.cell
def _(mcdonalds_reviews, mo):
    scatter_data = mo.sql(
        f"""
        SELECT
            review_id,
            rating,
            LENGTH(review_text) AS text_length,
            store_name
        FROM mcdonalds_reviews
        """
    )
    return (scatter_data,)


@app.cell
def _(mcdonalds_reviews, px, scatter_data):
    fig_scatter = px.scatter(
        scatter_data,
        x="text_length",
        y="rating",
        color="store_name",
        title=f"Review Text Length vs. Rating (McDonald's, n={len(mcdonalds_reviews)})",
        labels={
            "text_length": "Text Length (chars)",
            "rating": "Rating",
            "store_name": "Store Type",
        },
        opacity=0.4,
    )
    fig_scatter.update_layout(height=500)
    fig_scatter


@app.cell(hide_code=True)
def _(mo):
    mo.accordion({"🔑 Musterlösung": mo.md("""
```sql
SELECT
    review_id,
    rating,
    LENGTH(review_text) AS text_length,
    store_name
FROM mcdonalds_reviews
```
Dann Visualisierung mit:
```python
px.scatter(scatter_data, x="text_length", y="rating", color="store_name")
```
**Beobachtung:** Schreiben unzufriedene Kunden längere Reviews? Gibt es einen Zusammenhang?
""")})
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ### ⭐ Aufgabe 13.30: Mini Text-Mining Dashboard

        Kombinieren Sie mehrere Analysen zu einem Überblick:
        1. **Produktbewertungen:** Top 10 Wörter (ohne Stoppwörter)
        2. **McDonald's:** Aspekt-Rating Korrelation
        3. **UFO:** Farben + Shapes Kreuzanalyse

        *Hinweis: Drei separate SQL-Queries — nutzen Sie alle gelernten Techniken!*
        """
    )
    return


@app.cell
def _(mo, produktbewertungen):
    _df = mo.sql(
        f"""
        -- Teil 1: Top 10 Wörter in Produktbewertungen (ohne Stoppwörter)
        -- Ihre Lösung hier
        SELECT 'Dashboard Teil 1: Top Wörter in Produktbewertungen' AS hinweis
        """
    )
    return


@app.cell
def _(mcdonalds_reviews, mo):
    _df = mo.sql(
        f"""
        -- Teil 2: Aspekt-Rating Korrelation (McDonald's)
        -- Ihre Lösung hier
        SELECT 'Dashboard Teil 2: Aspekt-Analyse McDonald''s' AS hinweis
        """
    )
    return


@app.cell
def _(mo, ufo_sightings):
    _df = mo.sql(
        f"""
        -- Teil 3: Farben × Shapes Kreuzanalyse (UFO)
        -- Ihre Lösung hier
        SELECT 'Dashboard Teil 3: Farben und Shapes bei UFOs' AS hinweis
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.accordion({"🔑 Musterlösung": mo.md("""
**Teil 1: Top 10 Wörter in Produktbewertungen**
```sql
WITH stoppwoerter AS (
    SELECT UNNEST(['der','die','das','und','ist','ein','eine','für',
                   'mit','nicht','auf','den','von','zu','im','ich',
                   'es','sich','auch','an','war','sehr','aber']) AS wort
),
woerter AS (
    SELECT UNNEST(regexp_split_to_array(
        LOWER(TRIM(bewertung_text)), '\\s+')) AS word
    FROM produktbewertungen
)
SELECT word, COUNT(*) AS frequency
FROM woerter
WHERE LENGTH(word) > 1 AND word NOT IN (SELECT wort FROM stoppwoerter)
GROUP BY word ORDER BY frequency DESC LIMIT 10
```

**Teil 2: Aspekt-Rating (McDonald's)**
```sql
SELECT 'Food' AS aspect, COUNT(*) AS n, ROUND(AVG(rating), 2) AS avg_rating
FROM mcdonalds_reviews WHERE LOWER(review_text) LIKE '%food%' OR LOWER(review_text) LIKE '%burger%'
UNION ALL
SELECT 'Service', COUNT(*), ROUND(AVG(rating), 2)
FROM mcdonalds_reviews WHERE LOWER(review_text) LIKE '%service%' OR LOWER(review_text) LIKE '%staff%'
UNION ALL
SELECT 'Cleanliness', COUNT(*), ROUND(AVG(rating), 2)
FROM mcdonalds_reviews WHERE LOWER(review_text) LIKE '%clean%' OR LOWER(review_text) LIKE '%dirty%'
ORDER BY avg_rating DESC
```

**Teil 3: Farben x Shapes (UFO)**
```sql
SELECT
    shape,
    UNNEST(regexp_extract_all(LOWER(description),
        '(red|orange|white|green|blue|silver)')) AS farbe,
    COUNT(*) AS anzahl
FROM ufo_sightings
GROUP BY shape, farbe
ORDER BY anzahl DESC
LIMIT 15
```
""")})
    return


# -----------------------------------------------------------------------
# Zusammenfassung
# -----------------------------------------------------------------------


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ---

        ## Zusammenfassung

        | Konzept | Syntax | Anwendung |
        |---------|--------|-----------|
        | **LENGTH** | `LENGTH(text)` | Textlänge messen |
        | **TRIM** | `TRIM(text)` | Leerzeichen entfernen |
        | **REPLACE** | `REPLACE(text, a, b)` | Zeichen ersetzen |
        | **LOWER** | `LOWER(text)` | Normalisierung |
        | **LIKE/ILIKE** | `text LIKE '%pattern%'` | Muster suchen |
        | **CASE WHEN + LIKE** | `CASE WHEN ... LIKE ... THEN 1` | Feature Engineering |
        | **regexp_matches** | `regexp_matches(text, '\d+')` | Pattern vorhanden? (Boolean) |
        | **regexp_extract** | `regexp_extract(text, '(\d+)', 1)` | Capture Group extrahieren |
        | **regexp_extract_all** | `regexp_extract_all(text, '(red|blue)')` | Alle Treffer als Liste |
        | **regexp_replace** | `regexp_replace(text, '[^a-z]', '', 'g')` | Global ersetzen |
        | **regexp_split_to_array** | `regexp_split_to_array(text, '\s+')` | Regex-Tokenisierung |
        | **Tokenisierung** | `UNNEST(regexp_split_to_array(...))` | Wörter zerlegen |
        | **Zeichen zählen** | `LENGTH(t) - LENGTH(REPLACE(t,'x',''))` | Vorkommen zählen |

        | Aufgaben | Thema |
        |----------|-------|
        | 13.1 – 13.3 | Datenüberblick & LENGTH-Profiling |
        | 13.4 – 13.7 | Textbereinigung: TRIM, REPLACE |
        | 13.8 – 13.10 | LOWER & Pattern Matching |
        | 13.11 – 13.14 | LIKE & Feature Engineering (McDonald's) |
        | 13.15 – 13.18 | Aspekt-Analyse & Sentiment |
        | 13.19 – 13.21 | Regex & Capture Groups (UFO) |
        | 13.22 – 13.25 | Tokenisierung & Text Mining |
        | 13.26 – 13.30 | Exploration & Dashboard |

        **Letzte Session!** Viel Erfolg bei der Klausur!
        """
    )
    return


if __name__ == "__main__":
    app.run()
