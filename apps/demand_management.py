import marimo

__generated_with = "0.13.4"
app = marimo.App(
    width="medium",
    app_title="Demand Management",
    css_file="d3.css",
)


@app.cell
def _():
    from utils.slides import SlideCreator
    from utils.data import DataLoader, DataSplitter
    from utils.forecast import ForecastManager, Evaluator, ForecastPlotter
    from utils.decomposition import LinearTrendSeasonalDecomposer, DecompositionPlotter
    from sklearn.utils import Bunch
    import marimo as mo
    import pandas as pd
    import numpy as np
    from io import StringIO

    return (
        Bunch,
        DataLoader,
        DataSplitter,
        DecompositionPlotter,
        Evaluator,
        ForecastManager,
        ForecastPlotter,
        LinearTrendSeasonalDecomposer,
        SlideCreator,
        mo,
        np,
    )


@app.cell
def _():
    lehrstuhl = "Chair of Logistics and Quantitative Methods"
    vorlesung = "Demand Planning"
    presenter = "Richard Pibernik, Moritz Beck"
    return lehrstuhl, presenter, vorlesung


@app.cell
def _(SlideCreator, lehrstuhl, presenter, vorlesung):
    sc = SlideCreator(lehrstuhl, vorlesung, presenter)
    return (sc,)


@app.cell
def _(sc):
    titleSlide = sc.create_slide(
        "Basic Data Analysis and Time Series Forecasting",
        layout_type="title-slide",
        newSection="Basic Data Analysis and Time Series Forecasting",
    )
    return (titleSlide,)


@app.cell
def _(mo, sc):
    introduction1 = sc.create_slide(
        "How are these tasks linked?", layout_type="1-column"
    )
    introduction1.content1 = mo.image(
        "public/Demand_Management/images/how_are_these_tasks_linked.png",
        width=1000,
        style={"margin-right": "auto", "margin-left": "auto"},
    )
    return (introduction1,)


@app.cell
def _(mo, sc):
    introduction2 = sc.create_slide(
        "Let’s start with a very basic DP (Forecasting) task...", layout_type="2-row"
    )
    introduction2.content1 = mo.image(
        "public/Demand_Management/images/distribution_center_fuerth.png",
        width=1000,
        style={"margin-right": "auto", "margin-left": "auto"},
    )
    introduction2.content2 = mo.md(
        """One of the many Demand Planning Tasks of Phoenix is to predict the demand of Amoxicillin of a 
    specific manufacturer and a specific dosage form for a single distribution center (here: Fürth) for the 
    4 weeks. This forecast will be used to determine the target inventory quantities and order quantities from a 
    central warehouse. """
    )
    return (introduction2,)


@app.cell
def _(DataLoader, DataSplitter):
    loader = DataLoader(file_path="public/data/demand_data_fuerth.csv")
    data = loader.load()
    splitter = DataSplitter(cutoff_date="2024-08-01")
    history, actuals = splitter.split(data)
    return actuals, data, history


@app.cell
def _(history, mo, sc):
    history_slide = sc.create_slide("Historical Dataframe", layout_type="3-row")
    history_slide.content1 = mo.md(
        """Assume that we have some 5 years of historical data for this product at the specific distribution center. \
        Let's read the data into python with the pandas library and have a look at it. The data contains the date and the demand for each week. """
    )
    history_slide.content2 = mo.md("""
    ```python
    import pandas as pd
    history = pd.read_csv(path_to_history_csv)
    ```
    """)
                                
    history_slide.content3 = mo.ui.table(history)
    return (history_slide,)


@app.cell
def _(ForecastPlotter, actuals, history):
    fc_plotter = ForecastPlotter(history=history, actuals=actuals)
    return (fc_plotter,)


@app.cell
def _(fc_plotter, mo, sc):
    basic_forecasting1 = sc.create_slide("Historical Data", layout_type="2-row")
    plot = fc_plotter.plot(
        title="Weekly Demand of Amoxicilin (Fürth Region)",
        vertical_line=False,
        shade=False,
    )
    basic_forecasting1.content1 = mo.md(
        "Lets start with a simple plot of the historical data. We can see that the demand is not constant, but has a clear trend and seasonality."
    )
    basic_forecasting1.content2 = mo.ui.altair_chart(plot)
    return (basic_forecasting1,)


@app.cell
def _(mo, sc):
    basic_forecasting2 = sc.create_slide(
        "Basic Forecasting", layout_type="side-by-side"
    )
    basic_forecasting2.content1 = mo.md(
        """### Now we want to decide how to forecast the demand for the next 4 weeks. The easiest way is to use the last week of data as a forecast. But is this a good idea?
                                        ### To answer this question, we need to find a way to evaluate different forecasting methods."""
    )
    basic_forecasting2.content2 = mo.image(
        "public/Demand_Management/images/evaluation.png",
        style={"margin-right": "auto", "margin-left": "auto"},
    )
    return (basic_forecasting2,)


@app.cell
def _(Bunch):

    MA_Q_MIN = 4
    MA_Q_MAX = 16
    MA_Q_STEP = 2

    MA_CONFIG = Bunch(
        q_min=MA_Q_MIN,
        q_max=MA_Q_MAX,
        q_step=MA_Q_STEP,
        q_default=MA_Q_MIN,
    )

    SES_CONFIG = Bunch(
        alpha_min=0.1,
        alpha_max=1.0,
        alpha_step=0.1,
        alpha_default=0.2,
    )

    return MA_CONFIG, SES_CONFIG


@app.cell
def _(
    ForecastManager,
    MA_CONFIG,
    SES_CONFIG,
    data,
    fc_plotter,
    history,
    mo,
    np,
):




    ma_qs = [
        q for q in range(MA_CONFIG.q_min, MA_CONFIG.q_max + 1, MA_CONFIG.q_step)
        ]
    ma_names = [f"MA_{q}" for q in ma_qs]

    ses_alphas = np.arange(
        SES_CONFIG.alpha_min,
        SES_CONFIG.alpha_max + 0.1,
        SES_CONFIG.alpha_step,
    )

    ses_names = [f"SES_{int(10*(alpha))}" for alpha in ses_alphas]

    params = {
        "naive": [{"alias": "Naive"}],
        "ma": [
            {"q": q, "alias": ma_alias}
            for q, ma_alias in zip(ma_qs, ma_names)
        ],
        "ses": [
            {"alpha": alpha, "alias": ses_alias}
            for ses_alias, alpha in zip(ses_names, ses_alphas)
        ]
        + [{"alias": "SES"}],
        "holt": [{"alias": "Holt"}],
        "holt_winters": [{"alias": "Holt‑Winters"}],
    }

    fc_manager = ForecastManager(
        freq="W",
        model_params=params,
        forecast_path="public/data/forecast_fuerth.csv",
        historic_path="public/data/historic_forecast_fuerth.csv",
        overwrite=False,
    )
    forecast, historic_forecast = fc_manager.run(
        data=data,
        history=history,
        n_windows=13,
        historic_n_windows=40,
        step_size=4,
        h=4,
    )

    mo.ui.dataframe(
        forecast,
        )
    mo.ui.dataframe(
        historic_forecast,
        )

    fc_plotter.add_forecast(forecast)
    fc_plotter.add_historic_forecast(historic_forecast)
    return forecast, historic_forecast


@app.cell
def _(fc_plotter, mo, sc):
    basic_forecasting3 = sc.create_slide("Forecasting Evaluation", layout_type="2-row")
    plot_shaded = fc_plotter.plot(
        title="Weekly Demand of Amoxicilin (Fürth Region)",
        vertical_line=True,
        shade=True,
    )
    basic_forecasting3.content1 = mo.md(
        "For evaluating our model, we take the last year consisting of 13 windows of 4 weeks. That means at the beginning of each window, we have to forecast the next 4 weeks."
    )
    basic_forecasting3.content2 = mo.ui.altair_chart(plot_shaded)
    return (basic_forecasting3,)


@app.cell
def _(mo, sc):
    # Create a slide that intuitively formalizes the forecasting evaluation process
    basic_forecasting4 = sc.create_slide(
        "Formal Introduction to Forecasting", layout_type="1-row"
    )

    # Use clear bullet points and mathematical notation for readability
    basic_forecasting4.content1 = mo.md(
        """
        ### In order to evaluate our forecasting method, we need to define the forecasting problem more formally.
        - **Forecasting Problem:** Given past demands \(d_{1}, d_{2}, \dots,  d_{t-1}, d_t\), produce forecasts for the next 4 weeks: \(f_{t+1}, f_{t+2}, f_{t+3}, f_{t+4}\).
        - **Naive Forecasting Method:** The simple naive forecasting method uses the last observed demand as the forecast for the next periods: \(f_{t+1} = d_t\, f_{t+2} = d_t, \dots, f_{t+4} = d_t\).
    """
    )


    return (basic_forecasting4,)



@app.cell
def _(mo, sc):
    # Create a slide that intuitively formalizes the forecasting evaluation process
    basic_forecasting_code = sc.create_slide(
        "Implementation of Naive Forecasting", layout_type="2-row"
    )

    # Use clear bullet points and mathematical notation for readability
    basic_forecasting_code.content1 = mo.md(
        """
        Lets implement the naive forecasting method in Python using the NumPy library. The naive forecast method takes a NumPy array (a list of numbers)
        of past observations and a horizon (number of future steps to forecast) as input, and returns a NumPy array of the same length as the horizon with the last observed value repeated.
        """
    )

    basic_forecasting_code.content2 = mo.md("""
        ```python
        import numpy as np

        def naive_forecast(history: np.ndarray, horizon: int = 4) -> np.ndarray:
            \"\"\"
            Generate a naive forecast by repeating the last observed value.
            
            :param history: 1D NumPy array of past observations.
            :param horizon: Number of future steps to forecast.
            :return: 1D NumPy array of length `horizon` with repeated last value.
            \"\"\"
            last_value = history[-1]
            return np.full(shape=horizon, fill_value=last_value)
        ``` 
        """)
    return (basic_forecasting_code,)





@app.cell
def _(fc_plotter, mo, sc):
    basic_forecasting_plot = sc.create_slide("Naive Forecasting", layout_type="2-row")
    plot_naive = fc_plotter.plot(
        model_col="Naive",
        title="Forecast of the Weekly Demand using the Naive Method",
        vertical_line=True,
        shade=True,
    )
    basic_forecasting_plot.content1 = mo.md(
        "As we can see, the naive forecasting method results in 13 constant forecasts of the last observed demand. To evaluate the forecasting method, we need to compare the forecast (orange) with the actual demand (blue)."
    )
    basic_forecasting_plot.content2 = mo.ui.altair_chart(plot_naive)
    return (basic_forecasting_plot,)


@app.cell
def _(mo, sc):
    # Create a slide that intuitively formalizes the forecasting evaluation process
    evaluation_metrics = sc.create_slide(
        "Formal Introduction to Evaluation", layout_type="1-column"
    )

    evaluation_metrics.content1 = mo.md(
        r"""

        ### In order to to compare the naive forecasting method with the actual demand, we need to calculate the forecasting error, which is the difference between the forecast and the actual demand.

        - **Mean Absolute Error (MAE):**  
        The MAE is the average of the absolute errors over all forecasting windows: 

        \[
            \mathrm{MAE}
            = \frac{1}{n} \sum_{i=1}^{n} \bigl|d_{t+i} - f_{t+i}\bigr|
        \]

        - **Mean Absolute Percentage Error (MAPE):**  
        The MAPE is the average of the absolute percentage errors over all forecasting windows: 

        \[
            \mathrm{MAPE}
            = \frac{1}{n} \sum_{i=1}^{n}
            \frac{\bigl|d_{t+i} - f_{t+i}\bigr|}{d_{t+i}}
            \times 100\%
        \]
        """
    )

    return (evaluation_metrics,)


@app.cell
def _(mo, sc):
    # Create a slide with Python-based implementations of MAE and MAPE
    eval_metrics_code = sc.create_slide(
        "Python Implementation of Evaluation Metrics", layout_type="2-row"
    )

    eval_metrics_code.content1 = mo.md(
        """
        - Here we implement MAE and MAPE using the NumPy library. These functions take two NumPy arrays as input: the actual demand and the forecasted values, and return the MAE and MAPE as floats (decimal numbers).
        - The MAPE is only calculated for non-zero actual values to avoid division by zero errors.
        """
    )

    eval_metrics_code.content2 = mo.md("""
        ```python
        import numpy as np

        def mean_absolute_error(actuals: np.ndarray, forecasts: np.ndarray) -> float:
            \"\"\"
            Compute MAE between actuals and forecasts using NumPy.
            
            :param actuals: array of true values, shape (n,)
            :param forecasts: array of forecasted values, shape (n,)
            :return: MAE as a float
            \"\"\"
            errors = np.abs(actuals - forecasts)
            return errors.mean()

        def mean_absolute_percentage_error(actuals: np.ndarray, forecasts: np.ndarray) -> float:
            \"\"\"
            Compute MAPE between actuals and forecasts using NumPy.
            
            :param actuals: array of true values, shape (n,)
            :param forecasts: array of forecasted values, shape (n,)
            :return: MAPE as a percentage float
            \"\"\"
            # Avoid division by zero by masking zero actuals
            nonzero = actuals != 0
            pct_errors = np.abs((actuals[nonzero] - forecasts[nonzero]) / actuals[nonzero])
            return pct_errors.mean() * 100
        ```
        """)

    return (eval_metrics_code,)


@app.cell
def _(Evaluator, fc_plotter, forecast, historic_forecast):
    evaluator = Evaluator(forecast=forecast, historic_forecast=historic_forecast)
    evaluations = evaluator.evaluate()
    fc_plotter.add_metrics(evaluations)
    return


@app.cell
def _(fc_plotter, mo, sc):
    evaluation_naive = sc.create_slide("Naive Forecasting", layout_type="2-row")
    plot_naive_with_metric = fc_plotter.plot(
        model_col="Naive",
        title="Forecast of the Weekly Demand using the Naive Method",
        vertical_line=True,
        shade=True,
    )
    evaluation_naive.content2 = mo.ui.altair_chart(plot_naive_with_metric)
    return (evaluation_naive,)


@app.cell
def _(mo, sc):
    # Slide 1: Introduction to Moving Average Forecasting
    ma_intro = sc.create_slide("Moving Average Forecasting", layout_type="1-column")
    ma_intro.content1 = mo.md(
        r"""
    ### Limitations of Naive Forecasting and Introduction to Moving Average

    - **Drawback of Naive Method:** Using only the last observed demand ignores trends and seasonality, and can be overly sensitive to random fluctuations in weekly demand.
    - **Moving Average Idea:** Instead of relying on a single most recent observation, we average the last \(q\) observations to smooth out noise.

    \[
    f_{t+1} = \frac{1}{q} \bigl(d_{t-q} + \dots + d_{t}\bigr)
    \]

    \[
    f_{t+2} = \frac{1}{q} \bigl(d_{t-q+1} + \dots + d_{t} + f_{t+1}\bigr)
    \]

    \[
    f_{t+4} = \frac{1}{q} \bigl(d_{t-q+3} + \dots + d_{t} + f_{t+1} + \dots + f_{t+3}\bigr)
    \]

    - Where:
    - \(q\) is the window size (number of past periods to average).
    - \(d_{t-i}\) are historical demands.
    - This method reduces the impact of random spikes or dips by incorporating multiple past points into each forecast.
    """
    )
    return (ma_intro,)

@app.cell
def _(mo, sc):
    # Slide 2: Python Implementation of Moving Average Forecasting
    ma_code_slide = sc.create_slide(
        "Python Implementation of Moving Average Forecast", layout_type="2-row"
    )

    ma_code_slide.content1 = mo.md("""
        - Below we implement a simple moving average forecaster in Python using NumPy.
        - **Function**: `moving_average_forecast`
        - **Inputs**:
          - `actuals`: NumPy array of historical demand of length \(T\).
          - `window`: integer \(q\), the number of past periods to average.
          - `horizon`: integer \(h\), number of future points to forecast.
        - **Output**: NumPy array of length \(h\), containing the \(h\)-step–ahead forecasts.
        - The function computes each forecast recursively, appending each new forecast to the history before computing the next.
        """
    )

    ma_code_slide.content2 = mo.md("""
        ```python
        import numpy as np

        def moving_average_forecast(actuals: np.ndarray, window: int, horizon: int) -> np.ndarray:
            \"\"\"
            Compute an h-step–ahead moving average forecast.

            :param actuals: array of historical values, shape (T,)
            :param window: number of past periods to average (q)
            :param horizon: number of future points to forecast (h)
            :return: array of forecasts, shape (h,)
            \"\"\"
            history = actuals.tolist()
            forecasts = []

            for _ in range(horizon):
                if len(history) < window:
                    # if not enough data, average all available points
                    avg = np.mean(history)
                else:
                    # average the last `window` points
                    avg = np.mean(history[-window:])
                forecasts.append(avg)
                # append the new forecast to history for recursive forecasting
                history.append(avg)

            return np.array(forecasts)
        ```
        """
    )

    return (ma_code_slide,)


@app.cell
def _(fc_plotter, mo, sc):
    evaluation_ma4 = sc.create_slide("Moving Average Forecasting", layout_type="2-row")
    evaluation_ma4.content1 = mo.md(
        "The moving average method with uses the last 4 weeks of data to forecast the next 4 weeks (q=4). But what is the best value of q?"
    )
    plot_ma4 = fc_plotter.plot(
        model_col="MA_4",
        title="Forecast of the Weekly Demand using the Moving Average Method [MA(4)]",
        vertical_line=True,
        shade=True,
    )
    evaluation_ma4.content2 = mo.ui.altair_chart(plot_ma4)
    return (evaluation_ma4,)


@app.cell
def _(MA_CONFIG, mo):
    q_slider = mo.ui.slider(
        MA_CONFIG.q_min,
        MA_CONFIG.q_max,
        value=MA_CONFIG.q_default,
        label="Window Size (q)",
        step=MA_CONFIG.q_step,
    )
    return (q_slider,)


@app.cell
def _(fc_plotter, mo, q_slider, sc):
    evaluation_ma_q = sc.create_slide("Moving Average Forecasting", layout_type="3-row")
    evaluation_ma_q.content1 = mo.md(""" The parameter q sets how many past points to average. A larger q makes the series smoother but slower to react; a smaller q is more responsive but noisier. 
    To pick the best q, compare forecasting errors (MAE or MAPE) across different q values on the historical data and choose the one with the lowest error.
    """
    )

    evaluation_ma_q.content2 = q_slider
    q = q_slider.value
    plot_ma_q = fc_plotter.plot(
        model_col=f"MA_{q}",
        title=f"Forecast of the Weekly Demand using the Moving Average Method [MA({q})]",
        vertical_line=True,
        shade=True,
        plot_mode="history",
    )
    evaluation_ma_q.content3 = mo.ui.altair_chart(plot_ma_q)
    return (evaluation_ma_q,)


@app.cell
def _(fc_plotter, mo, sc):
    evaluation_ma16 = sc.create_slide("Moving Average Forecasting", layout_type="2-row")
    evaluation_ma16.content1 = mo.md(
        "The best value of q turned out to be 16. This means that we use the last 16 weeks of data to forecast the next 4 weeks. Let's see how the result looks like on the last 13 weeks of data."
    )
    plot_ma16 = fc_plotter.plot(
        model_col="MA_16",
        title="Forecast of the Weekly Demand using the Moving Average Method [MA(4)]",
        vertical_line=True,
        shade=True,
    )
    evaluation_ma16.content2 = mo.ui.altair_chart(plot_ma16)
    return (evaluation_ma16,)


@app.cell
def _(mo, sc):
    ma_drawbacks = sc.create_slide("Moving Average Forecasting", layout_type="1-column")
    ma_drawbacks.content1 = mo.md(
        r"""
    ###  Limitations of Moving Average Forecasting And Time Series Decomposition
    - Increasing the window size \(q\) does make the forecast smoother and lowers the MAE, but it also means the forecast reacts more slowly to actual changes—and it still falls short of a simple naive approach.
    - **Drawbacks of Moving Averages:** Our Amoxicillin demand isn’t constant—it shows clear trends and seasonal swings. A plain moving average can’t capture these effects.
    - **Why Decompose the Series:** By breaking the data into **trend**, **seasonality**, and **noise**, we can model each pattern separately and produce more accurate forecasts.
    - **Trend:** The overall long-term direction (rising, falling, or flat).
    - **Seasonality:** Regular cycles or patterns (e.g., weekly, monthly, yearly).
    - **Noise:** Random fluctuations that aren’t explained by trend or seasonality.
    """
    )
    return (ma_drawbacks,)


@app.cell
def _(LinearTrendSeasonalDecomposer, history):
    decomposer = LinearTrendSeasonalDecomposer()
    components = decomposer.fit_transform(history)
    return (components,)


@app.cell
def _(DecompositionPlotter, components, history):
    dec_plotter = DecompositionPlotter(history, components)
    return (dec_plotter,)


@app.cell
def _(dec_plotter, mo, sc):
    decomposition1 = sc.create_slide("Decomposition of the Series", layout_type="3-row")
    plot_decomp = dec_plotter.plot(
        title="Decomposition of the Weekly Demand of Amoxicilin (Fürth Region)"
    )
    decomposition1.content1 = mo.md("""
        - The decomposition of the series shows that the demand has a clear positive trend and monthly seasonality with spikes at the end of the year and a dip in the summer months. " \
        - The residuals are small and show no clear pattern.
        """
    )
    decomposition1.content2 = mo.ui.altair_chart(plot_decomp[0])
    decomposition1.content3 = mo.ui.altair_chart(plot_decomp[1])
    return (decomposition1,)


@app.cell
def _(mo, sc):
    # Slide: Introduction to Exponential Smoothing
    exp_intro = sc.create_slide(
        "Introduction to Exponential Smoothing", layout_type="1-column"
    )
    exp_intro.content1 = mo.md(
        r"""
    ### Why Exponential Smoothing?
    - **Moving averages** smooth noise but lag behind trends and can’t adapt to changing level or seasonality.
    - **Exponential smoothing** assigns exponentially decreasing weights to older observations, allowing the forecast to adapt more quickly.
    - Different extensions of the basic idea handle **level**, **trend**, and **seasonality** in increasing sophistication.
    """
    )
    return (exp_intro,)


@app.cell
def _(mo, sc):
    # Slide: Simple Exponential Smoothing (SES)
    ses_slide = sc.create_slide("Simple Exponential Smoothing", layout_type="1-column")
    ses_slide.content1 = mo.md(
        r"""
    **Model:**  

    \[
      \hat d_{t+1}
      = \alpha\,d_t + (1-\alpha)\, f_t
    \]

    - where  
    - \(\alpha\in(0,1)\) is the smoothing parameter.  
    - Larger \(\alpha\) → more reactive to recent changes;  
    - Smaller \(\alpha\) → smoother, slower updates.
    - \( f_t\) is the forecast for period \(t\).
    - \(d_t\) is the actual demand for period \(t\)."""
    )
    return (ses_slide,)


@app.cell
def _(mo, sc):
    # Slide: Python Implementation of Simple Exponential Smoothing (SES)
    ses_code_slide = sc.create_slide(
        "Python Implementation of Simple Exponential Smoothing", layout_type="2-row"
    )

    ses_code_slide.content1 = mo.md(
        """
        - The following function implements Simple Exponential Smoothing (SES):
        - **Inputs**:
          - `actuals`: NumPy array of observed historical demand.
          - `alpha`: smoothing parameter (0 < alpha < 1).
          - `initial_forecast`: optional float, the initial forecast value \(f_1\).
        - **Output**: NumPy array of SES forecasts of same length as input.
        - The forecast for time \(t+1\) depends on the actual value at time \(t\) and the forecast for time \(t\).
        """
    )

    ses_code_slide.content2 = mo.md(
        """
        ```python
        import numpy as np

        def simple_exponential_smoothing(actuals: np.ndarray, alpha: float, initial_forecast: float = None) -> np.ndarray:
            \"\"\"
            Compute SES forecasts for a sequence of observations.

            :param actuals: array of observed values, shape (T,)
            :param alpha: smoothing coefficient between 0 and 1
            :param initial_forecast: optional initial forecast value (f_1)
            :return: array of SES forecasts, shape (T,)
            \"\"\"
            n = len(actuals)
            forecasts = np.zeros(n)

            # Set initial forecast
            forecasts[0] = actuals[0] if initial_forecast is None else initial_forecast

            for t in range(1, n):
                forecasts[t] = alpha * actuals[t - 1] + (1 - alpha) * forecasts[t - 1]

            return forecasts
        ```
        """
    )

    return (ses_code_slide,)


@app.cell
def _(mo):
    # Slider to explore α
    alpha_slider = mo.ui.slider(
        0.1, 1.0, value=0.2, step=0.1, label="Smoothing Parameter α"
    )
    return (alpha_slider,)


@app.cell
def _(alpha_slider, fc_plotter, mo, sc):
    # Slide: Simple Exponential Smoothing (SES)
    ses_slide_plot = sc.create_slide(
        "Simple Exponential Smoothing", layout_type="3-row"
    )
    ses_slide_plot.content1 = mo.md(
        "Let's see how the SES method works with different values of α. The best value of α is the one that minimizes the MAE on the historical data. (like q for MA)"
    )
    ses_slide_plot.content2 = alpha_slider
    # plot all windows for SES
    alpha = alpha_slider.value

    ses_name = f"SES_{int(10*(alpha))}"

    plot_ses = fc_plotter.plot(
        model_col=ses_name,
        title=f"SES Forecast (α={alpha})",
        vertical_line=True,
        shade=True,
        plot_mode="history",
    )
    ses_slide_plot.content3 = mo.ui.altair_chart(plot_ses)
    return (ses_slide_plot,)



@app.cell
def _(mo, sc):
    # Slide: SES Using StatsForecast Library
    ses_statsforecast_slide = sc.create_slide(
        "SES with StatsForecast Library", layout_type="2-row"
    )

    ses_statsforecast_slide.content1 = mo.md(
        """
        - Instead of implementing SES and tuning α manually, we can use the `StatsForecast` library. This library provides a simple interface for time series forecasting with:
        - Automatic parameter tuning
        - Scales to large datasets
        - Compatible with pandas DataFrames
        """
    )

    ses_statsforecast_slide.content2 = mo.md(
        """
        ```python
        from statsforecast import StatsForecast
        from statsforecast.models import SimpleExpSmoothing

        # Assume `historic` is a DataFrame with columns: unique_id, date, demand

        sf = StatsForecast(models=[SimpleExponentialSmoothingOptimized()], freq='W')
        forecasts_df = sf.forecast(df=historic, h=4, id_col="unique_id", time_col="date", target_col="demand")
        ```
        """
    )

    return (ses_statsforecast_slide,)


@app.cell
def _(fc_plotter, mo, sc):
    # Slide: Simple Exponential Smoothing (SES)
    ses_optimized_slide_plot = sc.create_slide(
        "Simple Exponential Smoothing", layout_type="2-row"
    )
    ses_optimized_slide_plot.content1 = mo.md(
        "The SES method with the best value of α turned out to be better than the Naive and the MA method. However it delivers the same forecast within each 4-week window."
    )
    plot_ses_opt = fc_plotter.plot(
        model_col="SES",
        title=f"SES Forecast",
        vertical_line=True,
        shade=True,
        plot_mode="forecast",
    )
    ses_optimized_slide_plot.content2 = mo.ui.altair_chart(plot_ses_opt)
    return (ses_optimized_slide_plot,)


@app.cell
def _(mo, sc):
    # Slide: Holt’s Linear Trend Method
    holt_intro = sc.create_slide("Holt’s Linear Trend Method", layout_type="1-column")
    holt_intro.content1 = mo.md(r"""
    - **Adds a trend component.**  
    - By including a trend component, Holt’s method can capture linear patterns in the data. For our Amoxicillin demand, which shows a clear upward trend,
    - Holt’s method increases the forecast over time—unlike SES, which keeps it constant over 4-week windows. 
    - Equations:

    \[
    \ell_t = \alpha\,f_t + (1-\alpha)\,(\ell_{t-1} + b_{t-1})
    \]

    \[
    b_t = \beta^*\,(\ell_t - \ell_{t-1}) + (1-\beta^*)\,b_{t-1}
    \]

    \[
     f_{t+h} = \ell_t + h\,b_t \quad (h=1,2,3,4)
    \]

    - **\(\ell_t\)**: estimated level at time t
    - **\(b_t\)**: estimated trend at time t
    - **\(f_{t+h}\)**: forecast for h weeks ahead (up to 4)
    - **\(\alpha, \beta^* \in [0,1]\)**: smoothing weights (level vs. trend)

    """)
    return (holt_intro,)


@app.cell
def _(mo, sc):
    # Slide: Holt’s Linear Trend Method with StatsForecast Library
    holt_statsforecast_slide = sc.create_slide(
        "Holt’s Linear Trend Method with StatsForecast Library",
        layout_type="2-row"
    )

    holt_statsforecast_slide.content1 = mo.md(
        """
        - Use the `statsforecast` library to apply Holt’s Linear Trend Method at scale:
        - Automatically optimizes both level (α) and trend (β) smoothing parameters.
        """
    )

    holt_statsforecast_slide.content2 = mo.md(
        """
        ```python
        from statsforecast import StatsForecast
        from statsforecast.models import Holt

        # Assume `historic` is a DataFrame with columns: unique_id, date, demand

        sf = StatsForecast(models=[Holt()], freq='W')
        forecasts_df = sf.forecast(
            df=historic,
            h=4,
            id_col="unique_id",
            time_col="date",
            target_col="demand"
        )
        ```
        """
    )

    return (holt_statsforecast_slide,)


@app.cell
def _(fc_plotter, mo, sc):
    # Slide: Holt Forecast Plot
    holt_slide = sc.create_slide("Holt Forecast", layout_type="2-row")
    holt_slide.content1 = mo.md("Forecast using Holt’s linear trend—captures both level and trend. α and β  are optimized automatically.")
    plot_holt = fc_plotter.plot(model_col="Holt", title="Holt’s Linear Trend Forecast", vertical_line=True, shade=True)
    holt_slide.content2 = mo.ui.altair_chart(plot_holt)
    return (holt_slide,)


@app.cell
def _(mo, sc):
    # Slide: Holt–Winters Seasonal Method
    hw_intro = sc.create_slide("Holt–Winters Seasonal Method", layout_type="1-column")
    hw_intro.content1 = mo.md(r"""
    - **Handles trend + seasonality.** Triple exponential smoothing:  
    - Equations:

    \[
    \ell_t = \alpha\,\frac{f_t}{s_{t-m}} + (1 - \alpha)(\ell_{t-1} + b_{t-1})
    \]

    \[
    b_t = \beta^*(\ell_t - \ell_{t-1}) + (1 - \beta^*)\,b_{t-1}
    \]

    \[
    s_t = \gamma\,\frac{f_t}{\ell_t} + (1 - \gamma)\,s_{t-m}
    \]

    \[
    f_{t+h} = (\ell_t + h\,b_t)\,s_{t-m+h_m}
    \]

    - **\(\ell_t\)**: level estimate
    - **\(b_t\)**: trend estimate
    - **\(s_t\)**: seasonal factor
    - **\(m\)**: season length (e.g. 52 for weekly seasonality)
    - **\(f_{t+h}\)**: forecast h periods ahead (e.g. next 4 weeks)
    - **\(\alpha, \beta^*, \gamma \in [0,1]\)**: smoothing weights for level, trend, seasonality
    """)
    return (hw_intro,)


@app.cell
def _(mo, sc):
    # Slide: Holt–Winters Seasonal Method with StatsForecast Library
    hw_statsforecast_slide = sc.create_slide(
        "Holt–Winters Seasonal Method with StatsForecast Library",
        layout_type="2-row"
    )

    hw_statsforecast_slide.content1 = mo.md(
        """
        - Use the `statsforecast` library’s ETS implementation to apply Holt–Winters (triple exponential smoothing) at scale.  
        - Specify both trend and seasonality components with your desired seasonal period (e.g., 52 weeks for yearly seasonality).  
        - The library will automatically fit the level (α), trend (β), and seasonal (γ) smoothing parameters.
        """
    )

    hw_statsforecast_slide.content2 = mo.md(
        """
        ```python
        from statsforecast import StatsForecast
        from statsforecast.models import HoltWinters

        # Assume `historic` is a DataFrame with columns: unique_id, date, demand
        # Weekly data with yearly seasonality (m = 52)

        sf = StatsForecast(
            models=[HoltWinters(season_length=52,)],
            freq='W'
        )

        forecasts_df = sf.forecast(
            df=historic,
            h=4,
            id_col="unique_id",
            time_col="date",
            target_col="demand"
        )
        ```
        """
    )

    return (hw_statsforecast_slide,)



@app.cell
def _(fc_plotter, mo, sc):
    # Slide: Holt–Winters Plot
    hw_slide = sc.create_slide("Holt–Winters Forecast", layout_type="2-row")
    hw_slide.content1 = mo.md("Forecast using Holt–Winters—to capture trend and seasonality simultaneously.")
    plot_hw = fc_plotter.plot(model_col="Holt‑Winters", title="Holt–Winters Seasonal Forecast", vertical_line=True, shade=True)
    hw_slide.content2 = mo.ui.altair_chart(plot_hw)
    return (hw_slide,)


@app.cell
def _(titleSlide):
    titleSlide.render_slide()
    return


@app.cell
def _(introduction1):
    introduction1.render_slide()
    return


@app.cell
def _(introduction2):
    introduction2.render_slide()
    return


@app.cell
def _(history_slide):
    history_slide.render_slide()
    return


@app.cell
def _(basic_forecasting1):
    basic_forecasting1.render_slide()
    return


@app.cell
def _(basic_forecasting2):
    basic_forecasting2.render_slide()
    return


@app.cell
def _(basic_forecasting3):
    basic_forecasting3.render_slide()
    return


@app.cell
def _(basic_forecasting4):
    basic_forecasting4.render_slide()
    return

@app.cell
def _(basic_forecasting_code):
    basic_forecasting_code.render_slide()
    return


@app.cell
def _(basic_forecasting_plot):
    basic_forecasting_plot.render_slide()
    return


@app.cell
def _(evaluation_metrics):
    evaluation_metrics.render_slide()
    return

@app.cell
def _(eval_metrics_code):
    eval_metrics_code.render_slide()
    return


@app.cell
def _(evaluation_naive):
    evaluation_naive.render_slide()
    return


@app.cell
def _(ma_intro):
    ma_intro.render_slide()
    return


@app.cell
def _(ma_code_slide):
    ma_code_slide.render_slide()
    return

@app.cell
def _(evaluation_ma4):
    evaluation_ma4.render_slide()
    return


@app.cell
def _(evaluation_ma_q):
    evaluation_ma_q.render_slide()
    return


@app.cell
def _(evaluation_ma16):
    evaluation_ma16.render_slide()
    return


@app.cell
def _(ma_drawbacks):
    ma_drawbacks.render_slide()
    return


@app.cell
def _(decomposition1):
    decomposition1.render_slide()
    return


@app.cell
def _(exp_intro):
    exp_intro.render_slide()
    return


@app.cell
def _(ses_slide):
    ses_slide.render_slide()
    return

@app.cell
def _(ses_code_slide):
    ses_code_slide.render_slide()
    return


@app.cell
def _(ses_slide_plot):
    ses_slide_plot.render_slide()
    return

@app.cell
def _(ses_statsforecast_slide):
    ses_statsforecast_slide.render_slide()
    return


@app.cell
def _(ses_optimized_slide_plot):
    ses_optimized_slide_plot.render_slide()
    return


@app.cell
def _(holt_intro):
    holt_intro.render_slide()
    return

@app.cell
def _(holt_statsforecast_slide):
    holt_statsforecast_slide.render_slide()
    return


@app.cell
def _(holt_slide):
    holt_slide.render_slide()
    return


@app.cell
def _(hw_intro):
    hw_intro.render_slide()
    return

@app.cell
def _(hw_statsforecast_slide):
    hw_statsforecast_slide.render_slide()
    return


@app.cell
def _(hw_slide):
    hw_slide.render_slide()
    return


if __name__ == "__main__":
    app.run()
