#!/usr/bin/env python3
"""
Data preparation script for DMA course.
Generates all CSV datasets for SQL exercises.

Run: python scripts/prepare_data.py
Output: public/*.csv
"""

import pandas as pd
import numpy as np
from pathlib import Path

# Output directory
OUTPUT_DIR = Path(__file__).parent.parent / "public"
OUTPUT_DIR.mkdir(exist_ok=True)


def create_bundesliga_final():
    """
    Bundesliga final standings (Abschlusstabelle).
    Cross-sectional data: 18 teams, 1 time point.
    Good for: Bar charts, sorting, filtering.
    """
    data = {
        "Mannschaft": [
            "Bayern München", "Bayer Leverkusen", "VfB Stuttgart", "RB Leipzig",
            "Borussia Dortmund", "Eintracht Frankfurt", "SC Freiburg", "VfL Wolfsburg",
            "1. FC Union Berlin", "Werder Bremen", "TSG Hoffenheim", "FC Augsburg",
            "Borussia Mönchengladbach", "1. FSV Mainz 05", "1. FC Köln", "VfL Bochum",
            "1. FC Heidenheim", "SV Darmstadt 98"
        ],
        "Spiele": [34] * 18,
        "Siege": [23, 22, 20, 19, 18, 14, 13, 12, 11, 11, 10, 10, 9, 8, 7, 6, 8, 4],
        "Unentschieden": [6, 8, 6, 8, 7, 10, 9, 8, 10, 8, 8, 6, 8, 10, 7, 8, 5, 8],
        "Niederlagen": [5, 4, 8, 7, 9, 10, 12, 14, 13, 15, 16, 18, 17, 16, 20, 20, 21, 22],
    }

    df = pd.DataFrame(data)
    df["ToreGeschossen"] = [94, 82, 78, 77, 68, 51, 45, 51, 42, 48, 56, 43, 56, 40, 34, 36, 42, 30]
    df["ToreKassiert"] = [45, 32, 42, 47, 52, 50, 52, 55, 46, 58, 66, 67, 67, 55, 68, 73, 70, 86]
    df["Tordifferenz"] = df["ToreGeschossen"] - df["ToreKassiert"]
    df["Punkte"] = df["Siege"] * 3 + df["Unentschieden"]

    df.to_csv(OUTPUT_DIR / "bundesliga.csv", index=False)
    print(f"Created: bundesliga.csv ({len(df)} teams)")
    return df


def create_bundesliga_spieltage():
    """
    Bundesliga match-day progression (all 34 Spieltage).
    Temporal data: 18 teams × 34 match days.
    Good for: Line charts, temporal analysis, window functions.
    """
    np.random.seed(42)  # Reproducible

    teams = [
        "Bayern München", "Bayer Leverkusen", "VfB Stuttgart", "RB Leipzig",
        "Borussia Dortmund", "Eintracht Frankfurt", "SC Freiburg", "VfL Wolfsburg",
        "1. FC Union Berlin", "Werder Bremen", "TSG Hoffenheim", "FC Augsburg",
        "Borussia Mönchengladbach", "1. FSV Mainz 05", "1. FC Köln", "VfL Bochum",
        "1. FC Heidenheim", "SV Darmstadt 98"
    ]

    # Final points (from standings above)
    final_points = [75, 74, 66, 65, 61, 52, 48, 44, 43, 41, 38, 36, 35, 34, 28, 26, 29, 20]

    # Strength factor determines win probability
    strength = {team: pts / 75 for team, pts in zip(teams, final_points)}

    rows = []
    for team in teams:
        cumulative_points = 0
        cumulative_goals = 0
        cumulative_conceded = 0

        for spieltag in range(1, 35):
            # Simulate match result based on team strength
            team_strength = strength[team]
            rand = np.random.random()

            if rand < team_strength * 0.6:  # Win
                points = 3
                goals = np.random.randint(1, 5)
                conceded = np.random.randint(0, goals)
            elif rand < team_strength * 0.6 + 0.25:  # Draw
                points = 1
                goals = np.random.randint(0, 3)
                conceded = goals
            else:  # Loss
                points = 0
                conceded = np.random.randint(1, 5)
                goals = np.random.randint(0, conceded)

            cumulative_points += points
            cumulative_goals += goals
            cumulative_conceded += conceded

            rows.append({
                "Spieltag": spieltag,
                "Mannschaft": team,
                "Punkte_Spiel": points,
                "Tore_Spiel": goals,
                "Gegentore_Spiel": conceded,
                "Punkte_Kumuliert": cumulative_points,
                "Tore_Kumuliert": cumulative_goals,
                "Gegentore_Kumuliert": cumulative_conceded
            })

    df = pd.DataFrame(rows)
    df.to_csv(OUTPUT_DIR / "bundesliga_spieltage.csv", index=False)
    print(f"Created: bundesliga_spieltage.csv ({len(df)} rows = {len(teams)} teams × 34 Spieltage)")
    return df


def create_spieler():
    """
    Player data with intentional NULL values.
    Good for: NULL handling, COALESCE, IS NULL exercises.
    """
    data = {
        "Name": ["Müller", "Gündogan", "Neuer", "Wirtz", "Musiala",
                 "Sané", "Havertz", "Kimmich", "Rüdiger", "Füllkrug",
                 "Gnabry", "Tah"],
        "Vorname": ["Thomas", "Ilkay", "Manuel", "Florian", "Jamal",
                    "Leroy", "Kai", "Joshua", "Antonio", "Niclas",
                    "Serge", "Jonathan"],
        "Position": ["Angriff", "Mittelfeld", "Tor", "Mittelfeld", "Mittelfeld",
                     "Angriff", "Angriff", "Mittelfeld", "Abwehr", "Angriff",
                     "Angriff", "Abwehr"],
        "Verein": ["Bayern München", "FC Barcelona", "Bayern München", "Bayer Leverkusen", "Bayern München",
                   "Bayern München", "FC Arsenal", "Bayern München", "Real Madrid", "Borussia Dortmund",
                   "Bayern München", "Bayer Leverkusen"],
        "Tore": [5, 2, None, 8, 4, 6, 7, 1, None, 9, 3, None],  # Goalkeepers/defenders often NULL
        "Vorlagen": [3, 4, None, 6, 5, 4, 2, 7, None, 2, 4, None],
        "Spitzname": ["Mülli", "Gundo", None, None, "Bambi",
                      None, None, "Jo", "Rüdi", "Fülle", None, None]
    }

    df = pd.DataFrame(data)
    df.to_csv(OUTPUT_DIR / "spieler.csv", index=False)
    print(f"Created: spieler.csv ({len(df)} players, with NULL values)")
    return df


def create_rechnungen():
    """
    Invoice data for Benford's Law analysis.
    Contains both 'natural' and 'suspicious' invoices.
    Good for: Digit analysis, fraud detection, SUBSTR/CAST.
    """
    np.random.seed(42)

    # Natural invoices: exponentially distributed (follow Benford)
    natural_amounts = np.round(10 ** np.random.uniform(1, 4, 300), 2)

    # Suspicious invoices: more uniform distribution (deviate from Benford)
    suspicious_amounts = np.round(np.random.uniform(100, 999, 100), 2)

    rows = []

    for i, amount in enumerate(natural_amounts, 1):
        rows.append({
            "RechnungID": i,
            "Betrag": amount,
            "Kategorie": "normal",
            "Datum": f"2024-{np.random.randint(1,13):02d}-{np.random.randint(1,29):02d}"
        })

    for i, amount in enumerate(suspicious_amounts, 301):
        rows.append({
            "RechnungID": i,
            "Betrag": amount,
            "Kategorie": "verdaechtig",
            "Datum": f"2024-{np.random.randint(1,13):02d}-{np.random.randint(1,29):02d}"
        })

    df = pd.DataFrame(rows)
    df = df.sample(frac=1, random_state=42).reset_index(drop=True)  # Shuffle
    df.to_csv(OUTPUT_DIR / "rechnungen.csv", index=False)
    print(f"Created: rechnungen.csv ({len(df)} invoices for Benford analysis)")
    return df


def create_deaths_shipman():
    """
    Simulated mortality data for Shipman case study.
    Good for: Anomaly detection, GROUP BY, time analysis.
    """
    np.random.seed(42)

    doctors = ["Dr. Shipman", "Dr. Smith", "Dr. Jones", "Dr. Brown", "Dr. Wilson"]

    rows = []
    death_id = 1

    for doctor in doctors:
        if doctor == "Dr. Shipman":
            # Anomalous pattern: many deaths, mostly during office hours, mostly female
            n_deaths = 150
            hours = np.random.choice(range(9, 18), n_deaths)  # Office hours only
            genders = np.random.choice(["F", "M"], n_deaths, p=[0.82, 0.18])
            ages = np.random.normal(78, 8, n_deaths).astype(int)
        else:
            # Normal pattern: fewer deaths, distributed hours, balanced gender
            n_deaths = np.random.randint(25, 45)
            hours = np.random.choice(range(0, 24), n_deaths)  # Any hour
            genders = np.random.choice(["F", "M"], n_deaths, p=[0.52, 0.48])
            ages = np.random.normal(75, 12, n_deaths).astype(int)

        for i in range(n_deaths):
            rows.append({
                "TodesfallID": death_id,
                "Arzt": doctor,
                "Todesstunde": int(hours[i]),
                "Alter": max(50, min(99, ages[i])),  # Clip to reasonable range
                "Geschlecht": genders[i],
                "Jahr": np.random.randint(1980, 1999)
            })
            death_id += 1

    df = pd.DataFrame(rows)
    df = df.sample(frac=1, random_state=42).reset_index(drop=True)
    df.to_csv(OUTPUT_DIR / "todesfaelle.csv", index=False)
    print(f"Created: todesfaelle.csv ({len(df)} deaths for Shipman analysis)")
    return df


def main():
    print("=" * 50)
    print("DMA Course Data Preparation")
    print("=" * 50)
    print(f"Output directory: {OUTPUT_DIR}\n")

    create_bundesliga_final()
    create_bundesliga_spieltage()
    create_spieler()
    create_rechnungen()
    create_deaths_shipman()

    print("\n" + "=" * 50)
    print("All datasets created successfully!")
    print("=" * 50)


if __name__ == "__main__":
    main()
