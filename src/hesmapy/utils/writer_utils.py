# Purpose utilities for writing to files
import pandas as pd
import numpy as np

from hesmapy.constants import HYDRO1D_SCHEMA, HYDRO1D_ABUNDANCE_REGEX


def _hydro1d_dataframe_to_json_dict(
    df: pd.DataFrame, model: str, sources: dict | list[dict] = None, units: dict = None
) -> dict:
    """
    Convert a DataFrame containing hydrodynamical data to a dictionary
    compatible with the HESMA scheme.

    Parameters
    ----------
    df : pd.DataFrame
        DataFrame containing the hydrodynamical data.
    model : str
        Name of the model.
    sources : dict | list[dict], optional
        Source(s) of the model, by default None. If None, the source
    units : dict, optional
        Units of the model, by default None. If None, the units will
        be set to "(arb. units)".

    Returns
    -------
    dict
        Dictionary compatible with the HESMA scheme.

    """

    columns = [
        "radius",
        "density",
        "pressure",
        "temperature",
        "mass",
        "velocity",
        "time",
    ]

    # Add abundance columns
    for col in df.columns:
        if HYDRO1D_ABUNDANCE_REGEX.match(col):
            columns.append(col)

    data = []
    for _, row in df.iterrows():
        data_dict = {}
        for col in columns:
            if col in row:
                data_dict[col] = row[col]
        data.append(data_dict)

    model_dict = {}
    model_dict["name"] = model
    model_dict["schema"] = HYDRO1D_SCHEMA
    if sources is not None:
        model_dict["sources"] = sources
    model_dict["units"] = units
    model_dict["data"] = data

    return {model: model_dict}


def _check_sources(sources: dict | list[dict]) -> list[dict]:
    if sources is not None:
        if isinstance(sources, dict):
            sources = [sources]
        elif isinstance(sources, list):
            if not all(isinstance(source, dict) for source in sources):
                raise TypeError("sources must be a dict or a list of dicts")
        else:
            raise TypeError("sources must be a dict or a list of dicts")

        for source in sources:
            if not any(key in source for key in ["bibcode", "reference", "url"]):
                raise ValueError(
                    "sources must contain at least one of the following keys: "
                    "'bibcode', 'reference', 'url'"
                )

    return sources


def _check_units(units: dict) -> dict:
    columns = [
        "radius",
        "density",
        "pressure",
        "temperature",
        "mass",
        "velocity",
        "time",
    ]
    if units is not None:
        if not isinstance(units, dict):
            raise TypeError("units must be a dict")
        for col in columns:
            if col not in units.keys():
                units[col] = "(arb. units)"
    else:
        units = {}
        for col in columns:
            units[col] = "(arb. units)"

    return units


def _check_model_names(model_names: str | list[str], len_data: int) -> list[str]:
    if model_names is None:
        model_names = [f"model_{i}" for i in range(len_data)]
    elif isinstance(model_names, str):
        if len_data != 1:
            raise ValueError(
                "model_names must be a list of strings with the same length as data"
            )
        model_names = [model_names]
    elif isinstance(model_names, list):
        if not all(isinstance(name, str) for name in model_names):
            raise TypeError("model_names must be a list of strings")
        if len(model_names) != len_data:
            raise ValueError(
                "model_names must be a list of strings with the same length as data"
            )
        if len(set(model_names)) != len(model_names):
            raise ValueError("model_names must be unique")

    return model_names


def _check_numpy_array(array: np.ndarray | list[np.ndarray]) -> list[np.ndarray]:
    if isinstance(array, np.ndarray):
        array = [array]
    elif isinstance(array, list):
        if not all(isinstance(arr, np.ndarray) for arr in array):
            raise TypeError("data must be a np.ndarray or a list of np.ndarray")
    else:
        raise TypeError("data must be a np.ndarray or a list of np.ndarray")

    return array
