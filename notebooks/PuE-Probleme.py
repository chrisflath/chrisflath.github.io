import marimo

__generated_with = "0.13.15"
app = marimo.App(width="full")


@app.cell(hide_code=True)
def _():
    import marimo as mo
    import pulp
    import numpy as np
    from scipy.optimize import linprog
    return linprog, mo, np, pulp


@app.cell(hide_code=True)
def _(linprog, np, pulp):
    def pulp_to_scipy_linprog(prob):
        variables = prob.variables()

        objective = np.array([prob.objective.get(v) if prob.objective.get(v) is not None else 0 for v in variables])
        constant_offset = prob.objective.constant

        if prob.sense == pulp.LpMaximize:
            c = -objective
            constant_offset = -constant_offset  # Flip constant offset too
        else:
            c = objective

        A_ub, b_ub = [], []
        A_eq, b_eq = [], []

        for constraint in prob.constraints.values():
            coeffs = [constraint.get(v, 0) for v in variables]
            const_term = constraint.constant

            if constraint.sense == pulp.LpConstraintLE:
                A_ub.append(coeffs)
                b_ub.append(-const_term)
            elif constraint.sense == pulp.LpConstraintGE:
                A_ub.append([-coef for coef in coeffs])
                b_ub.append(const_term)
            elif constraint.sense == pulp.LpConstraintEQ:
                A_eq.append(coeffs)
                b_eq.append(-const_term)

        bounds = []
        for v in variables:
            lb = v.lowBound if v.lowBound is not None else -np.inf
            ub = v.upBound if v.upBound is not None else np.inf
            bounds.append((lb, ub))

        integrality = np.array([1 if v.cat in [pulp.LpInteger, pulp.LpBinary] else 0 for v in variables])

        return {
            'c': c,
            'A_ub': np.array(A_ub) if A_ub else None,
            'b_ub': np.array(b_ub) if b_ub else None,
            'A_eq': np.array(A_eq) if A_eq else None,
            'b_eq': np.array(b_eq) if b_eq else None,
            'bounds': bounds,
            'integrality': integrality,
            'constant_offset': constant_offset,  # explicitly included
            'variable_names': [v.name for v in variables],
            'constraint_names': [con.name for con in prob.constraints.values()],
            'objective_sense': 'max' if prob.sense == pulp.LpMaximize else 'min',
            'problem_name': prob.name
        }

    def solve_with_scipy(prob):
        linprog_data = pulp_to_scipy_linprog(prob)

        res = linprog(
            c=linprog_data['c'],
            A_ub=linprog_data['A_ub'],
            b_ub=linprog_data['b_ub'],
            A_eq=linprog_data['A_eq'],
            b_eq=linprog_data['b_eq'],
            bounds=linprog_data['bounds'],
            integrality=linprog_data['integrality'],
            method='highs'
        )

        if res.success:
            for var_name, var_value in zip(linprog_data['variable_names'], res.x):
                prob.variablesDict()[var_name].varValue = var_value

            # Correctly add back constant offset
            prob.objective_value = res.fun + linprog_data['constant_offset']
            if prob.sense == pulp.LpMaximize:
                prob.objective_value = -prob.objective_value

            prob.status = pulp.LpStatusOptimal
        else:
            prob.status = pulp.LpStatusNotSolved

        return prob

    return (solve_with_scipy,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    # LP-Modellierung mit Python

    ## 💧 Produktionsplanung bei Blue Ridge Hot Tubs

    Ein Whirlpool-Hersteller plant die Produktion zweier Produkttypen mit dem Ziel, den Deckungsbeitrag zu maximieren. Die Produktion ist durch drei Ressourcen begrenzt: Montagekapazität, Pumpeneinsatz und Arbeitsstunden.

    ---

    ### 🧾 Entscheidungskontext

    Es stehen zwei Whirlpool-Modelle zur Auswahl:

    - **X₁**: Luxus-Modell (Deckungsbeitrag 350 $ pro Einheit)
    - **X₂**: Standard-Modell (Deckungsbeitrag 300 $ pro Einheit)

    ### 🚧 Ressourceneinschränkungen

    | Ressource         | X₁-Verbrauch | X₂-Verbrauch | Verfügbar |
    |-------------------|--------------|--------------|-----------|
    | Montagezeit       | 1 h          | 1 h          | 200 h     |
    | Pumpenkapazität   | 9 Einheiten  | 6 Einheiten  | 1.566     |
    | Arbeitszeit       | 12 h         | 16 h         | 2.880 h   |

    ---

    ### 🎯 Zielfunktion

    \[
    \text{maximiere } Z = 350X_1 + 300X_2
    \]
    """
    )
    return


@app.cell
def _(pulp, solve_with_scipy):
    br_model = pulp.LpProblem("Blue_Ridge_Hot_Tubs", pulp.LpMaximize)

    X1 = pulp.LpVariable("X1", lowBound=0)
    X2 = pulp.LpVariable("X2", lowBound=0)

    # Zielfunktion
    br_model += 350 * X1 + 300 * X2, "Deckungsbeitrag"

    # Nebenbedingungen
    br_model += X1 + X2 <= 200, "Montagezeit"
    br_model += 9 * X1 + 6 * X2 <= 1566, "Pumpen"
    br_model += 12 * X1 + 16 * X2 <= 2880, "Arbeitszeit"

    # Optimieren
    br_model = solve_with_scipy(br_model)

    # Ausgabe
    print(f"X1: {X1.varValue}, X2: {X2.varValue}")
    print("Maximaler Deckungsbeitrag:", pulp.value(br_model.objective))

    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    ## 🧸 Produktionsmix in der Spielzeugfabrik

    Ein Hersteller von Holzspielzeug produziert zwei Produkttypen: **Spielzeugsoldaten** und **Spielzeugzüge**. Die Produktion ist zweistufig aufgebaut und unterliegt mehreren Ressourcenrestriktionen sowie Absatzgrenzen.

    ---

    ### 🧾 Entscheidungskontext

    - **S**: Anzahl Spielzeugsoldaten  
    - **Z**: Anzahl Spielzeugzüge  
    - Deckungsbeitrag 3 respektive 2

    ### 🔨 Produktionsschritte und Restriktionen

    | Ressource                | Soldat (S) | Zug (Z) | Verfügbar |
    |--------------------------|------------|---------|-----------|
    | Schreinerei              | 1 h        | 1 h     | 80 h      |
    | Oberflächenveredelung    | 2 h        | 1 h     | 100 h     |
    | Absatzgrenze Soldaten    | max. 40    | –       | –         |

    ---

    ### 🎯 Zielfunktion

    \[
    \text{maximiere } Z = 3S + 2Z
    \]
    """
    )
    return


@app.cell
def _(pulp, solve_with_scipy):
    # %%
    toy_model = pulp.LpProblem("Spielzeugfabrik", pulp.LpMaximize)

    S = pulp.LpVariable("Soldaten", lowBound=0)
    Z = pulp.LpVariable("Zuege", lowBound=0)

    # Zielfunktion
    toy_model += 3 * S + 3 * Z, "Deckungsbeitrag"

    # Nebenbedingungen
    toy_model += S + Z <= 80, "Schreinerei"
    toy_model += 2 * S + Z <= 100, "Veredelung"
    toy_model += S <= 40, "Verkaufsschranke_Soldaten"

    # Optimieren
    toy_model = solve_with_scipy(toy_model)

    # Ausgabe
    print(f"Soldaten: {S.varValue}, Züge: {Z.varValue}")
    print("Maximaler Deckungsbeitrag:", pulp.value(toy_model.objective))

    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    ## 🏭 Make-or-Buy Problem: Produktionsentscheidungen bei Electro-Poly

    Die Firma **Electro-Poly** ist Hersteller von Schaltkästen und möchte mehrere Kundenaufträge möglichst kosteneffizient erfüllen. Für jedes der drei Produktmodelle (1, 2 und 3) steht die Entscheidung an: **intern produzieren** oder **extern zukaufen** ("make or buy").

    ---

    ### 🎯 Ziel

    Minimiere die **Gesamtkosten**, die sich aus interner Fertigung und externem Zukauf ergeben. Dabei sind **Kapazitätsgrenzen** in der Fertigung zu berücksichtigen.

    \[
    \text{Minimiere: } \sum_{i=1}^3 \left( \text{Kosten}_{\text{make},i} \cdot M_i + \text{Kosten}_{\text{buy},i} \cdot B_i \right)
    \]

    ---

    ### 📥 Parameter

    | Modell | Bedarf | Make-Kosten (€/Stück) | Buy-Kosten (€/Stück) | Verkabelung (h/Stück) | Verpackung (h/Stück) |
    |--------|--------|------------------------|-----------------------|------------------------|-----------------------|
    | 1      | 3.000  | 50                     | 61                    | 2,0                    | 1,0                   |
    | 2      | 2.000  | 83                     | 97                    | 1,5                    | 2,0                   |
    | 3      |   900  | 130                    | 145                   | 3,0                    | 1,0                   |

    **Verfügbare interne Kapazitäten:**

    - Verkabelung: 10.000 Stunden  
    - Verpackung: 5.000 Stunden
    """
    )
    return


@app.cell
def _(pulp, solve_with_scipy):
    # %%
    # Make-or-Buy Problem – LP-Formulierung mit PuLP

    # Modellinitialisierung
    model = pulp.LpProblem("Make-or-Buy-Problem", pulp.LpMinimize)

    # Entscheidungsvariablen
    M = [pulp.LpVariable(f"M{i+1}", lowBound=0) for i in range(3)]  # in-house
    B = [pulp.LpVariable(f"B{i+1}", lowBound=0) for i in range(3)]  # outsourcing

    # Zielfunktion: Kostenminimierung
    model += (50*M[0] + 83*M[1] + 130*M[2] + 61*B[0] + 97*B[1] + 145*B[2]), "Gesamtkosten"

    # Bedarfsdeckung
    model += M[0] + B[0] == 3000
    model += M[1] + B[1] == 2000
    model += M[2] + B[2] == 900

    # Ressourcenverfügbarkeit
    model += 2*M[0] + 1.5*M[1] + 3*M[2] <= 10000  # Verkabelung
    model += 1*M[0] + 2*M[1] + 1*M[2] <= 5000     # Verpackung

    # Optimieren
    model = solve_with_scipy(model)

    # Ergebnisse
    for var in M + B:
        print(f"{var.name}: {var.varValue}")
    print("Gesamtkosten:", pulp.value(model.objective))

    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    ## 💰 Investitionsentscheidung

    In diesem Optimierungsmodell soll ein Budget von **750.000 €** auf sechs verschiedene Unternehmensanleihen verteilt werden. Ziel ist es, den erwarteten **Gesamtertrag zu maximieren**, wobei verschiedene **Risikobegrenzungen** und **Laufzeitvorgaben** eingehalten werden müssen.

    ---

    ### 🧾 Problemhintergrund

    Ein Investor bewertet sechs unterschiedliche Anleihen hinsichtlich folgender Merkmale:

    - **Ertragsrate (Zinssatz)**
    - **Restlaufzeit**: Ist die Anleihe langfristig (>10 Jahre)?
    - **Risikoeinstufung**: Hat die Anleihe eine Bewertung >2?

    ---

    ### 🎯 Zielsetzung

    Maximiere den **Gesamtertrag** über alle Anleihen hinweg:

    $$\text{Maximiere:} \quad \sum_i (\text{Rendite}_i \cdot \text{Investition}_i)$$

    ---

    ### 🔒 Nebenbedingungen

    1. **Investitionssumme**: $\sum_i \text{Investition}_i = 750.000 \,€$

    3. **Diversifikation**:
       - Max. **25 %** der Summe (187.500 €) in **eine einzelne Anleihe**

    4. **Laufzeitvorgabe**:
       - Mind. **50 %** des Kapitals in Anleihen mit **Restlaufzeit > 10 Jahre**

    5. **Risikobegrenzung**:
       - Max. **35 %** in Anleihen mit **Bewertung > 2**
    """
    )
    return


@app.cell
def _(pulp, solve_with_scipy):
    # %%
    # 💡 Eleganter und nachvollziehbarer Ansatz mit strukturierter Datendefinition
    model2 = pulp.LpProblem("Investitionsentscheidung", pulp.LpMaximize)

    # Definition der Anleihen: Name, Ertrag, Laufzeit (>10J), Bewertung (>2)
    bonds = [
        {"name": "ACME Chemical",    "return": 0.0865, "long_term": True,  "rating_above_2": False},
        {"name": "DynaStar",         "return": 0.095,  "long_term": True,  "rating_above_2": True},
        {"name": "Eagle Vision",     "return": 0.10,   "long_term": False, "rating_above_2": True},
        {"name": "MicroModeling",    "return": 0.0875, "long_term": True,  "rating_above_2": False},
        {"name": "OptiPro",          "return": 0.0925, "long_term": False, "rating_above_2": True},
        {"name": "Sabre Systems",    "return": 0.09,   "long_term": True,  "rating_above_2": False},
    ]

    # Entscheidungsvariablen
    X = [pulp.LpVariable(f"X{i+1}", lowBound=0) for i in range(len(bonds))]

    # Zielfunktion: Ertragsmaximierung
    model2 += pulp.lpSum(X[i] * bonds[i]["return"] for i in range(len(bonds))), "Gesamtertrag"

    # Gesamtsumme: 750.000 €
    model2 += pulp.lpSum(X) == 750000, "Investitionssumme"

    # Max. 25 % in jede einzelne Anleihe
    for i in range(len(bonds)):
        model2 += X[i] <= 187500, f"Max25Prozent_{bonds[i]['name']}"

    # Mind. 50 % in langlaufende Anleihen
    model2 += pulp.lpSum(X[i] for i in range(len(bonds)) if bonds[i]["long_term"]) >= 375000, "Min50ProzentLangläufer"

    # Max. 35 % in Anleihen mit Bewertung > 2
    model2 += pulp.lpSum(X[i] for i in range(len(bonds)) if bonds[i]["rating_above_2"]) <= 262500, "Max35ProzentHighRisk"

    # Optimierung
    model2 = solve_with_scipy(model2)

    # Ausgabe
    for i, var2 in enumerate(X):
        print(f"{bonds[i]['name']}: {var2.varValue:.2f} EUR")
    print("Maximaler Ertrag:", pulp.value(model2.objective))

    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    ## 🚛 Einstufiges Transportproblem: Tropicsun

    Tropicsun, ein fiktives Fruchtlogistikunternehmen, möchte Erzeugnisse aus **drei Produktionsstandorten** an **drei Zielorte** transportieren. Ziel ist es, die Transportmengen so zuzuweisen, dass **die gesamten transportbedingten Distanzen gewichtet mit der Liefermenge minimal** sind.

    ---

    ### 🌍 Problemübersicht

    🏭 Produktionsstandorte (Quellen):

    1. **Mt. Dora** – 275.000 Einheiten verfügbar  
    2. **Eustis** – 400.000 Einheiten verfügbar  
    3. **Clermont** – 300.000 Einheiten verfügbar  

    🏪 Zielorte (Senken):

    4. **Ocala** – max. 200.000 Einheiten  
    5. **Orlando** – max. 600.000 Einheiten  
    6. **Leesburg** – max. 225.000 Einheiten  

    ---

    ### 📏 Distanzmatrix (Kosten je Einheit)

    |                | Ocala (4) | Orlando (5) | Leesburg (6) |
    |----------------|------------|-------------|--------------|
    | **Mt. Dora (1)**   | 21         | 50          | 40           |
    | **Eustis (2)**     | 35         | 30          | 22           |
    | **Clermont (3)**   | 55         | 20          | 25           |

    > Jede Zahl steht für die Entfernung (oder Kosten) pro transportierter Einheit von Quelle zu Zielort.

    ---

    ### 🎯 Zielsetzung

    Minimiere die **transportierte Menge × Entfernung**:

    $$
    \text{Minimiere: } \sum_{i \in \text{Quelle}} \sum_{j \in \text{Ziel}} \text{Distanz}_{ij} \cdot x_{ij}
    $$
    """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""## Variante 1 (ausführlicher)""")
    return


@app.cell
def _(pulp, solve_with_scipy):
    model3 = pulp.LpProblem("Tropicsun-Transport", pulp.LpMinimize)

    transport = {}
    for quelle in [1, 2, 3]:
        for senke in [4, 5, 6]:
            transport[(quelle, senke)] = pulp.LpVariable(f"X{quelle}{senke}", lowBound=0)

    kosten = {
        (1,4): 21, (1,5): 50, (1,6): 40,
        (2,4): 35, (2,5): 30, (2,6): 22,
        (3,4): 55, (3,5): 20, (3,6): 25,
    }
    model3 += pulp.lpSum([kosten[i]*transport[i] for i in kosten]), "Gesamtkosten"

    model3 += transport[1,4] + transport[1,5] + transport[1,6] == 275000
    model3 += transport[2,4] + transport[2,5] + transport[2,6] == 400000
    model3 += transport[3,4] + transport[3,5] + transport[3,6] == 300000

    model3 += transport[1,4] + transport[2,4] + transport[3,4] <= 200000
    model3 += transport[1,5] + transport[2,5] + transport[3,5] <= 600000
    model3 += transport[1,6] + transport[2,6] + transport[3,6] <= 225000

    model3 = solve_with_scipy(model3)

    for key, var3 in transport.items():
        print(f"transport{key[0]}{key[1]}: {var3.varValue}")
    print("Transportkosten:", pulp.value(model3.objective))
    return (transport,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""##Variante 2 (kompakt)""")
    return


@app.cell
def _(pulp, solve_with_scipy, transport):
    # Initialisierung des Modells
    model3b = pulp.LpProblem("Tropicsun-Transport", pulp.LpMinimize)

    # Definition der Quellen und Senken
    quellen = [1, 2, 3]
    senken = [4, 5, 6]

    # Entscheidungsvariablen (transport[i, j])
    transportb = {
        (q, s): pulp.LpVariable(f"X{q}{s}", lowBound=0)
        for q in quellen for s in senken
    }

    # Transportkostenmatrix (Distanz in km)
    kostenb = {
        (1, 4): 21, (1, 5): 50, (1, 6): 40,
        (2, 4): 35, (2, 5): 30, (2, 6): 22,
        (3, 4): 55, (3, 5): 20, (3, 6): 25,
    }

    # Zielfunktion: Gesamttransportkosten minimieren
    model3b += pulp.lpSum(kostenb[(q, s)] * transportb[(q, s)] for (q, s) in transport), "Gesamtkosten"

    # Angebotsmengen je Quelle (Produktionsstätten)
    kapazitaet = {
        1: 200000,  # Ocala
        2: 600000,  # Orlando
        3: 225000,  # Leesburg
    }

    # Nachfragegrenzen je Ziel (Kundenorte)
    bedarf = {
        4: 275000,  # Mt. Dora
        5: 400000,  # Eustis
        6: 300000,  # Clermont
    }

    # Nebenbedingung: Gesamte Menge je Quelle muss geliefert werden
    for q in quellen:
        model3b += pulp.lpSum(transportb[(q, s)] for s in senken) <= kapazitaet[q], f"Liefermenge_Quelle_{q}"

    # Nebenbedingung: Gesamteingang je Ziel <= Bedarf
    for s in senken:
        model3b += pulp.lpSum(transportb[(q, s)] for q in quellen) == bedarf[s], f"Kapazitaet_Ziel_{s}"

    # Lösung berechnen
    model3b = solve_with_scipy(model3b)

    # Ausgabe der Lösung
    for (q, s), var3b in transportb.items():
        print(f"Transport von {q} → {s}: {var3b.varValue:.0f} Einheiten")

    print("Minimale Transportkosten:", pulp.value(model3b.objective))

    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    ## 🚚 Mehrstufiges Transportproblem: Bavarian Motor Company

    Die Bavarian Motor Company betreibt zwei **Produktionsstätten** (Knoten 1: Newark, Knoten 7: Jacksonville), von denen aus Waren an verschiedene **Kundenzentren** (Knoten 2–6) geliefert werden sollen. Der Transport kann direkt oder über **Zwischenlagerknoten** erfolgen.

    ---

    ### 🔄 Struktur des Netzwerks

    - **Quellen (Produktion):**
      - Newark (Knoten 1): **+200 Einheiten**
      - Jacksonville (Knoten 7): **+300 Einheiten**

    - **Senken (Kundenbedarf):**
      - Boston (2): −100  
      - Columbus (3): −60  
      - Richmond (4): −80  
      - Atlanta (5): −170  
      - Mobile (6): −70  

    - **Knoten mit Nettobedarf = 0 (Transit erlaubt):**
      - keiner in diesem Fall – alle Knoten sind entweder Quelle oder Senke.

    - **Transportkosten (\$ pro Einheit)** sind auf den Kanten angegeben.

    ---

    ### 🎯 Ziel

    Minimiere die **Gesamtkosten des Transports**, wobei der Bedarf aller Senken genau gedeckt und das gesamte Angebot ausgeschöpft werden soll.

    \[
    \text{Minimiere } \sum_{(i,j) \in \text{Kanten}} \text{Kosten}_{ij} \cdot x_{ij}
    \]
    """
    )
    return


@app.cell
def _(pulp, solve_with_scipy):
    # Modellinitialisierung
    model4 = pulp.LpProblem("BMC_Transshipment", pulp.LpMinimize)

    # Knoten (1–7) mit Angebots-/Nachfragesalden
    b = {
        1: +200,
        2: -100,
        3: -60,
        4: -80,
        5: -170,
        6: -70,
        7: +300,
    }

    # Kostenmatrix (nur erlaubte Kanten)
    kosten4 = {
        (1, 2): 30,
        (1, 4): 40,
        (2, 3): 50,
        (3, 5): 40,
        (3, 4): 40,
        (4, 2): 30,
        (5, 3): 35,
        (5, 4): 30,
        (5, 6): 25,
        (6, 5): 35,
        (6, 7): 50,
        (7, 5): 45,
        (7, 6): 50,
    }

    # Entscheidungsvariablen: Transportmengen x_{ij}
    lieferung = {
        (i4, j4): pulp.LpVariable(f"x_{i4}_{j4}", lowBound=0) for (i4, j4) in kosten4
    }

    # Zielfunktion: Transportkosten minimieren
    model4 += pulp.lpSum(kosten4[i4, j4] * lieferung[i4, j4] for (i4, j4) in lieferung), "Gesamtkosten"

    # Flusserhaltung an jedem Knoten
    for k in b:
        eingang = pulp.lpSum(lieferung[i4, j4] for (i4, j4) in lieferung if j4 == k)
        ausgang = pulp.lpSum(lieferung[i4, j4] for (i4, j4) in lieferung if i4 == k)
        model4 += eingang - ausgang + b[k] >= 0, f"Flusserhaltung_Knoten_{k}"

    # Optimieren
    model4 = solve_with_scipy(model4)

    # Ausgabe
    for (i4, j4), var4 in lieferung.items():
        if var4.varValue > 0:
            print(f"Transport {i4} → {j4}: {var4.varValue:.0f} Einheiten")

    print("Minimale Gesamtkosten:", pulp.value(model4.objective))

    return


if __name__ == "__main__":
    app.run()
