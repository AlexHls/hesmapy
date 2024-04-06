import pandas as pd
import plotly.graph_objects as go

from hesmapy.json_base import HesmaBaseJSONFile
from hesmapy.constants import RT_SPECTRUM_JSON_SCHEMA, ARB_UNIT_STRING
from hesmapy.utils.plot_utils import (
    plot_spectra,
    add_timestep_slider,
    add_log_axis_buttons,
)


class RTSpectrum(HesmaBaseJSONFile):
    def __init__(self, path) -> None:
        self.schema = RT_SPECTRUM_JSON_SCHEMA
        super().__init__(path)

    def get_data(
        self, time: float = None, model: str | int = None
    ) -> pd.DataFrame | list[pd.DataFrame]:
        """
        Get the data for a specific time

        Parameters
        ----------
        time : float, optional
            Time to get data for, by default None
        model : str | int, optional
            Model to plot, by default None. Accepts either the model name or
            the index of the model in the list of models. If model is None,
            the first model is plotted

        Returns
        -------
        pd.DataFrame | list[pd.DataFrame]
        """
        if not self.valid:
            raise NotImplementedError("Getting data of invalid data not implemented")

        model = self._get_model(model=model)
        data = self.data[model]["data"]

        if time is not None:
            for d in data:
                if d["time"] == time:
                    df_data = {
                        "wavelength": d["wavelength"],
                        "flux": d["flux"],
                    }
                    if "flux_err" in d:
                        df_data["flux_err"] = d["flux_err"]
                    return pd.DataFrame(df_data)
        else:
            dfs = []
            for time in self.get_unique_times(model=model):
                dfs.append(self.get_data(time=time, model=model))
            return dfs

    def get_unique_times(self, model: str | int = None) -> list:
        """
        Get the unique times

        Parameters
        ----------
        model : str | int, optional
            Model to plot, by default None. Accepts either the model name or
            the index of the model in the list of models. If model is None,
            the first model is accessed

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

    def get_units(self, model: str | int = None) -> dict:
        """
        Get the units for a model

        Parameters
        ----------
        model : str | int, optional
            Model to plot, by default None. Accepts either the model name or
            the index of the model in the list of models. If model is None,
            the first model is accessed

        Returns
        -------
        dict
        """
        if not self.valid:
            raise NotImplementedError("Getting units of invalid data not implemented")

        model = self._get_model(model=model)

        time_unit = (
            self.data[model]["units"]["time"]
            if "time" in self.data[model]["units"]
            else ARB_UNIT_STRING
        )
        wavelength_unit = (
            self.data[model]["units"]["wavelength"]
            if "wavelength" in self.data[model]["units"]
            else ARB_UNIT_STRING
        )
        flux_unit = (
            self.data[model]["units"]["flux"]
            if "flux" in self.data[model]["units"]
            else ARB_UNIT_STRING
        )
        flux_err_unit = (
            self.data[model]["units"]["flux_err"]
            if "flux_err" in self.data[model]["units"]
            else ARB_UNIT_STRING
        )

        units = {
            "time": time_unit,
            "wavelength": wavelength_unit,
            "flux": flux_unit,
            "flux_err": flux_err_unit,
        }

        return units

    def plot(self, model: str | int = None, show_plot: bool = False) -> go.Figure:
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

        Returns
        -------
        go.Figure
        """
        if not self.valid:
            raise NotImplementedError("Plotting of invalid data not implemented")

        model = self._get_model(model=model)

        fig = go.Figure()

        # TODO: Add support for multiple models
        unique_times = self.get_unique_times(model=model)
        units = self.get_units(model=model)

        # Split data into unique time steps
        for t in unique_times:
            data = self.get_data(time=t, model=model)
            num_data = plot_spectra(fig, data, t, units)

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

        fig.update_layout(xaxis=dict(showexponent="all", exponentformat="none"))
        fig.update_layout(yaxis=dict(showexponent="all", exponentformat="e"))

        fig = add_log_axis_buttons(fig, axis="y")

        fig.update_xaxes(title_text=f"Wavelength ({units['wavelength']})")
        fig.update_yaxes(title_text=f"Flux ({units['flux']})")

        if show_plot:
            fig.show()

        return fig
