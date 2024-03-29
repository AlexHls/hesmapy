import numpy as np
import pandas as pd
import plotly.graph_objects as go

from hesmapy.constants import ARB_UNIT_STRING

ABUNDANCE_COLORS = [
    "#8C564B",
    "#E377C2",
    "#7F7F7F",
    "#BCBD22",
    "#17BECF",
]  # Colors for abundance traces

# DONT TOUCH THE ORDER OF THESE COLUMNS!
DERIVED_LIGHTCURVE_COLUMNS = [
    ("band", "Band"),
    ("decline_rate_15", r"$\Delta m_{15}$"),
    ("peak_mag", r"$m_\text{max}$"),
    ("peak_time", r"$t_\text{max}$"),
    ("rise_time", r"$t_\text{rise}$"),
    ("decline_rate_40", r"$\Delta m_{40}$"),
]  # DO NOT CHANGE THE ORDER OF THESE COLUMNS!
# For some reason the column labels disappear if you change the order of the columns
# and you use the viewing angle slider. I have no idea why this happens


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
        time_unit = ARB_UNIT_STRING

    steps = []
    for i in range(len(time)):
        if time is not None:
            title = "Time: " + "{:.4f}".format(time[i]) + " " + time_unit
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
            step["args"][0]["visible"][
                i * num_data + j
            ] = True  # Toggle i'th trace to "visible"
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


def add_viewing_angle_slider(
    fig: go.Figure,
    viewing_angles: list | None = None,
    num_data: list = [1],
    has_derived_data: bool = False,
) -> go.Figure:
    """
    Add a slider to the figure

    Parameters
    ----------
    fig : go.Figure
        Figure to add slider to
    viewing_angles : list, optional
        List of viewing angles to use for slider, by default None
    num_data : list, optional
        Number of data sets for each viewing angle, by default [1]
    has_derived_data : bool, optional
        Whether or not the figure has derived data, by default False

    Returns
    -------
    go.Figure
    """

    assert len(num_data) == len(
        viewing_angles
    ), "num_data must have the same length as viewing_angles"

    total_data = np.sum(num_data)

    steps = []
    for i in range(len(viewing_angles)):
        if viewing_angles is not None:
            title = "Viewing angle bin: " + f"{viewing_angles[i]}"
        else:
            title = "Viewing angle bin: " + str(i)
        step = dict(
            method="update",
            args=[
                {"visible": [False] * len(fig.data)},
                {"title": title},
            ],  # layout attribute
        )
        for j in range(num_data[i]):
            step["args"][0]["visible"][
                i * num_data[i] + j
            ] = True  # Toggle i'th trace to "visible"
        if has_derived_data:
            step["args"][0]["visible"][
                total_data + i
            ] = True  # Toggle i'th table to "visible"
        steps.append(step)

    sliders = [
        dict(
            active=0,
            currentvalue={"prefix": "Viewing angle bin: "},
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


def add_reverse_y_axis_button(fig: go.Figure) -> go.Figure:
    """
    Add buttons to reverse the y axis

    Parameters
    ----------
    fig : go.Figure
        Figure to add buttons to

    Returns
    -------
    go.Figure
    """
    # Define the layout button
    button = dict(
        label="Inverted Y-Axis",
        method="relayout",
        args=[
            {
                "yaxis.autorange": not True
                if fig.layout.yaxis.autorange == "reversed"
                else "reversed"
            }
        ],
    )
    button2 = dict(
        label="Regular Y-Axis",
        method="relayout",
        args=[
            {
                "yaxis.autorange": not True
                if fig.layout.yaxis.autorange == "reversed"
                else "max"  # I have no idea why 'max' works and True doesn't. DON'T TOUCH THIS
            }
        ],
    )

    # Add the button to the updatemenus attribute
    fig.update_layout(
        updatemenus=[
            dict(
                type="buttons",
                buttons=[button, button2],
                pad={"r": 2, "t": 10},
                showactive=True,
                xanchor="right",
                yanchor="top",
            )
        ]
    )
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


def plot_lightcurves(
    fig: go.Figure, data: pd.DataFrame, units: dict, bands: list
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
    bands : list
        Bands to plot


    Returns
    -------
    int
    """
    num_data = 0
    for band in bands:
        subset = data[data["band"] == band]
        hovertemplate = (
            f"{band}"
            + ": %{y:.2e}"
            + f" {units[band]}<br>Time: "
            + "%{x:.2e}"
            + f" {units['time']}<br>"
        )
        fig.add_trace(
            go.Scatter(
                visible=False,
                x=subset["time"],
                y=subset["magnitude"],
                name=band,
                hovertemplate=hovertemplate,
            ),
            row=1,
            col=1,
        )
        num_data += 1

    return num_data


def plot_spectra(fig: go.Figure, data: pd.DataFrame, time: float, units: dict) -> int:
    """
    Plot spectra data

    Parameters
    ----------
    fig : go.Figure
        Figure to add traces to
    data : pd.DataFrame
        Data to plot
    time : float
        Time of data
    units : dict
        Units of data

    Returns
    -------
    int
    """
    num_data = 0
    hovertemplate = (
        "Flux: %{y:.2e}"
        + f" {units['flux']}<br>Wavelength: "
        + "%{x:.2e}"
        + f" {units['wavelength']}<br>"
    )
    fig.add_trace(
        go.Scatter(
            visible=False,
            x=data["wavelength"],
            y=data["flux"],
            name=f"{time:.3f} {units['time']}",
            hovertemplate=hovertemplate,
        )
    )
    num_data += 1  # This is useless for now, maybe it's useful in the future

    return num_data


def plot_derived_lightcurve_data(fig: go.Figure, data: pd.DataFrame) -> None:
    """
    Plot derived lightcurve data

    Parameters
    ----------
    fig : go.Figure
        Figure to add traces to
    data : pd.DataFrame
        Data to plot

    Returns
    -------
    None
    """
    values_header = []
    values_cells = []
    for col, label in DERIVED_LIGHTCURVE_COLUMNS:
        values_header.append(label)
        try:
            values_cells.append(data[col])
        except KeyError:
            values_cells.append(["-"] * len(data))

    fig.add_trace(
        go.Table(
            header=dict(values=values_header),
            cells=dict(
                values=values_cells,
            ),
            visible=False,
        ),
        row=2,
        col=1,
    )
