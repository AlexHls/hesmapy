import json
from jsonschema import ValidationError, validate
import plotly.graph_objects as go
import pandas as pd
from hesmapy.utils.plot_utils import add_timestep_slider


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
                        "required": ["radius", "density", "time"],
                    },
                },
            },
            "required": ["name", "data"],
        }

        self.path = path
        self.data = self._load_data()
        self.valid = self._validate_data()

        # This is a hacky way to deal with multiple models and individual
        # models at the same time
        if isinstance(self.data, dict):
            self.models = list(self.data.keys())
        elif isinstance(self.data, list):
            self.models = []
            for item in self.data:
                if isinstance(item, dict):
                    self.models.append(list(item.keys())[0])
                else:
                    self.valid = False
                    break
            else:
                # Put all data in a single dict so we don't have to deal with
                # with a list of dicts
                data = {}
                for i, item in enumerate(self.data):
                    data[self.models[i]] = item[self.models[i]]
        else:
            # This collects all the edge cases I can't think of
            self.models = []
            self.valid = False

    def _load_data(self) -> dict:
        with open(self.path) as f:
            try:
                data = json.load(f)
            except json.decoder.JSONDecodeError:
                raise IOError("Invalid JSON file")
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

    def get_unique_times(self, model: str) -> list:
        """
        Get the unique time steps for a model.
        Returns an empty list if the data is invalid

        Parameters
        ----------
        model : str
            Model to get unique time steps for

        Returns
        -------
        list
        """

        if not self.valid:
            return []
        unique_times = list(set([d["time"] for d in self.data[model]["data"]]))
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

        # TODO: Add support for multiple models

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

        if len(self.unique_times) > 1:
            time_unit = (
                self.data["units"]["time"] if "time" in self.data["units"] else None
            )
            fig = add_timestep_slider(fig, time=self.unique_times, time_unit=time_unit)

        fig.update_layout(showlegend=True)
        fig.update_layout(xaxis=dict(showexponent="all", exponentformat="e"))
        fig.update_layout(yaxis=dict(showexponent="all", exponentformat="e"))

        radius_unit = (
            self.data["units"]["radius"]
            if "radius" in self.data["units"]
            else "(arb. units)"
        )
        fig.update_xaxes(title_text=f"Radius ({radius_unit})")

        if show_plot:
            fig.show()

        return fig
