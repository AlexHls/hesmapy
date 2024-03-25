import numpy as np
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

from hesmapy.json_base import HesmaBaseJSONFile
from hesmapy.constants import RT_LIGHTCURVE_JSON_SCHEMA
from hesmapy.utils.plot_utils import (
    plot_lightcurves,
    plot_derived_lightcurve_data,
    add_viewing_angle_slider,
    add_reverse_y_axis_button,
)


class RTLightcurve(HesmaBaseJSONFile):
    def __init__(self, path) -> None:
        self.schema = RT_LIGHTCURVE_JSON_SCHEMA
        super().__init__(path)

    def get_data(
        self, viewing_angle: float = None, model: str | int = None
    ) -> pd.DataFrame:
        """
        Get the data for a specific viewing angle

        Parameters
        ----------
        viewing_angle : float, optional
            Viewing angle to get data for, by default None
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

        if viewing_angle is None:
            return df

        return df[df["viewing_angle"] == viewing_angle]

    def get_derived_data(
        self, viewing_angle: float = None, model: str | int = None
    ) -> pd.DataFrame:
        """
        Get the derived data for a specific viewing angle

        Parameters
        ----------
        viewing_angle : float, optional
            Viewing angle to get data for, by default None
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
        df = pd.DataFrame(self.data[model]["derived_data"])

        if viewing_angle is None:
            return df

        return df[df["viewing_angle"] == viewing_angle]

    def get_unique_viewing_angles(self, model: str | int = None) -> list:
        """
        Get the unique viewing angles

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
        unique_viewing_angles = list(
            set([d["viewing_angle"] for d in self.data[model]["data"]])
        )
        unique_viewing_angles.sort()
        return unique_viewing_angles

    def get_unique_bands(self, model: str | int = None) -> list:
        """
        Get the unique bands

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
        unique_bands = list(set([d["band"] for d in self.data[model]["data"]]))
        unique_bands.sort()
        return unique_bands

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
        unique_bands = self.get_unique_bands(model=model)

        time_unit = (
            self.data[model]["units"]["time"]
            if "time" in self.data[model]["units"]
            else "(arb. units)"
        )
        units = {
            "time": time_unit,
        }
        for band in unique_bands:
            if band not in self.data[model]["units"]:
                self.data[model]["units"][band] = "(arb. units)"
            units[band] = self.data[model]["units"][band]

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

        fig = make_subplots(
            rows=2,
            cols=1,
            vertical_spacing=0.12,
            subplot_titles=("Lightcurves", "Derived Data"),
            specs=[[{"type": "scatter"}], [{"type": "table"}]],
        )

        # TODO: Add support for multiple models
        unique_viewing_angles = self.get_unique_viewing_angles(model=model)
        unique_bands = self.get_unique_bands(model=model)
        units = self.get_units(model=model)

        # Split data into unique time steps
        num_data = []
        for va in unique_viewing_angles:
            data = self.get_data(viewing_angle=va, model=model)
            num_data.append(plot_lightcurves(fig, data, units, unique_bands))

        # Plot derived data
        for va in unique_viewing_angles:
            derived_data = self.get_derived_data(viewing_angle=va, model=model)
            plot_derived_lightcurve_data(fig, derived_data)

        # Make 0th trace visible
        for j in range(num_data[0]):
            fig.data[j].visible = True
        # Make 0th table visible
        fig.data[np.sum(num_data)].visible = True

        if len(unique_viewing_angles) > 1:
            fig = add_viewing_angle_slider(
                fig,
                viewing_angles=unique_viewing_angles,
                num_data=num_data,
            )

        # Add a title for the 0th trace
        if unique_viewing_angles is not None:
            title = "Viewing angle bin: " + "{:d}".format(unique_viewing_angles[0])
            fig.update_layout(title=title)

        fig.update_layout(showlegend=True)
        fig.update_xaxes(title_text=f"Time ({units['time']})")
        fig.update_yaxes(title_text="Luminosity")

        fig = add_reverse_y_axis_button(fig)

        if show_plot:
            fig.show()

        return fig
