# Utility functions for hydro data


def normalize_hydro1d_data(data: dict) -> tuple[dict, dict]:
    """
    Normalize the data to SI units

    Parameters
    ----------
    data : dict
        Hydro1D data

    Returns
    -------
    tuple(dict, dict)
        Normalized data and normalization factors
    """

    normalization_factors = {}

    if "density" in data:
        norm = data["density"].max()
        data["density"] /= norm
        normalization_factors["density"] = norm
    if "pressure" in data:
        norm = data["pressure"].max()
        data["pressure"] /= norm
        normalization_factors["pressure"] = norm
    if "temperature" in data:
        norm = data["temperature"].max()
        data["temperature"] /= norm
        normalization_factors["temperature"] = norm
    if "mass" in data:
        norm = data["mass"].max()
        data["mass"] /= norm
        normalization_factors["mass"] = norm
    if "velocity" in data:
        norm = data["velocity"].max()
        data["velocity"] /= norm
        normalization_factors["velocity"] = norm

    return data, normalization_factors
