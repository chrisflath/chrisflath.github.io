import numpy as np
import pandas as pd
from statsmodels.api import OLS, add_constant


class LinearTrendSeasonalDecomposer:
    """
    Decompose one or more univariate time series in long format into
    a strictly linear trend, calendar‑aligned seasonal component,
    and residual noise per series (unique_id).
    """

    def __init__(
        self,
        period: int = 52,
        date_col: str = "date",
        actual_col: str = "demand",
        unique_id_col: str = "unique_id",
    ):
        if period < 2:
            raise ValueError("`period` must be at least 2.")
        self.period = period
        self.date_col = date_col
        self.actual_col = actual_col
        self.unique_id_col = unique_id_col

    def _get_calendar_index(self, dates: pd.Series) -> np.ndarray:
        """Map dates to a 0‑based seasonal index for grouping."""
        freq = pd.infer_freq(dates)
        if freq and freq.startswith("W"):
            # ISO week 1…53 → 0…52
            return dates.dt.isocalendar().week.astype(int).values - 1
        elif freq and freq.startswith("M"):
            # Month 1…12 → 0…11
            return dates.dt.month.astype(int).values - 1
        elif freq and freq.startswith("D"):
            # Weekday 0…6
            return dates.dt.weekday.astype(int).values
        else:
            # fallback to simple modulo
            return np.arange(len(dates)) % self.period

    def fit_transform(self, df: pd.DataFrame) -> pd.DataFrame:
        # 1) Validate & sort
        for col in (self.date_col, self.unique_id_col, self.actual_col):
            if col not in df.columns:
                raise KeyError(f"Required column '{col}' not found in DataFrame.")
        df_sorted = df.copy()
        df_sorted[self.date_col] = pd.to_datetime(df_sorted[self.date_col])
        df_sorted = df_sorted.sort_values([self.unique_id_col, self.date_col])

        components = []
        # 2) Decompose each series separately
        for uid, group in df_sorted.groupby(self.unique_id_col, sort=False):
            demand = group[self.actual_col].values
            n = len(demand)
            t = np.arange(n)

            # 2a) Fit & remove linear trend
            X = add_constant(t)
            trend_model = OLS(demand, X).fit()
            trend_vals = trend_model.predict(X)
            detrended = demand - trend_vals

            # 2b) Build seasonal component via calendar buckets
            cal_idx = self._get_calendar_index(group[self.date_col])
            # compute mean detrended per bucket
            seasonal_series = pd.Series(detrended, index=cal_idx)
            seasonal_index = seasonal_series.groupby(level=0).mean()
            # map back to each timestamp
            seasonal_vals = seasonal_index.loc[cal_idx].values

            # 2c) Residual
            residual_vals = demand - trend_vals - seasonal_vals

            comp_df = pd.DataFrame(
                {
                    self.date_col: group[self.date_col].values,
                    self.unique_id_col: uid,
                    "trend": trend_vals,
                    "seasonal": seasonal_vals,
                    "residual": residual_vals,
                }
            )
            components.append(comp_df)

        # 3) Combine & return
        result_df = pd.concat(components, ignore_index=True)
        result_df[self.date_col] = pd.to_datetime(result_df[self.date_col])
        result_df[self.unique_id_col] = result_df[self.unique_id_col].astype(
            df[self.unique_id_col].dtype
        )
        return result_df


import pandas as pd
import altair as alt


class DecompositionPlotter:
    """
    Plot historical series and its decomposition components.

    Parameters
    ----------
    history : pd.DataFrame
        DataFrame of original series with columns [date_col, actual_col].
    decomposition : pd.DataFrame
        DataFrame of decomposition components with columns [date_col, 'trend', 'seasonal', 'residual'].
    date_col : str, default 'date'
        Column name for dates in both DataFrames.
    actual_col : str, default 'demand'
        Column name for actual values in history.
    """

    def __init__(
        self,
        history: pd.DataFrame,
        decomposition: pd.DataFrame,
        date_col: str = "date",
        actual_col: str = "demand",
    ):
        # Validate inputs
        for df, name, req_cols in [
            (history, "history", [date_col, actual_col]),
            (
                decomposition,
                "decomposition",
                [date_col, "trend", "seasonal", "residual"],
            ),
        ]:
            missing = set(req_cols) - set(df.columns)
            if missing:
                raise KeyError(f"DataFrame '{name}' is missing columns: {missing}")

        # Prepare copies
        self.history = history.copy()
        self.decomp = decomposition.copy()
        self.date_col = date_col
        self.actual_col = actual_col

        # Ensure date column is datetime
        self.history[self.date_col] = pd.to_datetime(self.history[self.date_col])
        self.decomp[self.date_col] = pd.to_datetime(self.decomp[self.date_col])

    def plot(self, title: str = "Time Series Decomposition") -> alt.VConcatChart:
        """
        Generate a vertical concatenation of four Altair charts:
        history, trend, seasonal, and residual.
        """
        # Base chart properties
        x_enc = alt.X(f"{self.date_col}:T", title="Date")
        width = 600

        # 1. History
        chart_hist = (
            alt.Chart(self.history)
            .mark_line(point=True)
            .encode(
                x=x_enc,
                y=alt.Y(f"{self.actual_col}:Q", title="Observations"),
                tooltip=[
                    alt.Tooltip(f"{self.date_col}:T", title="Date"),
                    alt.Tooltip(f"{self.actual_col}:Q", title="Value"),
                ],
            )
            .properties(title="History", width=width)
        )

        # 2. Trend
        chart_trend = (
            alt.Chart(self.decomp)
            .mark_line(point=False)
            .encode(
                x=x_enc,
                y=alt.Y("trend:Q", title="Trend"),
                tooltip=[
                    alt.Tooltip(f"{self.date_col}:T", title="Date"),
                    alt.Tooltip("trend:Q", title="Trend"),
                ],
            )
            .properties(title="Linear Trend", width=width)
        )

        # 3. Seasonality
        chart_season = (
            alt.Chart(self.decomp)
            .mark_line(point=False)
            .encode(
                x=x_enc,
                y=alt.Y("seasonal:Q", title="Seasonal"),
                tooltip=[
                    alt.Tooltip(f"{self.date_col}:T", title="Date"),
                    alt.Tooltip("seasonal:Q", title="Seasonal"),
                ],
            )
            .properties(title="Seasonality", width=width)
        )

        # 4. Residual
        chart_resid = (
            alt.Chart(self.decomp)
            .mark_line(point=False)
            .encode(
                x=x_enc,
                y=alt.Y("residual:Q", title="Residual"),
                tooltip=[
                    alt.Tooltip(f"{self.date_col}:T", title="Date"),
                    alt.Tooltip("residual:Q", title="Residual"),
                ],
            )
            .properties(title="Residual", width=width)
        )

        # Concatenate vertically

        first_row = (
            alt.hconcat(
                chart_hist,
                chart_trend,
            )
            .properties(title=title)
            .configure_title(fontSize=16, fontWeight="bold")
            .configure_axis(labelFontSize=12, titleFontSize=14)
        )

        second_row = (
            alt.hconcat(
                chart_season,
                chart_resid,
            )
            .properties(title="")
            .configure_title(fontSize=16, fontWeight="bold")
            .configure_axis(labelFontSize=12, titleFontSize=14)
        )

        return [first_row, second_row]
