import marimo

__generated_with = "0.14.10"
app = marimo.App(width="full")


@app.cell
def _():
    import marimo as mo
    import pulp
    import numpy as np
    from scipy.optimize import linprog, milp, LinearConstraint, Bounds
    import pandas as pd
    from scipy.spatial import distance_matrix
    import matplotlib.pyplot as plt
    from drawdata import ScatterWidget

    def pulp_to_scipy_linprog(prob):
        variables = prob.variables()

        # Objective
        objective = np.array([prob.objective.get(v) or 0 for v in variables])
        constant_offset = prob.objective.constant
        if prob.sense == pulp.LpMaximize:
            c = -objective
            constant_offset = -constant_offset
        else:
            c = objective

        # Constraints
        A_ub, b_ub = [], []
        A_eq, b_eq = [], []
        for constraint in prob.constraints.values():
            coeffs = [constraint.get(v, 0) for v in variables]
            const_term = -constraint.constant

            if constraint.sense == pulp.LpConstraintLE:
                A_ub.append(coeffs)
                b_ub.append(const_term)
            elif constraint.sense == pulp.LpConstraintGE:
                A_ub.append([-coef for coef in coeffs])
                b_ub.append(-const_term)
            elif constraint.sense == pulp.LpConstraintEQ:
                A_eq.append(coeffs)
                b_eq.append(const_term)

        A_ub_arr = np.array(A_ub) if A_ub else None
        b_ub_arr = np.array(b_ub) if b_ub else None
        A_eq_arr = np.array(A_eq) if A_eq else None
        b_eq_arr = np.array(b_eq) if b_eq else None

        # Bounds as sequence
        raw_bounds = []
        for v in variables:
            lb = v.lowBound if v.lowBound is not None else -np.inf
            ub = v.upBound if v.upBound is not None else np.inf
            raw_bounds.append((lb, ub))

        # Integrality flags
        integrality = np.array(
            [
                1 if v.cat in [pulp.LpInteger, pulp.LpBinary] else 0
                for v in variables
            ],
            dtype=int,
        )

        return {
            "c": c,
            "A_ub": A_ub_arr,
            "b_ub": b_ub_arr,
            "A_eq": A_eq_arr,
            "b_eq": b_eq_arr,
            "bounds": raw_bounds,
            "integrality": integrality,
            "constant_offset": constant_offset,
            "variable_names": [v.name for v in variables],
            "constraint_names": [c.name for c in prob.constraints.values()],
        }


    def solve_with_scipy(prob, custom_gap=None):
        data = pulp_to_scipy_linprog(prob)

        # Solve integer or continuous
        if data["integrality"].any():
            # Build constraints list
            constraints = []
            if data["A_ub"] is not None:
                constraints.append(
                    LinearConstraint(data["A_ub"], -np.inf, data["b_ub"])
                )
            if data["A_eq"] is not None:
                constraints.append(
                    LinearConstraint(data["A_eq"], data["b_eq"], data["b_eq"])
                )

            # Convert bounds to scipy Bounds
            lbs, ubs = zip(*data["bounds"])
            bounds_obj = Bounds(np.array(lbs), np.array(ubs))
            options = {"mip_rel_gap": 1e-3}
            if custom_gap is not None:
                options["mip_rel_gap"] = custom_gap
            res = milp(
                c=data["c"],
                constraints=constraints,
                bounds=bounds_obj,
                integrality=data["integrality"],
                options=options,
            )
        else:
            res = linprog(
                c=data["c"],
                A_ub=data["A_ub"],
                b_ub=data["b_ub"],
                A_eq=data["A_eq"],
                b_eq=data["b_eq"],
                bounds=data["bounds"],
            )

        # Write back solution
        if res.success:
            for name, val in zip(data["variable_names"], res.x):
                prob.variablesDict()[name].varValue = val
            opt = res.fun + data["constant_offset"]
            prob.objective_value = -opt if prob.sense == pulp.LpMaximize else opt
            prob.status = pulp.LpStatusOptimal
        else:
            prob.status = pulp.LpStatusNotSolved
        return prob
    return (
        ScatterWidget,
        distance_matrix,
        mo,
        np,
        pd,
        plt,
        pulp,
        solve_with_scipy,
    )


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    # Übersicht: Diskrete Optimierungsprobleme

    In dieser Demo stellen wir folgende Modelle vor:

    - Warehouse Location Problem  
    - Set Covering Problem  
    - Fixed-Charge Facility Location  
    - Quantity Discount Modell  
    - Bin Packing Problem
    """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    ## 📦 Warehouse Location Problem

    - **Entscheidungsvariablen:**  
      - $y_j \in \{0,1\}$: Eröffnung von Lager $j$  
      - $x_{ij} \ge 0$: Lieferung von Lager $j$ an Kunde $i$

    - **Zielfunktion:**  
      $\min \sum_j f_j y_j + \sum_{i,j} c_{ij} x_{ij}$

    - **Nebenbedingungen:**  
      - Nachfrage: $\sum_j x_{ij} \ge d_i$ für alle $i$  
      - Kapazität: $\sum_i x_{ij} \le u_j \, y_j$ für alle $j$
    """
    )
    return


@app.cell
def _(pulp, solve_with_scipy):
    def solve_wlp_ev():
        # Daten
        # Entfernungen (6 Standorte × 10 Kunden)
        d = [
            [10, 20, 30, 15, 25, 18, 12, 8,  15, 10],
            [20, 10, 25, 12, 15, 20, 25, 30, 35, 40],
            [30, 15, 18, 10, 20, 25, 30, 35, 40, 45],
            [40, 25, 12, 15, 10, 20, 25, 30, 35, 40],
            [15, 18, 20, 25, 30, 15, 10, 12, 15, 18],
            [25, 30, 25, 18, 12, 15, 20, 25, 30, 35],
        ]

        fixed_costs   = [10000, 8000, 12000, 15000, 10000, 13000]
        capacities    = [500, 650, 600, 400, 450, 800]
        demand        = [100, 200, 150, 50, 75, 80, 120, 90, 200, 150]

        num_sites     = len(fixed_costs)   # 6
        num_customers = len(demand)        # 10

        # Problemdefinition
        prob = pulp.LpProblem("Facility_Location", pulp.LpMinimize)

        # Entscheidungsvariablen
        # y[j] = 1, wenn Station j eröffnet wird
        y = pulp.LpVariable.dicts("Oeffnen",   range(num_sites), cat="Binary")
        # x[i][j] = 1, wenn Kunde i von Station j bedient wird
        x = pulp.LpVariable.dicts("Zuordnen",
                                  (range(num_customers), range(num_sites)),
                                  cat="Binary")

        # Zielfunktion: Fixkosten + Transportkosten (Entfernung × Nachfrage)
        prob += (
            # Fixkosten
            pulp.lpSum(fixed_costs[j] * y[j]
                       for j in range(num_sites))
            # Transportkosten: d[j][i] statt d[i]
            + pulp.lpSum(d[j][i] * demand[i] * x[i][j]
                         for i in range(num_customers)
                         for j in range(num_sites))
        )

        # Restriktionen
        # 1) Jeder Kunde i muss genau von einer Station versorgt werden
        for i in range(num_customers):
            prob += pulp.lpSum(x[i][j] for j in range(num_sites)) == 1

        # 2) Kapazitätsbeschränkung: Gesamtnachfrage an Station j ≤ Kapazität_j falls geöffnet
        for j in range(num_sites):
            prob += pulp.lpSum(demand[i] * x[i][j] 
                               for i in range(num_customers)) <= capacities[j] * y[j]

        # Modell lösen
        prob = solve_with_scipy(prob)

        # Ergebnisse ausgeben
        print("Status:", pulp.LpStatus[prob.status])
        print("Gesamtkosten: ", pulp.value(prob.objective))


        print("\nGeöffnete Stationen:")
        Fixkosten = 0
        for j in range(num_sites):
            print(y[j].value(), y[j].name)
            if y[j].value() > 0.5:
                Fixkosten += fixed_costs[j]
                print(f"  Standort {j} (Fixkosten {fixed_costs[j]}, Kapazität {capacities[j]})")
        print(f"Fixkosten: {Fixkosten}")


        print("\nKunden-Zuordnung:")
        Lieferkosten = 0
        for i in range(num_customers):
            for j in range(num_sites):
                if x[i][j].value() > 0.5:
                    Lieferkosten += d[j][i] * demand[i]
                    print(f"  Kunde {i+1} (Nachfrage {demand[i]}) → Standort {j}")
        print(f"Lieferkosten: {Lieferkosten}")

    return (solve_wlp_ev,)


@app.cell
def _(solve_wlp_ev):
    solve_wlp_ev()
    return


@app.cell
def _(pulp, solve_with_scipy):
    def solve_wlp_versand():
        # 1) Daten
        site_names = ["London", "Madrid", "Paris", "Berlin", "Turin"]
        market_names = ["UK", "DE", "CH", "IT", "F"]

        # Standorte: 0=London,1=Madrid,2=Paris,3=Berlin,4=Turin
        fixed_costs = [20, 15, 22, 21, 16]    # in T€
        # Zielmärkte: 0=UK,1=DE,2=CH,3=IT,4=F
        k = [0.25, 0.30, 0.15, 0.10, 0.20]    # Anteile der Kunden

        # Lieferzeiten d[j][i] in Tagen
        d = [
            [0.5, 2,   3,   3,   1.5],   # London
            [2.5, 3,   2,   1,   2  ],   # Madrid
            [1.5, 1,   2,   2,   0.5],   # Paris
            [2,   0.5, 1.5, 2,   1  ],   # Berlin
            [3,   2,   1,   0.5, 2  ],   # Turin
        ]

        num_sites   = len(fixed_costs)  # 5
        num_markets = len(k)            # 5

        # 2) Modell anlegen
        prob = pulp.LpProblem("WLP_Qualitaetsvariante", pulp.LpMinimize)

        # 3) Entscheidungsvariablen
        y = pulp.LpVariable.dicts("Open",   range(num_sites), cat="Binary")
        x = pulp.LpVariable.dicts("Assign",
                                  (range(num_markets), range(num_sites)),
                                  cat="Binary")

        # 4) Zielfunktion: nur Fixkosten minimieren
        prob += pulp.lpSum(fixed_costs[j] * y[j] 
                           for j in range(num_sites))

        # 5) Restriktionen

        # 5.1) Genau 2–3 Zentren öffnen
        prob += pulp.lpSum(y[j] for j in range(num_sites)) >= 2
        prob += pulp.lpSum(y[j] for j in range(num_sites)) <= 3

        # 5.2) Jeder Markt wird genau einem Zentrum zugewiesen
        for i in range(num_markets):
            prob += pulp.lpSum(x[i][j] for j in range(num_sites)) == 1

        # 5.3) Zuordnung nur, wenn Zentrum offen
        for i in range(num_markets):
            for j in range(num_sites):
                prob += x[i][j] <= y[j]

        # 5.4) Qualitätsniveau: für jeden Markt max 1.5 Tage
        for i in range(num_markets):
            prob += pulp.lpSum(d[j][i] * x[i][j]
                               for j in range(num_sites)) <= 1.5

        # 5.5) Systemweite durchschnittliche Lieferzeit ≤ 1.1 Tage
        prob += pulp.lpSum(k[i] * d[j][i] * x[i][j]
                           for i in range(num_markets)
                           for j in range(num_sites)) <= 1.1

        # 6) Lösen
        prob = solve_with_scipy(prob)

        # 7) Ergebnisse ausgeben
        print("Status:", pulp.LpStatus[prob.status])
        print("Geöffnete Zentren:")
        for j in range(num_sites):
            if y[j].value() > 0.5:
                print(f"  {site_names[j]} – Fixkosten {fixed_costs[j]}")

        print("\nMarkt-Zuweisungen:")
        for i in range(num_markets):
            for j in range(num_sites):
                if x[i][j].value() > 0.5:
                    print(f"   {site_names[j]} → {market_names[i]}   (Lieferzeit {d[j][i]} Tage)")


    return (solve_wlp_versand,)


@app.cell
def _(solve_wlp_versand):
    solve_wlp_versand()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    # Fixed‐Charge (Festkosten) in Optimierungsmodellen

    ## 1. Was ist „Fixed Charge“?

    Ein **Fixed Charge** (oder Festkosten) bezeichnet einen einmalig anfallenden, unabhängigen Kostenbestandteil, der nur entsteht, wenn eine bestimmte Aktivität durchgeführt oder eine Anlage in Betrieb genommen wird.  
    - **Beispiele:**  
      - Einmalige Einrichtungskosten („Setup Costs“) für eine Maschine oder Produktionslinie  
      - Anlaufkosten für das Eröffnen eines Lagers oder einer Ladestation  
      - Pauschale Lizenzkosten, die bei Nutzung einer Software anfallen  

    ## 2. Charakteristik

    | Merkmal                 | Fixed Charge                           |
    |-------------------------|----------------------------------------|
    | Abhängig von Stückzahl? | **Nein** (unabhängig von der Menge)    |
    | Form der Kostenfunktion | Sprungfunktion (stair‐step)          |
    | Modellierung            | Mischung aus binären und kontinuierlichen Variablen |

    Reine lineare Modelle (LP) können nur stetige, lineare Kostenstrukturen abbilden. Ein Fixed Charge erzeugt eine **nicht‐lineare**, diskontinuierliche Kostenkomponente.

    Deshalb benötigen wir **Mixed‐Integer Programming (MIP)**:

    - **Binärvariable** \(y\in\{0,1\}\) markiert, ob die Aktivität genutzt wird.  
    - **Kontinuierliche Variable** \(x\ge0\) steht für die ausgelieferte Menge / Produktionsmenge.
    """
    )
    return


@app.cell
def _(pulp, solve_with_scipy):
    def fixed_charge():
        product_names = ["P1", "P2", "P3"]
        profit = {"P1":48, "P2":55, "P3":50}
        setup  = {"P1":1000, "P2":800, "P3":900}
        time_req = {
          "P1":{"Drehen":2, "Fräsen":6, "Montage":5},
          "P2":{"Drehen":3, "Fräsen":3, "Montage":6},
          "P3":{"Drehen":6, "Fräsen":4, "Montage":2},
        }
        avail = {"Drehen":600, "Fräsen":300, "Montage":400}

        # Big M
        M = 10000

        # Modell
        prob = pulp.LpProblem("Remington_BigM", pulp.LpMaximize)

        # Variablen
        x = pulp.LpVariable.dicts("x", product_names, lowBound=0, cat="Integer")
        y = pulp.LpVariable.dicts("y", product_names, cat="Binary")

        # Zielfunktion
        prob += (
            pulp.lpSum(profit[p]*x[p] for p in product_names)
          - pulp.lpSum(setup[p]*y[p]  for p in product_names)
        )

        # Kapazitäten je Maschine
        for m in avail:
            prob += pulp.lpSum(time_req[p][m] * x[p] for p in product_names) <= avail[m]

        # Big M - Kopplung
        for p in product_names:
            prob += x[p] <= M * y[p], f"BigM_{p}"

        # Lösen
        prob = solve_with_scipy(prob)

        # Ausgabe
        print("Status:", pulp.LpStatus[prob.status])
        print("Gewinn:", pulp.value(prob.objective))
        for p in product_names:
            print(f"{p}: Menge={x[p].value():.0f}, Setup={int(y[p].value())}")

    return (fixed_charge,)


@app.cell
def _(fixed_charge):
    fixed_charge()
    return


@app.cell
def _(pulp, solve_with_scipy):
    def mengenrabatt():
        # === 1) Parameter ===

        # Gewinne π_ij pro Einheit (bitte deine Werte hier einsetzen):
        #   π11 = Profit für x[1,1], π12 = Profit für x[1,2], usw.
        pi11 = 10   # <-- z.B. Ersatzwert, bitte anpassen
        pi12 = 15
        pi21 = 12
        pi22 = 18

        # Als Dictionary für den Zugriff pi[i][j]
        pi = {
            1: { 
                1: 300,   # Standard-Profit Aqua Spa (Beispielwert, bitte anpassen)
                2: 375    # Rabatt-Profit Aqua Spa, wenn >75 Stück produziert
            },
            2: {
                1: 250,   # Standard-Profit Hydro-Lux (Beispielwert, bitte anpassen)
                2: 325    # Rabatt-Profit Hydro-Lux, wenn >50 Stück produziert
            },
        }


        # Ressourcenbedarf a_mij  (m in ["Pumps","Labor","Pipelines"])
        a = {
            "Pumps":     { (1,1): 1,  (1,2): 1,  (2,1): 1,  (2,2): 1   },
            "Labor":     { (1,1): 9,  (1,2): 9,  (2,1): 6,  (2,2): 6   },
            "Pipelines": { (1,1): 12, (1,2): 12, (2,1): 16, (2,2): 16  },
        }

        # Verfügbare Kapazitäten
        b = {"Pumps":200, "Labor":1566, "Pipelines":2880}

        # Big-M für die Kopplung x[i,2] ≤ M·y[i]
        M = 10000

        # Mindestmengen, um Kondition 2 "zu aktivieren"
        min_vol = {1: 75, 2: 50}


        # === 2) Modell aufsetzen ===
        prob = pulp.LpProblem("Verbindungs_Nebenbedingungen", pulp.LpMaximize)

        # Indizes
        products   = [1, 2]      # i
        conds      = [1, 2]      # j (1 = Standard, 2 = Vorteil)


        # === 3) Variablen ===
        # x[i,j] = produzierte Menge von Produkt i unter Kondition j
        x = pulp.LpVariable.dicts("x",
            [(i,j) for i in products for j in conds],
            lowBound=0, cat="Continuous")

        # y[i] = 1, wenn wir für Produkt i die Vorteilskondition (j=2) nutzen
        y = pulp.LpVariable.dicts("y", products, cat="Binary")


        # === 4) Zielfunktion ===
        prob += pulp.lpSum(pi[i][j] * x[(i,j)]
                           for i in products
                           for j in conds), "Maximiere_Profit"


        # === 5) Nebenbedingungen ===

        # 5.1) Ressourcen­beschränkungen
        for m, cap in b.items():
            prob += (
                pulp.lpSum(a[m][(i,j)] * x[(i,j)]
                           for i in products for j in conds)
                <= cap,
                f"Kapaz_{m}"
            )

        # 5.2) Verbindungs-NB nur für j=2 (Vorteilskondition)
        for i in products:
            # a) Mindestmenge bei y=1
            prob += x[(i,2)] >= min_vol[i] * y[i], f"MinVol_{i}"
            # b) Big-M-Obergrenze bei y=0
            prob += x[(i,2)] <= M        * y[i], f"MaxVol_{i}"


        # === 6) Lösen ===
        prob = solve_with_scipy(prob)


        # === 7) Ergebnisse ausgeben ===
        print("Status:", pulp.LpStatus[prob.status])
        print("Optimaler Profit:", pulp.value(prob.objective))

        for i in products:
            print(f"\nProdukt {i}:")
            for j in conds:
                print(f"  x[{i},{j}] = {x[(i,j)].value():.1f}")
            print(f"  y[{i}] (Vorteilskondition aktiv?) = {int(y[i].value())}")
    return (mengenrabatt,)


@app.cell
def _(mengenrabatt):
    mengenrabatt()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    # Bin-Packing Problem

    Gegeben sind  
    - eine Menge von \(n\) **Items** mit Gewichten \(w_1, w_2, \dots, w_n\),  
    - identische **Bins** (Behälter) mit Kapazität \(C\).  

    Ziel ist es, alle Items in so wenige Bins wie möglich zu verteilen, ohne dass in einem Bin die Kapazität überschritten wird.
    """
    )
    return


@app.cell
def _(pulp, solve_with_scipy):
    def binpacking():
        # === 1) Daten ===
        # Gewichte der 10 Items
        w = [3, 3, 3, 5, 2, 2, 2, 2, 2]
        n = len(w)

        # Kapazität jedes Bins
        C = 8

        # Wir erlauben im schlimmsten Fall so viele Bins wie Items
        bins = list(range(n))

        # === 2) Modell anlegen ===
        prob = pulp.LpProblem("Bin_Packing", pulp.LpMinimize)

        # === 3) Entscheidungsvariablen ===
        # y[j] = 1, wenn Bin j benutzt wird
        y = pulp.LpVariable.dicts("BinUsed", bins, cat="Binary")

        # x[i][j] = 1, wenn Item i in Bin j landet
        x = pulp.LpVariable.dicts("Assign",
                                  (range(n), bins),
                                  cat="Binary")

        # === 4) Zielfunktion ===
        # Minimiere die Anzahl benutzter Bins
        prob += pulp.lpSum(y[j] for j in bins)

        # === 5) Nebenbedingungen ===

        # 5.1) Jedes Item muss genau in einem Bin landen
        for i in range(n):
            prob += pulp.lpSum(x[i][j] for j in bins) == 1, f"OneBinPerItem_{i}"

        # 5.2) Kapazitäts­beschränkung pro Bin
        for j in bins:
            prob += pulp.lpSum(w[i] * x[i][j] for i in range(n)) \
                    <= C * y[j], f"Cap_Bin_{j}"

        # === 6) Lösen ===
        prob = solve_with_scipy(prob)

        # === 7) Ergebnis ausgeben ===
        print("Status:", pulp.LpStatus[prob.status])
        print("Benötigte Bins:", sum(y[j].value() for j in bins))
        print()

        for j in bins:
            if y[j].value() > 0.5:
                assigned = [i for i in range(n) if x[i][j].value() > 0.5]
                total_w  = sum(w[i] for i in assigned)
                print(f"Bin {j}: Items {assigned}, Gesamtgewicht = {total_w}")

    return (binpacking,)


@app.cell
def _(binpacking):
    binpacking()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    # Traveling-Salesman-Problem (TSP) mit MTZ-Formulierung

    Gegeben sind  
    - eine Menge von \(n\) **Städten** (Knoten) \(1,2,\dots,n\),  
    - paarweise Distanzen \(d_{ij}\ge0\) zwischen jeder Stadt \(i\) und \(j\).  

    Gesucht ist eine **Rundreise** („Tour“), die jede Stadt genau einmal besucht und zum Start zurückkehrt, mit minimaler Gesamtdistanz.

    ---

    ## Variablen

    - \(x_{ij}\in\{0,1\}\) für alle \(i,j\in\{1,\dots,n\}\):  
      \[
        x_{ij}=1\quad\Leftrightarrow\quad\text{die Tour geht von Stadt \(i\) nach Stadt \(j\).}
      \]
    - Hilfsvariablen \(u_i\in\mathbb{Z}\) für \(i=1,\dots,n\), um Subtouren zu verhindern.

    ---

    ## Zielfunktion

    \[
    \min\;\sum_{i=1}^{n}\sum_{j=1}^{n} d_{ij}\,x_{ij}.
    \]

    ---

    ## Grundlegende Einschränkungen

    1. **Ausgehender Grad = 1**
   
    \[
         \sum_{j=1}^{n} x_{ij} = 1
         \quad\forall\,i=1,\dots,n.
    \]
   
    3. **Eingehender Grad = 1**
    
    \[
         \sum_{i=1}^{n} x_{ij} = 1
         \quad\forall\,j=1,\dots,n.
    \]

    ---

    ## MTZ-Subtour-Elimination

    ### 1. Startknoten festlegen  
    Wähle z. B. Stadt 1 als Start:  

    \[
      u_1 = 1.
    \]

    ### 2. Indizes für die übrigen Knoten  

    \[
      u_i \in \{2,3,\dots,n\}
      \quad\forall\,i=2,\dots,n.
    \]

    ### 3. MTZ-Bedingungen  
    Für alle \(i\neq1\), \(j\neq1\), \(i\neq j\) gilt:

    \[
      u_i \;-\; u_j \;+\; n\,x_{ij}\;\le\; n - 1.
    \]
  
    - Wenn \(x_{ij}=1\), erzwingen wir  
      \(\;u_i - u_j \le -1\),  
      d. h. der Index ­\(u_i\) liegt genau um 1 höher als \(u_j\).  
    - Wenn \(x_{ij}=0\), ist nur  
      \(\;u_i - u_j \le n-1\)  
      aktiv (keine Restriktion).

    Damit werden alle Subtouren, die nicht über Stadt 1 laufen, unterbunden.

    ---

    **Hinweis:**  
    Die MTZ-Formulierung ist kompakt (nur \(O(n^2)\) Nebenbedingungen), aber für große \(n\) oft weniger effizient als stärkere Schnittmengen- oder Flow-basierten Modelle.  
    """
    )
    return


@app.cell
def _(ScatterWidget, mo):
    widget = mo.ui.anywidget(ScatterWidget(height=300))
    return (widget,)


@app.cell
def _(pd, widget):
    df = pd.DataFrame(widget.data
                     , columns=["x", "y", "label"])
    return (df,)


@app.cell(hide_code=True)
def _(df, distance_matrix, mo, np):
    if len(df.index) <= 1:
        coords = np.array([[0, 0], [0, 0]])
    else:
        # 1. Calculate the Distance Matrix
        coords = df[['x', 'y']].values
    dist_matrix = distance_matrix(coords, coords)
    mip_gap_chooser = mo.ui.slider(start=0.001, stop=0.2, step=0.001, value=0.05, label="MIP Gap", show_value=True)
    return coords, dist_matrix, mip_gap_chooser


@app.cell
def _(mip_gap_chooser, pulp, solve_with_scipy):
    def solveTSP(distances):
        if distances is None or len(distances) == 0:
            return([])
        n = distances.shape[0]
        prob = pulp.LpProblem("TSP", pulp.LpMinimize)

        # Decision variables
        x = pulp.LpVariable.dicts("x", (range(n), range(n)), cat="Binary")

        # Objective function: minimize total distance
        prob += pulp.lpSum(distances[i][j] * x[i][j] for i in range(n) for j in range(n))

        # Constraints
        for i in range(n):
            prob += pulp.lpSum(x[i][j] for j in range(n) if j != i) == 1, f"Out_{i}"
            prob += pulp.lpSum(x[j][i] for j in range(n) if j != i) == 1, f"In_{i}"

        # Subtour elimination constraints
        u = pulp.LpVariable.dicts("u", range(n), lowBound=0, cat="Integer")
        for i in range(1, n):
            for j in range(1, n):
                if i != j:
                    prob += u[i] - u[j] + (n-1) * x[i][j] <= n - 2

        # Solve the problem
        prob = solve_with_scipy(prob, custom_gap=mip_gap_chooser.value)
        print(f"Optimale Routenlänge: {prob.objective.value()}")
        #need to return the solution path as a sequence of coordinates
        path = []
        for i in range(n):
            for j in range(n):
                if x[i][j]:
                    if x[i][j].value() > 0.5:
                        path.append((i, j))
        return path
    return (solveTSP,)


@app.cell(hide_code=True)
def _(coords, df, dist_matrix, mip_gap_chooser, mo, plt, solveTSP, widget):
    #i receive a sequence of points from solving and want to plot them
    route = solveTSP(dist_matrix)
    # Plot the optimal route
    plt.figure(figsize=(8, 6))
    plt.scatter(coords[:, 0], coords[:, 1], c='blue', label='Points')


    # Plot the route
    for i in range(len(route)):
        start = route[i][0]
        end = route[i][1]
        plt.plot([coords[start, 0], coords[end, 0]], 
                 [coords[start, 1], coords[end, 1]], 
                 'r-')

    plt.title(f"Lösungsroute - MIP Gap: {mip_gap_chooser.value:.3f}")
    plt.xlabel('X Coordinate')
    plt.ylabel('Y Coordinate')
    plt.legend()
    plt.grid()

    if len(df.index) > 1:
        outputRoute = plt.gca()
    else:
        outputRoute = mo.callout("insufficient number of points")

    mo.hstack([mo.vstack([mip_gap_chooser,widget]),outputRoute], justify="start")
    return


if __name__ == "__main__":
    app.run()
