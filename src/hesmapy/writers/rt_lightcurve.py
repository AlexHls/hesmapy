import os
import json
import pandas as pd
import numpy as np

from hesmapy.utils.writer_utils import (
    _check_data_dataframe,
    _check_data_dict,
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

    data = _check_data_dataframe(
        data, columns=["magnitude", "time", "viewing_angle", "band"]
    )

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


def write_rt_lightcurve_from_dict(
    data: dict | list[dict],
    path: str,
    derived_data: dict | list[dict] = None,
    model_names: str | list[str] = None,
    sources: dict | list[dict] = None,
    units: dict = None,
    overwrite: bool = False,
    create_path: bool = True,
) -> None:
    """
    Write lightcurve data to a JSON file
    compatible with the HESMA scheme from a dict.

    Parameters
    ----------
    data : dict | list[dict]
        Dictionary or list of dictionaries containing the
        lightcurve data.
    path : str
        Path to the JSON file.
    derived_data : dict | list[dict], optional
        Dictionary or list of dictionaries containing the
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
    The dict(s) must contain the following keys:
    - magnitude
    - time
    - viewing_angle
    - band
    Other keys are optional. Only keys compliant with
    the HESMA scheme will be written to the JSON file.

    """

    data = _check_data_dict(data)

    data_dfs = []
    for d in data:
        data_dfs.append(pd.DataFrame(d))

    # We only check the shape and defer the length check to the
    # check in the write_rt_lightcurve_from_dataframe function.
    # The try block is only to change the error message
    # and make it less confusing.
    if derived_data is not None:
        try:
            derived_data = _check_data_dict(derived_data)
        except TypeError:
            raise TypeError(
                "Derived data must be a dictionary or a list of dictionaries"
            )
        derived_data_dfs = []
        for d in derived_data:
            derived_data_dfs.append(pd.DataFrame(d))

    write_rt_lightcurve_from_dataframe(
        data_dfs,
        path,
        derived_data=derived_data_dfs if derived_data is not None else None,
        model_names=model_names,
        sources=sources,
        units=units,
        overwrite=overwrite,
        create_path=create_path,
    )
