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
    app_title="DMA Session 11: Statistische Inferenz & A/B-Tests — Übungen",
)


@app.cell(hide_code=True)
def _():
    import marimo as mo
    return (mo,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        # Session 11: Statistische Inferenz & A/B-Tests — Übungen

        Theorie und geführte Beispiele → **11-inferenz-ab-tests-guide.py**

        **Aufgabentypen:**

        - 🟢 **Geführt**: Vollständige Lösung zum Nachvollziehen
        - 🟡 **Angepasst**: Teillösung zum Ergänzen (`???`)
        - 🔵 **Selbstständig**: Eigene Lösung schreiben
        - 🔴 **Debugging**: Fehler finden und beheben
        - ⭐ **Entdecken**: Offene Herausforderungen

        > **Hinweis:** 🟡-Aufgaben enthalten `???` als Platzhalter. Die Zelle zeigt einen SQL-Fehler, bis Sie die `???` durch die richtige Lösung ersetzen — das ist Absicht!
        """
    )
    return


@app.cell
def _(mo):
    import polars as pl
    import plotly.express as px

    try:
        csv_path = mo.notebook_location() / "public" / "ab_test_checkout.csv"
        ab_test = pl.read_csv(str(csv_path))
    except Exception:
        ab_test = pl.DataFrame({
            "user_id": list(range(1, 11)),
            "gruppe": ["Control"] * 5 + ["Treatment"] * 5,
            "geraet": ["Desktop", "Mobile", "Desktop", "Mobile", "Desktop"] * 2,
            "konvertiert": [1, 0, 1, 0, 1, 1, 1, 0, 1, 0],
            "umsatz": [45.0, 0.0, 62.0, 0.0, 38.0, 55.0, 48.0, 0.0, 71.0, 0.0],
        })

    return ab_test, mo, pl, px


# -----------------------------------------------------------------------
# Phase 1: Deskriptive Statistik
# -----------------------------------------------------------------------


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
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
        ### 🟢 Aufgabe 1.1: Conversion Rate pro Gruppe

        Wie viele Nutzer sind in jeder Gruppe? Wie viele haben konvertiert?
        Berechne die **Conversion Rate** pro Gruppe.
        """
    )
    return


@app.cell
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
    mo.accordion({"🔑 Musterlösung": mo.md("""
```sql
SELECT
    gruppe,
    COUNT(*) AS n,
    SUM(konvertiert) AS conversions,
    ROUND(AVG(konvertiert) * 100, 1) AS conv_rate_pct
FROM ab_test
GROUP BY gruppe
ORDER BY gruppe
```
""")})
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ### 🟢 Aufgabe 1.2: Umsatzstatistiken für Konverter

        Berechne für jede Gruppe den **Mittelwert**, die **Standardabweichung**,
        **Minimum** und **Maximum** des Umsatzes (nur für konvertierte Nutzer).
        """
    )
    return


@app.cell
def _(ab_test, mo):
    _df = mo.sql(
        f"""
        SELECT
            gruppe,
            COUNT(*) AS n,
            ROUND(AVG(umsatz), 2) AS mittelwert,
            ROUND(STDDEV(umsatz), 2) AS standardabw,
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
    mo.accordion({"🔑 Musterlösung": mo.md("""
```sql
SELECT
    gruppe,
    COUNT(*) AS n,
    ROUND(AVG(umsatz), 2) AS mittelwert,
    ROUND(STDDEV(umsatz), 2) AS standardabw,
    ROUND(MIN(umsatz), 2) AS min_umsatz,
    ROUND(MAX(umsatz), 2) AS max_umsatz
FROM ab_test
WHERE konvertiert = 1
GROUP BY gruppe
```
""")})
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ### 🟡 Aufgabe 1.3: Umsatz pro Nutzer inkl. Nicht-Konverter (Scaffolded)

        Berechne den **durchschnittlichen Umsatz pro Nutzer** (inkl. Nicht-Konverter mit 0€).
        Dies ist oft die wichtigere Metrik als die Conversion Rate allein.
        Ergänzen Sie die fehlenden Teile (`???`):
        """
    )
    return


@app.cell
def _(ab_test, mo):
    _df = mo.sql(
        f"""
        SELECT
            gruppe,
            COUNT(*) AS n,
            ROUND(AVG(???), 2) AS avg_umsatz_alle,
            ROUND(STDDEV(???), 2) AS std_umsatz,
            ROUND(SUM(???), 2) AS total_umsatz
        FROM ab_test
        GROUP BY ???
        ORDER BY gruppe
        -- Tipp: Ersetzen Sie alle ??? durch die richtige Spalte
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.accordion({"🔑 Musterlösung": mo.md("""
```sql
SELECT
    gruppe,
    COUNT(*) AS n,
    ROUND(AVG(umsatz), 2) AS avg_umsatz_alle,
    ROUND(STDDEV(umsatz), 2) AS std_umsatz,
    ROUND(SUM(umsatz), 2) AS total_umsatz
FROM ab_test
GROUP BY gruppe
ORDER BY gruppe
```
**Beachte:** Hier wird `umsatz` ohne `WHERE konvertiert = 1` verwendet — Nicht-Konverter haben Umsatz 0 und ziehen den Durchschnitt nach unten.
""")})
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ### 🔵 Aufgabe 1.4: Deskriptive Stats nach Gerät und Gruppe (Selbstständig)

        Berechne Conversion Rate und Durchschnittsumsatz (aller Nutzer) nach **Gerät und Gruppe**.

        *Hinweis: `GROUP BY geraet, gruppe` — gleiche Aggregation, nur feiner segmentiert*
        """
    )
    return


@app.cell
def _(ab_test, mo):
    _df = mo.sql(
        f"""
        -- Ihre Lösung hier
        -- Tipp: GROUP BY geraet, gruppe
        -- Erwartete Spalten: geraet, gruppe, n, conv_rate_pct, avg_umsatz
        SELECT 'Schreiben Sie Ihre Abfrage hier' AS hinweis
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.accordion({"🔑 Musterlösung": mo.md("""
```sql
SELECT
    geraet,
    gruppe,
    COUNT(*) AS n,
    ROUND(AVG(konvertiert) * 100, 1) AS conv_rate_pct,
    ROUND(AVG(umsatz), 2) AS avg_umsatz
FROM ab_test
GROUP BY geraet, gruppe
ORDER BY geraet, gruppe
```
""")})
    return


# -----------------------------------------------------------------------
# Phase 2: z-Scores und Ausreißer
# -----------------------------------------------------------------------


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
        ### 🟢 Aufgabe 2.1: z-Score berechnen

        Berechne den z-Score des Umsatzes für jeden konvertierten Nutzer
        mittels **Window Functions**. Zeige die **Top 5 Ausreißer** (höchster |z-Score|).
        """
    )
    return


@app.cell
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
    mo.accordion({"🔑 Musterlösung": mo.md("""
```sql
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
```
**Erklärung:** `AVG(umsatz) OVER()` und `STDDEV(umsatz) OVER()` berechnen Mittelwert und Standardabweichung über **alle** Zeilen (leeres `OVER()`).
""")})
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ### 🟡 Aufgabe 2.2: z-Score > 2 zählen pro Gruppe (Scaffolded)

        Wie viele konvertierte Nutzer haben einen |z-Score| > 2?
        Zähle pro Gruppe. Ergänzen Sie `???`:
        """
    )
    return


@app.cell
def _(ab_test, mo):
    _df = mo.sql(
        f"""
        WITH z_scores AS (
            SELECT
                user_id,
                gruppe,
                umsatz,
                (umsatz - AVG(umsatz) OVER())
                / STDDEV(umsatz) OVER() AS z_score
            FROM ab_test
            WHERE konvertiert = 1
        )
        SELECT
            gruppe,
            COUNT(*) AS n_total,
            SUM(CASE WHEN ABS(z_score) > 2 THEN 1 ELSE 0 END) AS ???,
            ROUND(SUM(CASE WHEN ABS(???) > 2 THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 1) AS pct_ausreisser
        FROM z_scores
        GROUP BY gruppe
        -- Tipp: n_ausreisser und z_score
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.accordion({"🔑 Musterlösung": mo.md("""
```sql
WITH z_scores AS (
    SELECT
        user_id,
        gruppe,
        umsatz,
        (umsatz - AVG(umsatz) OVER())
        / STDDEV(umsatz) OVER() AS z_score
    FROM ab_test
    WHERE konvertiert = 1
)
SELECT
    gruppe,
    COUNT(*) AS n_total,
    SUM(CASE WHEN ABS(z_score) > 2 THEN 1 ELSE 0 END) AS n_ausreisser,
    ROUND(SUM(CASE WHEN ABS(z_score) > 2 THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 1) AS pct_ausreisser
FROM z_scores
GROUP BY gruppe
```
""")})
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ### 🔵 Aufgabe 2.3: z-Score getrennt pro Gruppe (Selbstständig)

        Berechne den z-Score **getrennt pro Gruppe** (Treatment und Control jeweils
        mit eigenem Mittelwert und eigener Standardabweichung).

        *Hinweis: Nutzen Sie `PARTITION BY gruppe` in der Window Function.*
        """
    )
    return


@app.cell
def _(ab_test, mo):
    _df = mo.sql(
        f"""
        -- Ihre Lösung hier
        -- Tipp: AVG(umsatz) OVER(PARTITION BY gruppe) statt OVER()
        -- Erwartete Spalten: user_id, gruppe, umsatz, z_score
        -- Sortierung: ABS(z_score) DESC, LIMIT 10
        SELECT 'Schreiben Sie Ihre Abfrage hier' AS hinweis
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.accordion({"🔑 Musterlösung": mo.md("""
```sql
SELECT
    user_id,
    gruppe,
    umsatz,
    ROUND(
        (umsatz - AVG(umsatz) OVER(PARTITION BY gruppe))
        / STDDEV(umsatz) OVER(PARTITION BY gruppe),
    2) AS z_score
FROM ab_test
WHERE konvertiert = 1
ORDER BY ABS(
    (umsatz - AVG(umsatz) OVER(PARTITION BY gruppe))
    / STDDEV(umsatz) OVER(PARTITION BY gruppe)
) DESC
LIMIT 10
```
**Unterschied:** Jetzt wird der z-Score relativ zur **eigenen Gruppe** berechnet, nicht über alle Konverter.
""")})
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ### 🔴 Aufgabe 2.4: Debugging — Fehlende OVER()-Klausel

        Die folgende Abfrage soll z-Scores berechnen. Sie hat einen Fehler!
        """
    )
    return


@app.cell
def _(ab_test, mo):
    _df = mo.sql(
        f"""
        -- 🔴 Diese Abfrage hat einen Fehler — finden und beheben Sie ihn!
        SELECT
            user_id,
            gruppe,
            umsatz,
            ROUND(
                (umsatz - AVG(umsatz))
                / STDDEV(umsatz),
            2) AS z_score
        FROM ab_test
        WHERE konvertiert = 1
        ORDER BY ABS(z_score) DESC
        LIMIT 5
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.accordion({"🔑 Lösung": mo.md("""
**Problem:** `AVG(umsatz)` und `STDDEV(umsatz)` werden **ohne `OVER()`** aufgerufen.
Ohne `OVER()` sind es Aggregatfunktionen, die eine GROUP BY erwarten — keine Window Functions.

**Lösung:** Fügen Sie `OVER()` hinzu, um sie als Window Functions zu verwenden:

```sql
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
ORDER BY ABS(
    (umsatz - AVG(umsatz) OVER())
    / STDDEV(umsatz) OVER()
) DESC
LIMIT 5
```
""")})
    return


# -----------------------------------------------------------------------
# Phase 3: Hypothesentests
# -----------------------------------------------------------------------


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
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
    mo.md(
        r"""
        ### 🟢 Aufgabe 3.1: t-Test für Umsatz (Konverter)

        Berechne die t-Statistik für den Umsatzvergleich zwischen Control und Treatment
        (nur konvertierte Nutzer). Ist der Unterschied signifikant?
        """
    )
    return


@app.cell
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
    mo.accordion({"🔑 Musterlösung": mo.md("""
```sql
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
```
**Erklärung:** Die CTE `stats` berechnet n, Mittelwert und Std pro Gruppe. Dann wird die Welch-t-Formel angewendet.
""")})
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ### 🟡 Aufgabe 3.2: t-Test für Conversion Rate (Scaffolded)

        Berechne einen t-Test für die **Conversion Rate** (Proportionentest).
        Hier ist `AVG(konvertiert)` die Rate und die Standardabweichung berechnet sich als
        $\sqrt{p \cdot (1-p)}$. Ergänzen Sie `???`:
        """
    )
    return


@app.cell
def _(ab_test, mo):
    _df = mo.sql(
        f"""
        WITH stats AS (
            SELECT
                gruppe,
                COUNT(*) AS n,
                AVG(konvertiert) AS p_rate,
                SQRT(AVG(konvertiert) * (1 - AVG(konvertiert))) AS std
            FROM ab_test
            GROUP BY gruppe
        )
        SELECT
            ROUND(c.p_rate * 100, 2) AS cr_control_pct,
            ROUND(t.p_rate * 100, 2) AS cr_treatment_pct,
            ROUND((t.p_rate - c.p_rate) * 100, 2) AS diff_pct,
            ROUND(
                ABS(c.p_rate - t.p_rate)
                / SQRT(POWER(c.???, 2) / c.n + POWER(t.???, 2) / t.n),
            2) AS t_statistik,
            CASE
                WHEN ABS(c.p_rate - t.p_rate)
                     / SQRT(POWER(c.std, 2) / c.n + POWER(t.std, 2) / t.n) > ???
                THEN 'Signifikant (p < 0.05)'
                ELSE 'Nicht signifikant'
            END AS ergebnis
        FROM stats c, stats t
        WHERE c.gruppe = 'Control'
          AND t.gruppe = 'Treatment'
        -- Tipp: std und 1.96
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.accordion({"🔑 Musterlösung": mo.md("""
```sql
WITH stats AS (
    SELECT
        gruppe,
        COUNT(*) AS n,
        AVG(konvertiert) AS p_rate,
        SQRT(AVG(konvertiert) * (1 - AVG(konvertiert))) AS std
    FROM ab_test
    GROUP BY gruppe
)
SELECT
    ROUND(c.p_rate * 100, 2) AS cr_control_pct,
    ROUND(t.p_rate * 100, 2) AS cr_treatment_pct,
    ROUND((t.p_rate - c.p_rate) * 100, 2) AS diff_pct,
    ROUND(
        ABS(c.p_rate - t.p_rate)
        / SQRT(POWER(c.std, 2) / c.n + POWER(t.std, 2) / t.n),
    2) AS t_statistik,
    CASE
        WHEN ABS(c.p_rate - t.p_rate)
             / SQRT(POWER(c.std, 2) / c.n + POWER(t.std, 2) / t.n) > 1.96
        THEN 'Signifikant (p < 0.05)'
        ELSE 'Nicht signifikant'
    END AS ergebnis
FROM stats c, stats t
WHERE c.gruppe = 'Control'
  AND t.gruppe = 'Treatment'
```
""")})
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ### 🔵 Aufgabe 3.3: t-Test nur für Desktop-Nutzer (Selbstständig)

        Führe den Umsatz-t-Test (wie 3.1) **nur für Desktop-Nutzer** durch.

        *Hinweis: Fügen Sie `AND geraet = 'Desktop'` zur WHERE-Klausel der CTE hinzu.*
        """
    )
    return


@app.cell
def _(ab_test, mo):
    _df = mo.sql(
        f"""
        -- Ihre Lösung hier
        -- Tipp: Wie 3.1, aber mit WHERE konvertiert = 1 AND geraet = 'Desktop'
        -- Erwartete Spalten: mittel_control, mittel_treatment, differenz, t_statistik, ergebnis
        SELECT 'Schreiben Sie Ihre Abfrage hier' AS hinweis
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.accordion({"🔑 Musterlösung": mo.md("""
```sql
WITH stats AS (
    SELECT
        gruppe,
        COUNT(*) AS n,
        AVG(umsatz) AS mittel,
        STDDEV(umsatz) AS std
    FROM ab_test
    WHERE konvertiert = 1
      AND geraet = 'Desktop'
    GROUP BY gruppe
)
SELECT
    ROUND(c.mittel, 2) AS mittel_control,
    ROUND(t.mittel, 2) AS mittel_treatment,
    ROUND(c.mittel - t.mittel, 2) AS differenz,
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
```
""")})
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ### 🔴 Aufgabe 3.4: Debugging — Fehlende GROUP BY in CTE

        Die folgende Abfrage soll die Gruppenstatistiken berechnen. Sie hat einen Fehler!
        """
    )
    return


@app.cell
def _(ab_test, mo):
    _df = mo.sql(
        f"""
        -- 🔴 Diese Abfrage hat einen Fehler — finden und beheben Sie ihn!
        WITH stats AS (
            SELECT
                gruppe,
                COUNT(*) AS n,
                AVG(umsatz) AS mittel,
                STDDEV(umsatz) AS std
            FROM ab_test
            WHERE konvertiert = 1
        )
        SELECT
            ROUND(c.mittel, 2) AS mittel_control,
            ROUND(t.mittel, 2) AS mittel_treatment,
            ROUND(
                ABS(c.mittel - t.mittel)
                / SQRT(POWER(c.std, 2) / c.n + POWER(t.std, 2) / t.n),
            2) AS t_statistik
        FROM stats c, stats t
        WHERE c.gruppe = 'Control'
          AND t.gruppe = 'Treatment'
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.accordion({"🔑 Lösung": mo.md("""
**Problem:** In der CTE `stats` fehlt `GROUP BY gruppe`! Ohne GROUP BY wird nur **eine** Zeile
mit den Gesamtstatistiken berechnet — die WHERE-Bedingungen `c.gruppe = 'Control'` finden
dann keine passenden Zeilen.

**Lösung:**
```sql
WITH stats AS (
    SELECT
        gruppe,
        COUNT(*) AS n,
        AVG(umsatz) AS mittel,
        STDDEV(umsatz) AS std
    FROM ab_test
    WHERE konvertiert = 1
    GROUP BY gruppe        -- ← das fehlte!
)
SELECT
    ROUND(c.mittel, 2) AS mittel_control,
    ROUND(t.mittel, 2) AS mittel_treatment,
    ROUND(
        ABS(c.mittel - t.mittel)
        / SQRT(POWER(c.std, 2) / c.n + POWER(t.std, 2) / t.n),
    2) AS t_statistik
FROM stats c, stats t
WHERE c.gruppe = 'Control'
  AND t.gruppe = 'Treatment'
```
""")})
    return


# -----------------------------------------------------------------------
# Phase 4: Effektstärken und Konfidenzintervalle
# -----------------------------------------------------------------------


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ---

        ## Phase 4: Effektstärken und Konfidenzintervalle

        ### Cohen's d — Wie groß ist der Effekt?

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


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ### 🟢 Aufgabe 4.1: Cohen's d berechnen

        Berechne Cohen's d für den Umsatzunterschied zwischen den Gruppen (nur Konverter).
        """
    )
    return


@app.cell
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
    mo.accordion({"🔑 Musterlösung": mo.md("""
```sql
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
```
**Erklärung:** Cohen's d normalisiert den Mittelwertunterschied durch die gepoolte Standardabweichung und gibt so eine einheitslose Effektstärke an.
""")})
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ### 🟡 Aufgabe 4.2: Konfidenzintervall für Conversion Rate (Scaffolded)

        Berechne die Conversion Rate pro Gruppe mit einem **95%-Konfidenzintervall**.

        Für Proportionen: $CI = p \pm 1.96 \cdot \sqrt{\frac{p(1-p)}{n}}$

        Ergänzen Sie `???`:
        """
    )
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
                (AVG(konvertiert) - 1.96 * SQRT(??? * (1 - ???) / COUNT(*))) * 100,
            1) AS ci_lower_pct,
            ROUND(
                (AVG(konvertiert) + 1.96 * SQRT(??? * (1 - ???) / COUNT(*))) * 100,
            1) AS ci_upper_pct
        FROM ab_test
        GROUP BY gruppe
        ORDER BY gruppe
        -- Tipp: Ersetzen Sie jedes ??? durch AVG(konvertiert)
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.accordion({"🔑 Musterlösung": mo.md("""
```sql
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
```
**Interpretation:** Wenn sich die Konfidenzintervalle **nicht überlappen**, deutet das auf einen signifikanten Unterschied hin.
""")})
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ### 🔵 Aufgabe 4.3: Konfidenzintervall für Umsatz pro Nutzer (Selbstständig)

        Berechne ein 95%-Konfidenzintervall für den **durchschnittlichen Umsatz pro Nutzer**
        (inkl. Nicht-Konverter) pro Gruppe.

        Für Mittelwerte: $CI = \bar{x} \pm 1.96 \cdot \frac{s}{\sqrt{n}}$

        *Hinweis: `AVG(umsatz) - 1.96 * STDDEV(umsatz) / SQRT(COUNT(*))`*
        """
    )
    return


@app.cell
def _(ab_test, mo):
    _df = mo.sql(
        f"""
        -- Ihre Lösung hier
        -- Erwartete Spalten: gruppe, n, avg_umsatz, ci_lower, ci_upper
        SELECT 'Schreiben Sie Ihre Abfrage hier' AS hinweis
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.accordion({"🔑 Musterlösung": mo.md("""
```sql
SELECT
    gruppe,
    COUNT(*) AS n,
    ROUND(AVG(umsatz), 2) AS avg_umsatz,
    ROUND(AVG(umsatz) - 1.96 * STDDEV(umsatz) / SQRT(COUNT(*)), 2) AS ci_lower,
    ROUND(AVG(umsatz) + 1.96 * STDDEV(umsatz) / SQRT(COUNT(*)), 2) AS ci_upper
FROM ab_test
GROUP BY gruppe
ORDER BY gruppe
```
**Interpretation:** Das CI gibt den Bereich an, in dem der wahre Mittelwert mit 95% Wahrscheinlichkeit liegt.
""")})
    return


# -----------------------------------------------------------------------
# Phase 5: Simpson's Paradox
# -----------------------------------------------------------------------


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
        ### 🟢 Aufgabe 5.1: Conversion Rate nach Gerät und Gruppe

        Berechne die Conversion Rate **getrennt nach Gerätetyp** (Desktop vs. Mobile).
        Was fällt auf?
        """
    )
    return


@app.cell
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
    mo.accordion({"🔑 Musterlösung": mo.md("""
```sql
SELECT
    geraet,
    gruppe,
    COUNT(*) AS n,
    SUM(konvertiert) AS conversions,
    ROUND(AVG(konvertiert) * 100, 1) AS conv_rate_pct
FROM ab_test
GROUP BY geraet, gruppe
ORDER BY geraet, gruppe
```
**Simpson's Paradox!** Treatment ist in **beiden** Segmenten besser, aber im Gesamtergebnis schlechter. Warum? Die Gruppen sind **nicht gleich zusammengesetzt**.
""")})
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ### 🟡 Aufgabe 5.2: Gruppenkomposition analysieren (Scaffolded)

        Zeige die **Geräteverteilung** pro Gruppe. Das erklärt den Paradox.
        Ergänzen Sie `???`:
        """
    )
    return


@app.cell
def _(ab_test, mo):
    _df = mo.sql(
        f"""
        SELECT
            gruppe,
            geraet,
            COUNT(*) AS n,
            ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER(PARTITION BY ???), 1) AS anteil_pct
        FROM ab_test
        GROUP BY gruppe, geraet
        ORDER BY gruppe, geraet
        -- Tipp: PARTITION BY gruppe
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.accordion({"🔑 Musterlösung": mo.md("""
```sql
SELECT
    gruppe,
    geraet,
    COUNT(*) AS n,
    ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER(PARTITION BY gruppe), 1) AS anteil_pct
FROM ab_test
GROUP BY gruppe, geraet
ORDER BY gruppe, geraet
```
**Ergebnis:** Die Treatment-Gruppe hat deutlich **mehr Mobile-Nutzer** als die Control-Gruppe. Da Mobile-Nutzer generell weniger konvertieren, zieht das den Gesamtdurchschnitt der Treatment-Gruppe nach unten.
""")})
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ### 🔵 Aufgabe 5.3: Segmentierter t-Test — nur Desktop (Selbstständig)

        Führe den t-Test für die **Conversion Rate** nur für **Desktop-Nutzer** durch.
        Verändert sich das Ergebnis im Vergleich zum Gesamttest?

        *Hinweis: Wie 3.2, aber mit `WHERE geraet = 'Desktop'`*
        """
    )
    return


@app.cell
def _(ab_test, mo):
    _df = mo.sql(
        f"""
        -- Ihre Lösung hier
        -- Tipp: Wie 3.2 (Proportionentest), aber WHERE geraet = 'Desktop'
        -- Erwartete Spalten: cr_control_pct, cr_treatment_pct, diff_pct, t_statistik, ergebnis
        SELECT 'Schreiben Sie Ihre Abfrage hier' AS hinweis
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.accordion({"🔑 Musterlösung": mo.md("""
```sql
WITH stats AS (
    SELECT
        gruppe,
        COUNT(*) AS n,
        AVG(konvertiert) AS p_rate,
        SQRT(AVG(konvertiert) * (1 - AVG(konvertiert))) AS std
    FROM ab_test
    WHERE geraet = 'Desktop'
    GROUP BY gruppe
)
SELECT
    ROUND(c.p_rate * 100, 2) AS cr_control_pct,
    ROUND(t.p_rate * 100, 2) AS cr_treatment_pct,
    ROUND((t.p_rate - c.p_rate) * 100, 2) AS diff_pct,
    ROUND(
        ABS(c.p_rate - t.p_rate)
        / SQRT(POWER(c.std, 2) / c.n + POWER(t.std, 2) / t.n),
    2) AS t_statistik,
    CASE
        WHEN ABS(c.p_rate - t.p_rate)
             / SQRT(POWER(c.std, 2) / c.n + POWER(t.std, 2) / t.n) > 1.96
        THEN 'Signifikant (p < 0.05)'
        ELSE 'Nicht signifikant'
    END AS ergebnis
FROM stats c, stats t
WHERE c.gruppe = 'Control'
  AND t.gruppe = 'Treatment'
```
""")})
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ### 🔴 Aufgabe 5.4: Debugging — Falsches PARTITION BY

        Die folgende Abfrage soll den Anteil jedes Gerätetyps **innerhalb jeder Gruppe** zeigen.
        Sie hat einen Fehler!
        """
    )
    return


@app.cell
def _(ab_test, mo):
    _df = mo.sql(
        f"""
        -- 🔴 Diese Abfrage hat einen Fehler — finden und beheben Sie ihn!
        SELECT
            gruppe,
            geraet,
            COUNT(*) AS n,
            ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER(PARTITION BY geraet), 1) AS anteil_pct
        FROM ab_test
        GROUP BY gruppe, geraet
        ORDER BY gruppe, geraet
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.accordion({"🔑 Lösung": mo.md("""
**Problem:** `PARTITION BY geraet` partitioniert nach **Gerätetyp** statt nach **Gruppe**.
Dadurch wird der Anteil *innerhalb jedes Gerätetyps* statt *innerhalb jeder Gruppe* berechnet.

**Lösung:** Ändern Sie `PARTITION BY geraet` zu `PARTITION BY gruppe`:

```sql
SELECT
    gruppe,
    geraet,
    COUNT(*) AS n,
    ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER(PARTITION BY gruppe), 1) AS anteil_pct
FROM ab_test
GROUP BY gruppe, geraet
ORDER BY gruppe, geraet
```

**Merke:** Das PARTITION BY muss zur **Bezugsgröße** passen: „Anteil pro Gruppe" → `PARTITION BY gruppe`.
""")})
    return


# -----------------------------------------------------------------------
# Exploration
# -----------------------------------------------------------------------


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ---

        ## Exploration

        Offene Herausforderungen für Fortgeschrittene.

        **Tipp:** Diskutieren Sie Ihre Ergebnisse mit Ihrem Nachbarn — bei der Interpretation von p-Werten und Effektgrößen hilft der Austausch!
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ### ⭐ Exploration 1: Stichprobengröße — Wie viele Nutzer brauchen wir?

        Bei einem beobachteten Conversion-Rate-Unterschied: Wie groß müsste die Stichprobe sein,
        damit der Unterschied bei einem z-Test signifikant wird?

        Formel (vereinfacht): $n \geq \frac{(z_{\alpha/2})^2 \cdot 2 \cdot \bar{p} \cdot (1 - \bar{p})}{(\Delta p)^2}$

        wobei $\bar{p}$ die gepoolte Conversion Rate und $\Delta p$ der beobachtete Unterschied ist.

        Berechnen Sie dies mit SQL!
        """
    )
    return


@app.cell
def _(ab_test, mo):
    _df = mo.sql(
        f"""
        -- Ihre Lösung hier
        -- Tipp: Berechnen Sie zuerst p_pooled und delta_p, dann die Formel anwenden
        SELECT 'Schreiben Sie Ihre Abfrage hier' AS hinweis
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.accordion({"🔑 Musterlösung": mo.md("""
```sql
WITH rates AS (
    SELECT
        AVG(konvertiert) AS p_pooled,
        AVG(CASE WHEN gruppe = 'Treatment' THEN konvertiert END)
            - AVG(CASE WHEN gruppe = 'Control' THEN konvertiert END) AS delta_p
    FROM ab_test
)
SELECT
    ROUND(p_pooled * 100, 2) AS pooled_cr_pct,
    ROUND(delta_p * 100, 2) AS unterschied_pct,
    ROUND(
        POWER(1.96, 2) * 2 * p_pooled * (1 - p_pooled) / POWER(delta_p, 2),
    0) AS min_n_pro_gruppe,
    ROUND(
        POWER(1.96, 2) * 2 * p_pooled * (1 - p_pooled) / POWER(delta_p, 2) * 2,
    0) AS min_n_gesamt
FROM rates
```
**Interpretation:** So viele Nutzer bräuchten Sie *mindestens* pro Gruppe, um den beobachteten Unterschied mit 95% Konfidenz zu erkennen.
""")})
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ### ⭐⭐ Exploration 2: Bonferroni-Korrektur — Mehrere Metriken testen

        Wenn wir **mehrere** Metriken gleichzeitig testen (Conversion Rate, Umsatz, Umsatz pro Nutzer),
        steigt die Wahrscheinlichkeit eines Typ-I-Fehlers. Die **Bonferroni-Korrektur** teilt das
        Signifikanzniveau durch die Anzahl der Tests: $\alpha_{\text{korr}} = \frac{\alpha}{k}$

        Berechnen Sie t-Statistiken für alle drei Metriken und prüfen Sie Signifikanz
        mit dem korrigierten Schwellenwert (3 Tests → $\alpha = 0.05/3 \approx 0.0167$, kritischer Wert $\approx 2.39$).
        """
    )
    return


@app.cell
def _(ab_test, mo):
    _df = mo.sql(
        f"""
        -- Ihre Lösung hier
        -- Tipp: Drei separate CTEs oder UNION ALL für die drei Metriken
        -- Kritischer Wert bei Bonferroni (k=3): 2.39 statt 1.96
        SELECT 'Schreiben Sie Ihre Abfrage hier' AS hinweis
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.accordion({"🔑 Musterlösung": mo.md("""
```sql
WITH
-- Test 1: Conversion Rate
cr_stats AS (
    SELECT
        gruppe,
        COUNT(*) AS n,
        AVG(konvertiert) AS mittel,
        SQRT(AVG(konvertiert) * (1 - AVG(konvertiert))) AS std
    FROM ab_test
    GROUP BY gruppe
),
cr_test AS (
    SELECT
        'Conversion Rate' AS metrik,
        ROUND(
            ABS(c.mittel - t.mittel)
            / SQRT(POWER(c.std, 2) / c.n + POWER(t.std, 2) / t.n),
        2) AS t_stat
    FROM cr_stats c, cr_stats t
    WHERE c.gruppe = 'Control' AND t.gruppe = 'Treatment'
),
-- Test 2: Umsatz (nur Konverter)
rev_stats AS (
    SELECT
        gruppe,
        COUNT(*) AS n,
        AVG(umsatz) AS mittel,
        STDDEV(umsatz) AS std
    FROM ab_test
    WHERE konvertiert = 1
    GROUP BY gruppe
),
rev_test AS (
    SELECT
        'Umsatz (Konverter)' AS metrik,
        ROUND(
            ABS(c.mittel - t.mittel)
            / SQRT(POWER(c.std, 2) / c.n + POWER(t.std, 2) / t.n),
        2) AS t_stat
    FROM rev_stats c, rev_stats t
    WHERE c.gruppe = 'Control' AND t.gruppe = 'Treatment'
),
-- Test 3: Umsatz pro Nutzer (alle)
rpu_stats AS (
    SELECT
        gruppe,
        COUNT(*) AS n,
        AVG(umsatz) AS mittel,
        STDDEV(umsatz) AS std
    FROM ab_test
    GROUP BY gruppe
),
rpu_test AS (
    SELECT
        'Umsatz pro Nutzer' AS metrik,
        ROUND(
            ABS(c.mittel - t.mittel)
            / SQRT(POWER(c.std, 2) / c.n + POWER(t.std, 2) / t.n),
        2) AS t_stat
    FROM rpu_stats c, rpu_stats t
    WHERE c.gruppe = 'Control' AND t.gruppe = 'Treatment'
)
SELECT
    metrik,
    t_stat,
    CASE WHEN t_stat > 1.96 THEN 'Ja' ELSE 'Nein' END AS sig_ohne_korrektur,
    CASE WHEN t_stat > 2.39 THEN 'Ja' ELSE 'Nein' END AS sig_mit_bonferroni
FROM (
    SELECT * FROM cr_test
    UNION ALL SELECT * FROM rev_test
    UNION ALL SELECT * FROM rpu_test
)
ORDER BY t_stat DESC
```
**Erklärung:** Die Bonferroni-Korrektur ist konservativ, verhindert aber das Multiple-Testing-Problem.
""")})
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ### ⭐⭐⭐ Exploration 3: Heterogene Treatment-Effekte

        Wirkt das Treatment für alle Nutzer gleich? Oder gibt es **heterogene Effekte** —
        z.B. profitieren Mobile-Nutzer mehr als Desktop-Nutzer?

        Berechnen Sie Cohen's d **getrennt nach Gerätetyp** und vergleichen Sie die Effektstärken.
        """
    )
    return


@app.cell
def _(ab_test, mo):
    _df = mo.sql(
        f"""
        -- Ihre Lösung hier
        -- Tipp: Wie 4.1, aber mit zusätzlichem GROUP BY geraet in der CTE
        -- und einem CROSS JOIN der Gruppen pro Gerät
        SELECT 'Schreiben Sie Ihre Abfrage hier' AS hinweis
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.accordion({"🔑 Musterlösung": mo.md("""
```sql
WITH stats AS (
    SELECT
        geraet,
        gruppe,
        COUNT(*) AS n,
        AVG(umsatz) AS mittel,
        STDDEV(umsatz) AS std
    FROM ab_test
    WHERE konvertiert = 1
    GROUP BY geraet, gruppe
)
SELECT
    c.geraet,
    ROUND(c.mittel, 2) AS mittel_control,
    ROUND(t.mittel, 2) AS mittel_treatment,
    ROUND(c.mittel - t.mittel, 2) AS differenz,
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
FROM stats c
JOIN stats t ON c.geraet = t.geraet
WHERE c.gruppe = 'Control'
  AND t.gruppe = 'Treatment'
ORDER BY c.geraet
```
**Interpretation:** Unterschiedliche Effektstärken deuten auf **heterogene Treatment-Effekte** hin. In der Praxis könnte man das Treatment nur für das Segment ausrollen, wo es am besten wirkt.
""")})
    return


# -----------------------------------------------------------------------
# Freie Exploration
# -----------------------------------------------------------------------


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ---

        ## Freie Exploration

        Probieren Sie eigene Analysen auf dem A/B-Test-Datensatz:
        """
    )
    return


@app.cell
def _(ab_test, mo):
    _df = mo.sql(
        f"""
        -- Eigene Abfrage hier:
        SELECT * FROM ab_test LIMIT 5
        """
    )
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

        | Konzept | Aufgaben | SQL-Werkzeug |
        |---------|----------|-------------|
        | **Deskriptive Statistik** | 1.1 – 1.4 | `AVG()`, `STDDEV()`, `GROUP BY` |
        | **z-Score** | 2.1 – 2.4 | Window Functions `OVER()` |
        | **t-Test** | 3.1 – 3.4 | `WITH` + Welch-Formel |
        | **Effektstärken** | 4.1 – 4.3 | Cohen's d, Konfidenzintervalle |
        | **Simpson's Paradox** | 5.1 – 5.4 | `GROUP BY` Segment |

        **Kernbotschaft:** Ein Unterschied ist nur dann aussagekräftig, wenn er
        **statistisch signifikant** *und* **praktisch relevant** ist — und wir auf
        **Confounding Variables** geprüft haben.

        **Nächste Session:** Zeitreihenanalyse — LAG, LEAD, Moving Averages
        """
    )
    return


if __name__ == "__main__":
    app.run()
