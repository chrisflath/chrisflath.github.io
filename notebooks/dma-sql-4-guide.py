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
    app_title="DMA Session 4: CRISP-DM & Fallstudien — Guide",
)


@app.cell(hide_code=True)
def _():
    import marimo as mo
    return (mo,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        # Session 4: CRISP-DM & Fallstudien — Guide

        **Kursfahrplan:** **▸ I: SQL-Grundlagen (S1–4)** · II: Datenmodellierung (S5–7) · III: Fortgeschrittenes SQL (S8–9) · IV: Datenanalyse (S10–13)

        ### Lernziele

        Nach dieser Session können Sie:

        - Den **CRISP-DM** Prozess beschreiben und anwenden
        - **Anomalieerkennung** bei Mortalitätsdaten durchführen (Fallstudie Shipman)
        - **Benford's Law** zur Betrugserkennung erklären
        - Den richtigen **Visualisierungstyp** für Datenanalysen wählen

        ---
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ## Daten laden

        Wir arbeiten heute mit:
        1. **Todesfälle** aus der Shipman-Untersuchung
        2. **Rechnungsbeträge** für Benford-Analyse
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    import polars as pl

    try:
        url = "https://chrisflath.github.io/notebooks/public/todesfaelle.csv"
        todesfaelle = pl.read_csv(url)
    except Exception:
        todesfaelle = pl.DataFrame({
            "Arzt": (["Shipman"] * 15 + ["Referenz"] * 10),
            "Geschlecht": ["W", "W", "M", "W", "W", "M", "W", "W", "M", "W",
                           "W", "M", "W", "W", "W",
                           "W", "M", "W", "M", "W", "W", "M", "W", "M", "W"],
            "Alter": [76, 82, 71, 79, 84, 68, 91, 77, 73, 88,
                      80, 65, 85, 74, 81,
                      85, 79, 72, 66, 90, 78, 81, 87, 69, 83],
            "Todesstunde": [14, 15, 13, 14, 16, 15, 14, 13, 15, 14,
                            16, 14, 15, 13, 14,
                            3, 22, 8, 17, 1, 11, 19, 6, 14, 23],
        })
        mo.callout(
            mo.md("**Hinweis:** Todesfälle-Daten konnten nicht geladen werden. Es werden Beispieldaten verwendet."),
            kind="warn",
        )

    import random
    import math
    random.seed(42)
    echte_betraege = [round(10 ** (random.uniform(1, 4)), 2) for _ in range(200)]
    verdächtige_betraege = [random.randint(10, 999) + random.random() for _ in range(200)]

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
    return math, pl, rechnungen, rechnungen_echt, rechnungen_verdächtig, todesfaelle


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ---

        ## Phase 1: Der CRISP-DM Prozess

        CRISP-DM (**CR**oss **I**ndustry **S**tandard **P**rocess for **D**ata **M**ining) ist der Standard-Prozess für Datenanalyse-Projekte:

        ```
        Business Understanding → Data Understanding → Data Preparation
                ↑                                              ↓
           Deployment ← Evaluation ← Modeling
        ```

        | Phase | Beschreibung | Shipman-Beispiel |
        |-------|-------------|------------------|
        | Business Understanding | Problem definieren | Ungewöhnlich viele Todesfälle? |
        | Data Understanding | Daten erkunden | Mortalitätsdaten sammeln |
        | Data Preparation | Daten bereinigen | Todesstunden kodieren |
        | Modeling | Analyse durchführen | Statistische Vergleiche |
        | Evaluation | Ergebnisse prüfen | Signifikante Abweichungen? |
        | Deployment | Lösung einsetzen | Überwachungssystem |

        **Wichtig:** Der Prozess ist **iterativ** — man springt häufig zwischen Phasen zurück, wenn neue Erkenntnisse die Fragestellung verändern.
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Vorhersage: CRISP-DM Reihenfolge
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    pred_crisp = mo.ui.radio(
        options={
            "business": "Business Understanding",
            "data_prep": "Data Preparation",
            "modeling": "Modeling",
            "evaluation": "Evaluation",
        },
        label="**Vorhersage:** Welche CRISP-DM Phase kommt *vor* der Datenanalyse (Modeling)?",
    )
    pred_crisp
    return (pred_crisp,)


@app.cell(hide_code=True)
def _(mo, pred_crisp):
    if pred_crisp.value == "business":
        mo.output.replace(
            mo.md(
                "✅ **Richtig!** **Business Understanding** ist immer der erste Schritt. "
                "Bevor Sie Daten analysieren, müssen Sie das Geschäftsproblem verstehen: "
                "Was genau wollen wir herausfinden? Welche Entscheidung hängt davon ab? "
                "Ohne dieses Verständnis ist jede Analyse ziellos."
            )
        )
    elif pred_crisp.value == "data_prep":
        mo.output.replace(
            mo.md(
                "❌ Data Preparation kommt zwar vor Modeling, aber es ist nicht die *erste* Phase. "
                "Vor der Datenaufbereitung müssen Sie zuerst das Problem verstehen (**Business Understanding**) "
                "und die verfügbaren Daten erkunden (**Data Understanding**)."
            )
        )
    elif pred_crisp.value == "modeling":
        mo.output.replace(
            mo.md(
                "❌ Modeling ist die Phase, auf die wir uns beziehen — die Frage war, was *davor* kommt. "
                "Die richtige Antwort ist **Business Understanding**: Erst das Problem verstehen, dann analysieren."
            )
        )
    elif pred_crisp.value == "evaluation":
        mo.output.replace(
            mo.md(
                "❌ Evaluation kommt *nach* dem Modeling, nicht davor. "
                "Die richtige Reihenfolge: Business Understanding → Data Understanding → "
                "Data Preparation → **Modeling** → Evaluation → Deployment."
            )
        )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ---

        ## Fallstudie I: Dr. Harold Shipman

        **Hintergrund:**
        - Britischer Hausarzt (1946–2004)
        - Mindestens **215 Patienten ermordet** — einer der schlimmsten Serienmörder der Geschichte
        - Erst **1998** durch eine gefälschte Testamentsurkunde entdeckt
        - **Statistische Anomalien waren jahrelang sichtbar**, wurden aber nie systematisch untersucht

        Die Shipman-Untersuchung zeigte: Mit den richtigen Datenanalyse-Werkzeugen hätte man das Muster
        Jahre früher erkennen können. Genau die SQL-Werkzeuge, die Sie in Sessions 1–3 gelernt haben
        (GROUP BY, COUNT, AVG), reichen dafür aus.

        ---
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Geführtes Beispiel 1.1: Todesfälle pro Arzt
    """)
    return


@app.cell(hide_code=True)
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
        **Beobachtung:** Shipman hat deutlich mehr Todesfälle als die Referenzgruppe — das ist die erste Anomalie.

        ---

        ### Geführtes Beispiel 1.2: Todesfälle nach Tageszeit

        Natürliche Todesfälle verteilen sich über den gesamten Tag. Mordopfer sterben oft während der „Arbeitszeit" des Täters.
        """
    )
    return


@app.cell(hide_code=True)
def _(mo, todesfaelle):
    _df = mo.sql(
        f"""
        SELECT
            Arzt,
            CASE
                WHEN Todesstunde BETWEEN 9 AND 17 THEN 'Praxiszeit (9-17)'
                ELSE 'Außerhalb'
            END AS Zeitraum,
            COUNT(*) AS Anzahl
        FROM todesfaelle
        GROUP BY Arzt, Zeitraum
        ORDER BY Arzt, Zeitraum
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        **Beobachtung:** Bei Shipman sterben fast alle Patienten während der Praxiszeit — bei der Referenzgruppe verteilen sich die Todesfälle gleichmäßiger.

        ---

        ### Referenzverteilung: Todesfälle nach Tageszeit

        Die folgende Grafik vergleicht die prozentuale Verteilung der Todesfälle nach Tageszeit.
        Die **Referenzdaten** stammen aus dem Buch *Art of Statistics* (David Spiegelhalter)
        und zeigen das typische Muster anderer Ärzte im Vergleich zu Shipman.
        """
    )
    return


@app.cell(hide_code=True)
def _():
    import plotly.express as px
    return (px,)


@app.cell(hide_code=True)
def _(pl, px):
    referenz = pl.DataFrame({
        "Stunde": list(range(24)),
        "Shipman": [2.6, 1.0, 2.6, 3.0, 0.3, 1.2, 2.9, 1.8, 3.6, 2.6,
                    4.6, 5.8, 2.0, 9.0, 14.1, 13.0, 9.0, 5.8, 3.8, 2.9,
                    3.6, 0.8, 3.6, 2.0],
        "Vergleichsgruppe": [1.1, 3.0, 3.1, 3.8, 4.0, 4.3, 4.2, 4.1, 3.4, 5.6,
                             5.5, 5.8, 4.0, 3.8, 2.0, 3.4, 6.6, 5.2, 3.3, 5.0,
                             4.1, 3.8, 2.9, 4.1],
    })

    ref_long = referenz.unpivot(
        index="Stunde",
        on=["Shipman", "Vergleichsgruppe"],
        variable_name="Gruppe",
        value_name="Prozent",
    )

    fig_ref = px.line(
        ref_long,
        x="Stunde",
        y="Prozent",
        color="Gruppe",
        title="Verteilung der Todesfälle nach Tageszeit (%, Referenzdaten)",
        labels={"Stunde": "Todesstunde", "Prozent": "Anteil (%)", "Gruppe": ""},
        color_discrete_map={"Shipman": "#d62728", "Vergleichsgruppe": "#1f77b4"},
        markers=True,
    )
    fig_ref.update_layout(xaxis=dict(dtick=1))
    fig_ref
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        **Beobachtung:** Die Vergleichsgruppe zeigt eine relativ gleichmäßige Verteilung über den Tag.
        Shipmans Todesfälle konzentrieren sich dagegen stark auf die Nachmittagsstunden (13–16 Uhr)
        — genau seine typische Hausbesuchszeit.

        ---

        **Jetzt zum Übungs-Notebook → Aufgaben 2.x**

        ---
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Phase 3: Anomalieerkennung — Altersverteilung

    ### Vorhersage: Altersverteilung der Opfer
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    pred_age = mo.ui.radio(
        options={
            "correct": "Shipmans Opfer sind im Schnitt deutlich älter",
            "wrong1": "Alle Ärzte haben ähnliche Altersverteilungen",
            "wrong2": "Shipmans Opfer sind jünger als bei anderen Ärzten",
        },
        label="**Vorhersage:** Wie unterscheidet sich das Durchschnittsalter der Verstorbenen bei Shipman vs. anderen Ärzten?",
    )
    pred_age
    return (pred_age,)


@app.cell(hide_code=True)
def _(mo, pred_age):
    if pred_age.value == "correct":
        mo.output.replace(
            mo.md(
                "✅ **Richtig!** Shipmans Opfer waren überwiegend ältere Patientinnen — "
                "das ist eines der Muster, das die Ermittler schließlich auf seine Spur brachte. "
                "Er wählte gezielt vulnerable, alleinstehende ältere Menschen."
            )
        )
    elif pred_age.value == "wrong1":
        mo.output.replace(
            mo.md(
                "❌ Nicht ganz. Shipman wählte gezielt ältere, alleinstehende Patientinnen. "
                "Das Durchschnittsalter seiner Opfer weicht deutlich von der Referenzgruppe ab."
            )
        )
    elif pred_age.value == "wrong2":
        mo.output.replace(
            mo.md(
                "❌ Im Gegenteil — Shipmans Opfer waren im Schnitt **älter**, nicht jünger. "
                "Er suchte gezielt ältere Patientinnen, bei denen ein natürlicher Tod plausibler erschien."
            )
        )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Geführtes Beispiel: Altersstatistik nach Arzt
    """)
    return


@app.cell(hide_code=True)
def _(mo, todesfaelle):
    _df = mo.sql(
        f"""
        SELECT
            Arzt,
            ROUND(AVG(Alter), 1) AS Durchschnittsalter,
            MIN(Alter) AS Jüngster,
            MAX(Alter) AS Ältester,
            COUNT(*) AS Anzahl
        FROM todesfaelle
        GROUP BY Arzt
        ORDER BY Durchschnittsalter DESC
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        **Beobachtung:** Shipmans Opfer haben ein anderes Altersprofil als die Referenzgruppe. Solche Abweichungen in demografischen Mustern sind ein starkes Signal für Anomalieerkennung.

        ---

        **Jetzt zum Übungs-Notebook → Aufgaben 4.x**

        ---
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ## Phase 5: Benford's Law — Betrugserkennung durch Ziffernanalyse

        **Das Gesetz der ersten Ziffer:**

        In natürlich gewachsenen Datensätzen beginnen Zahlen überraschend häufig mit kleinen Ziffern:

        | Ziffer | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 |
        |--------|------|------|------|-----|-----|-----|-----|-----|-----|
        | Erwartet (%) | 30.1 | 17.6 | 12.5 | 9.7 | 7.9 | 6.7 | 5.8 | 5.1 | 4.6 |

        **Warum?** Weil natürliche Zahlen oft **multiplikativ wachsen**. Die Formel lautet:
        P(d) = log₁₀(1 + 1/d)

        **Anwendung:** Wenn Zahlen manipuliert oder erfunden werden, weichen sie oft von dieser Verteilung ab — das nutzen Prüfer und Forensiker zur Betrugserkennung!
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Geführtes Beispiel 2.1: Erste Ziffer extrahieren

    Um Benford anzuwenden, müssen wir die erste Ziffer jeder Zahl extrahieren:
    """)
    return


@app.cell(hide_code=True)
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
    mo.md(r"""
    ### Geführtes Beispiel 2.2: Benford-Verteilung berechnen

    Jetzt zählen wir, wie oft jede erste Ziffer vorkommt — getrennt nach echten und verdächtigen Rechnungen:
    """)
    return


@app.cell(hide_code=True)
def _(mo, rechnungen):
    benford_analyse = mo.sql(
        f"""
        SELECT
            kategorie,
            CAST(SUBSTR(CAST(CAST(betrag AS INT) AS TEXT), 1, 1) AS INT)
                AS erste_ziffer,
            COUNT(*) AS anzahl
        FROM rechnungen
        WHERE betrag >= 10
        GROUP BY kategorie, erste_ziffer
        ORDER BY kategorie, erste_ziffer
        """
    )
    return (benford_analyse,)


@app.cell(hide_code=True)
def _(benford_analyse, px):
    fig_benford = px.bar(
        benford_analyse,
        x="erste_ziffer",
        y="anzahl",
        color="kategorie",
        barmode="group",
        title="Benford-Analyse: Echte vs. Verdächtige Rechnungen",
        labels={"erste_ziffer": "Erste Ziffer", "anzahl": "Anzahl", "kategorie": "Kategorie"},
    )
    fig_benford
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        **Beobachtung:**
        - **Echte Rechnungen:** Mehr 1er und 2er — wie Benford vorhersagt
        - **Verdächtige Rechnungen:** Gleichmäßiger verteilt — ein klares Warnsignal!

        ---
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Vorhersage: Welche Daten folgen Benford's Law?
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    pred_benford = mo.ui.radio(
        options={
            "aktien": "Aktienkurse",
            "groessen": "Körpergrößen von Studierenden",
            "lotto": "Lottozahlen",
            "hausnummern": "Hausnummern in einer Stadt",
        },
        label="**Vorhersage:** Welcher Datensatz folgt Benford's Law am wahrscheinlichsten?",
    )
    pred_benford
    return (pred_benford,)


@app.cell(hide_code=True)
def _(mo, pred_benford):
    if pred_benford.value == "aktien":
        mo.output.replace(
            mo.md(
                "✅ **Richtig!** **Aktienkurse** wachsen multiplikativ (prozentuale Veränderungen), "
                "und genau solche Daten folgen Benford's Law. Über mehrere Größenordnungen hinweg "
                "beginnen die Kurswerte häufiger mit kleinen Ziffern."
            )
        )
    elif pred_benford.value == "groessen":
        mo.output.replace(
            mo.md(
                "❌ **Körpergrößen** folgen Benford's Law nicht. Sie liegen in einem engen Wertebereich "
                "(ca. 150–200 cm) und sind normalverteilt. Benford braucht Daten, die sich über "
                "**mehrere Größenordnungen** erstrecken."
            )
        )
    elif pred_benford.value == "lotto":
        mo.output.replace(
            mo.md(
                "❌ **Lottozahlen** sind gleichverteilte Zufallszahlen in einem festen Bereich (z.B. 1–49). "
                "Sie folgen Benford's Law nicht, weil sie nicht natürlich gewachsen sind — "
                "jede Zahl hat die gleiche Wahrscheinlichkeit."
            )
        )
    elif pred_benford.value == "hausnummern":
        mo.output.replace(
            mo.md(
                "❌ **Hausnummern** werden zugewiesen und folgen einem festen Vergabeschema. "
                "Sie sind nicht natürlich gewachsen und erstrecken sich nicht über viele Größenordnungen. "
                "Benford's Law braucht multiplikativ wachsende Daten wie **Aktienkurse**."
            )
        )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ---

        **Jetzt zum Übungs-Notebook → Aufgaben 6.x**

        ---
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ## Phase 7: Visualisierung — Den richtigen Charttyp wählen

        Gute Datenanalyse braucht die richtige Visualisierung. Hier nochmals die beiden
        zentralen Grafiken dieser Session:

        1. **Liniendiagramm** für die zeitliche Verteilung (Shipman vs. Vergleichsgruppe)
        2. **Balkendiagramm** für die Benford-Abweichung (Echte vs. Verdächtige Rechnungen)

        Die Wahl des Charttyps hängt vom **Datentyp** und der **Fragestellung** ab:

        | Charttyp | Gut für | Beispiel |
        |----------|---------|----------|
        | Balkendiagramm | Kategorien vergleichen | Tore pro Position |
        | Liniendiagramm | Entwicklung über Zeit/Sequenz | Todesfälle nach Stunde |
        | Streudiagramm | Zusammenhang zweier Variablen | Alter vs. Tore |
        | Histogramm | Verteilung einer Variable | Altersverteilung |
        """
    )
    return


@app.cell(hide_code=True)
def _(mo, math, pl, px, rechnungen_echt):
    benford_erwartung = pl.DataFrame({
        "ziffer": list(range(1, 10)),
        "benford_pct": [math.log10(1 + 1 / d) * 100 for d in range(1, 10)],
    })

    echt_ziffern = rechnungen_echt.filter(pl.col("betrag") >= 10).with_columns(
        pl.col("betrag").cast(pl.Int64).cast(pl.Utf8).str.slice(0, 1).cast(pl.Int64).alias("erste_ziffer")
    )
    echt_counts = echt_ziffern.group_by("erste_ziffer").agg(
        pl.len().alias("anzahl")
    ).sort("erste_ziffer")
    total = echt_ziffern.height
    echt_counts = echt_counts.with_columns(
        (pl.col("anzahl") / total * 100).alias("beobachtet_pct")
    )

    abweichung = echt_counts.join(
        benford_erwartung, left_on="erste_ziffer", right_on="ziffer"
    ).with_columns(
        (pl.col("beobachtet_pct") - pl.col("benford_pct")).alias("abweichung")
    )

    fig_abw = px.bar(
        abweichung,
        x="erste_ziffer",
        y="abweichung",
        title="Abweichung der echten Rechnungen von Benford's Law (Prozentpunkte)",
        labels={"erste_ziffer": "Erste Ziffer", "abweichung": "Abweichung (pp)"},
        color="abweichung",
        color_continuous_scale=["#d62728", "#f7f7f7", "#1f77b4"],
        color_continuous_midpoint=0,
    )
    fig_abw.update_layout(xaxis=dict(dtick=1))
    fig_abw
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Viz-Choice: Den richtigen Charttyp wählen
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    viz_choice_4 = mo.ui.radio(
        options={
            "bar": "Balkendiagramm",
            "line": "Liniendiagramm",
            "pie": "Kreisdiagramm",
            "scatter": "Streudiagramm",
        },
        label="Abweichung jeder Ziffer von der Benford-Erwartung darstellen — welcher Charttyp?",
    )
    viz_choice_4
    return (viz_choice_4,)


@app.cell(hide_code=True)
def _(mo, viz_choice_4):
    if viz_choice_4.value == "bar":
        mo.output.replace(
            mo.md(
                "✅ **Richtig!** Ein **Balkendiagramm** ist ideal, um die Abweichung pro Ziffer darzustellen. "
                "Jede Ziffer ist eine Kategorie, und die Balkenhöhe zeigt die Abweichung — "
                "positive und negative Werte sind sofort erkennbar."
            )
        )
    elif viz_choice_4.value == "line":
        mo.output.replace(
            mo.md(
                "❌ Nicht ganz. Ein Liniendiagramm suggeriert eine **Verbindung** zwischen den Datenpunkten "
                "und eignet sich für Zeitreihen. Die Ziffern 1–9 haben zwar eine Reihenfolge, aber die "
                "Abweichungen sind unabhängige Kategorien — ein **Balkendiagramm** passt besser."
            )
        )
    elif viz_choice_4.value == "pie":
        mo.output.replace(
            mo.md(
                "❌ Ein Kreisdiagramm zeigt Anteile am Ganzen (z.B. '30% beginnen mit 1'). "
                "Für **Abweichungen** (die positiv oder negativ sein können) ist es ungeeignet. "
                "Ein **Balkendiagramm** kann positive und negative Werte direkt darstellen."
            )
        )
    elif viz_choice_4.value == "scatter":
        mo.output.replace(
            mo.md(
                "❌ Streudiagramme zeigen den **Zusammenhang** zweier numerischer Variablen. "
                "Hier vergleichen wir kategorische Werte (Ziffern) mit ihren Abweichungen — "
                "ein **Balkendiagramm** eignet sich dafür besser."
            )
        )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## Selbsttest
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    selbsttest_4 = mo.ui.radio(
        options={
            "zeitlich": "Die zeitliche Konzentration der Todesfälle auf die Nachmittagsstunden",
            "alter": "Das Durchschnittsalter der Opfer",
            "gleichverteilt": "Die gleichmäßige Verteilung über alle Tageszeiten",
        },
        label="Welche Anomalie fiel bei Shipmans Todesfällen am stärksten auf?",
    )
    selbsttest_4
    return (selbsttest_4,)


@app.cell(hide_code=True)
def _(mo, selbsttest_4):
    if selbsttest_4.value == "zeitlich":
        mo.output.replace(
            mo.md(
                "✅ **Richtig!** Die auffälligste Anomalie war die extreme **Konzentration auf die "
                "Nachmittagsstunden** (13–16 Uhr). Während bei anderen Ärzten die Todesfälle "
                "gleichmäßig über den Tag verteilt waren, starben Shipmans Patienten fast "
                "ausschließlich während seiner Hausbesuchszeit."
            )
        )
    elif selbsttest_4.value == "alter":
        mo.output.replace(
            mo.md(
                "❌ Das Durchschnittsalter war zwar auch auffällig, aber nicht die **stärkste** Anomalie. "
                "Am deutlichsten war die **zeitliche Konzentration**: Fast alle Todesfälle fielen in "
                "Shipmans Nachmittags-Sprechstunden — ein Muster, das bei keinem anderen Arzt zu finden war."
            )
        )
    elif selbsttest_4.value == "gleichverteilt":
        mo.output.replace(
            mo.md(
                "❌ Eine gleichmäßige Verteilung wäre gerade **keine** Anomalie — das ist das erwartete Muster "
                "bei natürlichen Todesfällen. Die Anomalie bei Shipman war die **ungleichmäßige** Verteilung: "
                "eine extreme Häufung in den Nachmittagsstunden."
            )
        )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ---

        ## Zusammenfassung

        ### CRISP-DM
        | Phase | Beschreibung |
        |-------|--------------|
        | Business Understanding | Problem definieren |
        | Data Understanding | Daten erkunden |
        | Data Preparation | Daten bereinigen |
        | Modeling | Analyse durchführen |
        | Evaluation | Ergebnisse prüfen |
        | Deployment | Lösung einsetzen |

        ### Anomalieerkennung (Shipman)
        - Vergleichen Sie Kennzahlen zwischen Gruppen (COUNT, AVG)
        - Achten Sie auf **zeitliche Muster** (CASE WHEN + GROUP BY)
        - Prüfen Sie **demografische Verteilungen** (Alter, Geschlecht)
        - Die stärkste Anomalie: Konzentration der Todesfälle auf die Praxiszeit

        ### Benford's Law
        - Erste Ziffer extrahieren mit `SUBSTR(CAST(... AS TEXT), 1, 1)`
        - Erwartung: ~30% der Zahlen beginnen mit 1
        - Abweichungen von der Benford-Verteilung deuten auf Manipulation hin
        - Funktioniert bei multiplikativ wachsenden Daten (Umsätze, Aktienkurse, Einwohnerzahlen)

        ### Ausblick Session 5: Datenmodellierung — Von Anomalien zum ER-Modell
        """
    )
    return


if __name__ == "__main__":
    app.run()
