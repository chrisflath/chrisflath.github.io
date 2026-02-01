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

__generated_with = "0.10.14"
app = marimo.App(width="medium", app_title="DMA Session 14: Textanalyse")


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        # Vorlesung 14: Textanalyse

        **Kursfahrplan:** I: SQL-Grundlagen (S1–4) · II: Datenmodellierung (S5–8) · III: Fortgeschrittenes SQL (S9–10) · **▸ IV: Datenanalyse (S11–14)**

        In Sessions 11–13 haben wir numerische Daten analysiert — Verteilungen, Tests, Zeitreihen. Zum Abschluss wenden wir SQL auf **unstrukturierte Textdaten** an: die häufigste Datenform in der Praxis.

        **Lernziele:**
        - Textdaten mit SQL-String-Funktionen bereinigen und analysieren
        - Pattern Matching mit LIKE und regulären Ausdrücken anwenden
        - Texte in Wörter zerlegen (Tokenisierung) und Worthäufigkeiten berechnen
        - Aspekt-basierte Analyse: Themen aus Freitext extrahieren

        **Drei Datensätze — steigende Komplexität:**

        | Datensatz | Sprache | Größe | Fokus |
        |-----------|---------|-------|-------|
        | Produktbewertungen | Deutsch | 150 | String-Grundfunktionen |
        | McDonald's Reviews | Englisch | 3.000 | Aspekt-Analyse & LIKE |
        | UFO Sightings | Englisch | 5.000 | Regex, Tokenisierung, Mining |
        """
    )
    return


@app.cell
def _():
    import marimo as mo
    import polars as pl
    import plotly.express as px
    return mo, pl, px


@app.cell(hide_code=True)
def _(mo, pl):
    # --- Alle drei Datensätze laden ---
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
                # ~15 mentioning food
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
                # ~12 mentioning service
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
                # ~10 mentioning price
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
                # ~8 mentioning cleanliness
                "The restaurant was spotless, tables were clean and floors shiny.",
                "Disgusting! Dirty tables, filthy bathroom and trash everywhere.",
                "Very clean location, you can tell they take hygiene seriously.",
                "The dining area was dirty with sticky tables and old food on the floor.",
                "Clean kitchen visible from the counter, that is reassuring.",
                "Tables were clean but the bathroom needed serious attention.",
                "One of the cleanest fast food places I have been to, well maintained.",
                "Filthy restaurant, saw a cockroach near the drink station. Gross!",
                # ~5 mixed/other
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
    return mcdonalds_reviews, produktbewertungen, ufo_sightings


# =============================================================================
# PHASE 1–2: PRODUKTBEWERTUNGEN (guided)
# =============================================================================


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ---

        ## Phase 1–2: String-Grundfunktionen (Produktbewertungen)

        Wir starten mit einem kleinen, vertrauten Datensatz: 150 deutsche Produktbewertungen.
        Hier lernen wir die SQL-Werkzeuge kennen, bevor wir sie auf die großen Datensätze loslassen.
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ### Aufgabe 14.1: Datenüberblick

        Wie viele Bewertungen gibt es pro Kategorie? Wie sind die Sterne verteilt?
        """
    )
    return


@app.cell
def _(mo, produktbewertungen):
    mo.sql(
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


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ### Aufgabe 14.2: LENGTH-Profiling

        Wie lang sind die Bewertungstexte? Gibt es Unterschiede nach Kategorie oder Sternebewertung?
        """
    )
    return


@app.cell
def _(mo, produktbewertungen):
    mo.sql(
        f"""
        SELECT
            kategorie,
            ROUND(AVG(LENGTH(bewertung_text)), 0) AS avg_laenge,
            MIN(LENGTH(bewertung_text)) AS min_laenge,
            MAX(LENGTH(bewertung_text)) AS max_laenge
        FROM produktbewertungen
        GROUP BY kategorie
        ORDER BY avg_laenge DESC
        """
    )


@app.cell
def _(mo, produktbewertungen):
    mo.sql(
        f"""
        SELECT
            sterne,
            ROUND(AVG(LENGTH(bewertung_text)), 0) AS avg_laenge,
            COUNT(*) AS anzahl
        FROM produktbewertungen
        GROUP BY sterne
        ORDER BY sterne
        """
    )


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ### Aufgabe 14.3: Textbereinigung mit TRIM und REPLACE

        Einige Bewertungen haben führende/nachfolgende Leerzeichen oder doppelte Leerzeichen.
        Finden und bereinigen Sie diese.
        """
    )
    return


@app.cell
def _(mo, produktbewertungen):
    mo.sql(
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


@app.cell
def _(mo, produktbewertungen):
    mo.sql(
        f"""
        SELECT
            id,
            bewertung_text,
            REPLACE(bewertung_text, '  ', ' ') AS bereinigt
        FROM produktbewertungen
        WHERE bewertung_text LIKE '%  %'
        """
    )


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ### Aufgabe 14.4: Zeichen zählen — LENGTH-REPLACE Trick

        **Klausur-Pattern:** `LENGTH(text) - LENGTH(REPLACE(text, 'x', ''))` = Anzahl von 'x'

        Zählen Sie die Ausrufezeichen pro Bewertung als Emotionalitäts-Indikator.
        """
    )
    return


@app.cell
def _(mo, produktbewertungen):
    mo.sql(
        f"""
        SELECT
            id, sterne, bewertung_text,
            LENGTH(bewertung_text) - LENGTH(REPLACE(bewertung_text, '!', ''))
                AS anzahl_ausrufezeichen
        FROM produktbewertungen
        WHERE LENGTH(bewertung_text) - LENGTH(REPLACE(bewertung_text, '!', '')) > 0
        ORDER BY anzahl_ausrufezeichen DESC
        LIMIT 10
        """
    )


@app.cell
def _(mo, produktbewertungen):
    mo.sql(
        f"""
        SELECT
            sterne,
            ROUND(AVG(
                LENGTH(bewertung_text) - LENGTH(REPLACE(bewertung_text, '!', ''))
            ), 2) AS avg_ausrufezeichen
        FROM produktbewertungen
        GROUP BY sterne
        ORDER BY sterne
        """
    )


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ### Aufgabe 14.5: LOWER-Normalisierung

        Nutzen Sie `LOWER()` um zu prüfen, wie viele Bewertungen das Wort "qualität" (in jeder Schreibweise) enthalten.
        """
    )
    return


@app.cell
def _(mo, produktbewertungen):
    mo.sql(
        f"""
        SELECT
            COUNT(*) AS bewertungen_mit_qualitaet,
            ROUND(AVG(sterne), 2) AS avg_sterne_qualitaet
        FROM produktbewertungen
        WHERE LOWER(bewertung_text) LIKE '%qualität%'
           OR LOWER(bewertung_text) LIKE '%hochwertig%'
        """
    )


@app.cell(hide_code=True)
def _(mo):
    quiz_like_regex = mo.ui.radio(
        options={
            "correct": "LIKE eignet sich für 1-2 Muster; bei vielen Alternativen ist REGEXP sauberer",
            "equivalent": "LIKE und REGEXP geben immer das gleiche Ergebnis — persönliche Vorliebe",
            "always_regex": "REGEXP sollte immer verwendet werden, LIKE ist veraltet",
            "language": "LIKE funktioniert nur auf Englisch, Deutsch braucht REGEXP",
        },
        label="**Quiz:** Wann ist `regexp_matches(text, 'food|burger|fries')` besser als viele `LIKE`-Bedingungen?"
    )
    quiz_like_regex
    return (quiz_like_regex,)


@app.cell(hide_code=True)
def _(quiz_like_regex, mo):
    if quiz_like_regex.value == "correct":
        mo.output.replace(mo.md("Richtig! Bei 1-2 Mustern ist LIKE schneller zu lesen. Ab 3+ Alternativen wird REGEXP mit `|` (Oder) deutlich kompakter und weniger fehleranfällig als viele `OR LIKE`-Klauseln."))
    elif quiz_like_regex.value:
        mo.output.replace(mo.md("Nicht ganz. LIKE ist einfacher für einzelne Muster (`%food%`), aber bei vielen Alternativen braucht man viele OR-Klauseln. REGEXP kann mit `food|burger|fries` alle in einem Ausdruck prüfen."))
    return


# =============================================================================
# PHASE 3–4: McDONALD'S REVIEWS (guided)
# =============================================================================


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ---

        ## Phase 3–4: Aspekt-Analyse (McDonald's Reviews)

        Jetzt wechseln wir zu 3.000 englischen McDonald's-Bewertungen.
        Mit `LIKE` und `CASE WHEN` extrahieren wir Aspekte und korrelieren sie mit Ratings.
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ### Aufgabe 14.6: LIKE-Filterung — Food Reviews

        Finden Sie alle Reviews, die über das Essen sprechen.
        """
    )
    return


@app.cell
def _(mcdonalds_reviews, mo):
    mo.sql(
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


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ### Aufgabe 14.7: CASE WHEN + LIKE — Feature Engineering

        Erzeugen Sie boolesche Feature-Spalten für: Food, Service, Speed, Cleanliness, Price.
        """
    )
    return


@app.cell
def _(mcdonalds_reviews, mo):
    mo.sql(
        f"""
        SELECT
            review_id, rating,
            CASE WHEN LOWER(review_text) LIKE '%food%'
                      OR LOWER(review_text) LIKE '%burger%'
                      OR LOWER(review_text) LIKE '%fries%'
                      OR LOWER(review_text) LIKE '%nuggets%'
                      OR LOWER(review_text) LIKE '%coffee%'
                 THEN 1 ELSE 0 END AS food,
            CASE WHEN LOWER(review_text) LIKE '%service%'
                      OR LOWER(review_text) LIKE '%staff%'
                      OR LOWER(review_text) LIKE '%rude%'
                      OR LOWER(review_text) LIKE '%friendly%'
                      OR LOWER(review_text) LIKE '%employee%'
                 THEN 1 ELSE 0 END AS service,
            CASE WHEN LOWER(review_text) LIKE '%wait%'
                      OR LOWER(review_text) LIKE '%slow%'
                      OR LOWER(review_text) LIKE '%fast%'
                      OR LOWER(review_text) LIKE '%quick%'
                      OR LOWER(review_text) LIKE '%minute%'
                 THEN 1 ELSE 0 END AS speed,
            CASE WHEN LOWER(review_text) LIKE '%clean%'
                      OR LOWER(review_text) LIKE '%dirty%'
                      OR LOWER(review_text) LIKE '%filthy%'
                 THEN 1 ELSE 0 END AS cleanliness,
            CASE WHEN LOWER(review_text) LIKE '%price%'
                      OR LOWER(review_text) LIKE '%expensive%'
                      OR LOWER(review_text) LIKE '%value%'
                      OR LOWER(review_text) LIKE '%cheap%'
                 THEN 1 ELSE 0 END AS price
        FROM mcdonalds_reviews
        LIMIT 20
        """
    )


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ### Aufgabe 14.8: Aspekt-Rating Korrelation + Visualisierung

        Welche Aspekte haben die höchsten / niedrigsten Durchschnittsbewertungen?
        """
    )
    return


@app.cell
def _(mcdonalds_reviews, mo):
    aspekt_analyse = mo.sql(
        f"""
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
           OR LOWER(review_text) LIKE '%fast%'
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
        """
    )
    return (aspekt_analyse,)


@app.cell
def _(aspekt_analyse, px):
    df_aspekt = aspekt_analyse.to_pandas()
    fig_aspekt = px.bar(
        df_aspekt,
        x="aspect",
        y="avg_rating",
        text="n",
        title="Average Rating by Mentioned Aspect (McDonald's, n=3000)",
        labels={"aspect": "Aspect", "avg_rating": "Avg Rating", "n": "Count"},
        color="avg_rating",
        color_continuous_scale="RdYlGn",
        range_color=[1, 5],
    )
    fig_aspekt.update_traces(texttemplate="n=%{text}", textposition="outside")
    fig_aspekt.update_layout(yaxis_range=[0, 5.5])
    fig_aspekt


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ### Aufgabe 14.9: Aspekte nach Rating-Tier (selbstständig)

        Vergleichen Sie die Häufigkeit der Aspekte in positiven (4–5★) vs. negativen (1–2★) Reviews.

        *Hinweis: `COUNT(*) FILTER (WHERE rating >= 4)` vs. `FILTER (WHERE rating <= 2)`*
        """
    )
    return


@app.cell
def _(mcdonalds_reviews, mo):
    # Ihre Lösung hier:
    mo.sql(
        f"""
        SELECT 'Tipp: CTE mit Feature-Spalten, dann FILTER' AS hinweis
        """
    )


# =============================================================================
# PHASE 5–6: UFO SIGHTINGS (guided intro, then self-service)
# =============================================================================


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ---

        ## Phase 5: Reguläre Ausdrücke & Textzerlegung (UFO Sightings)

        Jetzt wird es wild: 5.000 UFO-Augenzeugenberichte. Lange Texte, chaotische Felder,
        inkonsistente Schreibweisen. Perfekt für Regex und Tokenisierung.

        ### Aufgabe 14.10: Regex mit Capture Groups — Dauer parsen

        Das `duration_text`-Feld ist chaotisch: "5 minutes", "about 30 seconds", "~10 min", "2-3 hours"...

        DuckDB kann mit **Capture Groups** Zahl UND Einheit in einem einzigen Pattern extrahieren:
        `regexp_extract(text, '(\d+)\s*(minutes?|seconds?|hours?)', gruppe)`

        - Gruppe 1 = die Zahl
        - Gruppe 2 = die Einheit
        """
    )
    return


@app.cell
def _(mo, ufo_sightings):
    mo.sql(
        f"""
        -- Capture Groups: Zahl UND Einheit in einem Schritt
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


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ### Aufgabe 14.11: Tokenisierung + Top-Wörter

        Zerlegen Sie alle UFO-Beschreibungen in Wörter und berechnen Sie die Top 25 Worthäufigkeiten.

        Wir nutzen `regexp_split_to_array` statt `string_split` — das handhabt
        mehrere Leerzeichen, Tabs und Zeilenumbrüche korrekt.
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
def _(px, word_freq):
    df_freq = word_freq.to_pandas()
    fig_freq = px.bar(
        df_freq,
        y="word",
        x="frequency",
        orientation="h",
        title="Top 25 Words in UFO Sighting Descriptions (n=5000)",
        labels={"word": "Word", "frequency": "Frequency"},
        color="frequency",
        color_continuous_scale="Blues",
    )
    fig_freq.update_layout(yaxis=dict(autorange="reversed"), height=600)
    fig_freq


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ---

        ## Phase 6: Text-Mining Projekt — Self Service

        Ab hier arbeiten Sie selbstständig. Sie haben alle Werkzeuge —
        Aufgaben geben Ziel und Hinweise, das SQL schreiben Sie.

        ---

        ### Aufgabe 14.11b: Geführtes Beispiel — Stoppwörter filtern (Produktbewertungen)

        Bevor wir mit den UFO-Daten weitermachen, hier das Muster für
        **Tokenisierung + Stoppwort-Filterung** am bekannten Datensatz:
        """
    )
    return


@app.cell
def _(mo, produktbewertungen):
    # Geführtes Beispiel: Stoppwörter filtern
    _stopword_demo = mo.sql(
        f"""
        -- Schritt 1: Stoppwörter definieren
        WITH stoppwoerter AS (
            SELECT UNNEST(['der','die','das','und','ist','ein','eine','für',
                           'mit','nicht','auf','den','von','zu','im','ich',
                           'es','sich','auch','an','war','sehr','aber']) AS wort
        ),
        -- Schritt 2: Tokenisieren
        woerter AS (
            SELECT
                UNNEST(regexp_split_to_array(
                    LOWER(TRIM(bewertung)), '\s+')) AS word
            FROM produktbewertungen
        )
        -- Schritt 3: Filtern + Zählen
        SELECT word, COUNT(*) AS frequency
        FROM woerter
        WHERE LENGTH(word) > 1
          AND word NOT IN (SELECT wort FROM stoppwoerter)
        GROUP BY word
        ORDER BY frequency DESC
        LIMIT 15
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        **Das Muster:** `WITH stoppwoerter → Tokenisieren → WHERE NOT IN → GROUP BY`

        Dieses Muster verwenden Sie jetzt auf die UFO- und McDonald's-Daten.

        ---

        ### Aufgabe 14.12: Stoppwort-Filterung (UFO)

        Die häufigsten Wörter sind "the", "a", "was" — wenig informativ. Filtern Sie Stoppwörter heraus.

        *Hinweis: `WHERE word NOT IN ('the', 'a', 'an', 'i', 'in', 'of', 'and', 'to', 'was', 'it', 'is', 'that', 'at', 'my', 'for', 'on', 'with', 'had', 'as', 'were', 'from', 'by', 'or', 'be', 'but', 'not', 'this', 'then', 'we', 'no', 'me', 'so', 'very', 'about')`*

        *Erwartete Ausgabe: 30 Zeilen, Spalten `word`, `frequency`, sortiert nach `frequency DESC`*
        """
    )
    return


@app.cell
def _(mo, ufo_sightings):
    # Ihre Lösung: Wörter ohne Stoppwörter, Top 30
    mo.sql(
        f"""
        -- Stoppwörter sind bereits definiert:
        WITH stoppwoerter AS (
            SELECT UNNEST(['the','a','an','and','or','to','in','of','it','is',
                           'was','for','on','that','with','as','at','by','from',
                           'this','i','we','no','me','so','very','about','had',
                           'were','but','not','then','be']) AS wort
        )
        -- Ihre Aufgabe: Tokenisieren + Filtern
        -- Tipp: UNNEST(regexp_split_to_array(LOWER(TRIM(description)), '\s+')) AS word
        --       WHERE word NOT IN (SELECT wort FROM stoppwoerter)
        --       GROUP BY word ORDER BY COUNT(*) DESC LIMIT 30
        SELECT 'Ergänzen Sie die Abfrage oben' AS hinweis
        """
    )


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ### Aufgabe 14.13: July 4th Spike — UFOs oder Feuerwerk?

        Gibt es einen Spike an UFO-Meldungen rund um den 4. Juli (US Independence Day)?
        Vergleichen Sie die Anzahl Sichtungen pro Monat — oder sogar pro Tag im Juli.

        *Hinweis: `EXTRACT(MONTH FROM CAST(datetime AS DATE))`, `EXTRACT(DAY FROM ...)`*

        *Bonus: Vergleichen Sie die gemeldeten Shapes am 4. Juli vs. Rest des Jahres — sind es eher "fireball" und "light"?*

        *Erwartete Ausgabe (Basis): 12 Zeilen (Monate), Spalten `monat`, `anzahl_sichtungen`, sortiert nach `monat`*
        """
    )
    return


@app.cell
def _(mo, ufo_sightings):
    # Ihre Lösung: July 4th Analyse
    mo.sql(
        f"""
        SELECT 'Finden Sie den July 4th Spike — und prüfen Sie ob die Shapes anders sind!' AS hinweis
        """
    )


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ### Aufgabe 14.14: Farbanalyse — Welche Farben werden gemeldet?

        UFO-Beschreibungen erwähnen oft Farben: "bright white", "orange", "red", "green", "blue"...

        DuckDB-Power: `regexp_extract_all` findet **alle** Farben pro Bericht als Liste!

        ```sql
        regexp_extract_all(LOWER(description),
            '(red|orange|white|green|blue|yellow)')
        ```

        Mit `UNNEST(...)` wird die Liste zu einzelnen Zeilen — perfekt für `GROUP BY` + `COUNT`.

        *Alternativ: `CASE WHEN + LIKE` für eine einzelne Hauptfarbe pro Bericht.*

        *Bonus: Korreliert die Farbe mit der Form (shape)?*

        *Erwartete Ausgabe: ~6 Zeilen (eine pro Farbe), Spalten `farbe`, `anzahl`, sortiert nach `anzahl DESC`*
        """
    )
    return


@app.cell
def _(mo, ufo_sightings):
    # Ihre Lösung: Farbanalyse
    mo.sql(
        f"""
        SELECT 'Welche Farben werden am häufigsten in UFO-Berichten erwähnt?' AS hinweis
        """
    )


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ### Aufgabe 14.15: Bewegungsmuster — Wie bewegen sich UFOs?

        Klassifizieren Sie die Bewegung der Objekte anhand der Beschreibungen:
        - **Hovering**: "hovering", "stationary", "hovered"
        - **Moving**: "moving", "moved", "flew", "flying"
        - **Erratic**: "zigzag", "erratic", "changed direction", "sharp turn"
        - **Vanishing**: "disappeared", "vanished"

        Welches Bewegungsmuster ist am häufigsten? Gibt es Unterschiede nach Shape?

        *Erwartete Ausgabe: 4–5 Zeilen, Spalten `bewegung`, `anzahl`, sortiert nach `anzahl DESC`*

        *Hinweis: `regexp_matches` mit `|` (Oder) ist eleganter als viele `LIKE`s:*

        ```sql
        CASE
            WHEN regexp_matches(LOWER(description),
                 'hover|stationary') THEN 'Hovering'
            WHEN regexp_matches(LOWER(description),
                 'zigzag|erratic|sharp turn') THEN 'Erratic'
            ...
        END
        ```
        """
    )
    return


@app.cell
def _(mo, ufo_sightings):
    # Ihre Lösung: Bewegungsmuster
    mo.sql(
        f"""
        SELECT 'Klassifizieren Sie die Bewegungsmuster der UFOs' AS hinweis
        """
    )


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ### Aufgabe 14.16: Wörter nach Rating-Tier (McDonald's)

        Welche Wörter kommen häufiger in positiven (4–5★) vs. negativen (1–2★) Reviews vor?

        *Hinweis: Tokenisieren + `COUNT(*) FILTER (WHERE rating >= 4)` vs. `FILTER (WHERE rating <= 2)`*

        *Erwartete Ausgabe: ~20 Zeilen, Spalten `word`, `count_positiv`, `count_negativ`, sortiert nach `count_positiv DESC`*
        """
    )
    return


@app.cell
def _(mcdonalds_reviews, mo):
    # Ihre Lösung: Wörter nach Rating
    mo.sql(
        f"""
        -- Schritt 1 (gegeben): Rating-Tiers bilden
        WITH bewertungen_mit_tier AS (
            SELECT *,
                CASE WHEN rating >= 4 THEN 'positiv'
                     WHEN rating <= 2 THEN 'negativ'
                     ELSE 'neutral' END AS tier
            FROM mcdonalds_reviews
        )
        -- Schritt 2 (Ihre Aufgabe): Tokenisieren und Wörter pro Tier zählen
        -- Tipp: UNNEST(regexp_split_to_array(LOWER(review_text), '\s+')) AS word
        --       GROUP BY tier, word
        --       Dann: Vergleichen Sie die häufigsten Wörter pro Tier
        SELECT 'Ergänzen Sie: UNNEST + GROUP BY tier, word' AS hinweis
        """
    )


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ### Aufgabe 14.17: Sentiment-Score (McDonald's)

        Bauen Sie einen einfachen Sentiment-Score:
        Zählen Sie positive Wörter (great, fresh, delicious, friendly, fast, clean, excellent, perfect)
        minus negative (terrible, cold, rude, slow, dirty, worst, wrong, disgusting).

        Korreliert der Score mit dem tatsächlichen Rating?

        *Hinweis: `CASE WHEN LOWER(review_text) LIKE '%great%' THEN 1 ELSE 0 END` für jedes Wort, dann summieren.*

        *Erwartete Ausgabe: Eine Zeile pro Review (oder gruppiert nach Rating), Spalten `rating`, `avg_sentiment_score`, sortiert nach `rating`*
        """
    )
    return


@app.cell
def _(mcdonalds_reviews, mo):
    # Ihre Lösung: Sentiment-Score
    mo.sql(
        f"""
        -- Wortlisten für einfache Sentiment-Analyse:
        WITH sentiment_woerter AS (
            SELECT 'positiv' AS typ,
                   UNNEST(['great','good','excellent','best','love',
                           'clean','fast','friendly','fresh','amazing']) AS wort
            UNION ALL
            SELECT 'negativ' AS typ,
                   UNNEST(['bad','worst','terrible','slow','rude',
                           'dirty','cold','wrong','horrible','disgusting']) AS wort
        )
        -- Ihre Aufgabe: Zählen Sie positive und negative Wörter pro Review
        -- Tipp: JOIN über LIKE ('%' || wort || '%') oder einzelne CASE WHEN Spalten
        --       Dann: SUM(positive) - SUM(negative) AS sentiment_score
        --       Vergleichen Sie mit dem tatsächlichen Rating
        SELECT 'Ergänzen Sie: JOIN + GROUP BY + SUM(CASE WHEN ...)' AS hinweis
        """
    )


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ### Aufgabe 14.18: Textlänge vs. Rating (McDonald's) — Scatter Plot

        Gibt es einen Zusammenhang zwischen Textlänge und Bewertung?

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
def _(px, scatter_data):
    df_scatter = scatter_data.to_pandas()
    fig_scatter = px.scatter(
        df_scatter,
        x="text_length",
        y="rating",
        color="store_name",
        title="Review Text Length vs. Rating (McDonald's, n=3000)",
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
    mo.md(
        r"""
        ---

        ## Freie Exploration

        **UFO-Ideen:**
        - Welche US-Staaten melden die meisten Sichtungen? (`GROUP BY state`)
        - Nacht- vs. Tagsichtungen — unterscheiden sich die Beschreibungen?
        - Werden Berichte über die Jahre länger? (Trend in `LENGTH(description)` über `EXTRACT(YEAR FROM ...)`)
        - Sichtungen mit mehreren Ausrufe-/Fragezeichen — emotionalste Berichte?
        - Shape + Farbe + Bewegung als vollständige Feature-Matrix

        **McDonald's-Ideen:**
        - "wrong order" Reviews — wie korreliert das mit dem Rating?
        - Welche Filialen (Drive-Thru vs. Airport vs. ...) haben die besten Reviews?
        - ALL-CAPS Reviews finden (`review_text = UPPER(review_text)`) — sind die wütend?
        """
    )
    return


@app.cell
def _(mo, ufo_sightings):
    # Eigene Analyse hier:
    mo.sql(
        f"""
        SELECT 'Freie Exploration — probieren Sie eigene Queries!' AS hinweis
        """
    )


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

        **Letzte Session!** Viel Erfolg bei der Klausur!
        """
    )
    return


if __name__ == "__main__":
    app.run()
