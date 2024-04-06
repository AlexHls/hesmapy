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
    else:
        derived_data = [None] * len(data)

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
            df, model_names[i], derived_data[i], sources, units
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


def write_rt_lightcurve_from_numpy(
    time: np.ndarray | list[np.ndarray],
    magnitude: np.ndarray | list[np.ndarray],
    band: str | list[str],
    viewing_angle: np.ndarray | list[np.ndarray],
    path: str,
    e_magnitude: np.ndarray | list[np.ndarray] = None,
    peak_mag: np.ndarray | list[np.ndarray] = None,
    peak_time: np.ndarray | list[np.ndarray] = None,
    rise_time: np.ndarray | list[np.ndarray] = None,
    decline_rate_15: np.ndarray | list[np.ndarray] = None,
    decline_rate_40: np.ndarray | list[np.ndarray] = None,
    derived_band: str | list[str] = None,
    derived_viewing_angle: np.ndarray | list[np.ndarray] = None,
    model_names: str | list[str] = None,
    sources: dict | list[dict] = None,
    units: dict = None,
    overwrite: bool = False,
    create_path: bool = True,
) -> None:
    """
    Write lightcurve data to a JSON file
    compatible with the HESMA scheme from numpy arrays.

    Parameters
    ----------
    time : np.ndarray | list[np.ndarray]
        Time of the lightcurve data.
    magnitude : np.ndarray | list[np.ndarray]
        Magnitude of the lightcurve data.
    band : str | list[str]
        Bands of the lightcurve data.
    viewing_angle : np.ndarray | list[np.ndarray]
        Viewing angles of the lightcurve data.
    path : str
        Path to the JSON file.
    e_magnitude : np.ndarray | list[np.ndarray], optional
        Error on the magnitude of the lightcurve data, by default None.
    peak_mag : np.ndarray | list[np.ndarray], optional
        Peak magnitude of the lightcurve data, by default None.
    peak_time : np.ndarray | list[np.ndarray], optional
        Peak time of the lightcurve data, by default None.
    rise_time : np.ndarray | list[np.ndarray], optional
        Rise time of the lightcurve data, by default None.
    decline_rate_15 : np.ndarray | list[np.ndarray], optional
        Decline rate at 15 days of the lightcurve data, by default None.
    decline_rate_40 : np.ndarray | list[np.ndarray], optional
        Decline rate at 40 days of the lightcurve data, by default None.
    derived_band : str | list[str], optional
        Bands of the derived data, by default None.
    derived_viewing_angle : np.ndarray | list[np.ndarray], optional
        Viewing angles of the derived data, by default None.
    model_names : str | list[str], optional
        Name(s) of the model(s) to write, by default None. If None,
        the models will be named "model_0", "model_1", etc.
    sources : dict | list[dict], optional
        Source(s) of the model, by default None.
    units : dict, optional
        Units of the model, by default None. If None, the units will
        be set to "(arb. units)".
    overwrite : bool, optional
        Overwrite the file if it already exists, by default False.
    create_path : bool, optional
        Create the path if it does not exist, by default True.

    Returns
    -------
    None

    Notes
    -----
    The numpy arrays of the data and derived data must have the same
    length, respectively. Multiple lightcurves of the same model should
    be given in the same one-dimensional numpy array. The time, magnitude
    and band arrays in combination will be used to extract the
    individual lightcurves.

    """

    time = _check_numpy_array(time)
    magnitude = _check_numpy_array(magnitude)
    band = _check_numpy_array(band)
    viewing_angle = _check_numpy_array(viewing_angle)
    if e_magnitude is not None:
        e_magnitude = _check_numpy_array(e_magnitude)
    if peak_mag is not None:
        peak_mag = _check_numpy_array(peak_mag)
    if peak_time is not None:
        peak_time = _check_numpy_array(peak_time)
    if rise_time is not None:
        rise_time = _check_numpy_array(rise_time)
    if decline_rate_15 is not None:
        decline_rate_15 = _check_numpy_array(decline_rate_15)
    if decline_rate_40 is not None:
        decline_rate_40 = _check_numpy_array(decline_rate_40)
    if derived_band is not None:
        derived_band = _check_numpy_array(derived_band)
    if derived_viewing_angle is not None:
        derived_viewing_angle = _check_numpy_array(derived_viewing_angle)

    if len(time) != len(magnitude) != len(band) != len(viewing_angle):
        raise ValueError("All data arrays must have the same length")
    if e_magnitude is not None:
        if len(e_magnitude) != len(time):
            raise ValueError("All arrays must have the same length")

    derived_lengths = []
    if peak_mag is not None:
        derived_lengths.append(len(peak_mag))
    if peak_time is not None:
        derived_lengths.append(len(peak_time))
    if rise_time is not None:
        derived_lengths.append(len(rise_time))
    if decline_rate_15 is not None:
        derived_lengths.append(len(decline_rate_15))
    if decline_rate_40 is not None:
        derived_lengths.append(len(decline_rate_40))
    if derived_band is not None:
        derived_lengths.append(len(derived_band))
    if derived_viewing_angle is not None:
        derived_lengths.append(len(derived_viewing_angle))

    if len(set(derived_lengths)) > 1:  # 0 if empty, 1 if all the same
        raise ValueError("All derived data arrays must have the same length")

    data_dfs = []
    for i, t in enumerate(time):
        data = {
            "time": t,
            "magnitude": magnitude[i],
            "band": band[i],
            "viewing_angle": viewing_angle[i],
        }
        if e_magnitude is not None:
            data["e_magnitude"] = e_magnitude[i]
        data_dfs.append(pd.DataFrame(data))

    derived_data_dfs = []
    if len(set(derived_lengths)) == 1:
        for i in range(derived_lengths[0]):
            data = {}
            if peak_mag is not None:
                data["peak_mag"] = peak_mag[i]
            if peak_time is not None:
                data["peak_time"] = peak_time[i]
            if rise_time is not None:
                data["rise_time"] = rise_time[i]
            if decline_rate_15 is not None:
                data["decline_rate_15"] = decline_rate_15[i]
            if decline_rate_40 is not None:
                data["decline_rate_40"] = decline_rate_40[i]
            if derived_band is not None:
                data["band"] = derived_band[i]
            if derived_viewing_angle is not None:
                data["viewing_angle"] = derived_viewing_angle[i]
            derived_data_dfs.append(pd.DataFrame(data))

    write_rt_lightcurve_from_dataframe(
        data_dfs,
        path,
        derived_data=derived_data_dfs if derived_data_dfs != [] else None,
        model_names=model_names,
        sources=sources,
        units=units,
        overwrite=overwrite,
        create_path=create_path,
    )
