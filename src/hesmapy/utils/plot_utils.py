# Purpose: Utility functions for plotting
import plotly.graph_objects as go


def add_timestep_slider(
    fig: go.Figure, time: list | None = None, time_unit: str | None = None
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

    Returns
    -------
    go.Figure
    """
    if time_unit is None:
        time_unit = "(arb. units)"

    steps = []
    for i in range(len(fig.data)):
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
        step["args"][0]["visible"][i] = True  # Toggle i'th trace to "visible"
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
