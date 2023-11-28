import os
import json
import pandas as pd

from hemsmapy.utils.writer_utils import (
    _check_sources,
    _check_units,
    _check_model_names,
    _hydro1d_dataframe_to_json_dict,
)


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
    compatible with the HESMA scheme.

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

    if isinstance(data, pd.DataFrame):
        data = [data]
    elif isinstance(data, list):
        if not all(isinstance(df, pd.DataFrame) for df in data):
            raise TypeError("data must be a DataFrame or a list of DataFrames")
    else:
        raise TypeError("data must be a DataFrame or a list of DataFrames")

    for i, df in enumerate(data):
        if not all(col in df.columns for col in ["time", "density", "radius"]):
            raise ValueError(f"DataFrame {i} does not contain the necessary columns")

    model_names = _check_model_names(model_names, len(data))
    sources = _check_sources(sources)
    units = _check_units(units)

    hydro = {}

    for i, df in enumerate(data):
        data_dict = _hydro1d_dataframe_to_json_dict(df, model_names[i], sources, units)
        hydro[model_names[i]] = data_dict[model_names[i]]

    if create_path:
        os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as f:
        json.dump(hydro, f)
