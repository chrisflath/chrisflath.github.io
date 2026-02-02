# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "marimo",
#     "polars",
#     "plotly",
# ]
# ///

import marimo

__generated_with = "0.13.0"
app = marimo.App(
    width="medium",
    app_title="DMA Session 4: CRISP-DM & Fallstudien — Übungen",
)


@app.cell(hide_code=True)
def _():
    import marimo as mo
    return (mo,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        # Session 4: CRISP-DM & Fallstudien — Übungen

        Theorie und geführte Beispiele → **04-crisp-dm-cases-guide.py**

        **Aufgabentypen:**
        - 🟡 **Scaffolded**: Teillösung zum Ergänzen
        - 🔵 **Selbstständig**: Eigene Lösung schreiben
        - 🔴 **Debugging**: Fehler finden und beheben
        - ⭐ **Exploration**: Offene Herausforderungen

        ---
        """
    )
    return


@app.cell
def _():
    import math
    import polars as pl
    import plotly.express as px

    # --- Todesfälle (Shipman-Untersuchung) ---
    try:
        url = "https://chrisflath.github.io/notebooks/public/todesfaelle.csv"
        todesfaelle = pl.read_csv(url)
    except Exception:
        todesfaelle = pl.DataFrame({
            "Arzt": (["Shipman"] * 15 + ["Referenz"] * 10),
            "Geschlecht": [
                "W", "W", "M", "W", "W", "M", "W", "W", "M", "W",
                "W", "M", "W", "W", "W",
                "W", "M", "W", "M", "W", "W", "M", "W", "M", "W",
            ],
            "Alter": [
                76, 82, 71, 79, 84, 68, 91, 77, 73, 88,
                80, 65, 85, 74, 81,
                85, 79, 72, 66, 90, 78, 81, 87, 69, 83,
            ],
            "Todesstunde": [
                14, 15, 13, 14, 16, 15, 14, 13, 15, 14,
                16, 14, 15, 13, 14,
                3, 22, 8, 17, 1, 11, 19, 6, 14, 23,
            ],
        })

    # --- Rechnungsbeträge (Benford-Analyse) ---
    import random
    random.seed(42)

    echte_betraege = [round(10 ** (random.uniform(1, 4)), 2) for _ in range(200)]
    verdächtige_betraege = [
        random.randint(10, 999) + random.random() for _ in range(200)
    ]

    rechnungen_echt = pl.DataFrame({
        "rechnung_id": list(range(1, 201)),
        "betrag": echte_betraege,
        "kategorie": ["echt"] * 200,
    })

    rechnungen_verdächtig = pl.DataFrame({
        "rechnung_id": list(range(201, 401)),
        "betrag": verdächtige_betraege,
        "kategorie": ["verdächtig"] * 200,
    })

    rechnungen = pl.concat([rechnungen_echt, rechnungen_verdächtig])

    return (
        math,
        pl,
        px,
        rechnungen,
        rechnungen_echt,
        rechnungen_verdächtig,
        todesfaelle,
    )


@app.cell(hide_code=True)
def _(mo, todesfaelle, rechnungen_echt, rechnungen_verdächtig):
    mo.md(
        f"""
        **Datensätze geladen:**

        | Datensatz | Zeilen | Beschreibung |
        |-----------|--------|--------------|
        | `todesfaelle` | {len(todesfaelle)} | Mortalitätsdaten aus der Shipman-Untersuchung |
        | `rechnungen_echt` | {len(rechnungen_echt)} | Echte Rechnungsbeträge (exponentiell verteilt) |
        | `rechnungen_verdächtig` | {len(rechnungen_verdächtig)} | Verdächtige Rechnungsbeträge (gleichverteilt) |

        ---
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ## Phase 2: CRISP-DM anwenden
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ### 🟢 Aufgabe 2.1: CRISP-DM Quiz

        Wählen Sie die richtige Reihenfolge der CRISP-DM Phasen:
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    quiz_crisp = mo.ui.radio(
        options={
            "correct": "Business Understanding → Data Understanding → Data Preparation → Modeling → Evaluation → Deployment",
            "wrong1": "Data Understanding → Data Preparation → Business Understanding → Modeling → Evaluation → Deployment",
            "wrong2": "Business Understanding → Modeling → Data Preparation → Evaluation → Data Understanding → Deployment",
            "wrong3": "Data Preparation → Data Understanding → Modeling → Business Understanding → Deployment → Evaluation",
        },
        label="**Quiz:** In welcher Reihenfolge werden die CRISP-DM Phasen typischerweise durchlaufen?",
    )
    quiz_crisp
    return (quiz_crisp,)


@app.cell(hide_code=True)
def _(mo, quiz_crisp):
    if quiz_crisp.value == "correct":
        mo.output.replace(
            mo.md(
                "✅ **Richtig!** CRISP-DM beginnt immer mit dem **Business Understanding** — "
                "erst das Problem verstehen, dann die Daten. In der Praxis ist der Prozess "
                "allerdings iterativ: Man springt oft zwischen Phasen zurück."
            )
        )
    elif quiz_crisp.value:
        mo.output.replace(
            mo.md(
                "❌ Nicht ganz. CRISP-DM beginnt immer mit **Business Understanding** — "
                "man muss zuerst das Problem verstehen, bevor man die Daten analysiert."
            )
        )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ### 🟡 Aufgabe 2.2: Szenario → CRISP-DM Phase zuordnen

        Ordnen Sie jede Aktivität der richtigen CRISP-DM Phase zu.
        Ersetzen Sie die `???` durch den passenden Phasennamen.
        """
    )
    return


@app.cell
def _(mo, todesfaelle):
    _df = mo.sql(
        f"""
        -- Ordnen Sie jede Aktivität der richtigen CRISP-DM Phase zu:
        -- 1. "Wir möchten Betrug bei Rechnungen erkennen" → ???
        -- 2. "Die Daten enthalten fehlende Werte, die wir bereinigen" → ???
        -- 3. "Wir berechnen Statistiken über die Todesfälle" → ???
        -- 4. "Wir prüfen, ob unsere Ergebnisse plausibel sind" → ???
        --
        -- Phasen: Business Understanding, Data Understanding,
        --         Data Preparation, Modeling, Evaluation, Deployment
        SELECT 'Ordnen Sie die Aktivitäten den Phasen zu' AS Aufgabe
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.accordion({"🔑 Musterlösung": mo.md("""
1. "Wir möchten Betrug bei Rechnungen erkennen" → **Business Understanding** (Problemdefinition)
2. "Die Daten enthalten fehlende Werte, die wir bereinigen" → **Data Preparation** (Daten bereinigen)
3. "Wir berechnen Statistiken über die Todesfälle" → **Modeling** (Analyse durchführen)
4. "Wir prüfen, ob unsere Ergebnisse plausibel sind" → **Evaluation** (Ergebnisse prüfen)
""")})
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ### 🔵 Aufgabe 2.3: Analyse-Schritte den Phasen zuordnen

        Stellen Sie sich vor, Sie sollen die Shipman-Daten analysieren.
        Schreiben Sie für **jede** der sechs CRISP-DM Phasen einen konkreten Satz,
        was Sie in dieser Phase tun würden.
        """
    )
    return


@app.cell
def _(mo, todesfaelle):
    _df = mo.sql(
        f"""
        -- 🔵 Beschreiben Sie für jede CRISP-DM Phase einen Schritt
        --    bezogen auf die Shipman-Fallstudie:
        --
        -- Business Understanding: ???
        -- Data Understanding:     ???
        -- Data Preparation:       ???
        -- Modeling:               ???
        -- Evaluation:             ???
        -- Deployment:             ???
        SELECT 'Beschreiben Sie Ihre Analyse-Schritte' AS Aufgabe
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.accordion({"🔑 Musterlösung": mo.md("""
**Beispiel-Antworten:**

| Phase | Konkreter Schritt |
|-------|-------------------|
| Business Understanding | Gibt es Ärzte mit auffällig vielen Todesfällen? |
| Data Understanding | Welche Spalten haben wir? Wie viele Datensätze? Gibt es fehlende Werte? |
| Data Preparation | Todesstunden in Kategorien einteilen (Praxiszeit vs. Außerhalb) |
| Modeling | GROUP BY Arzt mit COUNT, AVG, Zeitanalyse |
| Evaluation | Sind die Unterschiede statistisch signifikant oder Zufall? |
| Deployment | Frühwarnsystem für auffällige Mortalitätsmuster einrichten |
""")})
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ---

        ## Phase 4: Shipman-Daten analysieren
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ### 🟢 Aufgabe 4.1: Todesfälle pro Arzt

        Die einfachste Anomalie: Wer hat die meisten Todesfälle?
        Führen Sie die Abfrage aus und interpretieren Sie das Ergebnis.
        """
    )
    return


@app.cell
def _(mo, todesfaelle):
    _df = mo.sql(
        f"""
        SELECT
            Arzt,
            COUNT(*) AS Anzahl
        FROM todesfaelle
        GROUP BY Arzt
        ORDER BY Anzahl DESC
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ### 🟡 Aufgabe 4.2: Geschlechterverteilung

        Ergänzen Sie die `GROUP BY`-Klausel, um die Geschlechterverteilung
        pro Arzt zu analysieren:
        """
    )
    return


@app.cell
def _(mo, todesfaelle):
    _df = mo.sql(
        f"""
        SELECT
            Arzt,
            Geschlecht,
            COUNT(*) AS Anzahl
        FROM todesfaelle
        GROUP BY ???
        ORDER BY Arzt, Geschlecht
        -- Tipp: Sie brauchen beide Spalten in GROUP BY
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.accordion({"🔑 Musterlösung": mo.md("""
```sql
SELECT
    Arzt,
    Geschlecht,
    COUNT(*) AS Anzahl
FROM todesfaelle
GROUP BY Arzt, Geschlecht
ORDER BY Arzt, Geschlecht
```
""")})
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ### 🔵 Aufgabe 4.3: Durchschnittsalter pro Arzt

        Berechnen Sie das Durchschnittsalter, das Mindestalter und das Höchstalter
        der verstorbenen Patienten — gruppiert nach Arzt.
        """
    )
    return


@app.cell
def _(mo, todesfaelle):
    _df = mo.sql(
        f"""
        -- 🔵 Schreiben Sie Ihre Abfrage:
        -- Tipp: AVG(Alter), MIN(Alter), MAX(Alter) mit GROUP BY Arzt
        SELECT 'Ihre Lösung hier' AS hinweis
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.accordion({"🔑 Musterlösung": mo.md("""
```sql
SELECT
    Arzt,
    ROUND(AVG(Alter), 1) AS Durchschnittsalter,
    MIN(Alter) AS Jüngster,
    MAX(Alter) AS Ältester
FROM todesfaelle
GROUP BY Arzt
ORDER BY Durchschnittsalter DESC
```
""")})
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ### 🔴 Aufgabe 4.4: Debugging — Fehlende GROUP BY Klausel

        Diese Abfrage soll das Durchschnittsalter pro Arzt berechnen.
        **Führen Sie sie aus** — was ist das Problem? Beheben Sie den Fehler.
        """
    )
    return


@app.cell
def _(mo, todesfaelle):
    _df = mo.sql(
        f"""
        -- 🔴 Diese Abfrage hat einen Fehler — finden und beheben Sie ihn!
        SELECT Arzt, AVG(Alter) AS Durchschnittsalter
        FROM todesfaelle
        -- Fehler: Fehlende GROUP BY Klausel
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.accordion({"🔑 Lösung": mo.md("""
**Fehler:** `Arzt` im SELECT ohne `GROUP BY`! SQL weiß nicht, welcher Arzt zum
Durchschnitt gehört.

**Goldene Regel:** Im SELECT nur Spalten aus GROUP BY oder Aggregatfunktionen!

```sql
-- Korrektur:
SELECT Arzt, AVG(Alter) AS Durchschnittsalter
FROM todesfaelle
GROUP BY Arzt
```
""")})
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ---

        ## Phase 6: Benford's Law anwenden
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ### 🟢 Aufgabe 6.1: Erste Ziffer extrahieren

        Um Benford's Law anzuwenden, müssen wir die erste Ziffer jeder Zahl extrahieren.
        Führen Sie die Abfrage aus und verstehen Sie die Technik:
        """
    )
    return


@app.cell
def _(mo, rechnungen):
    _df = mo.sql(
        f"""
        SELECT
            betrag,
            CAST(SUBSTR(CAST(CAST(betrag AS INT) AS TEXT), 1, 1) AS INT)
                AS erste_ziffer
        FROM rechnungen
        WHERE betrag >= 10
        LIMIT 20
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ### 🟡 Aufgabe 6.2: Prozentuale Verteilung

        Berechnen Sie den Prozentanteil jeder ersten Ziffer bei den echten Rechnungen.
        Ergänzen Sie den fehlenden Teil für die Gesamtanzahl:
        """
    )
    return


@app.cell
def _(mo, rechnungen_echt):
    _df = mo.sql(
        f"""
        SELECT
            CAST(SUBSTR(CAST(CAST(betrag AS INT) AS TEXT), 1, 1) AS INT)
                AS erste_ziffer,
            COUNT(*) AS anzahl,
            ROUND(COUNT(*) * 100.0 / ???, 1) AS prozent
        FROM rechnungen_echt
        WHERE betrag >= 10
        GROUP BY erste_ziffer
        ORDER BY erste_ziffer
        -- Tipp: Ersetzen Sie ??? durch eine Unterabfrage,
        --       die die Gesamtanzahl der Rechnungen zählt
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.accordion({"🔑 Musterlösung": mo.md("""
```sql
SELECT
    CAST(SUBSTR(CAST(CAST(betrag AS INT) AS TEXT), 1, 1) AS INT)
        AS erste_ziffer,
    COUNT(*) AS anzahl,
    ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM rechnungen_echt WHERE betrag >= 10), 1) AS prozent
FROM rechnungen_echt
WHERE betrag >= 10
GROUP BY erste_ziffer
ORDER BY erste_ziffer
```
""")})
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ### 🟡 Aufgabe 6.3: Benford-Abweichung berechnen

        Vergleichen Sie die beobachteten Prozente mit den theoretischen Benford-Werten.
        Ergänzen Sie die Berechnung der Abweichung und die Sortierung:
        """
    )
    return


@app.cell
def _(mo, rechnungen_echt):
    _df = mo.sql(
        f"""
        WITH beobachtet AS (
            SELECT
                CAST(SUBSTR(CAST(CAST(betrag AS INT) AS TEXT), 1, 1) AS INT) AS erste_ziffer,
                COUNT(*) * 100.0 / (SELECT COUNT(*) FROM rechnungen_echt WHERE betrag >= 10) AS prozent
            FROM rechnungen_echt
            WHERE betrag >= 10
            GROUP BY erste_ziffer
        ),
        benford AS (
            SELECT 1 AS ziffer, 30.1 AS erwartet UNION ALL
            SELECT 2, 17.6 UNION ALL SELECT 3, 12.5 UNION ALL
            SELECT 4, 9.7 UNION ALL SELECT 5, 7.9 UNION ALL
            SELECT 6, 6.7 UNION ALL SELECT 7, 5.8 UNION ALL
            SELECT 8, 5.1 UNION ALL SELECT 9, 4.6
        )
        SELECT
            b.erste_ziffer,
            ROUND(b.prozent, 1) AS beobachtet_pct,
            e.erwartet AS benford_pct,
            ROUND(???, 1) AS abweichung
        FROM beobachtet b
        JOIN benford e ON b.erste_ziffer = e.ziffer
        ORDER BY ???
        -- Ergänzen Sie: ABS(b.prozent - e.erwartet) für die Abweichung
        -- Sortieren Sie nach abweichung DESC
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.accordion({"🔑 Musterlösung": mo.md("""
```sql
WITH beobachtet AS (
    SELECT
        CAST(SUBSTR(CAST(CAST(betrag AS INT) AS TEXT), 1, 1) AS INT) AS erste_ziffer,
        COUNT(*) * 100.0 / (SELECT COUNT(*) FROM rechnungen_echt WHERE betrag >= 10) AS prozent
    FROM rechnungen_echt
    WHERE betrag >= 10
    GROUP BY erste_ziffer
),
benford AS (
    SELECT 1 AS ziffer, 30.1 AS erwartet UNION ALL
    SELECT 2, 17.6 UNION ALL SELECT 3, 12.5 UNION ALL
    SELECT 4, 9.7 UNION ALL SELECT 5, 7.9 UNION ALL
    SELECT 6, 6.7 UNION ALL SELECT 7, 5.8 UNION ALL
    SELECT 8, 5.1 UNION ALL SELECT 9, 4.6
)
SELECT
    b.erste_ziffer,
    ROUND(b.prozent, 1) AS beobachtet_pct,
    e.erwartet AS benford_pct,
    ROUND(ABS(b.prozent - e.erwartet), 1) AS abweichung
FROM beobachtet b
JOIN benford e ON b.erste_ziffer = e.ziffer
ORDER BY abweichung DESC
```
""")})
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ### 🔵 Aufgabe 6.4: Verdächtige Rechnungen analysieren

        Führen Sie die gleiche Benford-Analyse für die **verdächtigen** Rechnungen durch.
        Berechnen Sie die erste Ziffer, den Prozentanteil und vergleichen Sie
        mit den erwarteten Benford-Werten.
        """
    )
    return


@app.cell
def _(mo, rechnungen_verdächtig):
    _df = mo.sql(
        f"""
        -- 🔵 Schreiben Sie Ihre Abfrage:
        -- Tipp: Wie in Aufgabe 6.3, aber für rechnungen_verdächtig
        SELECT 'Ihre Lösung hier' AS hinweis
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.accordion({"🔑 Musterlösung": mo.md("""
```sql
WITH beobachtet AS (
    SELECT
        CAST(SUBSTR(CAST(CAST(betrag AS INT) AS TEXT), 1, 1) AS INT) AS erste_ziffer,
        COUNT(*) * 100.0 / (SELECT COUNT(*) FROM rechnungen_verdächtig WHERE betrag >= 10) AS prozent
    FROM rechnungen_verdächtig
    WHERE betrag >= 10
    GROUP BY erste_ziffer
),
benford AS (
    SELECT 1 AS ziffer, 30.1 AS erwartet UNION ALL
    SELECT 2, 17.6 UNION ALL SELECT 3, 12.5 UNION ALL
    SELECT 4, 9.7 UNION ALL SELECT 5, 7.9 UNION ALL
    SELECT 6, 6.7 UNION ALL SELECT 7, 5.8 UNION ALL
    SELECT 8, 5.1 UNION ALL SELECT 9, 4.6
)
SELECT
    b.erste_ziffer,
    ROUND(b.prozent, 1) AS beobachtet_pct,
    e.erwartet AS benford_pct,
    ROUND(ABS(b.prozent - e.erwartet), 1) AS abweichung
FROM beobachtet b
JOIN benford e ON b.erste_ziffer = e.ziffer
ORDER BY abweichung DESC
```

**Beobachtung:** Die Abweichungen sind bei den verdächtigen Rechnungen deutlich größer — ein klares Warnsignal für mögliche Manipulation!
""")})
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ### 🔴 Aufgabe 6.5: Debugging — SUBSTR auf numerischen Wert

        Diese Abfrage hat einen Fehler. **Führen Sie sie aus**, finden Sie das Problem
        und korrigieren Sie es.
        """
    )
    return


@app.cell
def _(mo, rechnungen):
    _df = mo.sql(
        f"""
        -- 🔴 Diese Abfrage hat einen Fehler — finden und beheben Sie ihn!
        SELECT
            SUBSTR(betrag, 1, 1) AS erste_ziffer,
            COUNT(*) AS anzahl
        FROM rechnungen
        WHERE betrag >= 10
        GROUP BY erste_ziffer
        ORDER BY erste_ziffer
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.accordion({"🔑 Lösung": mo.md("""
**Fehler:** `betrag` ist numerisch — `SUBSTR` funktioniert nur mit Text!
Außerdem enthält `betrag` Dezimalstellen, die zu falschen ersten Ziffern führen können.

```sql
-- Korrektur:
SELECT
    CAST(SUBSTR(CAST(CAST(betrag AS INT) AS TEXT), 1, 1) AS INT) AS erste_ziffer,
    COUNT(*) AS anzahl
FROM rechnungen
WHERE betrag >= 10
GROUP BY erste_ziffer
ORDER BY erste_ziffer
```

**Erklärung:**
1. `CAST(betrag AS INT)` — Dezimalstellen entfernen
2. `CAST(... AS TEXT)` — In Text umwandeln für SUBSTR
3. `SUBSTR(..., 1, 1)` — Erste Ziffer extrahieren
4. `CAST(... AS INT)` — Zurück in Zahl für korrekte Sortierung
""")})
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ---

        ## Freie Exploration — Herausforderungen
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ### ⭐ Herausforderung 1: Prozentsatz weiblicher Opfer pro Arzt

        Berechnen Sie für jeden Arzt den Anteil weiblicher Opfer in Prozent.

        *Hinweis: Zählen Sie die weiblichen Opfer und teilen Sie durch die Gesamtanzahl pro Arzt.*
        """
    )
    return


@app.cell
def _(mo, todesfaelle):
    _df = mo.sql(
        f"""
        -- ⭐ Prozentsatz weiblicher Opfer pro Arzt
        SELECT 'Ihre Lösung hier' AS hinweis
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.accordion({"🔑 Musterlösung": mo.md("""
```sql
SELECT
    Arzt,
    COUNT(*) AS Gesamt,
    SUM(CASE WHEN Geschlecht = 'W' THEN 1 ELSE 0 END) AS Weiblich,
    ROUND(SUM(CASE WHEN Geschlecht = 'W' THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 1)
        AS Prozent_Weiblich
FROM todesfaelle
GROUP BY Arzt
ORDER BY Prozent_Weiblich DESC
```

**Erklärung:** `CASE WHEN Geschlecht = 'W' THEN 1 ELSE 0 END` erzeugt eine 1 für
jedes weibliche Opfer. `SUM(...)` zählt dann nur die weiblichen Opfer. Division durch
`COUNT(*)` ergibt den Prozentsatz.
""")})
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ### ⭐⭐ Herausforderung 2: Altersverteilung als Histogramm

        Erstellen Sie ein Histogramm der Altersverteilung — getrennt nach Arzt.
        Verwenden Sie Plotly (`px.histogram`).

        *Hinweis: Wandeln Sie die Polars-Tabelle mit `.to_pandas()` um, falls nötig.*
        """
    )
    return


@app.cell
def _(mo, px, todesfaelle):
    # ⭐⭐ Altersverteilung als Histogramm
    # Ihre Lösung hier:
    pass
    return


@app.cell(hide_code=True)
def _(mo):
    mo.accordion({"🔑 Musterlösung": mo.md("""
```python
fig = px.histogram(
    todesfaelle.to_pandas(),
    x="Alter",
    color="Arzt",
    barmode="overlay",
    opacity=0.6,
    nbins=15,
    title="Altersverteilung der Todesfälle nach Arzt",
    labels={"Alter": "Alter bei Tod", "count": "Anzahl", "Arzt": "Arzt"},
)
fig
```

**Beobachtung:** Shipmans Opfer sind tendenziell älter und die Verteilung
ist enger konzentriert — ein typisches Muster gezielter Opferauswahl.
""")})
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ### ⭐⭐⭐ Herausforderung 3: Chi-Quadrat-Abstand zu Benford

        Berechnen Sie den Chi-Quadrat-Abstand zur erwarteten Benford-Verteilung
        für **beide** Datensätze (echt und verdächtig). Die Formel lautet:

        $$\chi^2 = \sum \frac{(beobachtet - erwartet)^2}{erwartet}$$

        Ein höherer Wert bedeutet größere Abweichung von Benford.

        *Hinweis: Verwenden Sie eine CTE mit den Benford-Werten und berechnen Sie die Summe.*
        """
    )
    return


@app.cell
def _(mo, rechnungen):
    _df = mo.sql(
        f"""
        -- ⭐⭐⭐ Chi-Quadrat-Abstand zu Benford für beide Datensätze
        SELECT 'Ihre Lösung hier' AS hinweis
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.accordion({"🔑 Musterlösung": mo.md("""
```sql
WITH ziffern AS (
    SELECT
        kategorie,
        CAST(SUBSTR(CAST(CAST(betrag AS INT) AS TEXT), 1, 1) AS INT) AS erste_ziffer,
        COUNT(*) AS anzahl
    FROM rechnungen
    WHERE betrag >= 10
    GROUP BY kategorie, erste_ziffer
),
gesamt AS (
    SELECT kategorie, SUM(anzahl) AS total
    FROM ziffern
    GROUP BY kategorie
),
benford AS (
    SELECT 1 AS ziffer, 30.1 AS erwartet_pct UNION ALL
    SELECT 2, 17.6 UNION ALL SELECT 3, 12.5 UNION ALL
    SELECT 4, 9.7 UNION ALL SELECT 5, 7.9 UNION ALL
    SELECT 6, 6.7 UNION ALL SELECT 7, 5.8 UNION ALL
    SELECT 8, 5.1 UNION ALL SELECT 9, 4.6
)
SELECT
    z.kategorie,
    ROUND(SUM(
        POWER(z.anzahl - (b.erwartet_pct / 100.0 * g.total), 2)
        / (b.erwartet_pct / 100.0 * g.total)
    ), 2) AS chi_quadrat
FROM ziffern z
JOIN benford b ON z.erste_ziffer = b.ziffer
JOIN gesamt g ON z.kategorie = g.kategorie
GROUP BY z.kategorie
ORDER BY chi_quadrat DESC
```

**Interpretation:** Ein deutlich höherer Chi-Quadrat-Wert bei den verdächtigen Rechnungen
bestätigt, dass diese stärker von der erwarteten Benford-Verteilung abweichen.
""")})
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ---

        ## Zusammenfassung

        | Thema | Wichtige Erkenntnis |
        |-------|---------------------|
        | CRISP-DM | Strukturierter Analyseprozess in 6 iterativen Phasen |
        | Shipman | GROUP BY + COUNT/AVG deckt Anomalien in Mortalitätsdaten auf |
        | Benford | SUBSTR + CAST extrahiert erste Ziffern zur Betrugserkennung |
        | SQL-Werkzeuge | CASE WHEN, Unterabfragen, CTEs für komplexe Analysen |

        **Nächste Session:** Datenmodellierung — Von Anomalien zum ER-Modell
        """
    )
    return


if __name__ == "__main__":
    app.run()
