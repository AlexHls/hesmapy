import unittest
import pandas as pd
from hesmapy.hydro.utils import normalize_hydro1d_data, get_abundance_data


class TestHydro1D(unittest.TestCase):
    def setUp(self):
        self.valid_data = {
            "model": {
                "name": "test",
                "schema": "test_schema",
                "data": [
                    {
                        "radius": 1,
                        "density": 1,
                        "pressure": 1,
                        "temperature": 1,
                        "mass": 1,
                        "velocity": 1,
                        "time": 1,
                        "xHe4": 0.5,
                        "xC12": 0.5,
                    },
                    {
                        "radius": 2,
                        "density": 2,
                        "pressure": 2,
                        "temperature": 2,
                        "mass": 2,
                        "velocity": 2,
                        "time": 2,
                        "xHe4": 0.1,
                        "xC12": 0.9,
                    },
                ],
            },
        }
        self.valid_data_empty_abundances = {
            "model": {
                "name": "test",
                "schema": "test_schema",
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

    def test_normalize_hydro1d_data(self):
        data = pd.DataFrame(self.valid_data["model"]["data"])
        data, normalization_factors = normalize_hydro1d_data(data)
        self.assertEqual(data["density"].max(), 1)
        self.assertEqual(data["pressure"].max(), 1)
        self.assertEqual(data["temperature"].max(), 1)
        self.assertEqual(data["mass"].max(), 1)
        self.assertEqual(data["velocity"].max(), 1)
        self.assertEqual(normalization_factors["density"], 2)
        self.assertEqual(normalization_factors["pressure"], 2)
        self.assertEqual(normalization_factors["temperature"], 2)
        self.assertEqual(normalization_factors["mass"], 2)
        self.assertEqual(normalization_factors["velocity"], 2)

    def test_get_abundance_data(self):
        data = pd.DataFrame(self.valid_data["model"]["data"])
        abundances = get_abundance_data(data, 1)
        print(abundances)
        self.assertEqual(abundances["xC12"].iloc[1], 0.9)

    def test_get_abundance_data_empty(self):
        data = pd.DataFrame(self.valid_data_empty_abundances["model"]["data"])
        abundances = get_abundance_data(data, 1)
        self.assertEqual(abundances.empty, True)

    def test_get_abundance_data_no_mass(self):
        data = pd.DataFrame(self.valid_data["model"]["data"])
        data = data.drop(columns=["mass"])
        abundances = get_abundance_data(data, 1)
        self.assertEqual(abundances["xC12"].iloc[1], 0.9)


if __name__ == "__main__":
    unittest.main()
