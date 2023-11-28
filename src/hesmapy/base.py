from hesmapy.hydro.hydro1d import Hydro1D


def load_hydro_1d(path):
    """Load a 1D hydrological model from a JSON file.

    Parameters
    ----------
    path : str
        Path to the JSON file.

    Returns
    -------
    hydro : Hydro1D
        Hydro1D object.

    """
    return Hydro1D(path)
