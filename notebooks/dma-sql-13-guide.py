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
    app_title="DMA Session 13: Textanalyse — Guide",
)


@app.cell(hide_code=True)
def _():
    import marimo as mo
    return (mo,)


@app.cell(hide_code=True)
def _():
    import polars as pl
    import plotly.express as px
    return pl, px


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
# TITEL & EINFÜHRUNG
# =============================================================================


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        # Session 13: Textanalyse — Guide

        **Kursfahrplan:** I: SQL-Grundlagen (S1--4) · II: Datenmodellierung (S5--7) · III: Fortgeschrittenes SQL (S8--9) · **▸ IV: Datenanalyse (S10--13)**

        ### Lernziele

        Nach dieser Session können Sie:

        - Textdaten mit SQL-String-Funktionen bereinigen und analysieren
        - Pattern Matching mit LIKE und regulären Ausdrücken anwenden
        - Texte in Wörter zerlegen (Tokenisierung) und Worthäufigkeiten berechnen
        - Aspekt-basierte Analyse: Themen aus Freitext extrahieren

        **Drei Datensätze — steigende Komplexität:**

        | Datensatz | Sprache | Fokus |
        |-----------|---------|-------|
        | Produktbewertungen | Deutsch | String-Grundfunktionen |
        | McDonald's Reviews | Englisch | Aspekt-Analyse & LIKE |
        | UFO Sightings | Englisch | Regex, Tokenisierung, Mining |

        ---
        """
    )
    return


# =============================================================================
# PHASE 1–2: STRING-GRUNDFUNKTIONEN (Produktbewertungen)
# =============================================================================


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ## Phase 1--2: String-Grundfunktionen (Produktbewertungen)

        SQL bietet ein vollständiges **Text-Toolkit** für die Arbeit mit String-Daten:

        | Funktion | Zweck | Beispiel |
        |----------|-------|----------|
        | `LENGTH(text)` | Textlänge in Zeichen | `LENGTH('Hallo')` → 5 |
        | `TRIM(text)` | Leerzeichen am Rand entfernen | `TRIM('  Hi  ')` → `'Hi'` |
        | `REPLACE(text, alt, neu)` | Zeichenketten ersetzen | `REPLACE('ab', 'a', 'x')` → `'xb'` |
        | `LOWER(text)` | Alles kleinschreiben | `LOWER('SQL')` → `'sql'` |

        Wir starten mit 50 deutschen Produktbewertungen und lernen diese Werkzeuge Schritt für Schritt kennen.
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Geführtes Beispiel 13.1: Datenüberblick — Bewertungen pro Kategorie
    """)
    return


@app.cell(hide_code=True)
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
    mo.md(r"""
    ### Geführtes Beispiel 13.2: LENGTH-Profiling — Textlänge nach Kategorie und Sternen

    Wie lang sind die Bewertungstexte? Schreiben zufriedene Kunden mehr oder weniger als unzufriedene?
    """)
    return


@app.cell(hide_code=True)
def _(mo, produktbewertungen):
    _df = mo.sql(
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
    return


@app.cell(hide_code=True)
def _(mo, produktbewertungen):
    _df = mo.sql(
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
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ### Geführtes Beispiel 13.3: TRIM + REPLACE — Whitespace-Probleme finden und bereinigen

        In der Praxis enthalten Textdaten häufig **unsichtbare Fehler**: führende/nachfolgende
        Leerzeichen oder doppelte Leerzeichen mitten im Text. `TRIM` und `REPLACE` helfen beim Aufräumen.
        """
    )
    return


@app.cell(hide_code=True)
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
def _(mo, produktbewertungen):
    _df = mo.sql(
        f"""
        SELECT
            id,
            bewertung_text,
            REPLACE(bewertung_text, '  ', ' ') AS bereinigt
        FROM produktbewertungen
        WHERE bewertung_text LIKE '%  %'
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ### Geführtes Beispiel 13.4: LENGTH-REPLACE Trick — Zeichen zählen

        **Klausur-Pattern:** `LENGTH(text) - LENGTH(REPLACE(text, 'x', ''))` = Anzahl von `'x'`

        Warum funktioniert das? Wenn wir alle `!` durch nichts ersetzen, wird der Text um genau
        so viele Zeichen kürzer, wie `!` vorhanden waren. Die Differenz der Längen ist die Anzahl.

        Wir zählen Ausrufezeichen als **Emotionalitäts-Indikator**.
        """
    )
    return


@app.cell(hide_code=True)
def _(mo, produktbewertungen):
    _df = mo.sql(
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
    return


@app.cell(hide_code=True)
def _(mo, produktbewertungen):
    _df = mo.sql(
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
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ### Geführtes Beispiel 13.5: LOWER-Normalisierung — Case-insensitive Suche

        Texte enthalten Wörter in verschiedenen Schreibweisen: "Qualität", "qualität", "QUALITÄT".
        `LOWER()` normalisiert alles auf Kleinbuchstaben, damit `LIKE` zuverlässig funktioniert.
        """
    )
    return


@app.cell(hide_code=True)
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
    mo.md(r"""
    ### Vorhersage 1: TRIM und Whitespace
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    pred_trim = mo.ui.radio(
        options={
            "4 Zeichen — je 2 Leerzeichen vorne und hinten": "4",
            "2 Zeichen — TRIM entfernt nur am Anfang": "2",
            "0 Zeichen — TRIM entfernt keine Leerzeichen innerhalb des Texts": "0",
            "8 Zeichen — TRIM entfernt auch die Leerzeichen im Wort": "8",
        },
        label="**Vorhersage:** Wie viele Zeichen entfernt `TRIM('  Hallo  ')` im Vergleich zum Original?",
    )
    return (pred_trim,)


@app.cell(hide_code=True)
def _(mo, pred_trim):
    if pred_trim.value == "4":
        _result = (
            mo.md(
                "Richtig! `TRIM` entfernt **führende und nachfolgende** Leerzeichen. "
                "`'  Hallo  '` hat 2 vorne + 2 hinten = 4 entfernte Zeichen. "
                "Das Ergebnis ist `'Hallo'` mit LENGTH 5 statt 9. "
                "**Wichtig:** TRIM entfernt *keine* Leerzeichen innerhalb des Texts!"
            )
        )
    elif pred_trim.value == "2":
        _result = (
            mo.md(
                "Nicht ganz. `TRIM` entfernt Leerzeichen an **beiden** Enden, nicht nur am Anfang. "
                "Für nur den Anfang gäbe es `LTRIM`, für nur das Ende `RTRIM`. "
                "`TRIM('  Hallo  ')` entfernt 2+2 = **4 Zeichen**."
            )
        )
    elif pred_trim.value == "0":
        _result = (
            mo.md(
                "Das stimmt für Leerzeichen *innerhalb* des Texts, aber `TRIM` entfernt sehr wohl "
                "die Leerzeichen am **Rand**. `'  Hallo  '` → `'Hallo'`, also **4 Zeichen** weniger."
            )
        )
    elif pred_trim.value == "8":
        _result = (
            mo.md(
                "Nein, `TRIM` entfernt nur Leerzeichen am **Anfang und Ende**, nicht innerhalb des Worts. "
                "'Hallo' hat keine inneren Leerzeichen. Es werden nur die 2+2 = **4 Zeichen** am Rand entfernt."
            )
        )
    else:
        _result = mo.callout(mo.md("Bitte wählen."), kind="info")
    mo.vstack([pred_trim, _result])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ---

        **Jetzt zum Übungs-Notebook -> Aufgaben 1--5**

        ---
        """
    )
    return


# =============================================================================
# PHASE 3–4: ASPEKT-ANALYSE (McDonald's Reviews)
# =============================================================================


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ## Phase 3--4: Aspekt-Analyse (McDonald's Reviews)

        Jetzt wechseln wir zu 50 englischen McDonald's-Bewertungen. Mit `LIKE` und `CASE WHEN`
        extrahieren wir **Aspekte** (Food, Service, Price, ...) und korrelieren sie mit Ratings.

        ### Das Prinzip: Text -> Features

        Statt den ganzen Text zu analysieren, suchen wir nach **Schlüsselwörtern** für bestimmte Themen.
        `CASE WHEN ... LIKE ...` erzeugt daraus **boolesche Feature-Spalten** (0/1) --
        eine zentrale Technik im Feature Engineering.
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Geführtes Beispiel 13.6: LIKE-Filterung — Food Reviews finden
    """)
    return


@app.cell(hide_code=True)
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
    mo.md(
        r"""
        ### Geführtes Beispiel 13.7: CASE WHEN + LIKE — Feature Engineering

        Wir erzeugen für jede Review boolesche Spalten: Erwähnt sie Food? Service? Speed? Cleanliness? Price?
        """
    )
    return


@app.cell(hide_code=True)
def _(mcdonalds_reviews, mo):
    _df = mo.sql(
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
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ### Geführtes Beispiel 13.8: Aspekt-Rating Korrelation + Visualisierung

        Welche Aspekte haben die höchsten / niedrigsten Durchschnittsbewertungen?
        """
    )
    return


@app.cell(hide_code=True)
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


@app.cell(hide_code=True)
def _(aspekt_analyse, mcdonalds_reviews, px):
    fig_aspekt = px.bar(
        aspekt_analyse,
        x="aspect",
        y="avg_rating",
        text="n",
        title=f"Average Rating by Mentioned Aspect (McDonald's, n={len(mcdonalds_reviews)})",
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
    mo.md(r"""
    ### Vorhersage 2: LIKE vs. REGEXP
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    pred_like_regex = mo.ui.radio(
        options={
            "LIKE eignet sich für 1--2 Muster; bei vielen Alternativen ist REGEXP mit | (Oder) kompakter": "correct",
            "LIKE und REGEXP geben immer das gleiche Ergebnis — persönliche Vorliebe": "equivalent",
            "REGEXP sollte immer verwendet werden, LIKE ist veraltet": "always_regex",
            "LIKE ist immer schneller als REGEXP, deshalb sollte man LIKE bevorzugen": "performance",
        },
        label="**Vorhersage:** Wann ist `regexp_matches(text, 'food|burger|fries')` besser als viele `LIKE`-Bedingungen?",
    )
    return (pred_like_regex,)


@app.cell(hide_code=True)
def _(mo, pred_like_regex):
    if pred_like_regex.value == "correct":
        _result = (
            mo.md(
                "Richtig! Bei 1--2 Mustern ist `LIKE '%food%'` einfacher zu lesen. "
                "Ab 3+ Alternativen wird `regexp_matches(text, 'food|burger|fries')` "
                "deutlich kompakter als viele `OR LIKE`-Klauseln. "
                "Außerdem kann REGEXP komplexere Muster wie `'\\d+\\s*min'` ausdrücken, "
                "die mit LIKE nicht möglich sind."
            )
        )
    elif pred_like_regex.value == "equivalent":
        _result = (
            mo.md(
                "Nicht ganz. LIKE kann nur einfache Wildcards (`%`, `_`), "
                "während REGEXP volle reguläre Ausdrücke unterstützt (`\\d+`, `[a-z]`, `|`). "
                "Bei einfachen Mustern sind sie austauschbar, aber bei **vielen Alternativen** "
                "oder **komplexen Mustern** ist REGEXP klar überlegen."
            )
        )
    elif pred_like_regex.value == "always_regex":
        _result = (
            mo.md(
                "Nicht ganz. LIKE ist nicht veraltet — es ist einfacher und oft lesbarer "
                "für einfache Muster wie `'%food%'`. REGEXP lohnt sich erst bei "
                "**komplexen Mustern** oder **vielen Alternativen** (`'food|burger|fries'`)."
            )
        )
    elif pred_like_regex.value == "performance":
        _result = (
            mo.md(
                "Das stimmt nicht pauschal. In der Praxis sind beide für typische Abfragen "
                "schnell genug. Der Hauptunterschied ist **Ausdruckskraft**: "
                "LIKE kann nur `%` und `_`, REGEXP kann Zeichenklassen, Alternativen und Quantifizierer. "
                "Bei vielen OR-Bedingungen ist ein einzelner REGEXP sogar oft effizienter."
            )
        )
    else:
        _result = mo.callout(mo.md("Bitte wählen."), kind="info")
    mo.vstack([pred_like_regex, _result])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Vorhersage 3: Überlappende CASE WHEN Patterns
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    pred_overlap = mo.ui.radio(
        options={
            "Die Review bekommt food=1 UND service=1 — jede CASE WHEN wird unabhängig ausgewertet": "correct",
            "Nur der erste Treffer zählt — food=1, service=0": "first_only",
            "SQL gibt einen Fehler aus wegen der Mehrdeutigkeit": "error",
            "Es hängt von der Datenbank ab, welcher Aspekt zugewiesen wird": "random",
        },
        label="**Vorhersage:** Eine Review erwähnt 'food' UND 'service'. Was passiert bei unseren CASE WHEN Spalten?",
    )
    return (pred_overlap,)


@app.cell(hide_code=True)
def _(mo, pred_overlap):
    if pred_overlap.value == "correct":
        _result = (
            mo.md(
                "Richtig! Jede `CASE WHEN`-Spalte wird **unabhängig** ausgewertet. "
                "Eine Review die 'The food was great and the service was excellent' enthält, "
                "bekommt `food=1` **und** `service=1`. Das ist genau das, was wir wollen: "
                "Multi-Label Klassifikation! Eine Review kann mehrere Aspekte gleichzeitig ansprechen."
            )
        )
    elif pred_overlap.value == "first_only":
        _result = (
            mo.md(
                "Nicht ganz. Das wäre der Fall bei einem einzelnen `CASE WHEN ... WHEN ... END` "
                "mit mehreren `WHEN`-Zweigen — da gewinnt der erste Treffer. "
                "Aber hier haben wir **separate** `CASE WHEN`-Ausdrücke für jede Spalte, "
                "die **unabhängig** voneinander ausgewertet werden. Beide können 1 sein!"
            )
        )
    elif pred_overlap.value == "error":
        _result = (
            mo.md(
                "Kein Fehler! Mehrere `CASE WHEN`-Spalten sind völlig legal in SQL. "
                "Jede wird **unabhängig** ausgewertet. Die Review bekommt food=1 UND service=1."
            )
        )
    elif pred_overlap.value == "random":
        _result = (
            mo.md(
                "Nein, das Verhalten ist **deterministisch** und in allen SQL-Datenbanken gleich. "
                "Separate `CASE WHEN`-Ausdrücke werden unabhängig voneinander ausgewertet — "
                "die Review bekommt `food=1` **und** `service=1`."
            )
        )
    else:
        _result = mo.callout(mo.md("Bitte wählen."), kind="info")
    mo.vstack([pred_overlap, _result])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ---

        **Jetzt zum Übungs-Notebook -> Aufgaben 6--9**

        ---
        """
    )
    return


# =============================================================================
# PHASE 5: REGEX & TOKENISIERUNG (UFO Sightings)
# =============================================================================


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ## Phase 5: Reguläre Ausdrücke & Tokenisierung (UFO Sightings)

        Jetzt wird es anspruchsvoll: UFO-Augenzeugenberichte mit chaotischen Freitextfeldern.
        Hier reichen einfache `LIKE`-Muster nicht mehr — wir brauchen **reguläre Ausdrücke (Regex)**.

        ### Regex-Grundbausteine in DuckDB

        | Funktion | Zweck | Beispiel |
        |----------|-------|----------|
        | `regexp_matches(text, pattern)` | Prüft ob Pattern vorhanden | `regexp_matches('5 min', '\d+')` → true |
        | `regexp_extract(text, pattern, gruppe)` | Extrahiert Capture Group | `regexp_extract('5 min', '(\d+)', 1)` → `'5'` |
        | `regexp_split_to_array(text, pattern)` | Zerteilt Text an Pattern | `regexp_split_to_array('a b c', '\s+')` → `['a','b','c']` |
        | `UNNEST(array)` | Array-Elemente als Zeilen | Kombiniert mit split für Tokenisierung |

        ### Capture Groups: Das Herzstück

        Runde Klammern `()` in einem Regex definieren **Capture Groups**:

        ```
        Pattern: (\d+)\s*(minutes?|seconds?)
        Text:    "5 minutes"
        Gruppe 0: "5 minutes"   (der gesamte Match)
        Gruppe 1: "5"           (erste Klammer)
        Gruppe 2: "minutes"     (zweite Klammer)
        ```
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ### Geführtes Beispiel 13.9: Regex Capture Groups — Dauer parsen

        Das `duration_text`-Feld ist chaotisch: "5 minutes", "about 30 seconds", "~10 min"...

        Mit **Capture Groups** extrahieren wir Zahl UND Einheit in einem einzigen Pattern:
        """
    )
    return


@app.cell(hide_code=True)
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
    mo.md(
        r"""
        ### Geführtes Beispiel 13.10: Tokenisierung + Top-Wörter

        Wir zerlegen alle UFO-Beschreibungen in einzelne Wörter und zählen die häufigsten.
        `regexp_split_to_array` + `UNNEST` ist das Standard-Pattern dafür:

        ```sql
        UNNEST(regexp_split_to_array(LOWER(TRIM(text)), '\s+')) AS word
        ```

        1. `LOWER(TRIM(...))` — normalisieren
        2. `regexp_split_to_array(..., '\s+')` — an Whitespace splitten → Array
        3. `UNNEST(...)` — Array-Elemente als einzelne Zeilen
        """
    )
    return


@app.cell(hide_code=True)
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


@app.cell(hide_code=True)
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
    mo.md(
        r"""
        Die häufigsten Wörter sind Stoppwörter wie "the", "and", "in" — wenig informativ.
        Mit einer CTE filtern wir diese heraus:

        ### Geführtes Beispiel 13.11: Stoppwort-Filterung
        """
    )
    return


@app.cell(hide_code=True)
def _(mo, ufo_sightings):
    filtered_words = mo.sql(
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
        WHERE LENGTH(word) > 1
          AND word NOT IN (SELECT wort FROM stoppwoerter)
        GROUP BY word
        ORDER BY frequency DESC
        LIMIT 20
        """
    )
    return (filtered_words,)


@app.cell(hide_code=True)
def _(filtered_words, px, ufo_sightings):
    fig_filtered = px.bar(
        filtered_words,
        y="word",
        x="frequency",
        orientation="h",
        title=f"Top 20 Words nach Stoppwort-Filterung (UFO, n={len(ufo_sightings)})",
        labels={"word": "Wort", "frequency": "Häufigkeit"},
        color="frequency",
        color_continuous_scale="Oranges",
    )
    fig_filtered.update_layout(yaxis=dict(autorange="reversed"), height=500)
    fig_filtered


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Vorhersage 4: Capture Group Indexierung
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    pred_capture = mo.ui.radio(
        options={
            "Gruppe 0 = der gesamte Match, Gruppe 1 = erste Klammer, Gruppe 2 = zweite Klammer": "correct",
            "Gruppe 0 = erste Klammer, Gruppe 1 = zweite Klammer": "zero_first",
            "Es gibt kein Gruppe 0 — die Zählung beginnt bei 1": "no_zero",
            "Die Gruppen werden von rechts nach links nummeriert": "reversed",
        },
        label="**Vorhersage:** Bei `regexp_extract(text, '(\\d+)\\s*(min)', N)` — was liefert Gruppe 0?",
    )
    return (pred_capture,)


@app.cell(hide_code=True)
def _(mo, pred_capture):
    if pred_capture.value == "correct":
        _result = (
            mo.md(
                "Richtig! **Gruppe 0** ist immer der **gesamte Match** (alles was das Pattern matcht). "
                "Die nummerierten Gruppen (1, 2, ...) entsprechen den Klammern von links nach rechts. "
                "Bei `'(\\d+)\\s*(min)'` auf `'5 min'`: "
                "Gruppe 0 = `'5 min'`, Gruppe 1 = `'5'`, Gruppe 2 = `'min'`."
            )
        )
    elif pred_capture.value == "zero_first":
        _result = (
            mo.md(
                "Nicht ganz. Die Klammergruppen beginnen bei **1**, nicht bei 0. "
                "Gruppe 0 ist ein Sonderfall: der **gesamte Match**. "
                "Bei `'(\\d+)\\s*(min)'` auf `'5 min'`: "
                "Gruppe 0 = `'5 min'`, Gruppe 1 = `'5'`, Gruppe 2 = `'min'`."
            )
        )
    elif pred_capture.value == "no_zero":
        _result = (
            mo.md(
                "Gruppe 0 existiert! Sie enthält den **gesamten Match** — also alles, "
                "was das komplette Pattern matcht. Die nummerierten Gruppen (1, 2, ...) "
                "enthalten die Teilstücke aus den runden Klammern."
            )
        )
    elif pred_capture.value == "reversed":
        _result = (
            mo.md(
                "Nein, die Nummerierung läuft von **links nach rechts**. "
                "Die erste öffnende Klammer `(` definiert Gruppe 1, die zweite Gruppe 2, usw. "
                "Gruppe 0 ist der **gesamte Match**."
            )
        )
    else:
        _result = mo.callout(mo.md("Bitte wählen."), kind="info")
    mo.vstack([pred_capture, _result])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Vorhersage 5: regexp_split vs. string_split
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    pred_split = mo.ui.radio(
        options={
            "regexp_split trennt an einem Regex-Pattern (z.B. '\\s+' für beliebig viele Leerzeichen), string_split nur an einem festen Trennzeichen": "correct",
            "Beide sind identisch — verschiedene Namen für die gleiche Funktion": "same",
            "string_split ist schneller, regexp_split genauer": "speed",
            "string_split kann alles was regexp_split kann, plus mehr": "string_better",
        },
        label="**Vorhersage:** Was ist der Unterschied zwischen `regexp_split_to_array` und `string_split`?",
    )
    return (pred_split,)


@app.cell(hide_code=True)
def _(mo, pred_split):
    if pred_split.value == "correct":
        _result = (
            mo.md(
                "Richtig! `string_split('a  b', ' ')` trennt an **jedem einzelnen** Leerzeichen "
                "und erzeugt leere Strings dazwischen: `['a', '', 'b']`. "
                "`regexp_split_to_array('a  b', '\\s+')` behandelt **beliebig viele** Leerzeichen "
                "als einen Trenner: `['a', 'b']`. Für Tokenisierung ist `regexp_split` fast immer besser."
            )
        )
    elif pred_split.value == "same":
        _result = (
            mo.md(
                "Nicht ganz. `string_split` nimmt einen **festen String** als Trenner, "
                "`regexp_split_to_array` ein **Regex-Pattern**. "
                "Bei `'a  b'` (2 Leerzeichen): `string_split` erzeugt `['a','','b']` (leerer String!), "
                "während `regexp_split` mit `'\\s+'` korrekt `['a','b']` liefert."
            )
        )
    elif pred_split.value == "speed":
        _result = (
            mo.md(
                "Performance ist hier nicht der Hauptunterschied. Der entscheidende Punkt: "
                "`string_split` trennt an einem **festen Zeichen**, `regexp_split` an einem **Pattern**. "
                "Bei Texten mit unregelmäßigem Whitespace (2+ Leerzeichen, Tabs) "
                "ist `regexp_split` mit `'\\s+'` deutlich robuster."
            )
        )
    elif pred_split.value == "string_better":
        _result = (
            mo.md(
                "Umgekehrt! `regexp_split_to_array` kann alles was `string_split` kann, und mehr: "
                "Es unterstützt **Regex-Patterns** wie `'\\s+'` (beliebig viele Whitespace-Zeichen), "
                "`'[,;]'` (Komma oder Semikolon), etc."
            )
        )
    else:
        _result = mo.callout(mo.md("Bitte wählen."), kind="info")
    mo.vstack([pred_split, _result])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ---

        **Jetzt zum Übungs-Notebook -> Aufgaben 10--11**

        ---
        """
    )
    return


# =============================================================================
# PHASE 6: PROBIEREN SIE SELBST
# =============================================================================


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ## Phase 6: Probieren Sie selbst

        Sie haben jetzt alle Werkzeuge — experimentieren Sie frei mit den drei Datensätzen!

        **Produktbewertungen:** Welche Wörter kommen häufiger in positiven vs. negativen Bewertungen vor?

        **McDonald's:** Welche Filialen (Drive-Thru, Airport, ...) haben die besten/schlechtesten Reviews?

        **UFO Sightings:** Welche Farben werden am häufigsten gemeldet? Gibt es einen July-4th-Spike?
        """
    )
    return


@app.cell
def _(mo, produktbewertungen):
    # Produktbewertungen: Probieren Sie selbst!
    _df = mo.sql(
        f"""
        SELECT *
        FROM produktbewertungen
        LIMIT 5
        """
    )
    return


@app.cell
def _(mcdonalds_reviews, mo):
    # McDonald's Reviews: Probieren Sie selbst!
    _df = mo.sql(
        f"""
        SELECT *
        FROM mcdonalds_reviews
        LIMIT 5
        """
    )
    return


@app.cell
def _(mo, ufo_sightings):
    # UFO Sightings: Probieren Sie selbst!
    _df = mo.sql(
        f"""
        SELECT *
        FROM ufo_sightings
        LIMIT 5
        """
    )
    return


# =============================================================================
# SELBSTTEST
# =============================================================================


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ---

        ## Selbsttest
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    selbsttest_1 = mo.ui.radio(
        options={
            "REPLACE entfernt alle '!', der Text wird kürzer — die Differenz ist die Anzahl der '!'": "correct",
            "Es wäre einfacher, direkt COUNT('!') zu verwenden": "count_func",
            "REPLACE ersetzt nur das erste Vorkommen, deshalb funktioniert es nur für einzelne Zeichen": "only_first",
        },
        label="Wie funktioniert der Trick `LENGTH(t) - LENGTH(REPLACE(t, '!', ''))` zum Zählen?",
    )
    return (selbsttest_1,)


@app.cell(hide_code=True)
def _(mo, selbsttest_1):
    if selbsttest_1.value == "correct":
        _result = (
            mo.md(
                "Richtig! `REPLACE(t, '!', '')` entfernt **alle** Ausrufezeichen aus dem Text. "
                "Wenn der Text 3 Ausrufezeichen hat, wird er um 3 Zeichen kürzer. "
                "`LENGTH(original) - LENGTH(ohne_ausrufezeichen) = 3`. "
                "Dieser Trick funktioniert für **jedes einzelne Zeichen** — man muss nur "
                "den zu zählenden Character in REPLACE einsetzen."
            )
        )
    elif selbsttest_1.value:
        _result = (
            mo.md(
                "Nicht ganz. Es gibt kein `COUNT('!')` in Standard-SQL für Zeichen in einem String. "
                "Der LENGTH-REPLACE Trick ist die Standard-Methode: `REPLACE` entfernt **alle** Vorkommen "
                "des Zeichens, und die Längendifferenz ergibt die Anzahl."
            )
        )
    else:
        _result = mo.callout(mo.md("Bitte wählen."), kind="info")
    mo.vstack([selbsttest_1, _result])
    return


@app.cell(hide_code=True)
def _(mo):
    selbsttest_2 = mo.ui.radio(
        options={
            "Capture Groups extrahieren mehrere Teile in einem Durchlauf — effizienter und konsistenter als separate Aufrufe": "correct",
            "Kein Unterschied — beides liefert das gleiche Ergebnis": "same",
            "Separate regexp_extract-Aufrufe sind besser lesbar und deshalb zu bevorzugen": "separate_better",
        },
        label="Was ist der Vorteil von Capture Groups gegenüber mehreren separaten `regexp_extract`-Aufrufen?",
    )
    return (selbsttest_2,)


@app.cell(hide_code=True)
def _(mo, selbsttest_2):
    if selbsttest_2.value == "correct":
        _result = (
            mo.md(
                "Richtig! Mit `regexp_extract(text, '(\\d+)\\s*(min|sec)', 1)` und "
                "`regexp_extract(text, '(\\d+)\\s*(min|sec)', 2)` nutzen wir dasselbe Pattern "
                "und extrahieren verschiedene Teile. Die Capture Groups stellen sicher, "
                "dass Zahl und Einheit **aus demselben Match** stammen. "
                "Bei separaten Patterns könnte die Zahl aus einem anderen Teil des Texts kommen als die Einheit."
            )
        )
    elif selbsttest_2.value:
        _result = (
            mo.md(
                "Nicht ganz. Capture Groups garantieren, dass alle extrahierten Teile aus "
                "**demselben Match** stammen. Bei separaten Aufrufen mit verschiedenen Patterns "
                "könnten Zahl und Einheit aus verschiedenen Textstellen kommen. "
                "Außerdem ist ein Pattern mit Groups oft lesbarer als mehrere separate Patterns."
            )
        )
    else:
        _result = mo.callout(mo.md("Bitte wählen."), kind="info")
    mo.vstack([selbsttest_2, _result])
    return


@app.cell(hide_code=True)
def _(mo):
    selbsttest_3 = mo.ui.radio(
        options={
            "UNNEST macht aus Array-Elementen einzelne Zeilen — nötig für GROUP BY und COUNT nach der Tokenisierung": "correct",
            "Man kann direkt auf Arrays GROUP BY machen, UNNEST ist optional": "array_direct",
            "UNNEST funktioniert nur mit String-Arrays, nicht mit anderen Typen": "only_strings",
        },
        label="Welche Rolle spielt `UNNEST` bei der Tokenisierung mit `regexp_split_to_array`?",
    )
    return (selbsttest_3,)


@app.cell(hide_code=True)
def _(mo, selbsttest_3):
    if selbsttest_3.value == "correct":
        _result = (
            mo.md(
                "Richtig! `regexp_split_to_array` erzeugt pro Zeile ein **Array** von Wörtern. "
                "Um die Wörter zählen zu können, brauchen wir `UNNEST`: "
                "Es 'entpackt' jedes Array und erzeugt **eine Zeile pro Element**. "
                "Erst dann können wir `GROUP BY word` und `COUNT(*)` verwenden. "
                "Das Pattern: `UNNEST(regexp_split_to_array(LOWER(text), '\\s+')) AS word`"
            )
        )
    elif selbsttest_3.value:
        _result = (
            mo.md(
                "Nicht ganz. `GROUP BY` funktioniert nicht direkt auf Arrays — man muss sie erst "
                "in einzelne Zeilen aufklappen. Genau das macht `UNNEST`: "
                "Aus `['the', 'sky', 'was', 'blue']` werden 4 separate Zeilen. "
                "Dann kann man `GROUP BY word, COUNT(*)` für Worthäufigkeiten verwenden."
            )
        )
    else:
        _result = mo.callout(mo.md("Bitte wählen."), kind="info")
    mo.vstack([selbsttest_3, _result])
    return


# =============================================================================
# ZUSAMMENFASSUNG
# =============================================================================


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ---

        ## Zusammenfassung

        | Konzept | SQL-Befehl | Beispiel |
        |---------|-----------|----------|
        | **LENGTH** | `LENGTH(text)` | Textlänge messen |
        | **TRIM** | `TRIM(text)` | Leerzeichen entfernen |
        | **REPLACE** | `REPLACE(text, a, b)` | Zeichen ersetzen |
        | **LOWER** | `LOWER(text)` | Normalisierung |
        | **LIKE** | `text LIKE '%pattern%'` | Einfache Muster |
        | **CASE WHEN+LIKE** | `CASE WHEN ... LIKE ... THEN 1` | Feature Engineering |
        | **regexp_matches** | `regexp_matches(text, '\d+')` | Pattern vorhanden? |
        | **regexp_extract** | `regexp_extract(text, '(\d+)', 1)` | Capture Group |
        | **Tokenisierung** | `UNNEST(regexp_split_to_array(...))` | Wörter zerlegen |
        | **Zeichen zählen** | `LENGTH(t) - LENGTH(REPLACE(t,'x',''))` | Vorkommen zählen |

        ### Letzte Session! Viel Erfolg bei der Klausur!
        """
    )
    return


if __name__ == "__main__":
    app.run()
