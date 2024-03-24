from hesmapy.hydro.hydro1d import Hydro1D
from hesmapy.lightcurves.rt_lightcurve import RTLightcurve


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


def load_rt_lightcurve(path):
    """Load a radiative transfer lightcurve from a JSON file.

    Parameters
    ----------
    path : str
        Path to the JSON file.

    Returns
    -------
    rt : RTLightcurve
        RTLightcurve object.

    """
    return RTLightcurve(path)
