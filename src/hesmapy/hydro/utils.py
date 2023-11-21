# Utility functions for hydro data


def normalize_hydro1d_data(data: dict) -> dict:
    """
    Normalize the data to SI units

    Parameters
    ----------
    data : dict
        Hydro1D data

    Returns
    -------
    dict
        Normalized data
    """

    if "density" in data:
        data["density"] /= data["density"].max()
    if "pressure" in data:
        data["pressure"] /= data["pressure"].max()
    if "temperature" in data:
        data["temperature"] /= data["temperature"].max()
    if "mass" in data:
        data["mass"] /= data["mass"].max()
    if "velocity" in data:
        data["velocity"] /= data["velocity"].max()

    return data
