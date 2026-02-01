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
    # Quiz 6
    quiz6 = mo.ui.radio(
        options={
            "attribut": "Attribut (Eigenschaft einer Entität)",
            "entitaet": "Entität (eigenständiges Objekt)",
            "beziehung": "Beziehung (Verbindung zwischen Entitäten)"
        },
        label="**Frage 6:** Ist 'Raumnummer' in einem Universitätssystem ein Attribut oder eine Entität?"
    )
    quiz6
    return (quiz6,)


@app.cell(hide_code=True)
def _(mo, quiz6):
    if quiz6.value == "attribut":
        mo.output.replace(mo.md("✅ **Richtig!** Raumnummer ist typischerweise ein Attribut von z.B. einer Veranstaltung. *Aber:* Wenn Räume eigene Eigenschaften haben (Kapazität, Gebäude, Beamer), könnte 'Raum' auch eine eigene Entität sein!"))
    elif quiz6.value == "entitaet":
        mo.output.replace(mo.md("⚠️ **Möglich!** Wenn Räume eigene Eigenschaften haben (Kapazität, Ausstattung), kann 'Raum' eine Entität sein. Die einfache 'Raumnummer' allein ist aber eher ein Attribut."))
    elif quiz6.value:
        mo.output.replace(mo.md("❌ Nicht ganz. Eine Raumnummer ist eine Eigenschaft, keine Verbindung zwischen Objekten."))
    return


@app.cell(hide_code=True)
def _(mo):
    # Quiz 7
    quiz7 = mo.ui.radio(
        options={
            "weak": "Schwache Entität (existiert nicht ohne Buch)",
            "strong": "Starke Entität (existiert unabhängig)",
            "beziehung": "Beziehung (Verbindung zwischen Buch und Regal)",
            "attribut": "Attribut von Buch"
        },
        label="**Frage 7:** Ein Bibliotheks-Exemplar hat nur zusammen mit dem Buchtitel eine eindeutige ID (Buch-ISBN + Exemplar-Nr). Was ist es?"
    )
    quiz7
    return (quiz7,)


@app.cell(hide_code=True)
def _(mo, quiz7):
    if quiz7.value == "weak":
        mo.output.replace(mo.md("✅ **Richtig!** Ein Exemplar kann ohne das zugehörige Buch nicht existieren und hat keinen eigenständigen Schlüssel. Das ist eine **schwache Entität** mit einer **identifizierenden Beziehung** zum Buch."))
    elif quiz7.value:
        mo.output.replace(mo.md("❌ Nicht ganz. Das Exemplar braucht den Schlüssel des Buches, um eindeutig identifiziert zu werden. Es ist existenzabhängig vom Buch."))
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
        ---

        ## Übung: Bibliotheks-Szenario

        Identifizieren Sie die Entitäten, Beziehungen und Kardinalitäten:
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ### Szenario: Universitätsbibliothek

        *„Eine Bibliothek verwaltet Bücher und deren Exemplare. Jedes Buch hat eine ISBN,
        einen Titel und ein Erscheinungsjahr. Ein Buch kann mehrere Autoren haben, und
        Autoren können mehrere Bücher geschrieben haben. Jedes Buch gehört zu genau einem
        Verlag (Name, Ort). Von jedem Buch existieren ein oder mehrere physische Exemplare,
        die durch eine Exemplar-Nummer (innerhalb des Buches) unterschieden werden.
        Studierende können Exemplare ausleihen, wobei Ausleihdatum und Rückgabedatum
        gespeichert werden."*

        ---
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.accordion({
        "Lösung anzeigen": mo.md(r"""
**Entitäten:**
- **Buch** (ISBN, Titel, Erscheinungsjahr)
- **Autor** (AutorID, Name)
- **Verlag** (VerlagID, Name, Ort)
- **Exemplar** (ExemplarNr) — *schwache Entität*, abhängig von Buch
- **Student** (MatrikelNr, Name)

**Beziehungen:**
1. Autor **schreibt** Buch → **M:N** (Co-Autoren, Vielschreiber)
2. Verlag **veröffentlicht** Buch → **1:N** (ein Verlag, viele Bücher)
3. Buch **hat** Exemplar → **1:N** (identifizierende Beziehung, schwache Entität)
4. Student **leiht aus** Exemplar → **M:N** mit Attributen (Ausleihdatum, Rückgabedatum)

**Besonderheiten:**
- Exemplar ist eine **schwache Entität**: ExemplarNr allein ist nicht eindeutig, erst ISBN + ExemplarNr
- Die Ausleihe ist eine M:N-Beziehung mit **Beziehungsattributen** (Datum)
        """)
    })
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
### ER-Diagramm: Bibliothek (Mermaid)
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.mermaid(
        """
        erDiagram
            VERLAG ||--o{ BUCH : veroeffentlicht
            BUCH ||--|{ EXEMPLAR : hat
            AUTOR }|--|{ BUCH : schreibt
            STUDENT }|--o{ AUSLEIHE : leiht
            EXEMPLAR ||--o{ AUSLEIHE : "wird ausgeliehen"

            VERLAG {
                int ID PK
                string Name
                string Ort
            }

            BUCH {
                string ISBN PK
                string Titel
                int Erscheinungsjahr
                int Verlag_ID FK
            }

            AUTOR {
                int ID PK
                string Name
            }

            EXEMPLAR {
                string ISBN PK,FK
                int ExemplarNr PK
                string Standort
            }

            STUDENT {
                int MatrikelNr PK
                string Name
            }

            AUSLEIHE {
                int ID PK
                string ISBN FK
                int ExemplarNr FK
                int MatrikelNr FK
                date Ausleihdatum
                date Rueckgabedatum
            }
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
**Beobachtungen:**

- **Schwache Entität:** Exemplar hat einen zusammengesetzten Schlüssel (ISBN + ExemplarNr)
- **M:N mit Attributen:** Die Ausleihe speichert neben den Verweisen auch Datumsangaben
- **1:N:** Verlag → Buch (jedes Buch hat genau einen Verlag)
- **M:N:** Autor ↔ Buch (aufgelöst durch implizite Beziehungstabelle)

*Dieses Szenario kombiniert alle Beziehungstypen, die wir kennengelernt haben!*

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
        ## Selbstständig: Eigenes ER-Modell entwerfen

        **Szenario:** Eine Universitätsbibliothek möchte ihre Ausleihe digitalisieren.

        - Es gibt **Bücher** (ISBN, Titel, Erscheinungsjahr) und **Autoren** (Name, Nationalität)
        - **Studierende** (Matrikelnummer, Name, Studiengang) können Bücher **ausleihen** (Datum, Rückgabedatum)
        - Ein Buch kann von mehreren Autoren geschrieben sein
        - Ein Studierender kann mehrere Bücher gleichzeitig ausleihen

        **Aufgabe:** Zeichnen Sie ein ER-Diagramm auf Papier oder in [draw.io](https://draw.io):

        1. Welche **Entitäten** gibt es? (Tipp: 3 Stück)
        2. Welche **Attribute** hat jede Entität? Was ist der Primärschlüssel?
        3. Welche **Beziehungen** bestehen? (Tipp: 2 Stück)
        4. Was sind die **Kardinalitäten**? (1:1, 1:N, oder M:N?)

        ---

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
