import unittest
import os
import json
from tempfile import NamedTemporaryFile
from hesmapy.base import (
    load_hydro_1d,
    Hydro1D,
    load_rt_lightcurve,
    RTLightcurve,
    load_rt_spectrum,
    RTSpectrum,
)


class TestLoadHydro1D(unittest.TestCase):
    def setUp(self):
        self.valid_data = {
            "model": {
                "name": "test",
                "schema": "test_schema",
                "sources": [
                    {
                        "bibcode": "test",
                        "reference": "test",
                        "url": "test",
                    }
                ],
                "units": {
                    "radius": "test",
                    "density": "test",
                    "pressure": "test",
                    "temperature": "test",
                    "mass": "test",
                    "velocity": "test",
                    "time": "test",
                },
                "data": [
                    {
                        "radius": 1,
                        "density": 1,
                        "pressure": 1,
                        "temperature": 1,
                        "mass": 1,
                        "velocity": 1,
                        "time": 1,
                    },
                    {
                        "radius": 2,
                        "density": 2,
                        "pressure": 2,
                        "temperature": 2,
                        "mass": 2,
                        "velocity": 2,
                        "time": 2,
                    },
                ],
            },
        }

    def test_load_hydro_1d(self):
        with NamedTemporaryFile(mode="w", delete=False) as f:
            json.dump(self.valid_data, f)
            path = f.name
        hydro = load_hydro_1d(path)
        os.unlink(path)
        self.assertIsInstance(hydro, Hydro1D)


class TestLoadRTLightcurve(unittest.TestCase):
    def setUp(self):
        self.valid_data = {
            "test": {
                "name": "test",
                "schema": "test_schema",
                "sources": [
                    {
                        "bibcode": "2018ApJ...853..107S",
                        "reference": "Shen et al. (2018)",
                        "url": "https://ui.adsabs.harvard.edu/abs/2018ApJ...853..107S/abstract",
                    }
                ],
                "units": {
                    "time": "s",
                    "B": "mag",
                },
                "data": [
                    {
                        "time": 1.0,
                        "band": "B",
                        "magnitude": 1.0,
                        "e_magnitude": 0.1,
                        "viewing_angle": 1,
                    },
                    {
                        "time": 2.0,
                        "band": "B",
                        "magnitude": 2.0,
                        "e_magnitude": 0.2,
                        "viewing_angle": 1,
                    },
                    {
                        "time": 3.0,
                        "band": "B",
                        "magnitude": 3.0,
                        "e_magnitude": 0.3,
                        "viewing_angle": 1,
                    },
                ],
                "derived_data": [
                    {
                        "peak_mag": 1.0,
                        "peak_time": 1.0,
                        "rise_time": 1.0,
                        "decline_rate_15": 1.0,
                        "decline_rate_40": 1.0,
                        "band": "B",
                        "viewing_angle": 1,
                    }
                ],
            }
        }

    def test_load_rt_lightcurve(self):
        with NamedTemporaryFile(mode="w", delete=False) as f:
            json.dump(self.valid_data, f)
            path = f.name
        rt = load_rt_lightcurve(path)
        os.unlink(path)
        self.assertIsInstance(rt, RTLightcurve)


class TestLoadRTSpectrum(unittest.TestCase):
    def setUp(self):
        self.valid_data = {
            "model": {
                "name": "test",
                "schema": "test_schema",
                "sources": [
                    {
                        "bibcode": "2018ApJ...853..107S",
                        "reference": "Shen et al. (2018)",
                        "url": "https://ui.adsabs.harvard.edu/abs/2018ApJ...853..107S/abstract",
                    }
                ],
                "units": {
                    "time": "test",
                    "wavelength": "test",
                    "flux": "test",
                    "flux_err": "test",
                },
                "data": [
                    {
                        "time": 1,
                        "wavelength": [1, 2],
                        "flux": [1, 2],
                        "flux_err": [1, 2],
                    },
                    {
                        "time": 2,
                        "wavelength": [1, 2],
                        "flux": [1, 2],
                        "flux_err": [1, 2],
                    },
                ],
            },
        }

    def test_load_rt_spectrum(self):
        with NamedTemporaryFile(mode="w", delete=False) as f:
            json.dump(self.valid_data, f)
            path = f.name
        rt = load_rt_spectrum(path)
        os.unlink(path)
        self.assertIsInstance(rt, RTSpectrum)


if __name__ == "__main__":
    unittest.main()
