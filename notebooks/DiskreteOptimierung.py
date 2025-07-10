import marimo

__generated_with = "0.14.10"
app = marimo.App(width="full")


@app.cell
def _():
    import marimo as mo
    import pulp
    import numpy as np
    from scipy.optimize import linprog

    # Funktionen zur Umwandlung und Lösung mit SciPy

    def pulp_to_scipy_linprog(prob):
        variables = prob.variables()

        objective = np.array([prob.objective.get(v) if prob.objective.get(v) is not None else 0 for v in variables])
        constant_offset = prob.objective.constant

        if prob.sense == pulp.LpMaximize:
            c = -objective
            constant_offset = -constant_offset
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
            'constant_offset': constant_offset,
            'variable_names': [v.name for v in variables],
            'constraint_names': [con.name for con in prob.constraints.values()],
            'objective_sense': 'max' if prob.sense == pulp.LpMaximize else 'min',
            'problem_name': prob.name
        }


    def solve_with_scipy(prob):
        data = pulp_to_scipy_linprog(prob)
        res = linprog(
            c=data['c'],
            A_ub=data['A_ub'], b_ub=data['b_ub'],
            A_eq=data['A_eq'], b_eq=data['b_eq'],
            bounds=data['bounds'], method='highs'
        )
        if res.success:
            for name, val in zip(data['variable_names'], res.x):
                prob.variablesDict()[name].varValue = val
            val = res.fun + data['constant_offset']
            prob.objective_value = -val if prob.sense == pulp.LpMaximize else val
            prob.status = pulp.LpStatusOptimal
        else:
            prob.status = pulp.LpStatusNotSolved
        return prob
    return mo, pulp, solve_with_scipy


@app.cell
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


@app.cell
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
        y = pulp.LpVariable.dicts("Open",   range(num_sites), cat="Binary")
        # x[i][j] = 1, wenn Kunde i von Station j bedient wird
        x = pulp.LpVariable.dicts("Assign",
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
    
        # 3) Optional: verhindert, dass Kunden einer geschlossenen Station zugewiesen werden
        #    zwar redundant durch Kapazitätsbedingung, aber explizit:
        for i in range(num_customers):
            for j in range(num_sites):
                prob += x[i][j] <= y[j]
    
        # Modell lösen
        prob = solve_with_scipy(prob)
    
        # Ergebnisse ausgeben
        print("Status:", pulp.LpStatus[prob.status])
        print("Gesamtkosten: ", pulp.value(prob.objective))
    
        print("\nGeöffnete Stationen:")
        for j in range(num_sites):
            if y[j].value() > 0.5:
                print(f"  Standort {j+1} (Fixkosten {fixed_costs[j]}, Kapazität {capacities[j]})")
    
        print("\nKunden-Zuordnung:")
        for i in range(num_customers):
            for j in range(num_sites):
                if x[i][j].value() > 0.5:
                    print(f"  Kunde {i+1} (Nachfrage {demand[i]}) → Standort {j+1}")

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


@app.cell
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


@app.cell
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


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
