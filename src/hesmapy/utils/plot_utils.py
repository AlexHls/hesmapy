# Purpose: Utility functions for plotting
import plotly.graph_objects as go


def _add_timestep_slider(fig: go.Figure) -> go.Figure:
    """
    Add a slider to the figure

    Parameters
    ----------
    fig : go.Figure
        Figure to add slider to

    Returns
    -------
    go.Figure
    """
    steps = []
    for i in range(len(fig.data)):
        step = dict(
            method="update",
            args=[
                {"visible": [False] * len(fig.data)},
                {"title": "Timestep: " + str(i)},
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
