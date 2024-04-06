import os
import json
import pandas as pd
import numpy as np

from hesmapy.utils.writer_utils import (
    _check_nested_data_dataframe,
    _check_time,
    _check_nested_data_dict,
    _check_sources,
    _check_rt_spectrum_units,
    _check_model_names,
    _check_numpy_array,
    _rt_spectrum_dataframe_to_json_dict,
)


class SpecEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        if isinstance(obj, np.floating):
            return float(obj)
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return super(SpecEncoder, self).default(obj)


# This is the base rt_spectrum writer. All other writers should be wrappers
# around this one.
def write_rt_spectrum_from_dataframe(
    data: pd.DataFrame | list[pd.DataFrame] | list[list[pd.DataFrame]],
    num_models: int,
    path: str,
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
    data : pd.DataFrame | list[pd.DataFrame] | list[list[pd.DataFrame]]
        DataFrame or list of DataFrames containing the
        spectral data and time.
    num_models : int
        Number of models to write. This is used to check
        if the number of models is consistent with the
        shape of the data and the number of model names.
    path : str
        Path to the JSON file.
    model_names : str | list[str], optional
        Name(s) of the model(s) to write, by default None. If None,
        the models will be named "model_0", "model_1", etc.
    units : dict, optional
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
    - wavelength
    - flux
    - time
    The time columns must contain the same value for all rows
    per DataFrame. This is to avoid complex and potentially
    error-prone shape checking.
    Other columns are optional. Only columns compliant with
    the HESMA scheme will be written to the JSON file.

    """

    if os.path.exists(path) and not overwrite:
        raise IOError(f"File {path} already exists")

    data = _check_nested_data_dataframe(
        data, columns=["wavelength", "flux", "time"], num_models=num_models
    )
    time = _check_time(data)

    model_names = _check_model_names(model_names, num_models)
    sources = _check_sources(sources)

    units = _check_rt_spectrum_units(units)

    rt_spectrum = {}

    for i, model in enumerate(model_names):
        data_dict = _rt_spectrum_dataframe_to_json_dict(
            data[i], time[i], model, sources=sources, units=units
        )
        rt_spectrum[model] = data_dict[model]

    if (
        create_path
        and not os.path.exists(os.path.dirname(path))
        and os.path.dirname(path) != ""
    ):
        os.makedirs(os.path.dirname(path), exist_ok=True)

    with open(path, "w") as f:
        # SpecEncoder is used to serialize numpy arrays and ints
        json.dump(rt_spectrum, f, cls=SpecEncoder)


def write_rt_spectrum_from_dict(
    data: dict | list[dict] | list[list[dict]],
    num_models: int,
    path: str,
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
    data : dict | list[dict] | list[list[dict]]
        Dictionary or list of dictionaries containing the
        lightcurve data.
    num_models : int
        Number of models to write. This is used to check
        if the number of models is consistent with the
        shape of the data and the number of model names.
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
    - wavelength
    - flux
    - time
    The time columns must contain the same value for all rows
    per dict. This is to avoid complex and potentially
    error-prone shape checking.
    Other columns are optional. Only columns compliant with
    the HESMA scheme will be written to the JSON file.

    """

    data = _check_nested_data_dict(data, num_models=num_models)

    data_dfs = []
    for i in range(num_models):
        data_dfs.append([pd.DataFrame(d) for d in data[i]])

    write_rt_spectrum_from_dataframe(
        data_dfs,
        num_models,
        path,
        model_names=model_names,
        sources=sources,
        units=units,
        overwrite=overwrite,
        create_path=create_path,
    )


def write_rt_spectrum_from_numpy(
    time: float | list[float],
    wavelength: np.ndarray | list[np.ndarray],
    flux: np.ndarray | list[np.ndarray],
    path: str,
    flux_err: np.ndarray | list[np.ndarray] = None,
    model_names: str = None,
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
    time : float | list[float]
        Time of the spectra.
    wavelength : np.ndarray | list[np.ndarray]
        Wavelength of the spectra.
    flux : np.ndarray | list[np.ndarray]
        Flux of the spectra.
    path : str
        Path to the JSON file.
    flux_err : np.ndarray | list[np.ndarray], optional
        Flux error of the spectra, by default None.
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
    The numpy arrays of the data must have the same length.
    This function only allows to write one model at a time.
    For multiple models, use the write_rt_spectrum_from_dataframe
    or write_rt_spectrum_from_dict functions.

    """

    if isinstance(model_names, list):
        if len(model_names) > 1:
            raise ValueError(
                "This function only allows to write one model at a time. "
                "For multiple models, use the write_rt_spectrum_from_dataframe "
                "or write_rt_spectrum_from_dict functions."
            )

    wavelength = _check_numpy_array(wavelength)
    flux = _check_numpy_array(flux)
    if flux_err is not None:
        flux_err = _check_numpy_array(flux_err)

    if isinstance(time, float):
        time = [time]
    elif isinstance(time, list):
        pass
    else:
        raise ValueError("Time must be a float or a list of floats")

    if len(wavelength) != len(flux):
        raise ValueError("Wavelength and flux must have the same length")

    if len(time) != len(wavelength):
        raise ValueError("Time must have the same length as the data arrays")

    if flux_err is not None:
        if len(flux_err) != len(flux):
            raise ValueError("Flux and flux_err must have the same length")

    data_dfs = []
    for i, t in enumerate(time):
        data = {
            "time": [t] * len(wavelength[i]),
            "wavelength": wavelength[i],
            "flux": flux[i],
        }
        if flux_err is not None:
            data["flux_err"] = flux_err[i]
        data_dfs.append(pd.DataFrame(data))

    write_rt_spectrum_from_dataframe(
        data_dfs,
        1,
        path,
        model_names=model_names,
        sources=sources,
        units=units,
        overwrite=overwrite,
        create_path=create_path,
    )
