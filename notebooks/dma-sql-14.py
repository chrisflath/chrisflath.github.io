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
    base = mo.notebook_location() / "public"

    produktbewertungen = pl.read_csv(str(base / "produktbewertungen.csv"))
    mcdonalds_reviews = pl.read_csv(str(base / "mcdonalds_reviews.csv"))
    ufo_sightings = pl.read_csv(str(base / "ufo_sightings.csv"))

    mo.md(
        f"""
        **Geladen:** {len(produktbewertungen)} Produktbewertungen,
        {len(mcdonalds_reviews)} McDonald's Reviews,
        {len(ufo_sightings)} UFO Sightings
        """
    )
    return base, mcdonalds_reviews, produktbewertungen, ufo_sightings


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

        ### Aufgabe 14.12: Stoppwort-Filterung (UFO)

        Die häufigsten Wörter sind "the", "a", "was" — wenig informativ. Filtern Sie Stoppwörter heraus.

        *Hinweis: `WHERE word NOT IN ('the', 'a', 'an', 'i', 'in', 'of', 'and', 'to', 'was', 'it', 'is', 'that', 'at', 'my', 'for', 'on', 'with', 'had', 'as', 'were', 'from', 'by', 'or', 'be', 'but', 'not', 'this', 'then', 'we', 'no', 'me', 'so', 'very', 'about')`*
        """
    )
    return


@app.cell
def _(mo, ufo_sightings):
    # Ihre Lösung: Wörter ohne Stoppwörter, Top 30
    mo.sql(
        f"""
        SELECT 'Filtern Sie die Stoppwörter heraus — was sind die häufigsten inhaltlichen Wörter?' AS hinweis
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
        """
    )
    return


@app.cell
def _(mcdonalds_reviews, mo):
    # Ihre Lösung: Wörter nach Rating
    mo.sql(
        f"""
        SELECT 'Vergleichen Sie positive vs. negative Wörter' AS hinweis
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
        """
    )
    return


@app.cell
def _(mcdonalds_reviews, mo):
    # Ihre Lösung: Sentiment-Score
    mo.sql(
        f"""
        SELECT 'Berechnen Sie den Sentiment-Score und vergleichen Sie mit dem Rating' AS hinweis
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
