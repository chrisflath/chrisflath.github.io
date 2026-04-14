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
    app_title="DMA Session 10: Explorative Datenanalyse — Guide",
)


@app.cell(hide_code=True)
def _():
    import marimo as mo
    return (mo,)


@app.cell(hide_code=True)
def _(mo, pl):
    # Gehaltsdaten für EDA-Übungen
    gehaltsdaten = pl.DataFrame({
        "mitarbeiter_id": list(range(1, 101)),
        "name": [f"Mitarbeiter_{i}" for i in range(1, 101)],
        "abteilung": (["IT"] * 25 + ["HR"] * 20 + ["Vertrieb"] * 30 + ["Finanzen"] * 15 + ["Marketing"] * 10),
        "alter": [28, 32, 45, 29, 35, 41, 38, 27, 52, 33,
                  31, 29, 44, 36, 39, 42, 30, 48, 34, 37,
                  26, 55, 31, 40, 35, 28, 33, 46, 30, 38,
                  43, 29, 36, 50, 32, 41, 27, 34, 47, 39,
                  35, 30, 42, 28, 53, 37, 31, 44, 33, 40,
                  29, 36, 48, 32, 38, 45, 27, 41, 34, 51,
                  30, 43, 28, 37, 49, 33, 39, 46, 31, 42,
                  35, 29, 44, 32, 54, 38, 30, 47, 36, 41,
                  28, 50, 33, 40, 26, 43, 31, 45, 34, 39,
                  37, 29, 48, 32, 52, 36, 30, 42, 35, 280],  # Outlier: 280 statt 28
        "gehalt": [52000, 58000, 75000, 48000, 62000, 71000, 65000, 45000, 88000, 55000,
                   53000, 47000, 72000, 59000, 66000, 73000, 51000, 82000, 56000, 63000,
                   44000, 92000, 52000, 68000, 60000, 46000, 54000, 78000, 50000, 64000,
                   74000, 48000, 61000, 85000, 53000, 69000, 43000, 57000, 80000, 65000,
                   58000, 49000, 70000, 45000, 89000, 62000, 51000, 76000, 54000, 67000,
                   47000, 59000, 81000, 52000, 63000, 77000, 44000, 68000, 55000, 86000,
                   50000, 73000, 46000, 61000, 83000, 53000, 66000, 79000, 51000, 71000,
                   57000, 48000, 75000, 52000, 91000, 64000, 49000, 80000, 60000, 69000,
                   45000, 84000, 54000, 67000, 42000, 72000, 50000, 78000, 56000, 65000,
                   62000, 47000, 82000, 53000, 88000, 59000, 49000, 74000, 58000, 450000],  # Outlier: CEO
        "erfahrung_jahre": [3, 7, 20, 4, 10, 16, 13, 2, 27, 8,
                           6, 4, 19, 11, 14, 17, 5, 23, 9, 12,
                           1, 30, 6, 15, 10, 3, 8, 21, 5, 13,
                           18, 4, 11, 25, 7, 16, 2, 9, 22, 14,
                           10, 5, 17, 3, 28, 12, 6, 19, 8, 15,
                           4, 11, 23, 7, 13, 20, 2, 16, 9, 26,
                           5, 18, 3, 12, 24, 8, 14, 21, 6, 17,
                           10, 4, 19, 7, 29, 13, 5, 22, 11, 16,
                           3, 25, 8, 15, 1, 18, 6, 20, 9, 14,
                           12, 4, 23, 7, 27, 11, 5, 19, 10, 35],
        "geschlecht": (["M", "W"] * 50),
        "standort": (["München"] * 40 + ["Berlin"] * 35 + ["Hamburg"] * 25),
    })

    # Einige NULL-Werte einfügen
    gehaltsdaten = gehaltsdaten.with_columns([
        pl.when(pl.col("mitarbeiter_id").is_in([15, 42, 73, 88]))
        .then(None)
        .otherwise(pl.col("erfahrung_jahre"))
        .alias("erfahrung_jahre")
    ])

    return (gehaltsdaten,)


@app.cell(hide_code=True)
def _():
    import polars as pl
    import plotly.express as px
    return pl, px


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        # Session 10: Explorative Datenanalyse (EDA) — Guide

        **Kursfahrplan:** I: SQL-Grundlagen (S1–4) · II: Datenmodellierung (S5–7) · III: Fortgeschrittenes SQL (S8–9) · **▸ IV: Datenanalyse (S10–13)**

        ### Lernziele

        Nach dieser Session können Sie:

        - **EDA systematisch** durchführen: Inspektion → Univariat → Ausreißer → Missing Values → Bivariat
        - **Lagemaße und Streuungsmaße** mit SQL berechnen (AVG, MEDIAN, STDDEV, IQR)
        - **Ausreißer** mit der IQR-Regel identifizieren
        - **Fehlende Werte** aufspüren und deren Muster analysieren
        - **Korrelationen und Gruppenvergleiche** durchführen
        - **CASE WHEN** für Binning und Kategorisierung nutzen

        **Datensatz:** Fiktive Gehaltsdaten (100 Mitarbeiter, inkl. Ausreißer und Missing Values)

        ---
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ## Phase 1: Erste Dateninspektion

        Bevor wir analysieren, müssen wir die Daten **kennenlernen**. Eine systematische EDA beginnt immer mit:

        1. **Wie viele Datensätze?** → `COUNT(*)`
        2. **Welche Spalten und Datentypen?** → Schema prüfen
        3. **Erste Zeilen ansehen** → `LIMIT 10`
        4. **Grundlegende Statistiken** → `AVG`, `MIN`, `MAX`

        Das Ziel: Ein **Gefühl** für die Daten entwickeln, bevor wir tiefere Analysen starten.
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Geführtes Beispiel 10.1: Datenüberblick — Wie groß ist unser Datensatz?
    """)
    return


@app.cell(hide_code=True)
def _(gehaltsdaten, mo):
    _df = mo.sql(
        f"""
        SELECT
            COUNT(*) AS anzahl_zeilen
        FROM gehaltsdaten
        """
    )
    return


@app.cell(hide_code=True)
def _(gehaltsdaten):
    # Spalteninfo mit Polars
    gehaltsdaten.schema
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Geführtes Beispiel 10.2: Erste Zeilen ansehen

    Schauen Sie sich die ersten Datensätze an, um ein Gefühl für die Daten zu bekommen:
    """)
    return


@app.cell(hide_code=True)
def _(gehaltsdaten, mo):
    _df = mo.sql(
        f"""
        SELECT * FROM gehaltsdaten LIMIT 10
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        **Beobachtung:** Wir haben 100 Mitarbeiter mit 8 Spalten — numerisch (`alter`, `gehalt`, `erfahrung_jahre`) und kategorisch (`abteilung`, `geschlecht`, `standort`).

        ---

        **Jetzt zum Übungs-Notebook → Aufgaben 1.x**

        ---

        ## Phase 2: Univariate Analyse

        Jede Variable **einzeln** betrachten: Zentrum, Streuung, Verteilung.

        | Maß | SQL | Beschreibung |
        |-----|-----|--------------|
        | Mittelwert | `AVG(x)` | Arithmetisches Mittel — empfindlich gegen Ausreißer |
        | Median | `PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY x)` | Mittlerer Wert — robust gegen Ausreißer |
        | Standardabweichung | `STDDEV(x)` | Durchschnittliche Abweichung vom Mittelwert |
        | Min/Max | `MIN(x)`, `MAX(x)` | Extremwerte |
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Geführtes Beispiel 10.3: Deskriptive Statistiken für Gehalt
    """)
    return


@app.cell(hide_code=True)
def _(gehaltsdaten, mo):
    _df = mo.sql(
        f"""
        SELECT
            COUNT(*) AS n,
            ROUND(AVG(gehalt), 2) AS mittelwert,
            PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY gehalt) AS median,
            MIN(gehalt) AS minimum,
            MAX(gehalt) AS maximum,
            ROUND(STDDEV(gehalt), 2) AS std_abweichung
        FROM gehaltsdaten
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        **Beobachtung:** Der Mittelwert ist deutlich höher als der Median! Das deutet auf **Ausreißer nach oben** hin (das Maximum von 450.000 zieht den Mittelwert hoch).

        ---

        ### Vorhersage 1: Mean vs. Median
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    pred_mean_median = mo.ui.radio(
        options={
            "Rechtsschief — wenige hohe Werte ziehen den Mean nach oben": "rechtsschief",
            "Linksschief — wenige niedrige Werte ziehen den Mean nach unten": "linksschief",
            "Symmetrische Verteilung — Mean und Median sind immer ungefähr gleich": "symmetrisch",
            "Kein Zusammenhang — Mean > Median sagt nichts über die Verteilung": "kein_zusammenhang",
        },
        label="**Vorhersage:** Der Mittelwert ist deutlich höher als der Median. Was sagt uns das über die Verteilung?",
    )
    return (pred_mean_median,)


@app.cell(hide_code=True)
def _(mo, pred_mean_median):
    if pred_mean_median.value == "rechtsschief":
        _result = (
            mo.md(
                "✅ **Richtig!** Mean > Median deutet auf eine **rechtsschiefe** (positiv schiefe) Verteilung hin. "
                "Wenige sehr hohe Werte (hier: das CEO-Gehalt von 450.000 €) ziehen den Mittelwert nach oben, "
                "während der Median als 'mittlerer Wert' davon unbeeindruckt bleibt. "
                "Deshalb ist der Median oft das bessere Lagemaß bei schiefen Verteilungen."
            )
        )
    elif pred_mean_median.value == "linksschief":
        _result = (
            mo.md(
                "❌ Bei einer linksschiefen Verteilung wäre der Mean *niedriger* als der Median "
                "(wenige sehr niedrige Werte ziehen den Mean nach unten). "
                "Hier ist es umgekehrt: Mean > Median → **rechtsschief** — hohe Ausreißer ziehen den Mean nach oben."
            )
        )
    elif pred_mean_median.value == "symmetrisch":
        _result = (
            mo.md(
                "❌ Bei einer symmetrischen Verteilung wären Mean und Median tatsächlich ungefähr gleich. "
                "Aber hier liegt der Mean deutlich *über* dem Median — das zeigt, dass die Verteilung "
                "**rechtsschief** ist: wenige hohe Werte ziehen den Mittelwert hoch."
            )
        )
    elif pred_mean_median.value == "kein_zusammenhang":
        _result = (
            mo.md(
                "❌ Es gibt einen klaren Zusammenhang! Die Beziehung zwischen Mean und Median "
                "zeigt die **Schiefe** der Verteilung an: Mean > Median → rechtsschief, "
                "Mean < Median → linksschief, Mean ≈ Median → annähernd symmetrisch."
            )
        )
    else:
        _result = mo.callout(mo.md("Bitte wählen."), kind="info")
    mo.vstack([pred_mean_median, _result])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Geführtes Beispiel 10.4: Quartile und IQR

    Die Quartile teilen die Daten in vier gleich große Teile. Der **IQR** (Interquartile Range) ist der Abstand zwischen Q3 und Q1:
    """)
    return


@app.cell(hide_code=True)
def _(gehaltsdaten, mo):
    _df = mo.sql(
        f"""
        SELECT
            PERCENTILE_CONT(0.25) WITHIN GROUP (ORDER BY gehalt) AS q1,
            PERCENTILE_CONT(0.50) WITHIN GROUP (ORDER BY gehalt) AS median,
            PERCENTILE_CONT(0.75) WITHIN GROUP (ORDER BY gehalt) AS q3,
            PERCENTILE_CONT(0.75) WITHIN GROUP (ORDER BY gehalt)
                - PERCENTILE_CONT(0.25) WITHIN GROUP (ORDER BY gehalt) AS iqr
        FROM gehaltsdaten
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Visualisierung: Gehaltsverteilung
    """)
    return


@app.cell(hide_code=True)
def _(gehaltsdaten, px):
    fig_hist = px.histogram(
        gehaltsdaten,
        x="gehalt",
        nbins=30,
        title="Verteilung der Gehälter",
        labels={"gehalt": "Gehalt (EUR)", "count": "Anzahl"}
    )
    fig_hist.update_layout(showlegend=False)
    fig_hist


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        **Beobachtung:** Ein extremer Ausreißer ist deutlich sichtbar (450.000 € — CEO-Gehalt?). Die Masse der Daten liegt zwischen 40.000 und 95.000 €.

        ---

        **Jetzt zum Übungs-Notebook → Aufgaben 2.x**

        ---

        ## Phase 3: Ausreißer erkennen

        Die **IQR-Regel** definiert Ausreißer als Werte außerhalb der "Zäune":

        - **Untere Grenze:** Q1 − 1.5 × IQR
        - **Obere Grenze:** Q3 + 1.5 × IQR

        Der Faktor **1.5** ist eine Konvention. Bei normalverteilten Daten liegen ca. 99.3% der Werte innerhalb dieser Grenzen.
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Geführtes Beispiel 10.5: Ausreißer mit IQR-Regel finden (Gehalt)
    """)
    return


@app.cell(hide_code=True)
def _(gehaltsdaten, mo):
    _df = mo.sql(
        f"""
        WITH quartile AS (
            SELECT
                PERCENTILE_CONT(0.25) WITHIN GROUP (ORDER BY gehalt) AS q1,
                PERCENTILE_CONT(0.75) WITHIN GROUP (ORDER BY gehalt) AS q3
            FROM gehaltsdaten
        ),
        grenzen AS (
            SELECT
                q1 - 1.5 * (q3 - q1) AS untere_grenze,
                q3 + 1.5 * (q3 - q1) AS obere_grenze
            FROM quartile
        )
        SELECT g.mitarbeiter_id, g.name, g.abteilung, g.gehalt,
               gr.untere_grenze, gr.obere_grenze
        FROM gehaltsdaten g, grenzen gr
        WHERE g.gehalt < gr.untere_grenze
           OR g.gehalt > gr.obere_grenze
        ORDER BY g.gehalt DESC
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        **Beobachtung:** Ein Gehalt von 450.000 € — offensichtlich kein typischer Mitarbeiter. In einer echten Analyse würden wir prüfen: Ist das ein CEO? Ein Datenfehler? Oder eine eigene Kategorie?

        ---

        ### Vorhersage 2: IQR-Faktor
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    pred_iqr = mo.ui.radio(
        options={
            "Mehr Ausreißer — der strengere Faktor markiert mehr Werte als auffällig": "strenger",
            "Weniger Ausreißer — ein größerer Faktor bedeutet weniger extreme Werte": "weniger",
            "Gleich viele — der Faktor hat keinen Einfluss auf die Anzahl": "gleich",
            "3× findet mehr Ausreißer, weil 3 > 1.5": "drei_weiter",
        },
        label="**Vorhersage:** Was passiert, wenn wir den IQR-Faktor von 1.5 auf 3.0 erhöhen?",
    )
    return (pred_iqr,)


@app.cell(hide_code=True)
def _(mo, pred_iqr):
    if pred_iqr.value == "weniger":
        _result = (
            mo.md(
                "✅ **Richtig!** Ein größerer Faktor (3.0 statt 1.5) macht die Grenzen **weiter**. "
                "Die obere Grenze liegt dann bei Q3 + 3.0 × IQR statt Q3 + 1.5 × IQR. "
                "Dadurch werden weniger Werte als Ausreißer markiert — nur die wirklich **extremen**. "
                "1.5× = 'milde Ausreißer', 3.0× = 'extreme Ausreißer'."
            )
        )
    elif pred_iqr.value == "strenger":
        _result = (
            mo.md(
                "❌ Ein größerer Faktor ist *weniger* streng, nicht strenger. "
                "3.0 × IQR ergibt **weitere** Grenzen als 1.5 × IQR. "
                "Dadurch fallen weniger Werte aus dem Bereich heraus → weniger Ausreißer werden erkannt."
            )
        )
    elif pred_iqr.value == "gleich":
        _result = (
            mo.md(
                "❌ Der Faktor hat sehr wohl Einfluss! Ein größerer Faktor verschiebt die Grenzen "
                "nach außen, sodass weniger Werte als Ausreißer gelten. "
                "1.5× ist die Standardwahl, 3.0× findet nur die extremsten Ausreißer."
            )
        )
    elif pred_iqr.value == "drei_weiter":
        _result = (
            mo.md(
                "❌ Hier muss man aufpassen: Ein größerer Faktor macht die Grenzen *weiter*, "
                "nicht enger. Q3 + 3.0 × IQR > Q3 + 1.5 × IQR. "
                "Also werden *weniger* Werte als Ausreißer erkannt, nur die extremsten."
            )
        )
    else:
        _result = mo.callout(mo.md("Bitte wählen."), kind="info")
    mo.vstack([pred_iqr, _result])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Geführtes Beispiel 10.6: Ausreißer im Alter — Datenfehler erkennen
    """)
    return


@app.cell(hide_code=True)
def _(gehaltsdaten, mo):
    _df = mo.sql(
        f"""
        WITH quartile AS (
            SELECT
                PERCENTILE_CONT(0.25) WITHIN GROUP (ORDER BY alter) AS q1,
                PERCENTILE_CONT(0.75) WITHIN GROUP (ORDER BY alter) AS q3
            FROM gehaltsdaten
        ),
        grenzen AS (
            SELECT
                q1 - 1.5 * (q3 - q1) AS untere_grenze,
                q3 + 1.5 * (q3 - q1) AS obere_grenze
            FROM quartile
        )
        SELECT g.mitarbeiter_id, g.name, g.alter, g.abteilung,
               gr.untere_grenze, gr.obere_grenze
        FROM gehaltsdaten g, grenzen gr
        WHERE g.alter < gr.untere_grenze
           OR g.alter > gr.obere_grenze
        ORDER BY g.alter DESC
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        **Beobachtung:** Ein Mitarbeiter hat Alter **280** — offensichtlich ein **Datenfehler** (vermutlich 28 gemeint). Im Gegensatz zum CEO-Gehalt (das plausibel sein könnte) ist das hier eindeutig ein Tippfehler.

        **Wichtige Unterscheidung:**
        - **CEO-Gehalt (450k):** Möglicherweise real → separat behandeln oder ausschließen
        - **Alter 280:** Definitiv ein Fehler → korrigieren (zu 28) oder als NULL markieren

        ---

        **Jetzt zum Übungs-Notebook → Aufgaben 3.x**

        ---

        ## Phase 4: Fehlende Werte

        NULL-Werte sind in der Praxis allgegenwärtig. Die erste Frage ist immer: **Wie viele fehlen, und gibt es ein Muster?**
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Geführtes Beispiel 10.7: Fehlende Werte zählen
    """)
    return


@app.cell(hide_code=True)
def _(gehaltsdaten, mo):
    _df = mo.sql(
        f"""
        SELECT
            COUNT(*) AS total,
            COUNT(erfahrung_jahre) AS vorhanden,
            COUNT(*) - COUNT(erfahrung_jahre) AS fehlend,
            ROUND((COUNT(*) - COUNT(erfahrung_jahre)) * 100.0 / COUNT(*), 1) AS prozent_fehlend
        FROM gehaltsdaten
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        **Beobachtung:** 4 von 100 Erfahrungswerten fehlen (4%). Ist das zufällig, oder gibt es ein Muster?

        ---

        ### Vorhersage 3: NULL-Strategie
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    pred_null = mo.ui.radio(
        options={
            "Erst das Muster analysieren — sind die NULLs zufällig oder systematisch?": "muster_analysieren",
            "Zeilen mit NULLs sofort löschen — sie verfälschen die Analyse": "sofort_loeschen",
            "NULLs durch 0 ersetzen — dann funktioniert jede Berechnung": "nullen_ersetzen",
            "NULLs durch den Mittelwert ersetzen — das ist immer die beste Lösung": "mittelwert",
        },
        label="**Vorhersage:** 4 von 100 Erfahrungswerten fehlen. Was sollte der erste Schritt sein?",
    )
    return (pred_null,)


@app.cell(hide_code=True)
def _(mo, pred_null):
    if pred_null.value == "muster_analysieren":
        _result = (
            mo.md(
                "✅ **Richtig!** Der erste Schritt ist immer: **Muster analysieren**. "
                "Fehlen die Werte zufällig (MCAR)? Oder hängen sie von anderen Variablen ab — "
                "z.B. fehlt die Erfahrung häufiger bei jüngeren Mitarbeitern (MAR)? "
                "Die richtige Strategie hängt vom Muster ab. Blindes Löschen oder Ersetzen kann "
                "die Analyse verzerren."
            )
        )
    elif pred_null.value == "sofort_loeschen":
        _result = (
            mo.md(
                "❌ Sofort löschen ist riskant! Wenn die NULLs nicht zufällig sind "
                "(z.B. fehlen bevorzugt bei bestimmten Abteilungen), dann verzerrt das Löschen "
                "die verbleibenden Daten. Erst das **Muster analysieren**, dann entscheiden."
            )
        )
    elif pred_null.value == "nullen_ersetzen":
        _result = (
            mo.md(
                "❌ NULLs durch 0 ersetzen wäre hier falsch! 0 Jahre Erfahrung ist ein *gültiger Wert* "
                "(Berufseinsteiger). Durch die Ersetzung würden wir den Durchschnitt verfälschen "
                "und falsche Korrelationen erzeugen. Erst das **Muster analysieren**."
            )
        )
    elif pred_null.value == "mittelwert":
        _result = (
            mo.md(
                "❌ Mittelwert-Imputation kann sinnvoll sein, aber erst nachdem wir das **Muster** "
                "verstanden haben. Wenn die NULLs systematisch auftreten (z.B. nur bei bestimmten "
                "Abteilungen), dann ist der Gesamtmittelwert möglicherweise nicht repräsentativ. "
                "Erst analysieren, dann imputieren."
            )
        )
    else:
        _result = mo.callout(mo.md("Bitte wählen."), kind="info")
    mo.vstack([pred_null, _result])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Geführtes Beispiel 10.8: NULL-Muster nach Abteilung

    Hängen die fehlenden Werte von der Abteilung ab?
    """)
    return


@app.cell(hide_code=True)
def _(gehaltsdaten, mo):
    _df = mo.sql(
        f"""
        SELECT
            abteilung,
            COUNT(*) AS total,
            COUNT(erfahrung_jahre) AS vorhanden,
            COUNT(*) - COUNT(erfahrung_jahre) AS fehlend
        FROM gehaltsdaten
        GROUP BY abteilung
        ORDER BY fehlend DESC
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        **Beobachtung:** Die fehlenden Werte verteilen sich auf verschiedene Abteilungen — kein offensichtliches Muster. Bei nur 4 fehlenden Werten (4%) können wir diese Zeilen für die Erfahrungs-Analyse ausschließen, ohne die Ergebnisse wesentlich zu verzerren.

        ---

        **Jetzt zum Übungs-Notebook → Aufgaben 4.x**

        ---

        ## Phase 5: Bivariate Analyse

        Zusammenhänge zwischen **zwei Variablen** untersuchen:
        - **Numerisch × Numerisch:** Korrelation (`CORR(x, y)`)
        - **Numerisch × Kategorisch:** Gruppenvergleich (`GROUP BY`)
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Geführtes Beispiel 10.9: Korrelation Alter–Gehalt
    """)
    return


@app.cell(hide_code=True)
def _(gehaltsdaten, mo):
    _df = mo.sql(
        f"""
        SELECT
            ROUND(CORR(alter, gehalt), 3) AS korrelation_alter_gehalt,
            ROUND(CORR(erfahrung_jahre, gehalt), 3) AS korrelation_erfahrung_gehalt
        FROM gehaltsdaten
        WHERE alter < 100  -- Ausreißer ausschließen
        """
    )
    return


@app.cell(hide_code=True)
def _(gehaltsdaten, px):
    # Daten ohne extreme Ausreißer für bessere Visualisierung
    clean_data = gehaltsdaten.filter(
        (gehaltsdaten["gehalt"] < 200000) & (gehaltsdaten["alter"] < 100)
    )

    fig_scatter = px.scatter(
        clean_data,
        x="erfahrung_jahre",
        y="gehalt",
        color="abteilung",
        title="Gehalt vs. Erfahrung (ohne extreme Ausreißer)",
        labels={"erfahrung_jahre": "Erfahrung (Jahre)", "gehalt": "Gehalt (EUR)"},
        trendline="ols"
    )
    fig_scatter


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Geführtes Beispiel 10.10: Gruppenvergleich nach Abteilung
    """)
    return


@app.cell(hide_code=True)
def _(gehaltsdaten, mo):
    _df = mo.sql(
        f"""
        SELECT
            abteilung,
            COUNT(*) AS n,
            ROUND(AVG(gehalt), 0) AS mittel_gehalt,
            ROUND(PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY gehalt), 0) AS median_gehalt,
            MIN(gehalt) AS min_gehalt,
            MAX(gehalt) AS max_gehalt
        FROM gehaltsdaten
        WHERE gehalt < 200000  -- Ausreißer ausschließen
        GROUP BY abteilung
        ORDER BY mittel_gehalt DESC
        """
    )
    return


@app.cell(hide_code=True)
def _(gehaltsdaten, px):
    clean_box = gehaltsdaten.filter(
        (gehaltsdaten["gehalt"] < 200000) & (gehaltsdaten["alter"] < 100)
    )

    fig_box = px.box(
        clean_box,
        x="abteilung",
        y="gehalt",
        title="Gehaltsverteilung nach Abteilung",
        labels={"abteilung": "Abteilung", "gehalt": "Gehalt (EUR)"}
    )
    fig_box


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ---

        ### Vorhersage 4: GROUP BY vs. Window Functions
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    pred_window = mo.ui.radio(
        options={
            "GROUP BY reduziert Zeilen (eine pro Gruppe), Window Functions behalten alle Zeilen": "correct",
            "Window Functions reduzieren Zeilen, GROUP BY behält alle Zeilen": "reversed",
            "GROUP BY ist schneller, Window Functions sind langsamer — sonst gleich": "speed",
            "GROUP BY braucht SELECT, Window Functions brauchen nur OVER()": "syntax",
        },
        label="**Vorhersage:** Was ist der Hauptunterschied zwischen GROUP BY und Window Functions?"
    )
    return (pred_window,)


@app.cell(hide_code=True)
def _(mo, pred_window):
    if pred_window.value == "correct":
        _result = (
            mo.md(
                "✅ **Richtig!** GROUP BY fasst viele Zeilen zu einer zusammen "
                "(z.B. eine Zeile pro Abteilung). Window Functions berechnen Aggregate, "
                "aber **jede Originalzeile bleibt erhalten** — Sie bekommen die Aggregation "
                "*neben* den Originaldaten."
            )
        )
    elif pred_window.value == "reversed":
        _result = (
            mo.md(
                "❌ Genau umgekehrt! GROUP BY *komprimiert* Zeilen (viele → eine pro Gruppe). "
                "Window Functions mit OVER() berechnen dasselbe, aber **behalten alle Originalzeilen** bei."
            )
        )
    elif pred_window.value == "speed":
        _result = (
            mo.md(
                "❌ Die Geschwindigkeit hängt von der konkreten Abfrage und dem Optimierer ab. "
                "Der entscheidende Unterschied: GROUP BY *komprimiert* Zeilen, "
                "Window Functions **behalten alle Zeilen** bei."
            )
        )
    elif pred_window.value == "syntax":
        _result = (
            mo.md(
                "❌ Beide brauchen SELECT. Der wahre Unterschied: GROUP BY reduziert die Zeilenzahl "
                "(eine pro Gruppe), Window Functions **behalten alle Zeilen** bei und berechnen "
                "das Aggregat *neben* den Originaldaten."
            )
        )
    else:
        _result = mo.callout(mo.md("Bitte wählen."), kind="info")
    mo.vstack([pred_window, _result])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Probieren Sie selbst: Bivariate Analyse

    Experimentieren Sie! Probieren Sie:
    - Korrelation nach Abteilung getrennt berechnen
    - Gehaltsverteilung nach Geschlecht vergleichen
    - `GROUP BY standort, geschlecht` für differenziertere Analyse
    """)
    return


@app.cell
def _(gehaltsdaten, mo):
    _df = mo.sql(
        f"""
        SELECT
            standort,
            geschlecht,
            COUNT(*) AS anzahl,
            ROUND(AVG(gehalt), 0) AS durchschnitt_gehalt
        FROM gehaltsdaten
        WHERE gehalt < 200000
        GROUP BY standort, geschlecht
        ORDER BY standort, geschlecht
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ---

        **Jetzt zum Übungs-Notebook → Aufgaben 5.x**

        ---

        ## Phase 6: SQL für EDA — Binning mit CASE WHEN

        **Binning** = numerische Werte in Kategorien einteilen. Beispiel: Gehälter in Klassen gruppieren.

        ```sql
        CASE
            WHEN gehalt < 50000 THEN '1: unter 50k'
            WHEN gehalt < 65000 THEN '2: 50-65k'
            ...
        END AS gehaltsklasse
        ```

        **Wichtig:** Die WHEN-Bedingungen werden **von oben nach unten** geprüft. Die erste zutreffende Bedingung "gewinnt".
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Geführtes Beispiel 10.11: Gehaltsklassen erstellen
    """)
    return


@app.cell(hide_code=True)
def _(gehaltsdaten, mo):
    _df = mo.sql(
        f"""
        SELECT
            CASE
                WHEN gehalt < 50000 THEN '1: unter 50k'
                WHEN gehalt < 65000 THEN '2: 50-65k'
                WHEN gehalt < 80000 THEN '3: 65-80k'
                WHEN gehalt < 100000 THEN '4: 80-100k'
                ELSE '5: über 100k'
            END AS gehaltsklasse,
            COUNT(*) AS anzahl,
            ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM gehaltsdaten), 1) AS prozent
        FROM gehaltsdaten
        GROUP BY gehaltsklasse
        ORDER BY gehaltsklasse
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        **Beobachtung:** Die meisten Mitarbeiter (über 75%) verdienen zwischen 42.000 und 80.000 €. Die Klasse "über 100k" enthält nur den CEO-Ausreißer.

        ---

        **Jetzt zum Übungs-Notebook → Aufgaben 6.x**

        ---

        ## Phase 7: Datasaurus Dozen — Warum Visualisierung unverzichtbar ist

        **Anscombe's Quartet** (1973) zeigte: 4 Datensätze mit identischen Statistiken, aber völlig verschiedenen Mustern.

        Das **Datasaurus Dozen** (2017) treibt das auf die Spitze: **13 Datensätze** mit nahezu identischen Statistiken — darunter ein Dinosaurier!

        Alle 13 Datensätze haben:
        - Gleichen Mittelwert (x ≈ 54.3, y ≈ 47.8)
        - Gleiche Standardabweichung (x ≈ 16.8, y ≈ 26.9)
        - Gleiche Korrelation (r ≈ −0.06)
        """
    )
    return


@app.cell(hide_code=True)
def _(pl):
    # Datasaurus Dozen laden
    try:
        datasaurus = pl.read_csv(
            "https://raw.githubusercontent.com/jumpingrivers/datasauRus/main/inst/extdata/DatasaurusDozen-long.csv"
        )
        ds_quelle = "Live-Daten (GitHub)"
    except Exception:
        # Minimaler Fallback: leerer Hinweis
        datasaurus = pl.DataFrame({"dataset": ["?"], "x": [0.0], "y": [0.0]})
        ds_quelle = "Fehler beim Laden — bitte Internetverbindung prüfen"

    return datasaurus, ds_quelle


@app.cell(hide_code=True)
def _(datasaurus, mo):
    _df = mo.sql(
        f"""
        SELECT
            dataset,
            ROUND(AVG(x), 2) AS mean_x,
            ROUND(AVG(y), 2) AS mean_y,
            ROUND(STDDEV(x), 2) AS std_x,
            ROUND(STDDEV(y), 2) AS std_y,
            ROUND(CORR(x, y), 3) AS korrelation,
            COUNT(*) AS n
        FROM datasaurus
        GROUP BY dataset
        ORDER BY dataset
        """
    )
    return


@app.cell(hide_code=True)
def _(datasaurus, px):
    px.scatter(
        datasaurus,
        x="x",
        y="y",
        facet_col="dataset",
        facet_col_wrap=4,
        width=900,
        height=900,
        title="Datasaurus Dozen — Gleiche Statistiken, völlig verschiedene Muster",
    )


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        **Goldene Regel der EDA:** Immer visualisieren! Deskriptive Statistiken allein können täuschen.

        ---

        ## Selbsttest
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    selbsttest_1 = mo.ui.radio(
        options={
            "Median — er ist robust gegen Ausreißer (Extremwerte verändern ihn kaum)": "robust",
            "Mittelwert — er nutzt alle Datenpunkte und ist deshalb genauer": "mean",
            "Modus — der häufigste Wert ist immer am aussagekräftigsten": "mode",
        },
        label="Warum ist der Median bei schiefen Verteilungen oft besser als der Mittelwert?",
    )
    return (selbsttest_1,)


@app.cell(hide_code=True)
def _(mo, selbsttest_1):
    if selbsttest_1.value == "robust":
        _result = (
            mo.md(
                "✅ **Richtig!** Der Median ist der Wert, der die Daten in zwei Hälften teilt. "
                "Ein einzelner Extremwert (z.B. CEO-Gehalt) verändert den Median kaum, "
                "kann aber den Mittelwert stark verschieben. "
                "Merkhilfe: Der Median fragt 'Was ist der typische Wert?', "
                "der Mittelwert 'Was ist das gewichtete Mittel?'."
            )
        )
    elif selbsttest_1.value == "mean":
        _result = (
            mo.md(
                "❌ 'Alle Datenpunkte nutzen' klingt gut, ist aber genau das Problem: "
                "Ein einziger Ausreißer (z.B. 450.000 €) zieht den Mittelwert stark nach oben. "
                "Der Median ignoriert Extremwerte und zeigt den **typischen** Wert."
            )
        )
    elif selbsttest_1.value == "mode":
        _result = (
            mo.md(
                "❌ Der Modus (häufigster Wert) ist bei stetigen Daten oft nicht sinnvoll "
                "(z.B. hat jedes Gehalt eine andere Höhe). Der Median ist bei schiefen "
                "Verteilungen das bessere Lagemaß, weil er robust gegen Ausreißer ist."
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
            "IQR — basiert auf Quartilen und ist robust gegen Ausreißer in den Rändern": "iqr_robust",
            "Histogramm — nur die Grafik zeigt die wahre Verteilung": "histogram",
            "Beide ergänzen sich — IQR für die Breite, Histogramm für die Form": "beide",
        },
        label="Was sagt die IQR über eine Verteilung aus, was ein Histogramm nicht zeigt?",
    )
    return (selbsttest_2,)


@app.cell(hide_code=True)
def _(mo, selbsttest_2):
    if selbsttest_2.value == "beide":
        _result = (
            mo.md(
                "✅ **Richtig!** IQR und Histogramm ergänzen sich perfekt. "
                "Der IQR gibt eine **robuste numerische Zusammenfassung** der Streuung "
                "(wo liegen die mittleren 50%?), während das Histogramm die **Form** zeigt "
                "(multimodal? schief? Lücken?). Beides zusammen ergibt das beste Bild."
            )
        )
    elif selbsttest_2.value == "iqr_robust":
        _result = (
            mo.md(
                "Teilweise richtig — IQR ist tatsächlich robust. Aber er zeigt nur die Breite der "
                "mittleren 50%, nicht die Form der Verteilung. Ein Histogramm kann z.B. bimodale "
                "Verteilungen oder Lücken zeigen, die der IQR verbirgt. Am besten: **beide nutzen**."
            )
        )
    elif selbsttest_2.value == "histogram":
        _result = (
            mo.md(
                "Teilweise richtig — Histogramme zeigen die Form. Aber der IQR liefert eine "
                "**kompakte, numerische Zusammenfassung**, die sich leicht vergleichen lässt. "
                "Am besten: **beide nutzen** — IQR für die Breite, Histogramm für die Form."
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
            "GROUP BY komprimiert (eine Zeile pro Gruppe), Window Functions behalten alle Zeilen": "window_keeps",
            "Kein Unterschied — beide berechnen Aggregate über Gruppen": "same",
            "Window Functions sind schneller als GROUP BY": "window_faster",
        },
        label="Was ist der Kernunterschied zwischen GROUP BY und Window Functions?",
    )
    return (selbsttest_3,)


@app.cell(hide_code=True)
def _(mo, selbsttest_3):
    if selbsttest_3.value == "window_keeps":
        _result = (
            mo.md(
                "✅ **Richtig!** Das ist der entscheidende Unterschied: "
                "GROUP BY reduziert viele Zeilen auf eine pro Gruppe. "
                "Window Functions (mit OVER()) berechnen das gleiche Aggregat, aber "
                "**jede Originalzeile bleibt erhalten** — das Aggregat steht daneben. "
                "Beispiel: Gehalt + Abteilungsdurchschnitt in derselben Zeile."
            )
        )
    elif selbsttest_3.value == "same":
        _result = (
            mo.md(
                "❌ Es gibt einen wichtigen Unterschied: GROUP BY **komprimiert** die Zeilen "
                "(eine pro Gruppe). Window Functions berechnen das Aggregat, aber "
                "**behalten alle Originalzeilen** — Sie sehen den Einzelwert neben dem Aggregat."
            )
        )
    elif selbsttest_3.value == "window_faster":
        _result = (
            mo.md(
                "❌ Geschwindigkeit ist nicht der Kernunterschied. GROUP BY **komprimiert** "
                "Zeilen, Window Functions **behalten alle Zeilen**. Das ist der entscheidende Punkt: "
                "Window Functions zeigen den Einzelwert *neben* dem Aggregat."
            )
        )
    else:
        _result = mo.callout(mo.md("Bitte wählen."), kind="info")
    mo.vstack([selbsttest_3, _result])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ---

        ## Zusammenfassung

        | Konzept | SQL-Befehl | Beispiel |
        |---------|-----------|----------|
        | **Lagemaße** | `AVG()`, `PERCENTILE_CONT(0.5)` | Mittelwert vs. Median |
        | **Streuung** | `STDDEV()`, `MAX()-MIN()`, IQR | Variabilität der Daten |
        | **Ausreißer (IQR)** | `Q1 - 1.5*IQR`, `Q3 + 1.5*IQR` | Gehalt > obere Grenze |
        | **Fehlende Werte** | `COUNT(*) - COUNT(spalte)` | 4 fehlende Erfahrungswerte |
        | **Korrelation** | `CORR(x, y)` | Erfahrung ↔ Gehalt |
        | **Gruppenvergleich** | `GROUP BY abteilung` + `AVG()` | Ø Gehalt pro Abteilung |
        | **Binning** | `CASE WHEN ... THEN ...` | Gehaltsklassen erstellen |

        ### EDA-Checkliste

        ```
        1. Inspektion     → COUNT, Schema, LIMIT 10
        2. Univariat      → AVG, Median, STDDEV, Histogramm
        3. Ausreißer      → IQR-Regel, Boxplot
        4. Missing Values → COUNT NULL, Muster prüfen
        5. Bivariat       → CORR, GROUP BY, Scatterplot
        6. Binning        → CASE WHEN Kategorien
        7. Visualisieren! → Datasaurus Dozen: Statistiken täuschen
        ```

        ### Ausblick Session 11: Statistische Inferenz & A/B-Tests

        In der nächsten Session gehen wir von der Beschreibung zur **Schlussfolgerung**: Wie können wir aus Stichproben auf die Grundgesamtheit schließen?
        """
    )
    return


if __name__ == "__main__":
    app.run()
