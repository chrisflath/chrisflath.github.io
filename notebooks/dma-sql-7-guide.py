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
    app_title="DMA Session 7: Normalisierung — Guide",
)


@app.cell(hide_code=True)
def _():
    import marimo as mo
    return (mo,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        # Session 7: Normalisierung — Guide

        **Kursfahrplan:** I: SQL-Grundlagen (S1–4) · **▸ II: Datenmodellierung (S5–7)** · III: Fortgeschrittenes SQL (S8–9) · IV: Datenanalyse (S10–13)

        ### Lernziele

        Nach dieser Session können Sie:

        - **Funktionale Abhängigkeiten (FDs)** erkennen und Armstrong-Axiome anwenden
        - **1NF**, **2NF** und **3NF** prüfen
        - Tabellen schrittweise **normalisieren**
        - Den **Trade-off** zwischen Normalisierung und Denormalisierung bewerten

        ---
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ## Rückblick: Warum Normalisierung?

        In Session 5 haben wir **Anomalien** kennengelernt — Probleme, die durch redundante Datenhaltung entstehen:

        | Anomalie | Problem | Beispiel |
        |----------|---------|----------|
        | **Änderungsanomalie** | Inkonsistenz bei Updates | Kundenadresse in 5 Zeilen ändern — eine vergessen |
        | **Einfügeanomalie** | Kann Daten nicht ohne andere einfügen | Neuer Kunde ohne Bestellung? |
        | **Löschanomalie** | Verliert ungewollt Daten | Letzte Bestellung löschen → Kundendaten weg |

        **Ursache:** Redundanz durch schlechtes Tabellendesign.

        **Lösung:** Systematische **Normalisierung** — ein schrittweises Verfahren, das Redundanz nach klaren Regeln beseitigt.

        ---
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ## Phase 1: Funktionale Abhängigkeiten

        ### Definition

        **A → B** bedeutet: "Wenn ich den Wert von A kenne, kenne ich auch den Wert von B."

        | FD | Gültig? | Erklärung |
        |----|---------|-----------|
        | Matrikelnr → Name | ✅ | Jede Matrikelnr gehört zu genau einem Namen |
        | PLZ → Ort | ✅ | Jede PLZ gehört zu einem Ort (in DE) |
        | Ort → PLZ | ❌ | München hat viele PLZs |
        | ISBN → Titel | ✅ | Jede ISBN identifiziert ein Buch |

        FDs sind die Grundlage der Normalisierung: Sie beschreiben, welche Attribute andere **bestimmen**.

        ---
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ### Armstrong-Axiome: Neue FDs ableiten

        Mit drei Grundregeln lassen sich aus bekannten FDs **neue** ableiten:

        | Axiom | Regel | Beispiel |
        |-------|-------|----------|
        | **Reflexivität** | Wenn B ⊆ A, dann A → B | {Vorname, Nachname} → Nachname |
        | **Verstärkung** | Wenn A → B, dann A,C → B,C | Matrikelnr → Name ⟹ Matrikelnr,Fach → Name,Fach |
        | **Transitivität** | Wenn A → B und B → C, dann A → C | Best_Nr → Kunde, Kunde → Stadt ⟹ Best_Nr → Stadt |

        ---
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ### Geführtes Beispiel: Unnormalisierte Bestelltabelle

        Wir erstellen eine typische unnormalisierte Tabelle und identifizieren die funktionalen Abhängigkeiten.
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    _df = mo.sql(
        f"""
        CREATE TABLE IF NOT EXISTS Bestellung_Unnorm (
            Best_Nr INTEGER,
            Kunde VARCHAR(50),
            K_Stadt VARCHAR(50),
            Produkt VARCHAR(50),
            P_Preis DECIMAL(10,2),
            Menge INTEGER,
            PRIMARY KEY (Best_Nr, Produkt)
        );

        INSERT OR IGNORE INTO Bestellung_Unnorm VALUES (1001, 'Müller', 'München', 'Laptop', 999.00, 1);
        INSERT OR IGNORE INTO Bestellung_Unnorm VALUES (1001, 'Müller', 'München', 'Maus', 29.00, 2);
        INSERT OR IGNORE INTO Bestellung_Unnorm VALUES (1002, 'Schmidt', 'Berlin', 'Laptop', 999.00, 1);
        INSERT OR IGNORE INTO Bestellung_Unnorm VALUES (1003, 'Müller', 'München', 'Tastatur', 79.00, 1);
        INSERT OR IGNORE INTO Bestellung_Unnorm VALUES (1004, 'Weber', 'Hamburg', 'Maus', 29.00, 3);
        INSERT OR IGNORE INTO Bestellung_Unnorm VALUES (1004, 'Weber', 'Hamburg', 'Laptop', 999.00, 1);

        SELECT * FROM Bestellung_Unnorm ORDER BY Best_Nr, Produkt;
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        **Identifizierte FDs in dieser Tabelle:**

        | FD | Erklärung |
        |----|-----------|
        | Best_Nr → Kunde, K_Stadt | Jede Bestellnummer gehört zu genau einem Kunden |
        | Kunde → K_Stadt | Jeder Kunde wohnt in einer Stadt |
        | Produkt → P_Preis | Jedes Produkt hat einen festen Preis |
        | (Best_Nr, Produkt) → Menge | Die Menge hängt von der konkreten Bestellposition ab |

        Beachten Sie: Der **Primärschlüssel** ist (Best_Nr, Produkt), aber nicht alle Attribute hängen vom *gesamten* Schlüssel ab!

        ---
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Vorhersage 1
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    pred_trans = mo.ui.radio(
        options={
            "mat_email": "Matrikelnr → Email",
            "email_mat": "Email → Matrikelnr",
            "email_student": "Email → Student",
            "nichts": "Keine neue FD ableitbar",
        },
        label="**Vorhersage:** Gegeben: Matrikelnr → Student, Student → Email. Was ergibt Transitivität?"
    )
    pred_trans
    return (pred_trans,)


@app.cell(hide_code=True)
def _(pred_trans, mo):
    if pred_trans.value == "mat_email":
        mo.output.replace(mo.md("✅ **Richtig!** Transitivität: Wenn A → B und B → C, dann A → C. Hier: Matrikelnr → Student und Student → Email ergibt **Matrikelnr → Email**."))
    elif pred_trans.value:
        mo.output.replace(mo.md("❌ Nicht ganz. Bei der Transitivität gilt: Wenn A → B und B → C, dann A → C. Hier: Matrikelnr → Student → Email, also ergibt sich **Matrikelnr → Email**."))
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ---

        **Jetzt zum Übungs-Notebook → Aufgaben 2.x**

        ---
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ## Phase 3: Erste Normalform (1NF) und Zweite Normalform (2NF)

        ### 1NF: Atomare Werte

        **Regel:** Alle Attributwerte müssen **atomar** sein — keine Listen, keine Wiederholungsgruppen, keine zusammengesetzten Werte in einer Zelle.

        **Gegenbeispiel:** Eine Tabelle mit komma-separierten Kursen in einer Spalte.
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    _df = mo.sql(
        f"""
        CREATE TABLE IF NOT EXISTS Student_Nicht1NF (
            Student VARCHAR(50) PRIMARY KEY,
            Kurse VARCHAR(200)
        );

        INSERT OR IGNORE INTO Student_Nicht1NF VALUES ('Anna', 'DMA, BWL, Statistik');
        INSERT OR IGNORE INTO Student_Nicht1NF VALUES ('Ben', 'DMA');
        INSERT OR IGNORE INTO Student_Nicht1NF VALUES ('Clara', 'BWL, Statistik');

        SELECT * FROM Student_Nicht1NF;
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        **Problem:** Wie finden Sie alle Studierenden, die "BWL" belegen?

        ```sql
        -- Das funktioniert NICHT zuverlässig:
        SELECT * FROM Student_Nicht1NF WHERE Kurse LIKE '%BWL%';
        ```

        **Lösung:** In 1NF überführen — jeder Kurs in einer eigenen Zeile:
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    _df = mo.sql(
        f"""
        CREATE TABLE IF NOT EXISTS Student_Kurs_1NF (
            Student VARCHAR(50),
            Kurs VARCHAR(50),
            PRIMARY KEY (Student, Kurs)
        );

        INSERT OR IGNORE INTO Student_Kurs_1NF VALUES ('Anna', 'DMA');
        INSERT OR IGNORE INTO Student_Kurs_1NF VALUES ('Anna', 'BWL');
        INSERT OR IGNORE INTO Student_Kurs_1NF VALUES ('Anna', 'Statistik');
        INSERT OR IGNORE INTO Student_Kurs_1NF VALUES ('Ben', 'DMA');
        INSERT OR IGNORE INTO Student_Kurs_1NF VALUES ('Clara', 'BWL');
        INSERT OR IGNORE INTO Student_Kurs_1NF VALUES ('Clara', 'Statistik');

        SELECT * FROM Student_Kurs_1NF ORDER BY Student, Kurs;
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        Jetzt funktioniert die Abfrage sauber:

        ```sql
        SELECT Student FROM Student_Kurs_1NF WHERE Kurs = 'BWL';
        ```

        ---

        ### 2NF: Volle funktionale Abhängigkeit

        **Regel:** Jedes Nicht-Schlüsselattribut muss **voll funktional abhängig** vom **gesamten** Primärschlüssel sein.

        **Problem in unserer Bestelltabelle:**

        - Primärschlüssel: **(Best_Nr, Produkt)**
        - Aber: `Kunde` hängt nur von `Best_Nr` ab, nicht von `Produkt` → **partielle Abhängigkeit**
        - Und: `P_Preis` hängt nur von `Produkt` ab, nicht von `Best_Nr` → **partielle Abhängigkeit**

        **Hinweis:** 2NF ist nur bei **zusammengesetzten** Schlüsseln relevant. Hat eine Tabelle einen einfachen Primärschlüssel, ist sie automatisch in 2NF (wenn sie 1NF erfüllt).
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Vorhersage 2
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    pred_2nf = mo.ui.radio(
        options={
            "1nf": "1NF (nicht atomare Werte)",
            "2nf": "2NF (partielle Abhängigkeit)",
            "3nf": "3NF (transitive Abhängigkeit)",
            "keine": "Keine Normalform verletzt",
        },
        label="**Vorhersage:** Schlüssel ist (Best_Nr, Produkt). Kunde hängt nur von Best_Nr ab. Welche NF ist verletzt?"
    )
    pred_2nf
    return (pred_2nf,)


@app.cell(hide_code=True)
def _(pred_2nf, mo):
    if pred_2nf.value == "2nf":
        mo.output.replace(mo.md("✅ **Richtig!** Kunde hängt nur von einem Teil des zusammengesetzten Schlüssels ab (Best_Nr, nicht vom gesamten Schlüssel Best_Nr + Produkt). Das ist eine **partielle Abhängigkeit** und verletzt die **2NF**."))
    elif pred_2nf.value:
        mo.output.replace(mo.md("❌ Nicht ganz. Wenn ein Attribut nur von einem *Teil* des zusammengesetzten Schlüssels abhängt, ist das eine **partielle Abhängigkeit** — ein Verstoß gegen die **2NF**."))
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ### Zerlegung in 2NF

        Wir zerlegen die Tabelle so, dass partielle Abhängigkeiten verschwinden:

        - **Bestellung_2NF:** Best_Nr → Kunde, K_Stadt
        - **Produkt_2NF:** Produkt → P_Preis
        - **Best_Position_2NF:** (Best_Nr, Produkt) → Menge
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    _df = mo.sql(
        f"""
        CREATE TABLE IF NOT EXISTS Bestellung_2NF (
            Best_Nr INTEGER PRIMARY KEY,
            Kunde VARCHAR(50),
            K_Stadt VARCHAR(50)
        );

        INSERT OR IGNORE INTO Bestellung_2NF
        SELECT DISTINCT Best_Nr, Kunde, K_Stadt
        FROM Bestellung_Unnorm;

        SELECT * FROM Bestellung_2NF ORDER BY Best_Nr;
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    _df = mo.sql(
        f"""
        CREATE TABLE IF NOT EXISTS Produkt_2NF (
            Produkt VARCHAR(50) PRIMARY KEY,
            P_Preis DECIMAL(10,2)
        );

        INSERT OR IGNORE INTO Produkt_2NF
        SELECT DISTINCT Produkt, P_Preis
        FROM Bestellung_Unnorm;

        SELECT * FROM Produkt_2NF ORDER BY Produkt;
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    _df = mo.sql(
        f"""
        CREATE TABLE IF NOT EXISTS Best_Position_2NF (
            Best_Nr INTEGER,
            Produkt VARCHAR(50),
            Menge INTEGER,
            PRIMARY KEY (Best_Nr, Produkt)
        );

        INSERT OR IGNORE INTO Best_Position_2NF
        SELECT Best_Nr, Produkt, Menge
        FROM Bestellung_Unnorm;

        SELECT * FROM Best_Position_2NF ORDER BY Best_Nr, Produkt;
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        **Ergebnis:** 3 Tabellen statt 1, aber **weniger Redundanz**!

        - Laptop-Preis steht nur noch **1x** (in Produkt_2NF)
        - Aber: Müller/München steht noch **2x** (in Bestellung_2NF, bei Best_Nr 1001 und 1003)

        → Wir brauchen noch **3NF**!

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
        ## Phase 5: Dritte Normalform (3NF) und Trade-off

        ### 3NF: Keine transitiven Abhängigkeiten

        **Regel:** Kein Nicht-Schlüsselattribut darf von einem anderen Nicht-Schlüsselattribut abhängen.

        **Problem in Bestellung_2NF:**

        - Best_Nr → Kunde (OK — Kunde hängt vom Schlüssel ab)
        - Kunde → K_Stadt (Problem! — K_Stadt hängt von Kunde ab, nicht direkt vom Schlüssel)
        - Also: Best_Nr → Kunde → K_Stadt (**transitive Abhängigkeit**)

        **Lösung:** Kunde in eigene Tabelle auslagern.
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    _df = mo.sql(
        f"""
        CREATE TABLE IF NOT EXISTS Kunde_3NF (
            Kunde VARCHAR(50) PRIMARY KEY,
            K_Stadt VARCHAR(50)
        );

        INSERT OR IGNORE INTO Kunde_3NF
        SELECT DISTINCT Kunde, K_Stadt
        FROM Bestellung_2NF;

        SELECT * FROM Kunde_3NF ORDER BY Kunde;
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    _df = mo.sql(
        f"""
        CREATE TABLE IF NOT EXISTS Bestellung_3NF (
            Best_Nr INTEGER PRIMARY KEY,
            Kunde VARCHAR(50)
        );

        INSERT OR IGNORE INTO Bestellung_3NF
        SELECT Best_Nr, Kunde
        FROM Bestellung_2NF;

        SELECT * FROM Bestellung_3NF ORDER BY Best_Nr;
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ### Finale Struktur in 3NF

        Aus **1 Tabelle** wurden **4 Tabellen**:

        | Tabelle | Inhalt | Primärschlüssel |
        |---------|--------|-----------------|
        | Kunde_3NF | Kundenstammdaten | Kunde |
        | Bestellung_3NF | Bestellkopf | Best_Nr |
        | Produkt_2NF | Produktstammdaten | Produkt |
        | Best_Position_2NF | Bestellpositionen | (Best_Nr, Produkt) |

        **Keine Redundanz mehr!** Jede Information steht genau einmal.

        ---
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Vorhersage 3
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    pred_3nf = mo.ui.radio(
        options={
            "transitiv": "Transitive Abhängigkeit (3NF verletzt)",
            "partiell": "Partielle Abhängigkeit (2NF verletzt)",
            "atomar": "Nicht atomare Werte (1NF verletzt)",
            "kein": "Kein Problem",
        },
        label="**Vorhersage:** Best_Nr → Kunde, Kunde → K_Stadt. Was ist das Problem?"
    )
    pred_3nf
    return (pred_3nf,)


@app.cell(hide_code=True)
def _(pred_3nf, mo):
    if pred_3nf.value == "transitiv":
        mo.output.replace(mo.md("✅ **Richtig!** Best_Nr → Kunde → K_Stadt ist eine **transitive Abhängigkeit**. K_Stadt hängt nicht direkt vom Schlüssel ab, sondern über den Umweg Kunde. Das verletzt die **3NF**."))
    elif pred_3nf.value:
        mo.output.replace(mo.md("❌ Nicht ganz. Schauen Sie auf die Kette: Best_Nr → Kunde → K_Stadt. K_Stadt hängt über Kunde *transitiv* vom Schlüssel ab — das ist eine **transitive Abhängigkeit** und verletzt die **3NF**."))
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ### Verlustfreie Zerlegung überprüfen

        Eine wichtige Eigenschaft der Normalisierung: Die Zerlegung muss **verlustfrei** sein — der JOIN aller Teiltabellen muss exakt die Originaldaten reproduzieren.
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    _df = mo.sql(
        f"""
        SELECT COUNT(*) AS Original_Zeilen FROM Bestellung_Unnorm;
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    _df = mo.sql(
        f"""
        SELECT COUNT(*) AS Rekonstruierte_Zeilen
        FROM Bestellung_3NF b
        JOIN Kunde_3NF k ON b.Kunde = k.Kunde
        JOIN Best_Position_2NF bp ON b.Best_Nr = bp.Best_Nr
        JOIN Produkt_2NF p ON bp.Produkt = p.Produkt;
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        **Beide Zählungen sind identisch!** Das beweist: Unsere Normalisierung war **verlustfrei** — keine Information ging beim Aufteilen verloren.

        ---
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ### Armstrong-Axiome: Quiz

        Testen Sie Ihr Verständnis der Ableitungsregeln!
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    armstrong_quiz = mo.ui.radio(
        options={
            "a_stadt": "Matrikelnr → Stadt",
            "stadt_name": "Stadt → Name",
            "name_matrikel": "Name → Matrikelnr",
            "stadt_matrikel": "Stadt → Matrikelnr"
        },
        label="**Quiz:** Gegeben: Matrikelnr → Student, Student → Stadt. Welche FD lässt sich per **Transitivität** ableiten?"
    )
    armstrong_quiz
    return (armstrong_quiz,)


@app.cell(hide_code=True)
def _(armstrong_quiz, mo):
    if armstrong_quiz.value == "a_stadt":
        mo.output.replace(mo.md("✅ **Richtig!** Transitivität: Matrikelnr → Student und Student → Stadt ergibt Matrikelnr → Stadt."))
    elif armstrong_quiz.value:
        mo.output.replace(mo.md("❌ Nicht ganz. Bei der Transitivität gilt: Wenn A → B und B → C, dann A → C. Hier: Matrikelnr → Student → Stadt, also Matrikelnr → Stadt."))
    return


@app.cell(hide_code=True)
def _(mo):
    aug_quiz = mo.ui.radio(
        options={
            "correct": "ISBN, Verlag → Titel, Verlag",
            "wrong1": "Verlag → Titel",
            "wrong2": "Titel → ISBN, Verlag",
            "wrong3": "ISBN, Titel → Verlag"
        },
        label="**Quiz:** Gegeben: ISBN → Titel. Welche FD folgt per **Verstärkung** (Augmentation) mit Verlag?"
    )
    aug_quiz
    return (aug_quiz,)


@app.cell(hide_code=True)
def _(aug_quiz, mo):
    if aug_quiz.value == "correct":
        mo.output.replace(mo.md("✅ **Richtig!** Verstärkung: Wenn A → B, dann A,C → B,C. Also ISBN,Verlag → Titel,Verlag."))
    elif aug_quiz.value:
        mo.output.replace(mo.md("❌ Nicht ganz. Verstärkung fügt auf **beiden Seiten** das gleiche Attribut hinzu: ISBN → Titel wird zu ISBN,Verlag → Titel,Verlag."))
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ---

        ### Normalformen bestimmen: Quiz

        Testen Sie Ihr Verständnis!
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    quiz1 = mo.ui.radio(
        options={
            "1nf": "Verletzt 1NF (nicht atomare Werte)",
            "2nf": "Verletzt 2NF (partielle Abhängigkeit)",
            "3nf": "Verletzt 3NF (transitive Abhängigkeit)",
            "ok": "Ist in 3NF (keine Verletzung)"
        },
        label="**Frage 1:** Mitarbeiter(\\underline{MitID}, Name, AbtID, AbtName) — was ist das Problem?"
    )
    quiz1
    return (quiz1,)


@app.cell(hide_code=True)
def _(mo, quiz1):
    if quiz1.value == "3nf":
        mo.output.replace(mo.md("✅ **Richtig!** MitID → AbtID → AbtName ist eine transitive Abhängigkeit."))
    elif quiz1.value:
        mo.output.replace(mo.md("❌ Nicht ganz. Denken Sie an die Kette: MitID → AbtID → AbtName"))
    return


@app.cell(hide_code=True)
def _(mo):
    quiz2 = mo.ui.radio(
        options={
            "1nf": "Verletzt 1NF (nicht atomare Werte)",
            "2nf": "Verletzt 2NF (partielle Abhängigkeit)",
            "3nf": "Verletzt 3NF (transitive Abhängigkeit)",
            "ok": "Ist in 3NF (keine Verletzung)"
        },
        label="**Frage 2:** Buch(\\underline{ISBN, AutorID}, Titel, AutorName) — was ist das Problem?"
    )
    quiz2
    return (quiz2,)


@app.cell(hide_code=True)
def _(mo, quiz2):
    if quiz2.value == "2nf":
        mo.output.replace(mo.md("✅ **Richtig!** Titel hängt nur von ISBN ab (partiell), AutorName nur von AutorID (partiell)."))
    elif quiz2.value:
        mo.output.replace(mo.md("❌ Nicht ganz. Bei zusammengesetztem Schlüssel: Hängen alle Attribute vom *gesamten* Schlüssel ab?"))
    return


@app.cell(hide_code=True)
def _(mo):
    quiz3 = mo.ui.radio(
        options={
            "1nf": "Verletzt 1NF (nicht atomare Werte)",
            "2nf": "Verletzt 2NF (partielle Abhängigkeit)",
            "3nf": "Verletzt 3NF (transitive Abhängigkeit)",
            "ok": "Ist in 3NF (keine Verletzung)"
        },
        label="**Frage 3:** Kurs(KursNr, Titel, DozentName, DozentBüro) mit KursNr → Titel, KursNr → DozentName, DozentName → DozentBüro"
    )
    quiz3
    return (quiz3,)


@app.cell(hide_code=True)
def _(mo, quiz3):
    if quiz3.value == "3nf":
        mo.output.replace(mo.md("✅ **Richtig!** KursNr → DozentName → DozentBüro ist eine transitive Abhängigkeit. DozentBüro hängt über DozentName indirekt vom Schlüssel ab. Lösung: Dozent in eigene Tabelle auslagern."))
    elif quiz3.value:
        mo.output.replace(mo.md("❌ Nicht ganz. Schauen Sie auf die Kette: KursNr → DozentName → DozentBüro. Das DozentBüro hängt nicht direkt vom Schlüssel ab."))
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
        ## Phase 7: Visualisierung — Normalisierung messbar machen

        Wie viel Redundanz haben wir bei jedem Normalisierungsschritt eliminiert?
        """
    )
    return


@app.cell(hide_code=True)
def _():
    import plotly.express as px
    return (px,)


@app.cell(hide_code=True)
def _():
    import polars as pl
    return (pl,)


@app.cell(hide_code=True)
def _(pl, px):
    _schritte = pl.DataFrame({
        "Normalform": ["Unnormalisiert", "2NF (3 Tabellen)", "3NF (4 Tabellen)"],
        "Redundante_Einträge": [12, 3, 0],
    })
    px.bar(
        _schritte,
        x="Normalform",
        y="Redundante_Einträge",
        title="Redundanz-Reduktion durch Normalisierung",
        labels={"Redundante_Einträge": "Redundante Wiederholungen", "Normalform": ""},
        color_discrete_sequence=["#E87722"],
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        In der unnormalisierten Tabelle werden Kundenname/-stadt und Produktname/-preis mehrfach
        gespeichert. Schritt für Schritt verschwinden diese Wiederholungen.

        ---
        """
    )
    return


@app.cell(hide_code=True)
def _(pl, px):
    _tradeoff = pl.DataFrame({
        "Normalform": ["Unnormalisiert", "2NF", "3NF"],
        "Tabellen": [1, 3, 4],
        "Redundante_Einträge": [12, 3, 0],
    })
    _fig = px.bar(
        _tradeoff,
        x="Normalform",
        y=["Tabellen", "Redundante_Einträge"],
        barmode="group",
        title="Trade-off: Mehr Tabellen, weniger Redundanz",
        labels={"value": "Anzahl", "variable": "Metrik", "Normalform": ""},
        color_discrete_map={
            "Tabellen": "#003560",
            "Redundante_Einträge": "#E87722",
        },
    )
    _fig.update_layout(legend_title_text="")
    _fig
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        **Trade-off der Normalisierung:** Aus einer Tabelle werden vier — aber die Redundanz sinkt auf null. In der Praxis ist das ein guter Tausch: Mehr Tabellen kosten kaum Speicher, aber Redundanz kostet Konsistenz.

        ---
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Viz-Choice: Den richtigen Charttyp wählen
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    viz_choice_7 = mo.ui.radio(
        options={
            "grouped_bar": "Gruppiertes Balkendiagramm",
            "scatter": "Streudiagramm",
            "line_dual": "Liniendiagramm mit Doppelachse",
            "stacked": "Gestapeltes Balkendiagramm",
        },
        label="Trade-off zwischen Tabellenanzahl und Redundanz über NF-Schritte zeigen?"
    )
    viz_choice_7
    return (viz_choice_7,)


@app.cell(hide_code=True)
def _(viz_choice_7, mo):
    if viz_choice_7.value == "grouped_bar":
        mo.output.replace(mo.md("✅ **Richtig!** Ein **gruppiertes Balkendiagramm** eignet sich hervorragend, um zwei Metriken (Tabellen und Redundanz) pro Kategorie (Normalform-Schritt) nebeneinander zu vergleichen. So sieht man sofort den gegenläufigen Trend."))
    elif viz_choice_7.value == "scatter":
        mo.output.replace(mo.md("❌ Nicht ganz. Ein Streudiagramm zeigt den Zusammenhang zwischen zwei numerischen Variablen, aber hier haben wir Kategorien (Normalform-Schritte) mit je zwei Metriken. Ein **gruppiertes Balkendiagramm** stellt das klarer dar."))
    elif viz_choice_7.value == "line_dual":
        mo.output.replace(mo.md("❌ Nicht ganz. Ein Liniendiagramm suggeriert eine kontinuierliche Entwicklung, aber Normalform-Schritte sind diskrete Kategorien. Ein **gruppiertes Balkendiagramm** passt hier besser."))
    elif viz_choice_7.value == "stacked":
        mo.output.replace(mo.md("❌ Nicht ganz. Ein gestapeltes Balkendiagramm zeigt Teile eines Ganzen — aber Tabellen und Redundanz sind keine Teile einer Summe. Ein **gruppiertes Balkendiagramm** zeigt die zwei Metriken besser nebeneinander."))
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
    selbsttest_7 = mo.ui.radio(
        options={
            "nichts_anderem": "...von nichts anderem als dem Schlüssel",
            "allen": "...von allen Attributen",
            "mindestens": "...von mindestens einem Schlüssel",
        },
        label="Merksatz 3NF: 'Jedes Attribut hängt vom Schlüssel ab, vom ganzen Schlüssel, und...?'"
    )
    selbsttest_7
    return (selbsttest_7,)


@app.cell(hide_code=True)
def _(selbsttest_7, mo):
    if selbsttest_7.value == "nichts_anderem":
        mo.output.replace(mo.md("✅ **Richtig!** Der vollständige Merksatz lautet: *\"Jedes Attribut hängt vom Schlüssel ab, vom ganzen Schlüssel, und von nichts anderem als dem Schlüssel.\"* — Das fasst 1NF (Schlüssel existiert), 2NF (ganzer Schlüssel) und 3NF (nichts anderes) zusammen."))
    elif selbsttest_7.value == "allen":
        mo.output.replace(mo.md("❌ Nicht ganz. Der Merksatz betont die *Exklusivität*: Attribute dürfen **nur** vom Schlüssel abhängen, nicht von anderen Nicht-Schlüsselattributen. Die korrekte Vervollständigung ist: *\"...von nichts anderem als dem Schlüssel.\"*"))
    elif selbsttest_7.value == "mindestens":
        mo.output.replace(mo.md("❌ Nicht ganz. Der dritte Teil des Merksatzes adressiert die 3NF und betont, dass es keine transitiven Abhängigkeiten geben darf. Die korrekte Vervollständigung ist: *\"...von nichts anderem als dem Schlüssel.\"*"))
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ---

        ## Zusammenfassung

        | Normalform | Regel | Lösung |
        |------------|-------|--------|
        | **1NF** | Atomare Werte | Listen auflösen, jeder Wert in eigener Zelle |
        | **2NF** | Volle Abhängigkeit vom gesamten Schlüssel | Partielle Abhängigkeiten in eigene Tabelle auslagern |
        | **3NF** | Keine transitiven Abhängigkeiten | Transitive Abhängigkeiten in eigene Tabelle auslagern |

        ### Merksatz

        *"Jedes Attribut hängt vom Schlüssel ab, vom ganzen Schlüssel, und von nichts anderem als dem Schlüssel."*

        ### Ausblick Session 8

        Nächste Woche: **JOINs** — die normalisierten Tabellen wieder zusammenführen!
        """
    )
    return


if __name__ == "__main__":
    app.run()
