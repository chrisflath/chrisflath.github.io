import pandas as pd
from typing import Dict, Any, Optional
from statsforecast import StatsForecast
from statsforecast.models import (
    Naive,
    AutoARIMA,
    ARIMA,
    SimpleExponentialSmoothing,
    SimpleExponentialSmoothingOptimized,
    Holt,
    HoltWinters,
)
from utilsforecast.evaluation import evaluate
from utilsforecast.losses import mae, mape
import altair as alt
import os
from typing import List, Union, Dict, Any, Tuple
from enum import Enum

ModelParam = Dict[str, Any]
ModelParamList = List[ModelParam]
ModelParams = Dict[str, Union[ModelParam, ModelParamList]]


class DemandForecaster:
    """
    Trains and forecasts demand using benchmark and ES models via StatsForecast,
    supporting multiple variants per family.

    Parameters
    ----------
    freq : str
        Pandas frequency string (e.g., 'W' for weekly).
    model_params : Dict[str, Union[Dict, List[Dict]]], optional
        Per-family hyperparameter lists. Keys may include:
          - 'naive':            [{}] or []
          - 'ma':               [{'q': int, 'alias': str}, ...]
          - 'ses':              [{'alpha': float, 'alias': str}, ...]
          - 'holt':             [{'alpha': float, 'beta': float,
                                  'damped': bool, 'alias': str}, ...]
          - 'holt_winters':     [{'season_length': int, 'alpha': float,
                                  'beta': float, 'gamma': float,
                                  'damped': bool, 'alias': str}, ...]
        Each value may be a single dict or a list of dicts; missing entries use one optimized model.
        To skip an entire family, set its value to an empty list.
    """

    def __init__(self, freq: str = "W", model_params: Optional[ModelParams] = None):
        self.freq = freq
        # Normalize params: wrap single dicts into lists
        raw = model_params or {}
        self.model_params: Dict[str, ModelParamList] = {}
        for key, val in raw.items():
            if isinstance(val, dict):
                self.model_params[key] = [val]
            elif isinstance(val, list):
                self.model_params[key] = val
            else:
                raise ValueError(f"model_params['{key}'] must be dict or list of dicts")

        self._build_models()
        self.sf = StatsForecast(models=self.models, freq=self.freq)

    def _build_models(self):
        """Instantiate models per family and parameter set."""
        mp = self.model_params
        self.models = []

        # 1) Naive: always one if present or default
        for cfg in mp.get("naive", [{}]):
            alias = cfg.get("alias", "Naive")
            self.models.append(Naive(alias=alias))

        # 2) Moving Average via ARIMA(0,0,q)
        ma_list = mp.get("ma", [{}])
        for cfg in ma_list:
            q = cfg.get("q")
            alias = cfg.get("alias", f"MA_q{q}" if q is not None else "MA")
            if q is None:
                self.models.append(
                    AutoARIMA(seasonal=False, max_p=0, max_q=8, alias=alias)
                )
            else:
                self.models.append(ARIMA(order=(0, 0, q), alias=alias))

        # 3) Single Exponential Smoothing
        ses_list = mp.get("ses", [{}])
        for cfg in ses_list:
            alpha = cfg.get("alpha")
            alias = cfg.get("alias", f"SES_a{alpha}" if alpha is not None else "SES")
            if alpha is None:
                self.models.append(SimpleExponentialSmoothingOptimized(alias=alias))
            else:
                self.models.append(SimpleExponentialSmoothing(alpha=alpha, alias=alias))

        # 4) Double Exponential Smoothing (Holt)
        holt_list = mp.get("holt", [{}])
        for cfg in holt_list:
            alpha = cfg.get("alpha")
            beta = cfg.get("beta")
            damped = cfg.get("damped", False)
            alias = cfg.get(
                "alias", f"Holt_a{alpha}_b{beta}" if alpha or beta else "Holt"
            )
            if alpha is None and beta is None:
                self.models.append(Holt(alias=alias))
            else:
                self.models.append(
                    Holt(
                        smoothing_level=alpha,
                        smoothing_trend=beta,
                        damped=damped,
                        alias=alias,
                    )
                )

        # 5) Triple Exponential Smoothing (Holt–Winters)
        hw_list = mp.get("holt_winters", [{}])
        for cfg in hw_list:
            m = cfg.get("season_length", 52)
            alpha = cfg.get("alpha")
            beta = cfg.get("beta")
            gamma = cfg.get("gamma")
            damped = cfg.get("damped", False)
            alias = cfg.get("alias", f"HW_s{m}_a{alpha}_b{beta}_g{gamma}")
            # optimized if no smoothing params
            if alpha is None and beta is None and gamma is None:
                self.models.append(HoltWinters(season_length=m, alias=alias))
            else:
                self.models.append(
                    HoltWinters(
                        season_length=m,
                        smoothing_level=alpha,
                        smoothing_trend=beta,
                        smoothing_seasonal=gamma,
                        damped=damped,
                        alias=alias,
                    )
                )

    def fit(self, df: pd.DataFrame) -> "DemandForecaster":
        """
        Fit all models on the provided data.

        Parameters
        ----------
        df : pd.DataFrame
            Long-format DataFrame with columns ['unique_id', 'date', 'demand'].
        """
        self.sf.fit(df, id_col="unique_id", time_col="date", target_col="demand")
        return self

    def forecast(self, h: int) -> pd.DataFrame:
        """
        Forecast the next `h` periods for all series and models.

        Parameters
        ----------
        h : int
            Forecast horizon (number of periods ahead).

        Returns
        -------
        pd.DataFrame
            A DataFrame with columns ['unique_id','date',<model_aliases>].
        """
        return self.sf.predict(h=h)

    def cross_validation(self, **kwargs) -> pd.DataFrame:
        """
        Perform cross-validation on the fitted models.

        Parameters
        ----------
        **kwargs : dict
            Additional parameters for cross-validation.

        Returns
        -------
        pd.DataFrame
            A DataFrame with cross-validation results.
        """
        return self.sf.cross_validation(**kwargs, id_col="unique_id", time_col="date", target_col="demand")


class Evaluator:

    def __init__(
        self,
        forecast: pd.DataFrame,
        historic_forecast: pd.DataFrame,
        cutoff_col: str = "cutoff",
        date_col: str = "date",
        actual_col: str = "demand",
        unique_id_col: str = "unique_id",
        metric_col: str = "metric",
    ):

        self.forecast = forecast.copy()
        self.historic_forecast = historic_forecast.copy()
        self.cutoff_col = cutoff_col
        self.date_col = date_col
        self.actual_col = actual_col
        self.unique_id_col = unique_id_col
        self.metric_col: str = metric_col

    @staticmethod
    def _rename_metric_columns(df: pd.DataFrame, suffix: str) -> pd.DataFrame:

        return df.rename({"mae": f"mae_{suffix}", "mape": f"mape_{suffix}"})

    def _get_model_columns(self, df: pd.DataFrame) -> List[str]:
        return

    def evaluate(self) -> pd.DataFrame:

        model_cols = [
            col
            for col in self.forecast.columns
            if col
            not in [self.date_col, self.actual_col, self.unique_id_col, self.cutoff_col]
        ]

        evaluation_fc: dict = (
            evaluate(
                df=self.forecast,
                models=model_cols,
                time_col=self.date_col,
                target_col=self.actual_col,
                id_col=self.unique_id_col,
                metrics=[mae, mape],
            )
            .groupby(self.metric_col)[model_cols]
            .mean()
            .to_dict()
        )

        evaluation_hist = (
            evaluate(
                df=self.historic_forecast,
                models=model_cols,
                time_col=self.date_col,
                target_col=self.actual_col,
                id_col=self.unique_id_col,
                metrics=[mae, mape],
            )
            .groupby(self.metric_col)[model_cols]
            .mean()
            .to_dict()
        )

        # Merge evaluations
        evaluation = {"forecast": evaluation_fc, "history": evaluation_hist}

        return evaluation


class ForecastManager:
    """
    Manages loading or generating forecasts and historic forecasts using DemandForecaster.

    Attributes:
        freq (str): Frequency string passed to DemandForecaster (e.g., 'W').
        model_params (dict): Parameters for the forecasting models.
        forecast_path (str): File path for saving/loading the forecast results.
        historic_path (str): File path for saving/loading the historic forecast results.
        overwrite (bool): If True, existing files will be regenerated and overwritten.
    """

    def __init__(
        self,
        freq: str,
        model_params: dict,
        forecast_path: str,
        historic_path: str,
        overwrite: bool = False,
    ):
        self.freq = freq
        self.model_params = model_params
        self.forecast_path = forecast_path
        self.historic_path = historic_path
        self.overwrite = (overwrite,)
        self.date_col = "date"

    def _file_exists_and_no_overwrite(self, path: str) -> bool:
        """
        Returns True if the file exists and overwrite flag is False.
        """
        return os.path.exists(path) and not self.overwrite

    def _load(self, path: str) -> pd.DataFrame:
        """
        Loads a DataFrame from CSV or pickle based on file extension.
        """
        ext = os.path.splitext(path)[1].lower()
        if ext == ".csv":
            df = pd.read_csv(path, index_col=0, parse_dates=True)
        elif ext in (".pkl", ".pickle"):
            df = pd.read_pickle(path)
        else:
            raise ValueError(f"Unsupported file extension: {ext}")
        df[self.date_col] = pd.to_datetime(df[self.date_col])
        return df

    def _save(self, df: pd.DataFrame, path: str) -> None:
        """
        Saves a DataFrame to CSV or pickle based on file extension.
        Creates parent directories if needed.
        """
        os.makedirs(os.path.dirname(path), exist_ok=True)
        ext = os.path.splitext(path)[1].lower()
        if ext == ".csv":
            df.to_csv(path)
        elif ext in (".pkl", ".pickle"):
            df.to_pickle(path)
        else:
            raise ValueError(f"Unsupported file extension: {ext}")

    def run(
        self,
        data: pd.DataFrame,
        history: pd.DataFrame,
        n_windows: int,
        historic_n_windows: int,
        step_size: int,
        h: int,
    ) -> Tuple[pd.DataFrame, pd.DataFrame]:
        """
        Loads or generates forecast and historic forecast results.

        Args:
            data (pd.DataFrame): DataFrame for current data forecasting.
            history (pd.DataFrame): DataFrame for historic data forecasting.
            n_windows (int): Number of cross-validation windows for forecast.
            historic_n_windows (int): Number of cross-validation windows for historic forecast.
            step_size (int): Step size between windows.
            h (int): Forecast horizon.

        Returns:
            Tuple of (forecast, historic_forecast) DataFrames.
        """
        # Forecast
        if self._file_exists_and_no_overwrite(self.forecast_path):
            forecast = self._load(self.forecast_path)
        else:
            forecaster = DemandForecaster(
                freq=self.freq, model_params=self.model_params
            )
            forecast = forecaster.cross_validation(
                df=data, n_windows=n_windows, step_size=step_size, h=h
            )
            self._save(forecast, self.forecast_path)

        # Historic Forecast
        if self._file_exists_and_no_overwrite(self.historic_path):
            historic_forecast = self._load(self.historic_path)
        else:
            forecaster = DemandForecaster(
                freq=self.freq, model_params=self.model_params
            )
            historic_forecast = forecaster.cross_validation(
                df=history, n_windows=historic_n_windows, step_size=step_size, h=h
            )
            self._save(historic_forecast, self.historic_path)

        return forecast, historic_forecast


class PlotMode(Enum):
    HISTORY = "history"
    FORECAST = "forecast"

    @classmethod
    def from_str(cls, mode: str):
        """Convert a string to a PlotMode enum."""
        if mode.lower() == "history":
            return cls.HISTORY
        elif mode.lower() == "forecast":
            return cls.FORECAST
        else:
            raise ValueError(f"Invalid plot mode: {mode}. Use 'history' or 'forecast'.")


class ForecastPlotter:
    """Handles plotting of history, actuals, forecast with provided performance metrics, via Altair."""

    def __init__(
        self,
        history: pd.DataFrame,
        actuals: pd.DataFrame,
        forecast: pd.DataFrame = None,
        historic_forecast: pd.DataFrame = None,
        metrics: dict = None,
        date_col: str = "date",
        actual_col: str = "demand",
        xlabel: str = "Date",
        ylabel: str = "Demand",
        history_label: str = "Historical Demand",
        actuals_label: str = "Actuals",
        horizon_label: str = "Forecast Horizon",
    ):
        self.history = history.copy()
        self.actuals = actuals.copy()
        self.forecast = forecast.copy() if forecast is not None else pd.DataFrame()
        self.historic_forecast = (
            historic_forecast.copy()
            if historic_forecast is not None
            else pd.DataFrame()
        )
        self.metrics = metrics
        self.date_col = date_col
        self.actual_col = actual_col
        self.xlabel = xlabel
        self.ylabel = ylabel
        self.history_label = history_label
        self.actuals_label = actuals_label
        self.horizon_label = horizon_label

    def add_forecast(self, forecast: pd.DataFrame):
        """Add forecast DataFrame (must contain date_col and model forecast column)."""
        self.forecast = forecast.copy()
        return self

    def add_historic_forecast(self, historic_forecast: pd.DataFrame):
        """Add historic forecast DataFrame (must contain date_col and model forecast column)."""
        self.historic_forecast = historic_forecast.copy()
        return self

    def add_metrics(self, metrics: pd.DataFrame):
        """Add performance metrics DataFrame (indexed by metric_col)."""
        self.metrics = metrics.copy()
        return self

    def plot(
        self,
        model_col: str = None,
        title: str = "Demand Forecast",
        forecast_label: str = None,
        vertical_line: bool = True,
        shade: bool = True,
        plot_mode: Union[str, PlotMode] = PlotMode.FORECAST,
    ) -> alt.Chart:
        """
        Return an Altair chart with history, actuals, optional forecast, and metrics annotation.
        """

        plot_mode = (
            PlotMode.from_str(plot_mode) if isinstance(plot_mode, str) else plot_mode
        )

        metrics_descr = ""

        # Add metrics text annotation
        if self.metrics and model_col:

            ms = self.metrics[plot_mode.value][model_col]
            mae = int(round(ms["mae"], 0))
            mape = round((ms["mape"] * 100), 1)

            metrics_descr += f" (MAE: {mae}, MAPE: {mape:.1f}%)"

        # Combine history + actuals for base line
        base = pd.concat([self.history, self.actuals], ignore_index=True)

        # Base line chart
        line_all = (
            alt.Chart(base)
            .mark_line(point=True)
            .encode(
                x=alt.X(
                    f"{self.date_col}:T",
                    title=self.xlabel,
                    axis=alt.Axis(format="%b %Y"),
                ),
                y=alt.Y(f"{self.actual_col}:Q", title=self.ylabel),
                tooltip=[
                    alt.Tooltip(
                        f"{self.date_col}:T", title=self.xlabel, format="%b %Y"
                    ),
                    alt.Tooltip(
                        f"{self.actual_col}:Q", title=self.ylabel, format=".1f"
                    ),
                ],
            )
            .properties(title=title + metrics_descr)
        )

        layers = [line_all]

        # Forecast layer

        if plot_mode == PlotMode.FORECAST and not self.forecast.empty:

            fc_label = forecast_label or f"{model_col} Forecast"
            line_fc = (
                alt.Chart(self.forecast)
                .mark_line(color="orange")
                .encode(
                    x=alt.X(f"{self.date_col}:T"),
                    y=alt.Y(f"{model_col}:Q"),
                    tooltip=[
                        alt.Tooltip(
                            f"{self.date_col}:T", title=self.xlabel, format="%b %d, %Y"
                        ),
                        alt.Tooltip(f"{model_col}:Q", title=fc_label, format=".2f"),
                    ],
                )
                .properties(name=fc_label)
            )
            layers.append(line_fc)

        elif plot_mode == PlotMode.HISTORY and not self.historic_forecast.empty:

            fc_label = forecast_label or f"{model_col} Forecast"
            line_fc = (
                alt.Chart(self.historic_forecast)
                .mark_line(color="orange")
                .encode(
                    x=alt.X(f"{self.date_col}:T"),
                    y=alt.Y(f"{model_col}:Q"),
                    tooltip=[
                        alt.Tooltip(
                            f"{self.date_col}:T", title=self.xlabel, format="%b %d, %Y"
                        ),
                        alt.Tooltip(f"{model_col}:Q", title=fc_label, format=".2f"),
                    ],
                )
                .properties(name=fc_label)
            )
            layers.append(line_fc)

        # Vertical line for cutoff date

        if vertical_line:

            cutoff_date = (
                self.actuals[self.date_col].min()
                if plot_mode == PlotMode.FORECAST
                else self.historic_forecast[self.date_col].min()
            )
            vline = (
                alt.Chart(pd.DataFrame({"cutoff": [cutoff_date]}))
                .mark_rule(
                    color="blue",
                    strokeDash=[2, 2],  # Creates a dotted line pattern
                    strokeWidth=2,  # Optional: sets the line thickness
                )
                .encode(
                    x=alt.X(
                        "cutoff:T",
                    ),
                    tooltip=alt.Tooltip("cutoff:T", format="%b %d, %Y"),
                )
            )
            layers.append(vline)

            # Add other vertical lines between the cutoff date and the end of the forecast (one line for each 4 weeks)
            end_date = (
                self.actuals[self.date_col].max()
                if plot_mode == PlotMode.FORECAST
                else self.historic_forecast[self.date_col].max()
            )

            n_four_weeks = (end_date - cutoff_date).days // (
                7 * 4
            )  # Number of 4-week intervals

            for i in range(1, n_four_weeks + 1):
                line = (
                    alt.Chart(
                        pd.DataFrame(
                            {"cutoff": [cutoff_date + pd.DateOffset(weeks=i * 4)]}
                        )
                    )
                    .mark_rule(
                        color="blue",
                        strokeDash=[2, 2],  # Creates a dotted line pattern
                        strokeWidth=2,  # Optional: sets the line thickness
                        opacity=0.3,
                    )
                    .encode(
                        x=alt.X("cutoff:T"),
                        tooltip=alt.Tooltip("cutoff:T", format="%b %d, %Y"),
                    )
                )
                layers.append(line)

        # Shaded region for forecast horizon
        if shade:

            # Define the forecast horizon
            start_shade = (
                self.actuals[self.date_col].min()
                if plot_mode == PlotMode.FORECAST
                else self.historic_forecast[self.date_col].min()
            )
            end_shade = (
                self.actuals[self.date_col].max()
                if plot_mode == PlotMode.FORECAST
                else self.historic_forecast[self.date_col].max()
            )

            # Create a DataFrame for the shaded region
            shaded_region = pd.DataFrame({"start": [start_shade], "end": [end_shade]})

            # Create the shaded rectangle
            span = (
                alt.Chart(shaded_region)
                .mark_rect(opacity=0.1, color="grey")
                .encode(x="start:T", x2="end:T")
            )

            # Insert the shaded region at the bottom layer
            layers.insert(0, span)

        # Combine layers
        chart = alt.layer(*layers).resolve_scale(color="independent")

        return (
            chart.configure_title(fontSize=16, fontWeight="bold")
            .configure_axis(labelFontSize=12, titleFontSize=14)
            .properties(width=1000)
        )
