import marimo

__generated_with = "0.13.0"
app = marimo.App(
    width="medium",
    app_title="DMA Session 6: ER-Modellierung",
)


@app.cell(hide_code=True)
def _():
    import marimo as mo
    return (mo,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        # Session 6: Entity-Relationship-Modellierung

        In dieser Session lernen Sie:

        - **Entitäten** und **Attribute** modellieren
        - **Beziehungen** zwischen Entitäten definieren
        - **Kardinalitäten** (1:1, 1:N, M:N) bestimmen
        - Die **Chen-Notation** für ER-Diagramme

        **Hinweis:** ER-Modellierung ist primär eine Papier-/Whiteboard-Übung.
        Dieses Notebook dient zur Vertiefung und Selbsttest.

        ---
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ## Rückblick: Session 5

        In der letzten Session haben wir gesehen:

        - **Redundanz** führt zu Anomalien
        - **Lösung:** Daten auf mehrere Tabellen aufteilen
        - **Primär-** und **Fremdschlüssel** verbinden Tabellen

        **Die Frage:** Wie wissen wir, *welche* Tabellen wir brauchen?

        → **ER-Modellierung** gibt uns eine systematische Methode!

        ---
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ## Kernkonzepte

        | Element | Symbol | Beschreibung |
        |---------|--------|--------------|
        | **Entität** | Rechteck | Ein "Ding" der realen Welt (Spieler, Verein) |
        | **Attribut** | Ellipse | Eigenschaft einer Entität (Name, Alter) |
        | **Schlüssel** | Unterstrichen | Eindeutige Identifikation |
        | **Beziehung** | Raute | Verbindung zwischen Entitäten |

        ---
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
## Crow's Foot Notation (Kardinalitäten)

In ER-Diagrammen verwenden wir oft die **Crow's Foot Notation**:

| Symbol | Bedeutung |
|--------|-----------|
| `\|\|` (Strich) | Genau eins |
| `o\|` (Kreis + Strich) | Null oder eins |
| `\|{` (Strich + Gabel) | Eins oder mehr |
| `o{` (Kreis + Gabel) | Null oder mehr |

**Beispiel:** `VEREIN \|\|--\|{ SPIELER` bedeutet: Ein Verein hat *eins oder mehr* Spieler.

---
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ## Quiz: Kardinalitäten bestimmen

        Bestimmen Sie für jedes Beispiel die richtige Kardinalität!
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    # Quiz 1
    quiz1 = mo.ui.radio(
        options={
            "1:1": "1:1 (Eins zu Eins)",
            "1:N": "1:N (Eins zu Viele)",
            "M:N": "M:N (Viele zu Viele)"
        },
        label="**Frage 1:** Verein ↔ Spieler (ein Spieler spielt für einen Verein)"
    )
    quiz1
    return (quiz1,)


@app.cell(hide_code=True)
def _(mo, quiz1):
    if quiz1.value == "1:N":
        mo.output.replace(mo.md("✅ **Richtig!** Ein Verein hat viele Spieler, aber jeder Spieler gehört zu einem Verein."))
    elif quiz1.value:
        mo.output.replace(mo.md("❌ Nicht ganz. Denken Sie daran: Ein Verein kann *viele* Spieler haben."))
    return


@app.cell(hide_code=True)
def _(mo):
    # Quiz 2
    quiz2 = mo.ui.radio(
        options={
            "1:1": "1:1 (Eins zu Eins)",
            "1:N": "1:N (Eins zu Viele)",
            "M:N": "M:N (Viele zu Viele)"
        },
        label="**Frage 2:** Student ↔ Kurs (Studierende können mehrere Kurse besuchen, Kurse haben mehrere Studierende)"
    )
    quiz2
    return (quiz2,)


@app.cell(hide_code=True)
def _(mo, quiz2):
    if quiz2.value == "M:N":
        mo.output.replace(mo.md("✅ **Richtig!** Beide Seiten können mit vielen auf der anderen verbunden sein."))
    elif quiz2.value:
        mo.output.replace(mo.md("❌ Nicht ganz. Auf *beiden* Seiten sind mehrere möglich."))
    return


@app.cell(hide_code=True)
def _(mo):
    # Quiz 3
    quiz3 = mo.ui.radio(
        options={
            "1:1": "1:1 (Eins zu Eins)",
            "1:N": "1:N (Eins zu Viele)",
            "M:N": "M:N (Viele zu Viele)"
        },
        label="**Frage 3:** Person ↔ Personalausweis (jede Person hat genau einen Ausweis)"
    )
    quiz3
    return (quiz3,)


@app.cell(hide_code=True)
def _(mo, quiz3):
    if quiz3.value == "1:1":
        mo.output.replace(mo.md("✅ **Richtig!** Jede Person hat genau einen Ausweis, und jeder Ausweis gehört zu genau einer Person."))
    elif quiz3.value:
        mo.output.replace(mo.md("❌ Nicht ganz. Eine Person hat *genau einen* Ausweis (nicht mehrere)."))
    return


@app.cell(hide_code=True)
def _(mo):
    # Quiz 4
    quiz4 = mo.ui.radio(
        options={
            "1:1": "1:1 (Eins zu Eins)",
            "1:N": "1:N (Eins zu Viele)",
            "M:N": "M:N (Viele zu Viele)"
        },
        label="**Frage 4:** Autor ↔ Buch (ein Buch kann mehrere Autoren haben, Autoren schreiben mehrere Bücher)"
    )
    quiz4
    return (quiz4,)


@app.cell(hide_code=True)
def _(mo, quiz4):
    if quiz4.value == "M:N":
        mo.output.replace(mo.md("✅ **Richtig!** Co-Autoren und Vielschreiber → M:N!"))
    elif quiz4.value:
        mo.output.replace(mo.md("❌ Nicht ganz. Denken Sie an Co-Autoren: Ein Buch kann *mehrere* Autoren haben."))
    return


@app.cell(hide_code=True)
def _(mo):
    # Quiz 5
    quiz5 = mo.ui.radio(
        options={
            "1:1": "1:1 (Eins zu Eins)",
            "1:N": "1:N (Eins zu Viele)",
            "M:N": "M:N (Viele zu Viele)"
        },
        label="**Frage 5:** Abteilung ↔ Mitarbeiter (jeder Mitarbeiter gehört zu einer Abteilung)"
    )
    quiz5
    return (quiz5,)


@app.cell(hide_code=True)
def _(mo, quiz5):
    if quiz5.value == "1:N":
        mo.output.replace(mo.md("✅ **Richtig!** Eine Abteilung hat viele Mitarbeiter, aber jeder Mitarbeiter ist in einer Abteilung."))
    elif quiz5.value:
        mo.output.replace(mo.md("❌ Nicht ganz. Eine Abteilung hat *viele* Mitarbeiter."))
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ---

        ## Häufige Kardinalitäten

        | Kardinalität | Beispiele | Häufigkeit |
        |--------------|-----------|------------|
        | **1:1** | Person-Ausweis, Land-Hauptstadt | Selten |
        | **1:N** | Abteilung-Mitarbeiter, Verein-Spieler, Kunde-Bestellung | **Sehr häufig** |
        | **M:N** | Student-Kurs, Autor-Buch, Schauspieler-Film | Häufig |

        **Faustregel:** Die meisten Beziehungen sind 1:N!

        ---
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ## Übung: Entitäten und Beziehungen identifizieren

        Lesen Sie die folgende Beschreibung und identifizieren Sie:
        1. Welche **Entitäten** gibt es?
        2. Welche **Beziehungen** bestehen?
        3. Welche **Kardinalitäten** haben diese?
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ### Szenario: Fußball-Liga

        *„In einer Fußball-Liga spielen mehrere Vereine. Jeder Verein hat einen Namen,
        einen Ort und ein Gründungsjahr. Spieler gehören zu einem Verein und haben
        einen Namen, eine Position und ein Geburtsdatum. Vereine spielen Spiele
        gegeneinander, wobei jedes Spiel an einem bestimmten Datum stattfindet
        und ein Ergebnis (Tore Heim, Tore Gast) hat."*

        ---
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.accordion({
        "Lösung anzeigen": mo.md(r"""
**Entitäten:**
- **Verein** (Name, Ort, Gründungsjahr)
- **Spieler** (Name, Position, Geburtsdatum)
- **Spiel** (Datum, Tore_Heim, Tore_Gast)

**Beziehungen:**
1. Spieler **spielt für** Verein → **1:N** (ein Verein hat viele Spieler)
2. Verein **spielt** Spiel → **2:N** (jedes Spiel hat 2 Vereine; Heim und Gast)

**Alternativ:** Spiel als Beziehung zwischen zwei Vereinen modellieren (mit Attributen für Datum und Ergebnis)
        """)
    })
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
### ER-Diagramm: Fußball-Liga (Mermaid)

Das folgende Diagramm zeigt die Lösung in der **Crow's Foot Notation**:
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.mermaid(
        """
        erDiagram
            VEREIN ||--|{ SPIELER : hat
            VEREIN ||--|{ SPIEL : "spielt (Heim)"
            VEREIN ||--|{ SPIEL : "spielt (Gast)"

            VEREIN {
                int ID PK
                string Name
                string Ort
                int Gruendungsjahr
            }

            SPIELER {
                int ID PK
                string Name
                string Position
                date Geburtsdatum
                int Verein_ID FK
            }

            SPIEL {
                int ID PK
                date Datum
                int Tore_Heim
                int Tore_Gast
                int Heim_ID FK
                int Gast_ID FK
            }
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
---

## Beispiel: Online-Shop (M:N-Beziehung)

Ein Online-Shop mit Kunden, Bestellungen und Produkten:
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.mermaid(
        """
        erDiagram
            KUNDE ||--o{ BESTELLUNG : "gibt auf"
            BESTELLUNG ||--|{ BESTELLPOSITION : enthaelt
            PRODUKT ||--o{ BESTELLPOSITION : "ist in"
            KATEGORIE ||--o{ PRODUKT : beinhaltet

            KUNDE {
                int ID PK
                string Name
                string Email UK
            }

            BESTELLUNG {
                int ID PK
                date Datum
                int Kunde_ID FK
            }

            BESTELLPOSITION {
                int Bestellung_ID PK,FK
                int Produkt_ID PK,FK
                int Menge
            }

            PRODUKT {
                int ID PK
                string Name
                decimal Preis
                int Kategorie_ID FK
            }

            KATEGORIE {
                int ID PK
                string Name
            }
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
**Beobachtungen:**

- **1:N:** Kunde → Bestellung, Kategorie → Produkt
- **M:N:** Bestellung ↔ Produkt (aufgelöst durch Bestellposition)
- Die **Bestellposition** ist eine Beziehungstabelle mit zusammengesetztem Primärschlüssel

*In Session 7 werden wir dieses Modell in SQL CREATE TABLE umsetzen!*

---
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ## (Min,Max)-Notation

        Genauere Kardinalitätsangabe:

        | Notation | Bedeutung |
        |----------|-----------|
        | **(0,1)** | Optional, höchstens einer |
        | **(1,1)** | Genau einer (Pflicht) |
        | **(0,N)** | Optional, beliebig viele |
        | **(1,N)** | Mindestens einer, beliebig viele |
        | **(15,30)** | Zwischen 15 und 30 |

        **Beispiel:** Ein Bundesliga-Verein hat **(15,30)** Spieler im Kader.

        ---
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ## Zusammenfassung

        | Schritt | Frage |
        |---------|-------|
        | 1. Entitäten | Was sind die "Dinge"? |
        | 2. Attribute | Welche Eigenschaften haben sie? |
        | 3. Schlüssel | Was macht sie eindeutig? |
        | 4. Beziehungen | Wie hängen sie zusammen? |
        | 5. Kardinalitäten | Wie viele auf jeder Seite? |

        **Werkzeuge:** Papier, Whiteboard, draw.io, Lucidchart

        **Nächste Session:** ER-Modell → Relationales Schema → SQL CREATE TABLE
        """
    )
    return


if __name__ == "__main__":
    app.run()
