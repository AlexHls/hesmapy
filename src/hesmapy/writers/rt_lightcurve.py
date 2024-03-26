import os
import json
import pandas as pd
import numpy as np

from hesmapy.utils.writer_utils import (
    _check_data,
    _check_sources,
    _check_rt_lightcurve_units,
    _check_model_names,
    _check_numpy_array,
    _check_rt_lightcurve_derived_data,
    _rt_lightcurve_dataframe_to_json_dict,
)


# This is the base rt_lightcurve writer. All other writers should be wrappers
# around this one.
def write_rt_lightcurve_from_dataframe(
    data: pd.DataFrame | list[pd.DataFrame],
    path: str,
    derived_data: pd.DataFrame | list[pd.DataFrame] = None,
    model_names: str | list[str] = None,
    sources: dict | list[dict] = None,
    units: dict = None,
    overwrite: bool = False,
    create_path: bool = True,
) -> None:
    """
    Write lightcurve data to a JSON file
    compatible with the HESMA scheme from a DataFrame.

    Parameters
    ----------
    data : pd.DataFrame | list[pd.DataFrame]
        DataFrame or list of DataFrames containing the
        lightcurve data.
    path : str
        Path to the JSON file.
    derived_data : pd.DataFrame | list[pd.DataFrame], optional
        DataFrame or list of DataFrames containing the
        derived data, by default None.
    model_names : str | list[str], optional
        Name(s) of the model(s) to write, by default None. If None,
        the models will be named "model_0", "model_1", etc.
    overwrite : bool, optional
        Overwrite the file if it already exists, by default False.
    create_path : bool, optional
        Create the path if it does not exist, by default True.

    Returns
    -------
    None

    Notes
    -----
    The DataFrame(s) must contain the following columns:
    - magnitude
    - time
    - viewing_angle
    - band
    Other columns are optional. Only columns compliant with
    the HESMA scheme will be written to the JSON file.

    """

    if os.path.exists(path) and not overwrite:
        raise IOError(f"File {path} already exists")

    data = _check_data(data, columns=["magnitude", "time", "viewing_angle", "band"])

    if derived_data is not None:
        derived_data = _check_rt_lightcurve_derived_data(derived_data, len(data))

    model_names = _check_model_names(model_names, len(data))
    sources = _check_sources(sources)

    unique_bands = []
    for df in data:
        unique_bands.extend(df["band"].unique())
    unique_bands = list(set(unique_bands))
    units = _check_rt_lightcurve_units(units, unique_bands)

    rt_lightcurve = {}

    for i, df in enumerate(data):
        data_dict = _rt_lightcurve_dataframe_to_json_dict(
            df, model_names[i], sources, units
        )
        rt_lightcurve[model_names[i]] = data_dict[model_names[i]]

    if (
        create_path
        and not os.path.exists(os.path.dirname(path))
        and os.path.dirname(path) != ""
    ):
        os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as f:
        json.dump(rt_lightcurve, f)
