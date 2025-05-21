import marimo

__generated_with = "0.13.11"
app = marimo.App(width="full", app_title="DWZ Explorer Ufra")


@app.cell(hide_code=True)
def _():
    import marimo as mo
    import requests
    import pandas as pd

    # URL of the dataset (must allow direct downloads)
    url = "https://raw.githubusercontent.com/WIBA-DMA/exam-2024-pprm/refs/heads/main/dwz_all_leagues_long.csv"

    # Download and save the file
    filename = "dwz_all_leagues_long.csv"

    response = requests.get(url)
    if response.status_code == 200:
        with open(filename, "wb") as file:
            file.write(response.content)
        print(f"data setup successfull")
    else:
        print(f"Failed to download the file. Status code: {response.status_code}")

    long_df = pd.read_csv(filename)
    return long_df, mo


@app.cell
def _():
    leagues = {"Unterfrankenliga" : "https://www.ligamanager.schachbund-bayern.de/ufr/ergebnisse/spielplan.htm?ligaId=2326",
               "Bezirksliga Ost" : "https://www.ligamanager.schachbund-bayern.de/ufr/ergebnisse/spielplan.htm?ligaId=2328",
               "A-Klasse" : "https://www.ligamanager.schachbund-bayern.de/ufr-mitte/ergebnisse/spielplan.htm?ligaId=2359",
              "B-Klasse" : "https://www.ligamanager.schachbund-bayern.de/ufr-mitte/ergebnisse/spielplan.htm?ligaId=2360",
              }
    return (leagues,)


@app.cell
def _(leagues, mo):
    ligaSelector = mo.ui.multiselect(leagues.keys())
    return (ligaSelector,)


@app.cell
def _(ligaSelector):
    ligaSelector
    return


@app.cell
def _(leagues, ligaSelector, long_df):
    import altair as alt

    # Convert board to numeric if not already
    plot_df = long_df[["league", "round", "team_left", "team_right", "board", "player", "dwz", "color", "result"]].copy()
    plot_df = plot_df[plot_df["league"].isin(ligaSelector.value)]

    # Group by board number (Brett) and calculate mean DWZ
    dwz_avg = plot_df.groupby(["league","board"], as_index=False)["dwz"].mean().round(0)


    # Create dodged bar chart
    chart = alt.Chart(dwz_avg).mark_bar().encode(
        x=alt.X("board:O", title="Brett"),
        y=alt.Y("dwz:Q", title="DWZ-Schnitt"),
        xOffset=alt.XOffset("league:N", sort=leagues.keys()),
    color=alt.Color("league:N", sort=leagues.keys()),
        tooltip=["league", "board", "dwz"]
    ).properties(
        title="Durchschnittliche DWZ pro Brett und Liga",
        width=600,
        height=600
    )

    return chart, plot_df


@app.cell
def _(mo, plot_df):
    temp = mo.sql(
        f"""
        SELECT league AS Liga, board AS Brett, MIN(dwz) AS dwzMin,
            ROUND(AVG(dwz),0) AS DWZmittel,
            MAX(dwz) AS dwzMax,
        FROM plot_df
        GROUP BY board, league
        ORDER BY board, league, DWZmittel DESC
        """,
        output=False
    )
    return (temp,)


@app.cell
def _(chart, mo, temp):
    mo.hstack([temp,chart])
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
