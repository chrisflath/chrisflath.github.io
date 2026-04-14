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
    app_title="DMA Session 11: Statistische Inferenz & A/B-Tests — Guide",
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

    return ab_test, daten_quelle


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        # Session 11: Statistische Inferenz & A/B-Tests — Guide

        **Kursfahrplan:** I: SQL-Grundlagen (S1–4) · II: Datenmodellierung (S5–7) · III: Fortgeschrittenes SQL (S8–9) · **▸ IV: Datenanalyse (S10–13)**

        ### Lernziele

        Nach dieser Session können Sie:

        - **z-Scores** berechnen und Ausreißer identifizieren
        - **Hypothesentests** durchführen (t-Test) und p-Werte interpretieren
        - **Effektgrößen** (Cohen's d) berechnen und einordnen
        - **Konfidenzintervalle** für Proportionen berechnen
        - **Simpson's Paradox** erkennen und vermeiden

        **Datensatz:** Simulierter A/B-Test eines Online-Checkout-Prozesses (4.000 Nutzer)

        ---
        """
    )
    return


@app.cell(hide_code=True)
def _(daten_quelle, mo):
    mo.md(
        f"""
        **Datenquelle:** {daten_quelle}

        ## Phase 1: Deskriptive Statistik

        Bevor wir testen, müssen wir die Daten **verstehen**. Unser Datensatz enthält 4.000 Nutzer,
        zufällig einer von zwei Checkout-Varianten zugewiesen:

        - **Control:** Bestehende Checkout-Seite
        - **Treatment:** Neue, optimierte Checkout-Seite

        Spalten: `user_id`, `gruppe` (Control/Treatment), `geraet` (Desktop/Mobile),
        `konvertiert` (0/1), `umsatz` (€, 0 wenn nicht konvertiert)
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Geführtes Beispiel 11.1: Conversion Rate pro Gruppe
    """)
    return


@app.cell(hide_code=True)
def _(ab_test, mo):
    _df = mo.sql(
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
    mo.md(r"""
    ### Geführtes Beispiel 11.2: Umsatzstatistiken (nur Konverter)
    """)
    return


@app.cell(hide_code=True)
def _(ab_test, mo):
    _df = mo.sql(
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
    mo.md(r"""
    ### Visualisierung: Umsatzverteilung nach Gruppe
    """)
    return


@app.cell(hide_code=True)
def _(ab_test, mo, px):
    _data = mo.sql(
        f"""
        SELECT gruppe, umsatz
        FROM ab_test
        WHERE konvertiert = 1
        """
    )

    fig_hist = px.histogram(
        _data,
        x="umsatz",
        color="gruppe",
        barmode="overlay",
        opacity=0.6,
        nbins=40,
        title="Umsatzverteilung nach Gruppe (nur Konverter)",
        labels={"umsatz": "Umsatz (€)", "gruppe": "Gruppe", "count": "Anzahl"},
        color_discrete_map={"Control": "#004B8D", "Treatment": "#E87722"},
    )
    fig_hist


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ---

        **Jetzt zum Übungs-Notebook → Aufgaben 1.x**

        ---

        ## Phase 2: z-Scores und Ausreißer

        Der **z-Score** standardisiert Werte: Wie viele Standardabweichungen liegt ein Wert vom Mittelwert entfernt?

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
    mo.md(r"""
    ### Vorhersage 1: z-Score Interpretation
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    pred_zscore = mo.ui.radio(
        options={
            "Auffällig — der Wert liegt 2.5 Standardabweichungen vom Mittelwert entfernt": "auffaellig",
            "Normal — 2.5 ist nur etwas über dem Durchschnitt": "normal",
            "Ein Datenfehler — z-Scores können nicht so hoch sein": "fehler",
            "Der Umsatz liegt bei 250% des Durchschnitts": "prozent",
        },
        label="**Vorhersage:** Ein Nutzer hat einen z-Score von 2.5 beim Umsatz. Was bedeutet das?",
    )
    return (pred_zscore,)


@app.cell(hide_code=True)
def _(mo, pred_zscore):
    if pred_zscore.value == "auffaellig":
        _result = (
            mo.md(
                "✅ **Richtig!** z = 2.5 bedeutet: Der Umsatz liegt **2.5 Standardabweichungen** "
                "über dem Mittelwert. Bei einer Normalverteilung liegen nur ca. 0.6% der Werte "
                "so weit entfernt. Dieser Nutzer ist ein **Ausreißer** — möglicherweise ein "
                "besonders wertvoller Kunde oder ein Sonderfall."
            )
        )
    elif pred_zscore.value == "normal":
        _result = (
            mo.md(
                "❌ Ein z-Score von 2.5 ist nicht 'nur etwas über dem Durchschnitt'! "
                "z = 0 wäre der Durchschnitt. z = 2.5 bedeutet 2.5 **Standardabweichungen** darüber — "
                "das ist bei Normalverteilung ein sehr seltener Wert (nur ~0.6% aller Daten)."
            )
        )
    elif pred_zscore.value == "fehler":
        _result = (
            mo.md(
                "❌ z-Scores können theoretisch beliebig hoch sein — es gibt keine Obergrenze. "
                "z = 2.5 ist auffällig, aber durchaus möglich. Bei 4.000 Nutzern erwarten wir "
                "einige mit |z| > 2."
            )
        )
    elif pred_zscore.value == "prozent":
        _result = (
            mo.md(
                "❌ z = 2.5 bedeutet nicht '250% des Durchschnitts'. Der z-Score misst den "
                "Abstand in **Standardabweichungen**, nicht in Prozent. "
                "z = 2.5 → 2.5 Standardabweichungen über dem Mittelwert."
            )
        )
    else:
        _result = mo.callout(mo.md("Bitte wählen."), kind="info")
    mo.vstack([pred_zscore, _result])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Geführtes Beispiel 11.3: z-Scores berechnen — Top 5 Ausreißer
    """)
    return


@app.cell(hide_code=True)
def _(ab_test, mo):
    _df = mo.sql(
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
    mo.md(r"""
    ### Visualisierung: z-Score-Verteilung mit Grenzlinien
    """)
    return


@app.cell(hide_code=True)
def _(ab_test, mo, px):
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

    fig_z = px.histogram(
        _z_data,
        x="z_score",
        color="gruppe",
        barmode="overlay",
        opacity=0.6,
        nbins=40,
        title="z-Score-Verteilung der Umsätze",
        labels={"z_score": "z-Score", "gruppe": "Gruppe", "count": "Anzahl"},
        color_discrete_map={"Control": "#004B8D", "Treatment": "#E87722"},
    )
    fig_z.add_vline(x=-2, line_dash="dash", line_color="red", annotation_text="z = -2")
    fig_z.add_vline(x=2, line_dash="dash", line_color="red", annotation_text="z = +2")
    fig_z


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ---

        **Jetzt zum Übungs-Notebook → Aufgaben 2.x**

        ---

        ## Phase 3: Hypothesentests

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
    mo.md(r"""
    ### Geführtes Beispiel 11.4: t-Test für Umsatz (Konverter)
    """)
    return


@app.cell(hide_code=True)
def _(ab_test, mo):
    _df = mo.sql(
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
    mo.md(r"""
    ### Vorhersage 2: p-Wert Interpretation
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    pred_pvalue = mo.ui.radio(
        options={
            "Statistisch signifikant — wir lehnen H₀ ab, weil p < α": "correct",
            "Wir akzeptieren H₁ als wahr — der Effekt ist bewiesen": "accept",
            "Nicht signifikant — 0.03 ist zu klein für eine Aussage": "nonsig",
            "Wir müssen den Test wiederholen, da p nicht genau 0.05 ist": "repeat",
        },
        label="**Vorhersage:** Was bedeutet ein p-Wert von 0.03 bei einem Signifikanzniveau α = 0.05?"
    )
    return (pred_pvalue,)


@app.cell(hide_code=True)
def _(mo, pred_pvalue):
    if pred_pvalue.value == "correct":
        _result = (
            mo.md(
                "✅ **Richtig!** Da p = 0.03 < α = 0.05, lehnen wir die Nullhypothese ab. "
                "Das bedeutet: Die beobachteten Daten sind unter H₀ so unwahrscheinlich, "
                "dass wir einen echten Effekt annehmen. "
                "**Achtung:** Das *beweist* H₁ nicht — es macht sie nur wahrscheinlicher."
            )
        )
    elif pred_pvalue.value == "accept":
        _result = (
            mo.md(
                "❌ Ein signifikantes Ergebnis *beweist* H₁ nicht! Es sagt nur: "
                "'Unter H₀ wären so extreme Daten sehr unwahrscheinlich.' "
                "Deshalb lehnen wir H₀ ab — aber H₁ ist damit nicht bewiesen."
            )
        )
    elif pred_pvalue.value == "nonsig":
        _result = (
            mo.md(
                "❌ p = 0.03 ist *signifikant*! Da 0.03 < 0.05 (unser α), "
                "lehnen wir H₀ ab. 'Zu klein' wäre falsch — ein kleiner p-Wert "
                "spricht *gegen* H₀."
            )
        )
    elif pred_pvalue.value == "repeat":
        _result = (
            mo.md(
                "❌ Der p-Wert muss nicht genau 0.05 sein. Wir vergleichen: "
                "p < α → signifikant, p ≥ α → nicht signifikant. "
                "Da 0.03 < 0.05, ist das Ergebnis **signifikant**."
            )
        )
    else:
        _result = mo.callout(mo.md("Bitte wählen."), kind="info")
    mo.vstack([pred_pvalue, _result])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ---

        **Jetzt zum Übungs-Notebook → Aufgaben 3.x**

        ---

        ## Phase 4: Effektstärken und Konfidenzintervalle

        ### Cohen's d — Wie groß ist der Effekt?

        $$d = \frac{\bar{x}_1 - \bar{x}_2}{s_{\text{pooled}}}$$

        | |d| | Interpretation |
        |-----|----------------|
        | < 0.2 | Vernachlässigbar |
        | 0.2 – 0.5 | Klein |
        | 0.5 – 0.8 | Mittel |
        | > 0.8 | Groß |
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Geführtes Beispiel 11.5: Cohen's d
    """)
    return


@app.cell(hide_code=True)
def _(ab_test, mo):
    _df = mo.sql(
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
    mo.md(r"""
    ### Vorhersage 3: Revenue vs. Conversion Rate
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    pred_metric = mo.ui.radio(
        options={
            "Umsatz pro Nutzer — weil er Conversion Rate UND Warenkorbgröße kombiniert": "revenue",
            "Conversion Rate — weil mehr Käufer immer besser ist": "cr",
            "Beide separat — sie messen verschiedene Dinge": "both",
            "Gesamtumsatz — absolute Zahlen zählen am Ende": "total",
        },
        label="**Vorhersage:** Welche Metrik sollte bei einem A/B-Test die finale Entscheidung treiben?"
    )
    return (pred_metric,)


@app.cell(hide_code=True)
def _(mo, pred_metric):
    if pred_metric.value == "revenue":
        _result = (
            mo.md(
                "✅ **Richtig!** Der Umsatz pro Nutzer (inkl. Nicht-Konverter mit 0€) ist oft die "
                "wichtigste Metrik, weil er **beide Effekte** erfasst: Conversion Rate × Warenkorbgröße. "
                "Eine Variante mit weniger Konvertern aber höheren Warenkörben kann insgesamt "
                "mehr Umsatz generieren."
            )
        )
    elif pred_metric.value == "cr":
        _result = (
            mo.md(
                "❌ Mehr Käufer sind nicht immer besser! Wenn Treatment zwar mehr Konverter hat, "
                "aber diese weniger ausgeben, kann der Gesamtumsatz sinken. "
                "Der **Umsatz pro Nutzer** kombiniert beide Effekte."
            )
        )
    elif pred_metric.value == "both":
        _result = (
            mo.md(
                "Teilweise richtig — es ist gut, beide zu betrachten. Aber für die **finale Entscheidung** "
                "braucht man eine primäre Metrik. Meist ist das der **Umsatz pro Nutzer**, "
                "weil er CR und Warenkorbgröße kombiniert."
            )
        )
    elif pred_metric.value == "total":
        _result = (
            mo.md(
                "❌ Der Gesamtumsatz hängt von der Gruppengröße ab und ist kein guter Vergleich "
                "zwischen ungleich großen Gruppen. Der **Umsatz pro Nutzer** normalisiert auf "
                "die Gruppengröße und ist deshalb aussagekräftiger."
            )
        )
    else:
        _result = mo.callout(mo.md("Bitte wählen."), kind="info")
    mo.vstack([pred_metric, _result])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Probieren Sie selbst: Effektgrößen

    Experimentieren Sie! Probieren Sie:
    - Cohen's d nur für Desktop-Nutzer vs. nur für Mobile-Nutzer
    - Konfidenzintervall für die Conversion Rate
    """)
    return


@app.cell
def _(ab_test, mo):
    _df = mo.sql(
        f"""
        SELECT
            gruppe,
            COUNT(*) AS n,
            ROUND(AVG(konvertiert) * 100, 1) AS conv_rate_pct,
            ROUND(
                (AVG(konvertiert) - 1.96 * SQRT(AVG(konvertiert) * (1 - AVG(konvertiert)) / COUNT(*))) * 100,
            1) AS ci_lower_pct,
            ROUND(
                (AVG(konvertiert) + 1.96 * SQRT(AVG(konvertiert) * (1 - AVG(konvertiert)) / COUNT(*))) * 100,
            1) AS ci_upper_pct
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

        **Jetzt zum Übungs-Notebook → Aufgaben 4.x**

        ---

        ## Phase 5: Simpson's Paradox aufdecken

        Bisher sieht es so aus, als wäre **Control besser**. Aber stimmt das wirklich?
        Schauen wir uns die Daten **segmentiert** an.
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Geführtes Beispiel 11.6: Segmentierung nach Gerät
    """)
    return


@app.cell(hide_code=True)
def _(ab_test, mo):
    _df = mo.sql(
        f"""
        SELECT
            geraet,
            gruppe,
            COUNT(*) AS n,
            SUM(konvertiert) AS conversions,
            ROUND(AVG(konvertiert) * 100, 1) AS conv_rate_pct
        FROM ab_test
        GROUP BY geraet, gruppe
        ORDER BY geraet, gruppe
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        **Simpson's Paradox!** Treatment ist in **beiden** Segmenten besser,
        aber im Gesamtergebnis schlechter. Warum?
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Vorhersage 4: Simpson's Paradox Ursache
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    pred_simpson = mo.ui.radio(
        options={
            "Unterschiedliche Zusammensetzung — Treatment hat mehr Mobile-Nutzer": "komposition",
            "Zufall — bei 4.000 Nutzern passiert das manchmal": "zufall",
            "Datenfehler — die Zahlen können nicht stimmen": "fehler",
            "Ein dritter Faktor (Confounding Variable) verzerrt das Gesamtergebnis": "confounding",
        },
        label="**Vorhersage:** Treatment ist in jedem Segment besser, aber insgesamt schlechter. Was ist die Ursache?"
    )
    return (pred_simpson,)


@app.cell(hide_code=True)
def _(mo, pred_simpson):
    if pred_simpson.value == "komposition":
        _result = (
            mo.md(
                "✅ **Richtig!** Die Gruppen sind **nicht gleich zusammengesetzt**: Treatment hat mehr "
                "Mobile-Nutzer, und Mobile-Nutzer konvertieren generell weniger. Das zieht den "
                "Gesamtdurchschnitt der Treatment-Gruppe nach unten — obwohl Treatment innerhalb "
                "jedes Segments besser ist. Das ist Simpson's Paradox in Reinform!"
            )
        )
    elif pred_simpson.value == "confounding":
        _result = (
            mo.md(
                "Sehr nah dran! Der Gerätetyp ist tatsächlich ein **Confounding Variable** — "
                "er beeinflusst sowohl die Gruppenzugehörigkeit als auch die Conversion Rate. "
                "Konkret: Treatment hat **mehr Mobile-Nutzer**, die generell weniger konvertieren. "
                "Deshalb ist die Segmentierung so wichtig."
            )
        )
    elif pred_simpson.value == "zufall":
        _result = (
            mo.md(
                "❌ Simpson's Paradox ist kein Zufall — es hat eine systematische Ursache. "
                "Die Gruppen sind **unterschiedlich zusammengesetzt**: Treatment hat mehr "
                "Mobile-Nutzer, die generell weniger konvertieren."
            )
        )
    elif pred_simpson.value == "fehler":
        _result = (
            mo.md(
                "❌ Die Zahlen stimmen! Es ist kein Fehler, sondern ein mathematisch erklärbares "
                "Phänomen. Die Gruppen haben eine **unterschiedliche Zusammensetzung** — "
                "das verzerrt den Gesamtvergleich."
            )
        )
    else:
        _result = mo.callout(mo.md("Bitte wählen."), kind="info")
    mo.vstack([pred_simpson, _result])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Geführtes Beispiel 11.7: Gruppenkomposition — die Erklärung
    """)
    return


@app.cell(hide_code=True)
def _(ab_test, mo):
    _df = mo.sql(
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
def _(ab_test, mo, px):
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

    fig_simpson = px.bar(
        _comp,
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
    fig_simpson.update_traces(textposition="outside")
    fig_simpson


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Vorhersage 5: Praktische vs. statistische Signifikanz
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    pred_practical = mo.ui.radio(
        options={
            "Nein — statistisch signifikant heißt nicht praktisch relevant": "not_enough",
            "Ja — Signifikanz beweist, dass der Effekt wichtig ist": "yes",
            "Signifikante Ergebnisse sollten immer umgesetzt werden": "always",
            "Es hängt nur vom p-Wert ab — je kleiner, desto besser": "depends",
        },
        label="**Vorhersage:** Ein A/B-Test zeigt einen signifikanten Umsatzunterschied von 0.50€ pro Nutzer. Sollten wir die neue Variante einführen?"
    )
    return (pred_practical,)


@app.cell(hide_code=True)
def _(mo, pred_practical):
    if pred_practical.value == "not_enough":
        _result = (
            mo.md(
                "✅ **Richtig!** Statistische Signifikanz (p < 0.05) sagt nur: 'Der Unterschied ist "
                "wahrscheinlich nicht Zufall.' Aber 0.50€ pro Nutzer ist vielleicht weniger als die "
                "Kosten für die Umstellung. Man braucht auch **praktische Relevanz** — "
                "Cohen's d, ROI-Berechnung und Business-Kontext."
            )
        )
    elif pred_practical.value == "yes":
        _result = (
            mo.md(
                "❌ Signifikanz ≠ Relevanz! Bei großen Stichproben (n = 4.000) werden auch winzige "
                "Unterschiede signifikant. 0.50€ pro Nutzer könnte weniger sein als die "
                "Implementierungskosten. Immer auch **Cohen's d** und den Business Case prüfen."
            )
        )
    elif pred_practical.value == "always":
        _result = (
            mo.md(
                "❌ Nicht immer! Bei großen Stichproben werden sehr kleine Effekte signifikant. "
                "0.50€ pro Nutzer könnte die Umstellungskosten nicht decken. "
                "Signifikanz + **praktische Relevanz** zusammen ergeben die Entscheidung."
            )
        )
    elif pred_practical.value == "depends":
        _result = (
            mo.md(
                "❌ Ein kleiner p-Wert allein reicht nicht. p = 0.001 bei 0.50€ Unterschied "
                "heißt: 'Wir sind sehr sicher, dass der Unterschied existiert' — aber der Unterschied "
                "ist trotzdem winzig. **Effektgröße** und Business-Kontext zählen mehr."
            )
        )
    else:
        _result = mo.callout(mo.md("Bitte wählen."), kind="info")
    mo.vstack([pred_practical, _result])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ---

        **Jetzt zum Übungs-Notebook → Aufgaben 5.x**

        ---

        ## Selbsttest
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    selbsttest_1 = mo.ui.radio(
        options={
            "Bei großen Stichproben reicht |t| > 2 — weil die t-Verteilung bei n > 30 der Normalverteilung ähnelt": "correct",
            "Immer — |t| > 2 ist die exakte Grenze für Signifikanz": "always",
            "Nie — man braucht immer eine t-Tabelle": "never",
        },
        label="Wann ist die Daumenregel |t| > 2 ≈ signifikant gültig?",
    )
    return (selbsttest_1,)


@app.cell(hide_code=True)
def _(mo, selbsttest_1):
    if selbsttest_1.value == "correct":
        _result = (
            mo.md(
                "✅ **Richtig!** Bei großen Stichproben (n > 30 pro Gruppe) nähert sich die "
                "t-Verteilung der Normalverteilung an, und der kritische Wert für α = 0.05 "
                "liegt bei ca. 1.96 ≈ 2. Bei kleinen Stichproben sind die kritischen Werte "
                "größer und man braucht exakte Tabellen."
            )
        )
    elif selbsttest_1.value:
        _result = (
            mo.md(
                "Nicht ganz. Die Daumenregel |t| > 2 gilt nur bei **großen Stichproben** "
                "(n > 30 pro Gruppe), weil die t-Verteilung dann der Normalverteilung ähnelt. "
                "Bei kleinen Stichproben sind die kritischen Werte größer."
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
            "Nein — ein großer p-Wert bedeutet nur 'nicht genug Evidenz gegen H₀', nicht 'kein Effekt'": "correct",
            "Ja — wenn p > 0.05 gibt es definitiv keinen Effekt": "yes",
            "Es kommt auf die Effektgröße an": "maybe",
        },
        label="Bedeutet 'nicht signifikant' (p > 0.05), dass es keinen Effekt gibt?",
    )
    return (selbsttest_2,)


@app.cell(hide_code=True)
def _(mo, selbsttest_2):
    if selbsttest_2.value == "correct":
        _result = (
            mo.md(
                "✅ **Richtig!** 'Nicht signifikant' heißt: 'Wir haben nicht genug Evidenz, "
                "um H₀ abzulehnen.' Das ist nicht dasselbe wie 'H₀ ist wahr' oder 'es gibt keinen Effekt'. "
                "Vielleicht ist die Stichprobe zu klein, um einen vorhandenen Effekt zu entdecken. "
                "Merkhilfe: **Absence of evidence ≠ evidence of absence.**"
            )
        )
    elif selbsttest_2.value:
        _result = (
            mo.md(
                "Nicht ganz. 'Nicht signifikant' heißt nur: 'Nicht genug Evidenz gegen H₀.' "
                "Es kann trotzdem einen Effekt geben — die Stichprobe war vielleicht zu klein. "
                "**Absence of evidence ≠ evidence of absence.**"
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
            "Wenn ein Confounding Variable die Gruppenzusammensetzung verzerrt — z.B. unterschiedliche Geräteverteilung": "correct",
            "Immer wenn es mehr als zwei Gruppen gibt": "always",
            "Nie — bei korrekt randomisierten A/B-Tests kann es nicht auftreten": "never",
        },
        label="Unter welchen Bedingungen tritt Simpson's Paradox auf?",
    )
    return (selbsttest_3,)


@app.cell(hide_code=True)
def _(mo, selbsttest_3):
    if selbsttest_3.value == "correct":
        _result = (
            mo.md(
                "✅ **Richtig!** Simpson's Paradox tritt auf, wenn eine **Confounding Variable** "
                "(z.B. Gerätetyp) sowohl mit der Gruppenzugehörigkeit als auch mit dem Outcome "
                "korreliert und die Gruppen **unterschiedlich zusammengesetzt** sind. "
                "Lösung: Immer nach relevanten Segmenten aufschlüsseln."
            )
        )
    elif selbsttest_3.value:
        _result = (
            mo.md(
                "Nicht ganz. Simpson's Paradox entsteht durch **unterschiedliche Gruppenkomposition**: "
                "Ein Confounding Variable verzerrt den Gesamtvergleich. Auch bei Randomisierung "
                "kann es durch Zufall zu ungleicher Verteilung kommen. "
                "Deshalb: Immer segmentiert analysieren!"
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
        | **Deskriptive Statistik** | `AVG()`, `STDDEV()`, `COUNT()` | Conversion Rate, Umsatz pro Gruppe |
        | **z-Score** | `(x - AVG() OVER()) / STDDEV() OVER()` | Ausreißer: \|z\| > 2 |
        | **t-Test (Welch)** | `WITH stats ... ABS(diff) / SE` | Signifikanz: \|t\| > 1.96 |
        | **Cohen's d** | `diff / s_pooled` | Effektgröße: klein/mittel/groß |
        | **Konfidenzintervall** | `p ± 1.96 * SQRT(p*(1-p)/n)` | 95%-CI für Proportionen |
        | **Simpson's Paradox** | `GROUP BY segment, gruppe` | Immer segmentieren! |

        ### Kernbotschaft

        Ein Unterschied ist nur dann aussagekräftig, wenn er **statistisch signifikant** *und* **praktisch relevant** ist — und wir auf **Confounding Variables** geprüft haben.

        ### Ausblick Session 12: Zeitreihenanalyse

        Nächste Woche kommt die Zeitdimension dazu: LAG, LEAD, Moving Averages und Year-over-Year Vergleiche.
        """
    )
    return


if __name__ == "__main__":
    app.run()
