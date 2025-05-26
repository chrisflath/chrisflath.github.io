import marimo

__generated_with = "0.13.11"
app = marimo.App(width="full")


@app.cell
def _():
    import marimo as mo
    return (mo,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    # 🏨 Revenue Management at the Park Hyatt Philadelphia

    In this exercise, you'll take on the role of revenue manager at the **Park Hyatt Philadelphia**.  

    Your hotel has **118 King/Queen rooms**. You sell rooms to two types of customers:

    - **High-fare customers** (e.g., business travelers)  
      ➤ Book late, pay **€225**  
      ➤ Demand is uncertain: follows a Poisson distribution with mean **27.3**

    - **Low-fare customers** (e.g., vacationers)  
      ➤ Book early, pay **€159**  
      ➤ Demand is abundant

    You must decide:  
    **How many rooms should you protect for high-fare customers?**  
    Every room you sell early at a low fare cannot be sold later at the high fare. But if you protect too many, you leave rooms empty.

    Your task is to explore the **trade-off between spoilage and spillage** and find the optimal booking limit.

    ---

    ### 🟣 Spoilage
    **Definition:**  
    Spoilage occurs when inventory (e.g., rooms) goes unsold — even though it could have been sold earlier.

    **Example:**  
    You protect 40 rooms for high-fare guests, but only 25 actually show up. The 15 empty rooms are lost revenue.

    **Causes:**

    - Protecting too many rooms
    - Overestimating high-fare demand
    - Not selling to low-fare customers early enough

    **Implication: Spoilage = lost opportunity to sell.**

    ---

    ### 🟢 Spillage
    **Definition:**  
    Spillage occurs when high-paying customers are turned away because the inventory was already sold to lower-paying customers.

    **Example:**  
    You sell 110 rooms early at low rates. Later, 20 high-fare customers arrive — but all rooms are gone.

    **Causes:**

    - Protecting too few rooms
    - Underestimating late high-fare demand
    - Selling too much too soon

    **Implication: Spillage = lost opportunity to sell at a higher price.**

    ---
    """
    )
    return


@app.cell
def _(mo):
    import numpy as np
    import pandas as pd
    import altair as alt

    # Constants for the Hyatt scenario
    ROOM_CAPACITY = 118
    R_H = 225  # High fare
    R_L = 159  # Low fare
    MU = 27.3  # Mean high-fare demand

    rng = np.random.default_rng()  # no fixed seed!
    demand_sample = rng.poisson(lam=27.3, size=1000)

    # Sliders for student interaction
    protection_slider = mo.ui.slider(start=0, stop=ROOM_CAPACITY, step=1, value=30, label="Protection level for high-fare (Q)",
                                    show_value=True)
    return (
        ROOM_CAPACITY,
        R_H,
        R_L,
        alt,
        demand_sample,
        np,
        pd,
        protection_slider,
    )


@app.cell
def _(
    ROOM_CAPACITY,
    R_H,
    R_L,
    alt,
    demand_sample,
    mo,
    np,
    pd,
    protection_slider,
):
    def simulate_protection_level(n_sim = 10):
        Q = protection_slider.value
        Q_prev = max(0, Q - 1)

        high_demand = demand_sample[0:n_sim]

        def simulate(Q_val):
            high_served = np.minimum(high_demand, Q_val)
            low_served = np.minimum(ROOM_CAPACITY - Q_val, ROOM_CAPACITY - high_served)
            revenue = high_served * R_H + low_served * R_L
            return revenue, high_served, low_served

        # Current Q
        revenue, high_served, low_served = simulate(Q)
        lost_high = np.maximum(high_demand - Q, 0)
        unused_protected = np.maximum(Q - high_demand, 0)
        total_sold = high_served + low_served
        rev_per_room = np.where(total_sold > 0, revenue / total_sold, 0)

        # Previous Q - 1
        revenue_prev, _, _ = simulate(Q_prev)

        # Compute stats
        delta_rev = np.mean(revenue) - np.mean(revenue_prev)

        df = pd.DataFrame({
            "Simulation": np.arange(n_sim),
            "Revenue": revenue,
            "Lost high-fare sales": lost_high,
            "Unfilled protected rooms": unused_protected,
            "Revenue per sold room": rev_per_room
        })

        # Summary
        summary = f"""
        **Average revenue**: €{np.mean(revenue):,.2f}  
        **Avg. high-fare customers turned down**: {np.mean(lost_high):.2f}  
        **Avg. protected rooms unused**: {np.mean(unused_protected):.2f}  
        **Avg. revenue per sold room**: €{np.mean(rev_per_room):,.2f}  
        **ΔRevenue from increasing Q by 1**: €{delta_rev:,.2f}
        """

        chart = alt.Chart(df).mark_bar().encode(
            x=alt.X("Revenue:Q", bin=alt.Bin(step=1000), title="Total Revenue (€)", scale=alt.Scale(domain=[0, 25000]), axis=alt.Axis(values=[0, 5000, 10000, 15000, 20000, 25000])),
            y=alt.Y("count()", title="Frequency")
        ).properties(width=600, height=300, title="Revenue Distribution")

        return mo.vstack([
            mo.hstack([protection_slider]),
            mo.md(summary),

            chart
        ])
    return (simulate_protection_level,)


@app.cell
def _(simulate_protection_level):
    simulate_protection_level(n_sim=100)
    return


if __name__ == "__main__":
    app.run()
