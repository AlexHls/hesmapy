# Purpose: Utility functions for plotting
import plotly.graph_objects as go
import pandas as pd


ABUNDANCE_COLORS = [
    "#8C564B",
    "#E377C2",
    "#7F7F7F",
    "#BCBD22",
    "#17BECF",
]  # Colors for abundance traces


def add_timestep_slider(
    fig: go.Figure,
    time: list | None = None,
    time_unit: str | None = None,
    num_data: int = 1,
) -> go.Figure:
    """
    Add a slider to the figure

    Parameters
    ----------
    fig : go.Figure
        Figure to add slider to
    time : list, optional
        List of times to use for slider, by default None
    time_unit : str, optional
        Unit of time, by default None
    num_data : int, optional
        Number of data sets, by default 1

    Returns
    -------
    go.Figure
    """
    if time_unit is None:
        time_unit = "(arb. units)"

    steps = []
    for i in range(len(time)):
        if time is not None:
            title = "Time: " + str(time[i]) + " " + time_unit
        else:
            title = "Updated to timestep: " + str(i)
        step = dict(
            method="update",
            args=[
                {"visible": [False] * len(fig.data)},
                {"title": title},
            ],  # layout attribute
        )
        for j in range(num_data):
            step["args"][0]["visible"][i + j] = True  # Toggle i'th trace to "visible"
        steps.append(step)

    sliders = [
        dict(
            active=0,
            currentvalue={"prefix": "Timestep: "},
            pad={"t": 50},
            steps=steps,
        )
    ]

    fig.update_layout(sliders=sliders)

    return fig


def add_log_axis_buttons(fig: go.Figure, axis: str = "both") -> go.Figure:
    """
    Add buttons to toggle log x axis

    Parameters
    ----------
    fig : go.Figure
        Figure to add buttons to
    axis : str, optional
        Axis to add buttons to, by default "both". Can be "x", "y", or "both"

    Returns
    -------
    go.Figure
    """
    assert axis in ["x", "y", "both"], "axis must be 'x', 'y', or 'both'"

    updatemenus = []
    annotations = []

    x_buttons = dict(
        type="buttons",
        direction="left",
        buttons=list(
            [
                dict(
                    args=[{"xaxis.type": "linear"}], label="Linear", method="relayout"
                ),
                dict(args=[{"xaxis.type": "log"}], label="Log", method="relayout"),
            ]
        ),
        pad={},
        showactive=True,
        x=0.26,
        xanchor="left",
        y=1.15,
        yanchor="top",
    )
    y_buttons = dict(
        type="buttons",
        direction="left",
        buttons=list(
            [
                dict(
                    args=[{"yaxis.type": "linear"}], label="Linear", method="relayout"
                ),
                dict(args=[{"yaxis.type": "log"}], label="Log", method="relayout"),
            ]
        ),
        pad={},
        showactive=True,
        x=0.26,
        xanchor="left",
        y=1.1,
        yanchor="top",
    )
    x_labels = dict(
        text="X-Axis scale",
        showarrow=False,
        x=0.2,
        y=1.14,
        xref="paper",
        yref="paper",
        align="left",
    )
    y_labels = dict(
        text="Y-Axis scale",
        showarrow=False,
        x=0.2,
        y=1.09,
        xref="paper",
        yref="paper",
        align="left",
    )
    if axis in ["x", "both"]:
        updatemenus.append(x_buttons)
        annotations.append(x_labels)
    if axis in ["y", "both"]:
        updatemenus.append(y_buttons)
        annotations.append(y_labels)

    fig.update_layout(updatemenus=updatemenus)
    fig.update_layout(annotations=annotations)

    return fig


def plot_hydro_traces(
    fig: go.Figure, data: pd.DataFrame, units: dict, normalization_factors: dict = None
) -> int:
    """
    Plot hydro data

    Parameters
    ----------
    fig : go.Figure
        Figure to add traces to
    data : pd.DataFrame
        Data to plot
    units : dict
        Units of data
    normalization_factors : dict, optional
        Normalization factors, by default None


    Returns
    -------
    int
    """
    if normalization_factors is None:
        normalization_factors = {
            "density": 1,
            "pressure": 1,
            "temperature": 1,
            "mass": 1,
            "velocity": 1,
        }
    num_data = 1
    hovertemplate = (
        "Density: %{customdata:.2e}"
        + f" {units['density']}<br>Radius: "
        + "%{x:.2e}"
        + f" {units['radius']}<br>"
    )
    fig.add_trace(
        go.Scatter(
            visible=False,
            x=data["radius"],
            y=data["density"],
            name="Density",
            line=dict(color="#1F77B4"),
            customdata=data["density"] * normalization_factors["density"],
            hovertemplate=hovertemplate,
        )
    )
    if "pressure" in data:
        hovertemplate = (
            "Pressure: %{customdata:.2e}"
            + f" {units['pressure']}<br>Radius: "
            + "%{x:.2e}"
            + f" {units['radius']}<br>"
        )
        fig.add_trace(
            go.Scatter(
                visible=False,
                x=data["radius"],
                y=data["pressure"],
                name="Pressure",
                line=dict(color="#FF7F0E"),
                customdata=data["pressure"] * normalization_factors["pressure"],
                hovertemplate=hovertemplate,
            )
        )
        num_data += 1
    if "temperature" in data:
        hovertemplate = (
            "Temperature: %{customdata:.2e}"
            + f" {units['temperature']}<br>Radius: "
            + "%{x:.2e}"
            + f" {units['radius']}<br>"
        )
        fig.add_trace(
            go.Scatter(
                visible=False,
                x=data["radius"],
                y=data["temperature"],
                name="Temperature",
                line=dict(color="#2CA02C"),
                customdata=data["temperature"] * normalization_factors["temperature"],
                hovertemplate=hovertemplate,
            )
        )
        num_data += 1
    if "mass" in data:
        hovertemplate = (
            "Mass: %{customdata:.2e}"
            + f" {units['mass']}<br>Radius: "
            + "%{x:.2e}"
            + f" {units['radius']}<br>"
        )
        fig.add_trace(
            go.Scatter(
                visible=False,
                x=data["radius"],
                y=data["mass"],
                name="Mass",
                line=dict(color="#D62728"),
                customdata=data["mass"] * normalization_factors["mass"],
                hovertemplate=hovertemplate,
            )
        )
        num_data += 1
    if "velocity" in data:
        hovertemplate = (
            "Velocity: %{customdata:.2e}"
            + f" {units['velocity']}<br>Radius: "
            + "%{x:.2e}"
            + f" {units['radius']}<br>"
        )
        fig.add_trace(
            go.Scatter(
                visible=False,
                x=data["radius"],
                y=data["velocity"],
                name="Velocity",
                line=dict(color="#9467BD"),
                customdata=data["velocity"] * normalization_factors["velocity"],
                hovertemplate=hovertemplate,
            )
        )
        num_data += 1

    return num_data


def plot_abundance_traces(
    fig: go.Figure, abundance_data: pd.DataFrame, data: pd.DataFrame, units: dict
) -> int:
    """
    Plot abundance data

    Parameters
    ----------
    fig : go.Figure
        Figure to add traces to
    abundance_data : pd.DataFrame
        Abundance data to plot
    data : pd.DataFrame
        Hydro data
    units : dict
        Units of data

    Returns
    -------
    int
    """
    num_data = len(abundance_data.columns)
    for i, index in enumerate(abundance_data.columns):
        hovertemplate = (
            f"{index}"
            + ": %{y:.2e}"
            + "<br>Radius: "
            + "%{x:.2e}"
            + f" {units['radius']}<br>"
        )
        fig.add_trace(
            go.Scatter(
                visible=False,
                x=data["radius"],
                y=abundance_data[index],
                name=index,
                line=dict(color=ABUNDANCE_COLORS[i % len(ABUNDANCE_COLORS)]),
                hovertemplate=hovertemplate,
            )
        )

    return num_data
