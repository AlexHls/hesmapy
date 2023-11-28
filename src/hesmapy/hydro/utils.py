# Utility functions for hydro data
import pandas as pd
import numpy as np


def normalize_hydro1d_data(data: pd.DataFrame) -> tuple[pd.DataFrame, dict]:
    """
    Normalize the data to SI units

    Parameters
    ----------
    data : pd.DataFrame
        Hydro1D data

    Returns
    -------
    tuple[pd.DataFrame, dict]
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


def get_abundance_data(data: pd.DataFrame, max_abundances: int) -> pd.DataFrame:
    """
    Get the abundance data for a specific time step

    Parameters
    ----------
    data : pd.DataFrame
        Data to get abundance data for
    max_abundances : int
        Maximum number of abundances to get

    Returns
    pd.DataFrame
    """
    abundances = data.filter(regex=r"\bx[A-Z][a-z][0-9]{0,3}\b")

    if abundances.empty:
        return abundances

    # Get the mass of each cell. If the mass is not present, calculate it
    # from the density and radius
    if "mass" in data.columns:
        masses = data["mass"]
    else:
        volumes = 4 / 3 * np.pi * np.diff(np.insert(data["radius"], 0, 0)) ** 3
        masses = data["density"] * volumes

    total_mass = abundances.mul(masses, axis=0).sum().sort_values(ascending=False)

    # Get the top max_abundances elements
    abundances = abundances[total_mass.head(max_abundances).index]
    return abundances
