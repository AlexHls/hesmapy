import os
import json
import pandas as pd
import numpy as np

from hesmapy.utils.writer_utils import (
    _check_data,
    _check_sources,
    _check_hydro1d_units,
    _check_model_names,
    _check_numpy_array,
    _hydro1d_dataframe_to_json_dict,
)
from hesmapy.constants import HYDRO1D_ABUNDANCE_REGEX


# This is the base hydro1d writer. All other writers should be wrappers
# around this one.
def write_hydro1d_from_dataframe(
    data: pd.DataFrame | list[pd.DataFrame],
    path: str,
    model_names: str | list[str] = None,
    sources: dict | list[dict] = None,
    units: dict = None,
    overwrite: bool = False,
    create_path: bool = True,
) -> None:
    """
    Write a 1D Hydrodynamical model to a JSON file
    compatible with the HESMA scheme from a DataFrame.

    Parameters
    ----------
    data : pd.DataFrame | list[pd.DataFrame]
        DataFrame or list of DataFrames containing the
        hydrodynamical data.
    path : str
        Path to the JSON file.
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
    - time
    - density
    - radius
    Other columns are optional. Only columns compliant with
    the HESMA scheme will be written to the JSON file.

    """

    if os.path.exists(path) and not overwrite:
        raise IOError(f"File {path} already exists")

    data = _check_data(data, columns=["time", "density", "radius"])

    model_names = _check_model_names(model_names, len(data))
    sources = _check_sources(sources)
    units = _check_hydro1d_units(units)

    hydro = {}

    for i, df in enumerate(data):
        data_dict = _hydro1d_dataframe_to_json_dict(df, model_names[i], sources, units)
        hydro[model_names[i]] = data_dict[model_names[i]]

    if (
        create_path
        and not os.path.exists(os.path.dirname(path))
        and os.path.dirname(path) != ""
    ):
        os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as f:
        json.dump(hydro, f)


def write_hydro1d_from_dict(
    data: dict | list[dict],
    path: str,
    model_names: str | list[str] = None,
    sources: dict | list[dict] = None,
    units: dict = None,
    overwrite: bool = False,
    create_path: bool = True,
) -> None:
    """
    Write a 1D Hydrodynamical model to a JSON file
    compatible with the HESMA scheme from a dict.

    Parameters
    ----------
    data : dict | list[dict]
        dict or list of dicts containing the
        hydrodynamical data.
    path : str
        Path to the JSON file.
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
    The dict(s) must contain the following columns:
    - time
    - density
    - radius
    Other columns are optional. Only columns compliant with
    the HESMA scheme will be written to the JSON file.

    """

    if isinstance(data, dict):
        data = [data]
    elif isinstance(data, list):
        if not all(isinstance(df, dict) for df in data):
            raise TypeError("data must be a dict or a list of dicts")
    else:
        raise TypeError("data must be a dict or a list of dicts")

    data_dfs = []
    for i, df in enumerate(data):
        data_dfs.append(pd.DataFrame(df))

    write_hydro1d_from_dataframe(
        data_dfs,
        path,
        model_names=model_names,
        sources=sources,
        units=units,
        overwrite=overwrite,
        create_path=create_path,
    )


def write_hydro1d_from_numpy(
    radius: np.ndarray | list[np.ndarray],
    density: np.ndarray | list[np.ndarray],
    time: float | np.ndarray,
    path: str,
    pressure: np.ndarray | list[np.ndarray] = None,
    temperature: np.ndarray | list[np.ndarray] = None,
    mass: np.ndarray | list[np.ndarray] = None,
    velocity: np.ndarray | list[np.ndarray] = None,
    model_names: str | list[str] = None,
    sources: dict | list[dict] = None,
    units: dict = None,
    overwrite: bool = False,
    create_path: bool = True,
    **kwargs,
) -> None:
    """
    Write a 1D Hydrodynamical model to a JSON file
    compatible with the HESMA scheme from a dict.

    Parameters
    ----------
    radius : np.ndarray | list[np.ndarray]
        Radius of the model cells.
    density : np.ndarray | list[np.ndarray]
        Density of the model cells.
    time : float | np.ndarray | list[np.ndarray]
        Time of the model. If a float is given, it will be
        used for all models. If an array is given, it must
        have the same length as the number of models.
    path : str
        Path to the JSON file.
    pressure : np.ndarray | list[np.ndarray], optional
        Pressure of the model cells, by default None.
    temperature : np.ndarray | list[np.ndarray], optional
        Temperature of the model cells, by default None.
    mass : np.ndarray | list[np.ndarray], optional
        Mass of the model cells, by default None.
    velocity : np.ndarray | list[np.ndarray], optional
        Velocity of the model cells, by default None.
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
    Abundances can be added as keyword arguments. The keyword must
    match the following regular expression: r'\bx[a-zA-Z]{1,2}[0-9]{0,3}\b'.

    """

    radius = _check_numpy_array(radius)
    density = _check_numpy_array(density)
    if pressure is not None:
        pressure = _check_numpy_array(pressure)
    if temperature is not None:
        temperature = _check_numpy_array(temperature)
    if mass is not None:
        mass = _check_numpy_array(mass)
    if velocity is not None:
        velocity = _check_numpy_array(velocity)

    abundances = {}
    for arg in kwargs.keys():
        if HYDRO1D_ABUNDANCE_REGEX.match(arg):
            abundances[arg] = _check_numpy_array(kwargs[arg])

    if len(radius) != len(density):
        raise ValueError("radius and density must have the same length")
    if pressure is not None:
        if len(radius) != len(pressure):
            raise ValueError("radius and pressure must have the same length")
    if temperature is not None:
        if len(radius) != len(temperature):
            raise ValueError("radius and temperature must have the same length")
    if mass is not None:
        if len(radius) != len(mass):
            raise ValueError("radius and mass must have the same length")
    if velocity is not None:
        if len(radius) != len(velocity):
            raise ValueError("radius and velocity must have the same length")
    if len(abundances) != 0:
        for key in abundances.keys():
            if len(radius) != len(abundances[key]):
                raise ValueError(f"radius and {key} must have the same length")

    if isinstance(time, float):
        time = [time] * len(radius)
    elif isinstance(time, np.ndarray) or isinstance(time, list):
        if len(time) != len(radius):
            raise ValueError(
                "time must be a float or an array with the same length as"
                " the number of models"
            )

    data_dfs = []
    for i, df in enumerate(radius):
        data = {
            "radius": radius[i],
            "density": density[i],
            "time": time[i],
        }
        if pressure is not None:
            data["pressure"] = pressure[i]
        if temperature is not None:
            data["temperature"] = temperature[i]
        if mass is not None:
            data["mass"] = mass[i]
        if velocity is not None:
            data["velocity"] = velocity[i]
        if abundances is not None:
            for key in abundances.keys():
                data[key] = abundances[key][i]

        df = pd.DataFrame(data)
        data_dfs.append(pd.DataFrame(df))

    write_hydro1d_from_dataframe(
        data_dfs,
        path,
        model_names=model_names,
        sources=sources,
        units=units,
        overwrite=overwrite,
        create_path=create_path,
    )
