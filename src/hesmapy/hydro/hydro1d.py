import json
from jsonschema import ValidationError, validate
import plotly.graph_objects as go
import pandas as pd
from hesmapy.utils.plot_utils import (
    add_timestep_slider,
    plot_hydro_traces,
    add_log_axis_buttons,
    plot_abundance_traces,
)
from hesmapy.hydro.utils import normalize_hydro1d_data, get_abundance_data
from hesmapy.constants import HYDRO1D_JSON_SCHEMA


class Hydro1D:
    def __init__(self, path) -> None:
        self.schema = HYDRO1D_JSON_SCHEMA

        self.path = path
        self.data = self._load_data()

        # Naively assume that the data is valid
        self.valid = True

        self.models = []
        self.multi_model = self._multiple_models()

        self.valid = self._validate_data()

    def _multiple_models(self) -> bool:
        # This is a hacky way to deal with multiple models and individual
        # models at the same time
        if isinstance(self.data, dict):
            self.models = list(self.data.keys())
        elif isinstance(self.data, list):
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
                    modelname = self.models[i]
                    # Avoid duplicate keys
                    if modelname in data:
                        modelname = f"{modelname}_{i}"
                    data[modelname] = item[self.models[i]]
                    self.models[i] = modelname
                self.data = data
        else:
            # This collects all the edge cases I can't think of
            self.models = []
            self.valid = False
        return len(self.models) > 1

    def _load_data(self) -> dict:
        with open(self.path) as f:
            try:
                data = json.load(f)
            except json.decoder.JSONDecodeError:
                raise IOError("Invalid JSON file")
        return data

    def _validate_data(self) -> bool:
        for model in self.models:
            try:
                validate(self.data[model], schema=self.schema)
            except ValidationError:
                return False

        # TODO: Check if all data has the same length
        return True

    def _get_model(self, model: str | int = None) -> str:
        if model is None:
            model = self.models[0]
        elif isinstance(model, int):
            assert model < len(self.models), "Invalid model index"
            model = self.models[model]
        elif isinstance(model, str):
            assert model in self.models, "Invalid model name"
        else:
            raise TypeError("Invalid model type")
        return model

    def get_unique_times(self, model: str | int = None) -> list:
        """
        Get the unique time steps for a model.
        Returns an empty list if the data is invalid

        Parameters
        ----------
        model : str | int, optional
            Model to plot, by default None. Accepts either the model name or
            the index of the model in the list of models. If model is None,
            the first model is plotted

        Returns
        -------
        list
        """

        if not self.valid:
            return []
        model = self._get_model(model=model)
        unique_times = list(set([d["time"] for d in self.data[model]["data"]]))
        unique_times.sort()
        return unique_times

    def get_data(self, time: float = None, model: str | int = None) -> pd.DataFrame:
        """
        Get the data for a specific time step

        Parameters
        ----------
        time : float, optional
            Time step to get data for, by default None
        model : str | int, optional
            Model to plot, by default None. Accepts either the model name or
            the index of the model in the list of models. If model is None,
            the first model is plotted

        Returns
        -------
        pd.DataFrame
        """
        if not self.valid:
            raise NotImplementedError("Getting data of invalid data not implemented")

        model = self._get_model(model=model)
        df = pd.DataFrame(self.data[model]["data"])

        if time is None:
            return df

        return df[df["time"] == time]

    def get_units(self, model: str | int = None) -> dict:
        """
        Get the units for a model

        Parameters
        ----------
        model : str | int, optional
            Model to plot, by default None. Accepts either the model name or
            the index of the model in the list of models. If model is None,
            the first model is plotted

        Returns
        -------
        dict
        """
        if not self.valid:
            raise NotImplementedError("Getting units of invalid data not implemented")

        model = self._get_model(model=model)

        radius_unit = (
            self.data[model]["units"]["radius"]
            if "radius" in self.data[model]["units"]
            else "(arb. units)"
        )
        density_unit = (
            self.data[model]["units"]["density"]
            if "density" in self.data[model]["units"]
            else "(arb. units)"
        )
        pressure_unit = (
            self.data[model]["units"]["pressure"]
            if "pressure" in self.data[model]["units"]
            else "(arb. units)"
        )
        temperature_unit = (
            self.data[model]["units"]["temperature"]
            if "temperature" in self.data[model]["units"]
            else "(arb. units)"
        )
        mass_unit = (
            self.data[model]["units"]["mass"]
            if "mass" in self.data[model]["units"]
            else "(arb. units)"
        )
        velocity_unit = (
            self.data[model]["units"]["velocity"]
            if "velocity" in self.data[model]["units"]
            else "(arb. units)"
        )
        time_unit = (
            self.data[model]["units"]["time"]
            if "time" in self.data[model]["units"]
            else "(arb. units)"
        )
        units = {
            "radius": radius_unit,
            "density": density_unit,
            "pressure": pressure_unit,
            "temperature": temperature_unit,
            "mass": mass_unit,
            "velocity": velocity_unit,
            "time": time_unit,
        }

        return units

    def plot(
        self, model: str | int = None, show_plot: bool = False, max_abundances: int = 5
    ) -> go.Figure:
        """
        Plot the data

        Parameters
        ----------
        model : str | int, optional
            Model to plot, by default None. Accepts either the model name or
            the index of the model in the list of models. If model is None,
            the first model is plotted
        show_plot : bool, optional
            Show the plot, by default False
        max_abundances : int, optional
            Maximum number of abundances to plot, by default 5. Abundances will
            be plotted in order of decreasing abundance

        Returns
        -------
        go.Figure
        """
        if not self.valid:
            raise NotImplementedError("Plotting of invalid data not implemented")

        assert isinstance(max_abundances, int), "max_abundances must be an integer"

        model = self._get_model(model=model)

        fig = go.Figure()

        # TODO: Add support for multiple models
        unique_times = self.get_unique_times(model=model)
        units = self.get_units(model=model)

        # Split data into unique time steps
        for t in unique_times:
            data = self.get_data(time=t, model=model)
            data, normalization_factors = normalize_hydro1d_data(data)
            num_data = plot_hydro_traces(fig, data, units, normalization_factors)
            if max_abundances > 0:
                abundance_data = get_abundance_data(data, max_abundances)
                if abundance_data.empty:
                    continue
                num_data += plot_abundance_traces(fig, abundance_data, data, units)

        # Make 0th trace visible
        for j in range(num_data):
            fig.data[j].visible = True

        # Add a title for the 0th trace
        if unique_times is not None:
            title = "Time: " + "{:.4f}".format(unique_times[0]) + " " + units["time"]
            fig.update_layout(title=title)

        if len(unique_times) > 1:
            fig = add_timestep_slider(
                fig, time=unique_times, time_unit=units["time"], num_data=num_data
            )

        fig.update_layout(showlegend=True)
        fig.update_layout(xaxis=dict(showexponent="all", exponentformat="e"))
        fig.update_layout(yaxis=dict(showexponent="all", exponentformat="e"))

        fig = add_log_axis_buttons(fig, axis="both")

        fig.update_xaxes(title_text=f"Radius ({units['radius']})")
        fig.update_yaxes(title_text="Normalized data")

        if show_plot:
            fig.show()

        return fig
