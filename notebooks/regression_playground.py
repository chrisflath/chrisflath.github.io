import marimo
import pandas as pd

app = marimo.App(app_title="AIS 2025 - Regression Playground")


@app.cell
def _():
    import marimo as mo
    import pandas as pd
    import numpy as np
    import plotly.graph_objects as go
    from sklearn.linear_model import SGDRegressor, LinearRegression
    from sklearn.preprocessing import PolynomialFeatures, StandardScaler
    from sklearn.pipeline import make_pipeline
    from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
    from sklearn.model_selection import train_test_split

    get_app_state, set_app_state = mo.state({
        "train_data": pd.DataFrame(columns=['x1', 'x2', 'y']),
        "test_data": pd.DataFrame(columns=['x1', 'x2', 'y']),
        "fit_results": None,
        "message": "Hi! Click 'Generate New Data' to start.",
        "dim": "2D"
    })

    return (
        LinearRegression,
        PolynomialFeatures,
        SGDRegressor,
        StandardScaler,
        get_app_state,
        go,
        make_pipeline,
        mean_absolute_error,
        mean_squared_error,
        mo,
        np,
        pd,
        r2_score,
        set_app_state,
        train_test_split,
    )


@app.cell
def _(go):
    def create_2d_plot_layout(title):
        return go.Layout(
            title={'text': title, 'x': 0.5, 'font': {'size': 20}},
            xaxis={'range': [-10.5, 10.5], 'title': 'Feature (eg. Temperature)'},
            yaxis={'range': [-55, 55], 'title': 'Target (eg. Quality Score)'},
            dragmode=False,
            legend={'orientation': 'h', 'yanchor': 'bottom', 'y': 1.02, 'xanchor': 'right', 'x': 1},
            margin={'t': 40, 'b': 40, 'l': 40, 'r': 40},
            hovermode='x unified',
            template="plotly_white"
        )
    def create_3d_plot_layout(title):
        return go.Layout(
            title={'text': title, 'x': 0.5, 'font': {'size': 20}},
            scene=dict(
                xaxis_title='Feature 1 (e.g., Temperature)',
                yaxis_title='Feature 2 (e.g., Pressure)',
                zaxis_title='Target (e.g., Quality Score)',
                xaxis={'range': [-10.5, 10.5]},
                yaxis={'range': [-10.5, 10.5]},
                zaxis={'range': [-55, 55]},
                aspectmode='cube'
            ),
            margin={'t': 10, 'b': 0, 'l': 0, 'r': 0},
            legend={'orientation': 'h', 'yanchor': 'bottom', 'y': 1.02, 'xanchor': 'right', 'x': 1},
            dragmode='turntable',
            template="plotly_white"
        )
    return create_2d_plot_layout, create_3d_plot_layout


@app.cell
def _(
    LinearRegression,
    PolynomialFeatures,
    SGDRegressor,
    StandardScaler,
    get_app_state,
    make_pipeline,
    mo,
    np,
    pd,
    set_app_state,
    train_test_split,
):
    plot_dim_radio = mo.ui.radio(
        options=['2D', '3D'], value='2D', label="**Plot Dimension:**"
    )
    show_test_data_radio = mo.ui.radio(
        options={'On', 'Off'}, value="On", label="**Show Test Data:**"
    )
    function_dropdown = mo.ui.dropdown(
        options={'sine': 'sine', 'linear': 'linear', 'quadratic': 'quadratic'},
        value='sine', label="**Data Generation Function:**"
    )
    noise_slider = mo.ui.slider(0, 10, step=1, value=5, label="**Noise Level:**")
    loss_function_dropdown = mo.ui.dropdown(
        options={'mse': 'mse'}, value='mse', label="**Loss Function:**"
    )
    degree_slider = mo.ui.slider(1, 25, step=1, value=1, label="**Polynomial Degree:**")
    regularization_type_radio = mo.ui.radio(
        options={'none': 'none', 'l1': 'l1', 'l2': 'l2'},
        value='none', label="**Regularization Type:**"
    )
    alpha_slider = mo.ui.dropdown(
        options={'0.0001': 0.0001, '0.01': 0.01, '1': 1.0, '10': 10.0, '100': 100.0},
        value='1',
        label="**Alpha:**"
    )

    def handle_generate(_):
        num_points = 100 if plot_dim_radio.value == '3D' else 40
        dim = plot_dim_radio.value
        func = function_dropdown.value
        noise = noise_slider.value

        if dim == '2D':
            x1_data_np = np.random.uniform(-10, 10, num_points)
            x1_data_np.sort()
            x2_data_np = np.zeros(num_points)
            if func == 'sine': y_true_np = 25 * np.sin(x1_data_np / 2)
            elif func == 'linear': y_true_np = 2 * x1_data_np + 5
            else: y_true_np = 0.5 * (x1_data_np**2) - 3 * x1_data_np - 10
        else:
            x1_data_np = np.random.uniform(-10, 10, num_points)
            x2_data_np = np.random.uniform(-10, 10, num_points)
            if func == 'sine': y_true_np = 15 * np.sin(x1_data_np/2) + 15 * np.cos(x2_data_np/2)
            elif func == 'linear': y_true_np = 2 * x1_data_np + 3 * x2_data_np + 5
            else: y_true_np = 0.5 * (x1_data_np**2) - 0.2 * (x2_data_np**2) - 2 * x1_data_np + x2_data_np

        y_data_np = y_true_np + np.random.normal(0, noise, num_points)
        new_data_df = pd.DataFrame({'x1': x1_data_np, 'x2': x2_data_np, 'y': y_data_np})

        train_df, test_df = train_test_split(new_data_df, test_size=0.25, random_state=42)

        set_app_state({
            "train_data": train_df.to_dict('list'),
            "test_data": test_df.to_dict('list'),
            "fit_results": None,
            "message": f"{len(new_data_df)} points generated. ({len(train_df)} train, {len(test_df)} test)",
            "dim": dim
        })

    def handle_fit(_):
        try:
            state = get_app_state()
            train_data = pd.DataFrame(state["train_data"])
            test_data = pd.DataFrame(state["test_data"])
            dim = state["dim"]

            if train_data.empty:
                set_app_state(lambda s: {**s, "message": "Generate data first."})
                return

            features = ['x1', 'x2'] if dim == '3D' else ['x1']
            X_train, y_train = train_data[features], train_data['y'].values
            X_test, y_test = test_data[features], test_data['y'].values

            reg_type = regularization_type_radio.value
            alpha_val = float(alpha_slider.value) if reg_type != 'none' else None

            if reg_type == 'none': regressor = LinearRegression()
            else: regressor = SGDRegressor(loss='squared_error', penalty=reg_type, alpha=alpha_val, max_iter=1000, tol=1e-4, random_state=42)

            model = make_pipeline(PolynomialFeatures(degree_slider.value), StandardScaler(), regressor)
            model.fit(X_train, y_train)

            fit_results = {
                'dim': dim, 
                'y_true_train': y_train.tolist(), 'y_pred_train': model.predict(X_train).tolist(),
                'y_true_test': y_test.tolist(), 'y_pred_test': model.predict(X_test).tolist(),
                'degree': degree_slider.value, 'reg': reg_type, 'alpha': alpha_val
            }
            combined_data = pd.concat([train_data, test_data])
            if dim == '2D':
                x_range_np = np.linspace(combined_data['x1'].min(), combined_data['x1'].max(), 200)
                fit_results['x1_line'] = x_range_np.tolist()
                fit_results['y_line'] = model.predict(x_range_np.reshape(-1, 1)).tolist()
            else: # 3D
                x1_range = np.linspace(combined_data['x1'].min(), combined_data['x1'].max(), 30)
                x2_range = np.linspace(combined_data['x2'].min(), combined_data['x2'].max(), 30)
                xx1, xx2 = np.meshgrid(x1_range, x2_range)
                X_surface = np.c_[xx1.ravel(), xx2.ravel()]
                y_surface = model.predict(X_surface).reshape(xx1.shape)
                fit_results.update({'x1_surface': xx1.tolist(), 'x2_surface': xx2.tolist(), 'y_surface': y_surface.tolist()})

            fit_message = f"Fitted Deg {degree_slider.value}"
            if reg_type != 'none': fit_message += f" | {reg_type.upper()} (α={alpha_val:.4f})"

            set_app_state(lambda s: {**s, "fit_results": fit_results, "message": fit_message})
        except Exception as e:
            set_app_state(lambda s: {**s, "message": f"Error during fit: {e}"})

    generate_button = mo.ui.button(label="Generate New Data", on_click=handle_generate, kind="neutral")
    fit_button = mo.ui.button(label="Fit Model", on_click=handle_fit, kind="success")

    return (alpha_slider, degree_slider, fit_button, function_dropdown, generate_button, loss_function_dropdown, noise_slider, plot_dim_radio, regularization_type_radio, show_test_data_radio)



@app.cell
def _(create_2d_plot_layout, create_3d_plot_layout, get_app_state, go, mo, show_test_data_radio):
    state = get_app_state()
    train_data = pd.DataFrame(state["train_data"])
    test_data = pd.DataFrame(state["test_data"])
    current_fit, dim = state["fit_results"], state["dim"]

    if dim == '2D':
        fig = go.Figure(layout=create_2d_plot_layout(''))
        if not train_data.empty:
            fig.add_trace(go.Scatter(x=train_data['x1'], y=train_data['y'], mode='markers', name='Train Data', marker=dict(color='royalblue', size=8)))
            if show_test_data_radio.value == 'On':
                fig.add_trace(go.Scatter(x=test_data['x1'], y=test_data['y'], mode='markers', name='Test Data', marker=dict(color='orange', size=8, symbol='square')))
        if current_fit and current_fit['dim'] == '2D':
            fit_name = f"Fit (Deg {current_fit['degree']})"
            if current_fit['reg'] != 'none': fit_name += f" Reg α={current_fit['alpha']}"
            fig.add_trace(go.Scatter(x=current_fit['x1_line'], y=current_fit['y_line'], mode='lines', name=fit_name, line=dict(color='firebrick', width=3)))
    else:
        fig = go.Figure(layout=create_3d_plot_layout(''))
        if not train_data.empty:
            fig.add_trace(go.Scatter3d(x=train_data['x1'], y=train_data['x2'], z=train_data['y'], mode='markers', name='Train Data', marker=dict(color='royalblue', size=5, symbol='circle')))
            if show_test_data_radio.value == "On":
                fig.add_trace(go.Scatter3d(x=test_data['x1'], y=test_data['x2'], z=test_data['y'], mode='markers', name='Test Data', marker=dict(color='orange', size=5)))
        if current_fit and current_fit['dim'] == '3D':
            fit_name = f"Fit (Deg {current_fit['degree']})"
            if current_fit['reg'] != 'none': fit_name += f" Reg α={current_fit['alpha']}"
            fig.add_trace(go.Surface(x=current_fit['x1_surface'], y=current_fit['x2_surface'], z=current_fit['y_surface'], opacity=0.8, name=fit_name, colorscale='Reds', showscale=False))

    main_plot = mo.ui.plotly(fig)
    return (main_plot,)


@app.cell
def _(get_app_state, mean_absolute_error, mean_squared_error, mo, r2_score):
    def format_metrics_as_md(fit_results):
        if not fit_results: return mo.md("Fit a model to see performance metrics.")
        
        y_true_train, y_pred_train = fit_results['y_true_train'], fit_results['y_pred_train']
        mse_train = mean_squared_error(y_true_train, y_pred_train)
        mae_train = mean_absolute_error(y_true_train, y_pred_train)
        r2_train = r2_score(y_true_train, y_pred_train)

        y_true_test, y_pred_test = fit_results['y_true_test'], fit_results['y_pred_test']
        mse_test = mean_squared_error(y_true_test, y_pred_test)
        mae_test = mean_absolute_error(y_true_test, y_pred_test)
        r2_test = r2_score(y_true_test, y_pred_test)

        return mo.callout(mo.md(f"""
            | Metric                  | Train      | Test      |
            |:------------------------|:-----------|:----------|
            | Mean Squared Error (MSE)| {mse_train:.3f}  | {mse_test:.3f}  |
            | Mean Absolute Error(MAE)| {mae_train:.3f}  | {mae_test:.3f}  |
            | R-squared (R²)          | {r2_train:.3f}   | {r2_test:.3f}   |
            """), kind="info")
            
    metrics_display_md = format_metrics_as_md(get_app_state()["fit_results"])
    return (metrics_display_md,)


@app.cell
def _(get_app_state, mo):
    status_message = mo.md(f"**Status:** *{get_app_state()['message']}*")
    return (status_message,)


@app.cell
def _(function_dropdown, generate_button, mo, noise_slider, plot_dim_radio, show_test_data_radio):
    data_gen_card = mo.callout([
        mo.md("### Data Generation"),
        plot_dim_radio,
        show_test_data_radio,
        function_dropdown,
        noise_slider,
        generate_button,
    ])
    return (data_gen_card,)


@app.cell
def _(
    alpha_slider,
    degree_slider,
    fit_button,
    loss_function_dropdown,
    mo,
    regularization_type_radio,
):
    loss_formulas = {'mse': r"$$L(y, \hat{y}) = \frac{1}{n} \sum_{i=1}^{n} (y_i - \hat{y}_i)^2$$"}
    formula = loss_formulas.get(str(loss_function_dropdown.value), "")
    loss_display_md = mo.md(f"{formula}").style({'textAlign': 'center', 'padding': '5px', 'border': '1px solid #ddd', 'borderRadius': '5px', 'marginTop': '5px'})

    model_params_card = mo.callout([
        mo.md("### Model Fit"),
        loss_function_dropdown,
        loss_display_md,
        degree_slider,
        regularization_type_radio,
        alpha_slider if regularization_type_radio.value in ['l1', 'l2'] else mo.md(""),
        mo.md("---"),
        mo.hstack([fit_button], justify="center", gap=1),
    ])
    return (model_params_card,)


@app.cell
def _(
    data_gen_card,
    main_plot,
    metrics_display_md,
    mo,
    model_params_card,
    status_message,
):
    output_card = mo.callout([main_plot, metrics_display_md, status_message])
    header = mo.md("""
        ## AIS 2025 - Regression Playground
        #### Chair of Information Systems and Business Analytics
        #### Uni Würzburg
        ---
        """).style({"text-align": "left"})
    app_view = mo.vstack([
        header,
        mo.hstack([
            mo.vstack([data_gen_card, model_params_card], gap=0),
            output_card
        ], gap=2, widths=["42%", "58%"]),
    ], gap=1)
    app_view
    return


if __name__ == "__main__":
    app.run()
