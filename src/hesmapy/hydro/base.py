import json
from jsonschema import ValidationError, validate
import plotly.graph_objects as go
import numpy as np
import pandas as pd
from hesmapy.utils.plot_utils import _add_timestep_slider


class Hydro1D:
    def __init__(self, path) -> None:
        self.schema = {
            "type": "object",
            "properties": {
                "name": {"type": "string"},
                "schema": {"type": "string"},
                "sources": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "bibcode": {"type": "string"},
                            "reference": {"type": "string"},
                            "url": {"type": "string"},
                        },
                    },
                },
                "units": {
                    "type": "object",
                    "properties": {
                        "radius": {"type": "string"},
                        "density": {"type": "string"},
                        "pressure": {"type": "string"},
                        "temperature": {"type": "string"},
                        "mass": {"type": "string"},
                        "velocity": {"type": "string"},
                        "time": {"type": "string"},
                    },
                },
                "data": {
                    "type": "array",
                    "minItems": 2,
                    "items": {
                        "type": "object",
                        "properties": {
                            "radius": {"type": "number"},
                            "density": {"type": "number"},
                            "pressure": {"type": "number"},
                            "temperature": {"type": "number"},
                            "mass": {"type": "number"},
                            "velocity": {"type": "number"},
                            "time": {"type": "number"},
                            "\bx[A-Z][a-z][0-9]{0,3}\b": {"type": "number"},
                        },
                        "required": ["radius", "density"],
                    },
                },
            },
            "required": ["name", "data"],
        }

        self.path = path
        self.data = self._load_data()
        self.valid = self._validate_data()
        # Set data to the first object in the data array
        self.data = self.data[list(self.data.keys())[0]]
        self.unique_times = self._get_unique_times()

    def _load_data(self) -> dict:
        with open(self.path) as f:
            try:
                data = json.load(f)
            except json.decoder.JSONDecodeError:
                # TODO Implement propper error handling
                raise ValueError("Invalid JSON file")
        return data

    def _validate_data(self) -> bool:
        if len(self.data) > 1:
            return False
        try:
            obj = list(self.data.keys())[0]
            validate(self.data[obj], schema=self.schema)
        except ValidationError:
            return False

        # TODO: Check if all data has the same length
        return True

    def _get_unique_times(self) -> np.ndarray:
        unique_times = list(set([d["time"] for d in self.data["data"]]))
        unique_times.sort()
        return unique_times

    def get_data(self, time: float = None) -> pd.DataFrame:
        """
        Get the data for a specific time step

        Parameters
        ----------
        time : float, optional
            Time step to get data for, by default None

        Returns
        -------
        pd.DataFrame
        """
        if not self.valid:
            raise NotImplementedError("Getting data of invalid data not implemented")

        if time is None:
            return pd.DataFrame(self.data["data"])

        return pd.DataFrame(self.data["data"]).query(f"time == {time}")

    def plot(self, show_plot=False) -> go.Figure:
        """
        Plot the data

        Parameters
        ----------
        show_plot : bool, optional
            Show the plot, by default False

        Returns
        -------
        go.Figure
        """
        if not self.valid:
            raise NotImplementedError("Plotting of invalid data not implemented")

        fig = go.Figure()

        # Split data into unique time steps
        for t in self.unique_times:
            data = self.get_data(time=t)
            fig.add_trace(
                go.Scatter(
                    visible=False,
                    x=data["radius"],
                    y=data["density"],
                    name="Density",
                    line=dict(color="#33CFA5"),
                )
            )

        # Make 0th trace visible
        fig.data[0].visible = True

        fig = _add_timestep_slider(fig)

        if show_plot:
            fig.show()

        return fig
