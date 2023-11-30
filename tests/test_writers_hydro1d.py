import unittest
import os
import json
from tempfile import NamedTemporaryFile
import pandas as pd
import numpy as np

from hesmapy.writers.hydro1d import (
    write_hydro1d_from_dataframe,
    write_hydro1d_from_dict,
    write_hydro1d_from_numpy,
)
from hesmapy.constants import HYDRO1D_SCHEMA


class TestHydro1DWriter(unittest.TestCase):
    def setUp(self):
        self.data = {
            "radius": [1.0, 2.0, 3.0],
            "density": [1.0, 2.0, 3.0],
            "pressure": [1.0, 2.0, 3.0],
            "temperature": [1.0, 2.0, 3.0],
            "mass": [1.0, 2.0, 3.0],
            "velocity": [1.0, 2.0, 3.0],
            "time": [1.0, 1.0, 1.0],
            "xHe": [0.1, 0.2, 0.3],
            "xNi56": [0.1, 0.2, 0.3],
        }
        self.model_names = "test"
        self.sources = {
            "bibcode": "2018ApJ...853..107S",
            "reference": "Shen et al. (2018)",
            "url": "https://ui.adsabs.harvard.edu/abs/2018ApJ...853..107S/abstract",
        }
        self.units = {
            "radius": "cm",
            "density": "g/cm^3",
            "pressure": "g/cm^2",
            "temperature": "K",
            "mass": "g",
            "velocity": "cm/s",
            "time": "s",
        }
        self.expected_json = {
            "test": {
                "name": "test",
                "schema": HYDRO1D_SCHEMA,
                "sources": [
                    {
                        "bibcode": "2018ApJ...853..107S",
                        "reference": "Shen et al. (2018)",
                        "url": "https://ui.adsabs.harvard.edu/abs/2018ApJ...853..107S/abstract",
                    }
                ],
                "units": {
                    "radius": "cm",
                    "density": "g/cm^3",
                    "pressure": "g/cm^2",
                    "temperature": "K",
                    "mass": "g",
                    "velocity": "cm/s",
                    "time": "s",
                },
                "data": [
                    {
                        "radius": 1.0,
                        "density": 1.0,
                        "pressure": 1.0,
                        "temperature": 1.0,
                        "mass": 1.0,
                        "velocity": 1.0,
                        "time": 1.0,
                        "xHe": 0.1,
                        "xNi56": 0.1,
                    },
                    {
                        "radius": 2.0,
                        "density": 2.0,
                        "pressure": 2.0,
                        "temperature": 2.0,
                        "mass": 2.0,
                        "velocity": 2.0,
                        "time": 1.0,
                        "xHe": 0.2,
                        "xNi56": 0.2,
                    },
                    {
                        "radius": 3.0,
                        "density": 3.0,
                        "pressure": 3.0,
                        "temperature": 3.0,
                        "mass": 3.0,
                        "velocity": 3.0,
                        "time": 1.0,
                        "xHe": 0.3,
                        "xNi56": 0.3,
                    },
                ],
            }
        }
        self.maxDiff = None

    def test_write_hydro1d_from_dataframe(self):
        df = pd.DataFrame(self.data)
        with NamedTemporaryFile(mode="w+b", delete=False) as f:
            path = f.name
            write_hydro1d_from_dataframe(
                df, path, self.model_names, self.sources, self.units, overwrite=True
            )
        with open(path, "r") as f:
            json_data = json.load(f)
        os.unlink(path)
        self.assertEqual(json_data, self.expected_json)

    def test_write_hydro1d_form_dataframe_2(self):
        df_single = pd.DataFrame(self.data)
        df = [df_single, df_single]
        expected_json = {
            "test1": self.expected_json["test"].copy(),
            "test2": self.expected_json["test"].copy(),
        }
        expected_json["test1"]["name"] = "test1"
        expected_json["test2"]["name"] = "test2"
        model_names = ["test1", "test2"]
        with NamedTemporaryFile(mode="w+b", delete=False) as f:
            path = f.name
            write_hydro1d_from_dataframe(
                df, path, model_names, self.sources, self.units, overwrite=True
            )
        with open(path, "r") as f:
            json_data = json.load(f)
        os.unlink(path)
        self.assertEqual(json_data, expected_json)

    def test_write_hydro1d_from_dict(self):
        with NamedTemporaryFile(mode="w+b", delete=False) as f:
            path = f.name
            write_hydro1d_from_dict(
                self.data,
                path,
                self.model_names,
                self.sources,
                self.units,
                overwrite=True,
            )
        with open(path, "r") as f:
            json_data = json.load(f)
        os.unlink(path)
        self.assertEqual(json_data, self.expected_json)

    def test_write_hydro1d_from_numpy(self):
        radius = np.array(self.data["radius"])
        density = np.array(self.data["density"])
        pressure = np.array(self.data["pressure"])
        temperature = np.array(self.data["temperature"])
        mass = np.array(self.data["mass"])
        velocity = np.array(self.data["velocity"])
        time = np.unique(np.array(self.data["time"]))
        xHe = np.array(self.data["xHe"])
        xNi56 = np.array(self.data["xNi56"])
        with NamedTemporaryFile(mode="w+b", delete=False) as f:
            path = f.name
            write_hydro1d_from_numpy(
                radius,
                density,
                time,
                path,
                pressure=pressure,
                temperature=temperature,
                mass=mass,
                velocity=velocity,
                model_names=self.model_names,
                sources=self.sources,
                units=self.units,
                overwrite=True,
                xHe=xHe,
                xNi56=xNi56,
            )
        with open(path, "r") as f:
            json_data = json.load(f)
        os.unlink(path)
        self.assertEqual(json_data, self.expected_json)


if __name__ == "__main__":
    unittest.main()
