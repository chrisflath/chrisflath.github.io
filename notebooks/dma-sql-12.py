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
app = marimo.App(width="medium", app_title="DMA Session 12: Statistische Inferenz & A/B-Tests")


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        # Vorlesung 12: Statistische Inferenz & A/B-Tests

        **Kursfahrplan:** I: SQL-Grundlagen (S1–4) · II: Datenmodellierung (S5–8) · III: Fortgeschrittenes SQL (S9–10) · **▸ IV: Datenanalyse (S11–14)**

        In Session 11 haben wir Daten explorativ untersucht — Verteilungen, Ausreißer, Korrelationen. Heute gehen wir einen Schritt weiter: Wie können wir aus Stichproben auf die Grundgesamtheit schließen?

        **Lernziele:**
        - Hypothesentests durchführen und A/B-Test-Ergebnisse interpretieren
        - p-Wert und Signifikanzniveau verstehen
        - t-Test für Mittelwertvergleiche mit SQL berechnen
        - Simpson's Paradox erkennen und vermeiden

        **Datensatz:** Simulierter A/B-Test eines Online-Checkout-Prozesses (4.000 Nutzer)
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
    # A/B-Test Daten laden
    try:
        csv_path = mo.notebook_location() / "public" / "ab_test_checkout.csv"
        ab_test = pl.read_csv(str(csv_path))
        daten_quelle = "Simulierter A/B-Test: Checkout-Optimierung (4.000 Nutzer)"
    except Exception:
        ab_test = pl.DataFrame({
            "user_id": list(range(1, 11)),
            "gruppe": ["Control"] * 5 + ["Treatment"] * 5,
            "geraet": ["Desktop", "Mobile", "Desktop", "Mobile", "Desktop"] * 2,
            "konvertiert": [1, 0, 1, 0, 1, 1, 1, 0, 1, 0],
            "umsatz": [45.0, 0.0, 62.0, 0.0, 38.0, 55.0, 48.0, 0.0, 71.0, 0.0],
        })
        daten_quelle = "Offline-Daten (Fallback)"
        mo.callout(mo.md("**Hinweis:** CSV konnte nicht geladen werden. Es werden Beispieldaten verwendet."), kind="warn")
    return daten_quelle, ab_test


@app.cell(hide_code=True)
def _(daten_quelle, mo):
    mo.md(
        f"""
        **Datenquelle:** {daten_quelle}

        ---

        ## Phase 1: Deskriptive Statistik

        Bevor wir statistische Tests durchführen, müssen wir unsere Daten erst **verstehen**.
        Unser Datensatz enthält 4.000 Nutzer eines Online-Shops, die zufällig einer von zwei
        Checkout-Varianten zugewiesen wurden:

        - **Control:** Bestehende Checkout-Seite
        - **Treatment:** Neue, optimierte Checkout-Seite

        Spalten: `user_id`, `gruppe` (Control/Treatment), `geraet` (Desktop/Mobile),
        `konvertiert` (0/1), `umsatz` (€, 0 wenn nicht konvertiert)
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        > **Vorhersage:** Der A/B-Test hat 4.000 Nutzer, gleichmäßig auf Control und Treatment verteilt. Typische Checkout-Conversion-Rates liegen bei 3–5%. Wenn Treatment besser ist — um wie viel Prozentpunkte erwarten Sie den Unterschied?

        ### Aufgabe 12.1: Datenüberblick

        Wie viele Nutzer sind in jeder Gruppe? Wie viele haben konvertiert?
        Berechne die **Conversion Rate** pro Gruppe.
        """
    )
    return


@app.cell
def _(ab_test, mo):
    mo.sql(
        f"""
        SELECT
            gruppe,
            COUNT(*) AS n,
            SUM(konvertiert) AS conversions,
            ROUND(AVG(konvertiert) * 100, 1) AS conv_rate_pct
        FROM ab_test
        GROUP BY gruppe
        ORDER BY gruppe
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ### Aufgabe 12.2: Statistische Kennzahlen

        Berechne für jede Gruppe den **Mittelwert**, die **Standardabweichung**
        und den **Standardfehler** des Umsatzes (nur für konvertierte Nutzer).
        """
    )
    return


@app.cell
def _(ab_test, mo):
    mo.sql(
        f"""
        SELECT
            gruppe,
            COUNT(*) AS n,
            ROUND(AVG(umsatz), 2) AS mittelwert,
            ROUND(STDDEV(umsatz), 2) AS standardabw,
            ROUND(STDDEV(umsatz) / SQRT(COUNT(*)), 2) AS standardfehler,
            ROUND(MIN(umsatz), 2) AS min_umsatz,
            ROUND(MAX(umsatz), 2) AS max_umsatz
        FROM ab_test
        WHERE konvertiert = 1
        GROUP BY gruppe
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ### Aufgabe 12.3: Umsatzverteilung visualisieren

        Erstelle ein Histogramm der Umsätze, getrennt nach Gruppe (nur konvertierte Nutzer).
        """
    )
    return


@app.cell
def _(ab_test, mo):
    _data = mo.sql(
        f"""
        SELECT gruppe, umsatz
        FROM ab_test
        WHERE konvertiert = 1
        """
    )
    return (_data,)


@app.cell
def _(_data, px):
    px.histogram(
        _data.to_pandas(),
        x="umsatz",
        color="gruppe",
        barmode="overlay",
        opacity=0.6,
        nbins=40,
        title="Umsatzverteilung nach Gruppe (nur Konverter)",
        labels={"umsatz": "Umsatz (€)", "gruppe": "Gruppe", "count": "Anzahl"},
        color_discrete_map={"Control": "#004B8D", "Treatment": "#E87722"},
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ---

        ## Phase 2: z-Scores und Ausreißer

        Der **z-Score** standardisiert Werte: Wie viele Standardabweichungen liegt ein
        Wert vom Mittelwert entfernt?

        $$z = \frac{x - \bar{x}}{s}$$

        | |z| | Interpretation |
        |-----|----------------|
        | < 1 | Normal (68% der Daten) |
        | < 2 | Üblich (95% der Daten) |
        | > 2 | Auffällig |
        | > 3 | Sehr ungewöhnlich |
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ### Aufgabe 12.4: z-Scores berechnen

        Berechne den z-Score des Umsatzes für jeden konvertierten Nutzer.
        Finde die **Top 5 Ausreißer** (höchster |z-Score|).
        """
    )
    return


@app.cell
def _(ab_test, mo):
    mo.sql(
        f"""
        SELECT
            user_id,
            gruppe,
            geraet,
            umsatz,
            ROUND(
                (umsatz - AVG(umsatz) OVER())
                / STDDEV(umsatz) OVER(),
            2) AS z_score
        FROM ab_test
        WHERE konvertiert = 1
        ORDER BY ABS(
            (umsatz - AVG(umsatz) OVER())
            / STDDEV(umsatz) OVER()
        ) DESC
        LIMIT 5
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ### Aufgabe 12.5: Selbstständig — z-Score-Verteilung

        Wie viele konvertierte Nutzer haben einen |z-Score| > 2?
        Zähle pro Gruppe.

        *Hinweis: Wie Aufgabe 12.4, aber mit SUM(CASE WHEN ABS(z_score) > 2 ...) statt ORDER BY*
        """
    )
    return


@app.cell
def _(ab_test, mo):
    mo.sql(
        f"""
        -- Ihre Lösung hier
        -- Tipp: CTE mit z_scores wie in 12.4, dann GROUP BY gruppe
        -- SUM(CASE WHEN ABS(z_score) > 2 THEN 1 ELSE 0 END) AS n_ausreisser
        -- Erwartete Spalten: gruppe, n_total, n_ausreisser, pct_ausreisser
        SELECT 'Schreiben Sie Ihre Abfrage hier' AS hinweis
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ### Aufgabe 12.6: z-Score-Visualisierung

        Erstelle ein Histogramm der z-Scores mit Markierungslinien bei z = -2 und z = +2.
        """
    )
    return


@app.cell
def _(ab_test, mo):
    _z_data = mo.sql(
        f"""
        SELECT
            user_id,
            gruppe,
            umsatz,
            ROUND(
                (umsatz - AVG(umsatz) OVER())
                / STDDEV(umsatz) OVER(),
            2) AS z_score
        FROM ab_test
        WHERE konvertiert = 1
        """
    )
    return (_z_data,)


@app.cell
def _(_z_data, px):
    fig = px.histogram(
        _z_data.to_pandas(),
        x="z_score",
        color="gruppe",
        barmode="overlay",
        opacity=0.6,
        nbins=40,
        title="z-Score-Verteilung der Umsätze",
        labels={"z_score": "z-Score", "gruppe": "Gruppe", "count": "Anzahl"},
        color_discrete_map={"Control": "#004B8D", "Treatment": "#E87722"},
    )
    fig.add_vline(x=-2, line_dash="dash", line_color="red", annotation_text="z = -2")
    fig.add_vline(x=2, line_dash="dash", line_color="red", annotation_text="z = +2")
    fig
    return (fig,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ---

        ## Phase 3: Hypothesentests

        Jetzt wenden wir statistische Tests an, um zu prüfen, ob die beobachteten
        Unterschiede **statistisch signifikant** sind.

        **Hypothesen für den Umsatzvergleich:**
        - $H_0$: Der mittlere Umsatz ist in beiden Gruppen gleich ($\mu_C = \mu_T$)
        - $H_1$: Der mittlere Umsatz unterscheidet sich ($\mu_C \neq \mu_T$)

        **t-Test Formel (Welch):**

        $$t = \frac{\bar{x}_1 - \bar{x}_2}{\sqrt{\frac{s_1^2}{n_1} + \frac{s_2^2}{n_2}}}$$

        Daumenregel: |t| > 2 → signifikant auf 5%-Niveau (bei großen Stichproben)
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ### Aufgabe 12.7: t-Test für Umsatz (Konverter)

        Berechne die t-Statistik für den Umsatzvergleich zwischen Control und Treatment
        (nur konvertierte Nutzer). Ist der Unterschied signifikant?
        """
    )
    return


@app.cell
def _(ab_test, mo):
    mo.sql(
        f"""
        WITH stats AS (
            SELECT
                gruppe,
                COUNT(*) AS n,
                AVG(umsatz) AS mittel,
                STDDEV(umsatz) AS std
            FROM ab_test
            WHERE konvertiert = 1
            GROUP BY gruppe
        )
        SELECT
            ROUND(c.mittel, 2) AS mittel_control,
            ROUND(t.mittel, 2) AS mittel_treatment,
            ROUND(c.mittel - t.mittel, 2) AS differenz,
            ROUND(SQRT(POWER(c.std, 2) / c.n + POWER(t.std, 2) / t.n), 4) AS standardfehler,
            ROUND(
                ABS(c.mittel - t.mittel)
                / SQRT(POWER(c.std, 2) / c.n + POWER(t.std, 2) / t.n),
            2) AS t_statistik,
            CASE
                WHEN ABS(c.mittel - t.mittel)
                     / SQRT(POWER(c.std, 2) / c.n + POWER(t.std, 2) / t.n) > 1.96
                THEN 'Signifikant (p < 0.05)'
                ELSE 'Nicht signifikant'
            END AS ergebnis
        FROM stats c, stats t
        WHERE c.gruppe = 'Control'
          AND t.gruppe = 'Treatment'
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    quiz_pvalue = mo.ui.radio(
        options={
            "correct": "Statistisch signifikant — wir lehnen H₀ ab, weil p < α",
            "accept": "Wir akzeptieren H₁ als wahr — der Effekt ist bewiesen",
            "nonsig": "Nicht signifikant — 0.03 ist zu klein für eine Aussage",
            "repeat": "Wir müssen den Test wiederholen, da p nicht genau 0.05 ist",
        },
        label="**Quiz:** Was bedeutet ein p-Wert von 0.03 bei einem Signifikanzniveau α = 0.05?"
    )
    quiz_pvalue
    return (quiz_pvalue,)


@app.cell(hide_code=True)
def _(quiz_pvalue, mo):
    if quiz_pvalue.value == "correct":
        mo.output.replace(mo.md("Richtig! Da p = 0.03 < α = 0.05, lehnen wir die Nullhypothese ab. Das bedeutet: Die beobachteten Daten sind unter H₀ so unwahrscheinlich, dass wir einen echten Effekt annehmen. Achtung: Das *beweist* H₁ nicht — es macht sie nur wahrscheinlicher."))
    elif quiz_pvalue.value:
        mo.output.replace(mo.md("Nicht ganz. p = 0.03 bedeutet: *Wenn H₀ wahr wäre*, würden wir so extreme Daten nur in 3% der Fälle sehen. Da 3% < 5% (unser α), lehnen wir H₀ ab und sprechen von einem **statistisch signifikanten** Ergebnis."))
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ### Aufgabe 12.8: Effektgröße (Cohen's d)

        Berechne Cohen's d für den Umsatzunterschied.

        $$d = \frac{\bar{x}_1 - \bar{x}_2}{s_{\text{pooled}}}$$

        wobei $s_{\text{pooled}} = \sqrt{\frac{(n_1-1) \cdot s_1^2 + (n_2-1) \cdot s_2^2}{n_1 + n_2 - 2}}$

        | |d| | Interpretation |
        |-----|----------------|
        | < 0.2 | Vernachlässigbar |
        | 0.2 – 0.5 | Klein |
        | 0.5 – 0.8 | Mittel |
        | > 0.8 | Groß |
        """
    )
    return


@app.cell
def _(ab_test, mo):
    mo.sql(
        f"""
        WITH stats AS (
            SELECT
                gruppe,
                COUNT(*) AS n,
                AVG(umsatz) AS mittel,
                STDDEV(umsatz) AS std
            FROM ab_test
            WHERE konvertiert = 1
            GROUP BY gruppe
        )
        SELECT
            ROUND(c.mittel - t.mittel, 2) AS differenz,
            ROUND(
                SQRT(
                    ((c.n - 1) * POWER(c.std, 2) + (t.n - 1) * POWER(t.std, 2))
                    / (c.n + t.n - 2)
                ), 2
            ) AS s_pooled,
            ROUND(
                ABS(c.mittel - t.mittel)
                / SQRT(
                    ((c.n - 1) * POWER(c.std, 2) + (t.n - 1) * POWER(t.std, 2))
                    / (c.n + t.n - 2)
                ), 3
            ) AS cohens_d,
            CASE
                WHEN ABS(c.mittel - t.mittel)
                     / SQRT(((c.n-1)*POWER(c.std,2) + (t.n-1)*POWER(t.std,2)) / (c.n+t.n-2)) < 0.2
                THEN 'Vernachlässigbar'
                WHEN ABS(c.mittel - t.mittel)
                     / SQRT(((c.n-1)*POWER(c.std,2) + (t.n-1)*POWER(t.std,2)) / (c.n+t.n-2)) < 0.5
                THEN 'Klein'
                WHEN ABS(c.mittel - t.mittel)
                     / SQRT(((c.n-1)*POWER(c.std,2) + (t.n-1)*POWER(t.std,2)) / (c.n+t.n-2)) < 0.8
                THEN 'Mittel'
                ELSE 'Groß'
            END AS interpretation
        FROM stats c, stats t
        WHERE c.gruppe = 'Control'
          AND t.gruppe = 'Treatment'
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ---

        ## Phase 4: A/B-Test-Auswertung

        Jetzt analysieren wir den A/B-Test **systematisch** — genau wie in der Praxis.
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ### Aufgabe 12.9: Selbstständig — Conversion Rate mit Konfidenzintervall

        Berechne die Conversion Rate pro Gruppe mit einem **95%-Konfidenzintervall**.

        Für Proportionen: $CI = p \pm 1.96 \cdot \sqrt{\frac{p(1-p)}{n}}$

        *Hinweis: Wenden Sie die Formel direkt in SQL an — AVG(konvertiert) ist p, COUNT(*) ist n*
        """
    )
    return


@app.cell
def _(ab_test, mo):
    mo.sql(
        f"""
        -- Ergänzen Sie die fehlenden Berechnungen (???)
        SELECT
            gruppe,
            COUNT(*) AS n,
            ROUND(AVG(konvertiert) * 100, 1) AS conv_rate_pct,
            -- CI-Untergrenze: (p - 1.96 * sqrt(p*(1-p)/n)) * 100
            ROUND(
                (AVG(konvertiert) - 1.96 * SQRT(??? * (1 - ???) / COUNT(*))) * 100,
            1) AS ci_lower_pct,
            -- CI-Obergrenze: (p + 1.96 * sqrt(p*(1-p)/n)) * 100
            ROUND(
                (AVG(konvertiert) + 1.96 * SQRT(??? * (1 - ???) / COUNT(*))) * 100,
            1) AS ci_upper_pct
        FROM ab_test
        GROUP BY gruppe
        ORDER BY gruppe
        -- Tipp: Ersetzen Sie jedes ??? durch AVG(konvertiert)
        -- Erwartete Ausgabe: 2 Zeilen (control, treatment), 5 Spalten
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ### Aufgabe 12.10: Umsatz pro Nutzer (alle Nutzer)

        Vergleiche den **durchschnittlichen Umsatz pro Nutzer** (inkl. Nicht-Konverter mit 0€).
        Dies ist oft die wichtigere Metrik als die Conversion Rate allein.
        """
    )
    return


@app.cell
def _(ab_test, mo):
    mo.sql(
        f"""
        SELECT
            gruppe,
            COUNT(*) AS n,
            ROUND(AVG(umsatz), 2) AS avg_umsatz_alle,
            ROUND(STDDEV(umsatz), 2) AS std_umsatz,
            ROUND(SUM(umsatz), 2) AS total_umsatz
        FROM ab_test
        GROUP BY gruppe
        ORDER BY gruppe
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ---

        ## Phase 5: Simpson's Paradox aufdecken

        Bisher sieht es so aus, als wäre **Control besser**. Aber stimmt das wirklich?
        Schauen wir uns die Daten **segmentiert** an.
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ### Aufgabe 12.11: Selbstständig — Segmentierung nach Gerät

        Berechne die Conversion Rate **getrennt nach Gerätetyp** (Desktop vs. Mobile).
        Was fällt auf?

        *Hinweis: GROUP BY geraet, gruppe — gleiche Aggregation wie 12.1, nur feiner segmentiert*
        """
    )
    return


@app.cell
def _(ab_test, mo):
    mo.sql(
        f"""
        -- Ihre Lösung hier
        -- Tipp: GROUP BY geraet, gruppe statt nur GROUP BY gruppe
        -- Gleiche Aggregation: COUNT(*), SUM(konvertiert), AVG(konvertiert)
        -- Erwartete Spalten: geraet, gruppe, n, conversions, conv_rate_pct
        SELECT 'Schreiben Sie Ihre Abfrage hier' AS hinweis
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        **Simpson's Paradox!** Treatment ist in **beiden** Segmenten besser,
        aber im Gesamtergebnis schlechter. Warum?

        Der Grund: Die Gruppen sind **nicht gleich zusammengesetzt**.
        Treatment hat mehr Mobile-Nutzer, und Mobile-Nutzer konvertieren generell weniger.
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ### Aufgabe 12.12: Gruppenkomposition analysieren

        Zeige die **Geräteverteilung** pro Gruppe. Das erklärt den Paradox.
        """
    )
    return


@app.cell
def _(ab_test, mo):
    mo.sql(
        f"""
        SELECT
            gruppe,
            geraet,
            COUNT(*) AS n,
            ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER(PARTITION BY gruppe), 1) AS anteil_pct
        FROM ab_test
        GROUP BY gruppe, geraet
        ORDER BY gruppe, geraet
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        Die Treatment-Gruppe hat **60% Mobile-Nutzer** vs. nur **30% bei Control**.
        Da Mobile-Nutzer generell weniger konvertieren, zieht das den Gesamtdurchschnitt
        der Treatment-Gruppe nach unten — obwohl Treatment **innerhalb jedes Segments** besser ist.
        """
    )
    return


@app.cell
def _(ab_test, mo):
    _comp = mo.sql(
        f"""
        SELECT
            gruppe,
            geraet,
            COUNT(*) AS n,
            ROUND(AVG(konvertiert) * 100, 1) AS conv_rate_pct
        FROM ab_test
        GROUP BY gruppe, geraet
        ORDER BY geraet, gruppe
        """
    )
    return (_comp,)


@app.cell
def _(_comp, px):
    fig = px.bar(
        _comp.to_pandas(),
        x="geraet",
        y="conv_rate_pct",
        color="gruppe",
        barmode="group",
        title="Conversion Rate nach Gerät und Gruppe (Simpson's Paradox)",
        labels={
            "conv_rate_pct": "Conversion Rate (%)",
            "geraet": "Gerätetyp",
            "gruppe": "Gruppe",
        },
        color_discrete_map={"Control": "#004B8D", "Treatment": "#E87722"},
        text="conv_rate_pct",
    )
    fig.update_traces(textposition="outside")
    fig
    return (fig,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ---

        ## Zusammenfassung

        | Konzept | SQL-Werkzeug | Erkenntnis |
        |---------|-------------|------------|
        | Deskriptive Statistik | `AVG()`, `STDDEV()` | Gruppen beschreiben |
        | z-Score | Window Functions | Ausreißer identifizieren |
        | t-Test | `WITH` + Berechnungen | Signifikanz prüfen |
        | Cohen's d | Pooled Std | Effektgröße bewerten |
        | Konfidenzintervall | Proportions-Formel | Unsicherheit quantifizieren |
        | Simpson's Paradox | `GROUP BY` Segment | **Immer segmentieren!** |

        **Kernbotschaft:** Ein Unterschied ist nur dann aussagekräftig, wenn er
        **statistisch signifikant** *und* **praktisch relevant** ist — und wir auf
        **Confounding Variables** geprüft haben.
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ---

        ## Freie Exploration

        Nutze die Zelle unten, um eigene SQL-Abfragen auf dem A/B-Test-Datensatz auszuprobieren.
        """
    )
    return


@app.cell
def _(ab_test, mo):
    mo.sql(
        f"""
        -- Eigene Abfrage hier:
        SELECT * FROM ab_test LIMIT 5
        """
    )
    return


if __name__ == "__main__":
    app.run()
