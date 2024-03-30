import unittest
import os
import json
from tempfile import NamedTemporaryFile
import pandas as pd
import numpy as np

from hesmapy.writers.rt_spectrum import (
    write_rt_spectrum_from_dataframe,
    write_rt_spectrum_from_dict,
    write_rt_spectrum_from_numpy,
)
from hesmapy.constants import RT_SPECTRUM_SCHEMA


class TestWriteRTSpectrum(unittest.TestCase):
    def setUp(self):
        self.data = [
            {
                "wavelength": [1, 2, 3],
                "flux": [1, 2, 3],
                "time": [1, 1, 1],
            },
            {
                "wavelength": [4, 5, 6],
                "flux": [4, 5, 6],
                "time": [2, 2, 2],
            },
        ]
        self.df = [pd.DataFrame(data) for data in self.data]
        self.model_names = "test"
        self.sources = {
            "bibcode": "2018ApJ...853..107S",
            "reference": "Shen et al. (2018)",
            "url": "https://ui.adsabs.harvard.edu/abs/2018ApJ...853..107S/abstract",
        }
        self.units = {
            "time": "s",
            "wavelength": "Angstrom",
            "flux": "erg/s",
            "flux_err": "erg/s",
        }
        self.expected_json = {
            "test": {
                "name": "test",
                "schema": RT_SPECTRUM_SCHEMA,
                "sources": [
                    {
                        "bibcode": "2018ApJ...853..107S",
                        "reference": "Shen et al. (2018)",
                        "url": "https://ui.adsabs.harvard.edu/abs/2018ApJ...853..107S/abstract",
                    },
                ],
                "units": {
                    "time": "s",
                    "wavelength": "Angstrom",
                    "flux": "erg/s",
                    "flux_err": "erg/s",
                },
                "data": [
                    {
                        "time": 1,
                        "wavelength": [1, 2, 3],
                        "flux": [1, 2, 3],
                    },
                    {
                        "time": 2,
                        "wavelength": [4, 5, 6],
                        "flux": [4, 5, 6],
                    },
                ],
            },
        }
        self.maxDiff = None

    def test_write_rt_spectrum_from_dataframe(self):
        with NamedTemporaryFile(mode="w+b", delete=False) as f:
            path = f.name
            write_rt_spectrum_from_dataframe(
                self.df,
                1,
                path,
                model_names=self.model_names,
                sources=self.sources,
                units=self.units,
                overwrite=True,
            )
        with open(path, "r") as f:
            data = json.load(f)
        os.unlink(path)
        self.assertEqual(data, self.expected_json)

    def test_write_rt_spectrum_from_dataframe_2(self):
        data = [self.df, self.df]
        expected_json = {
            "test1": self.expected_json["test"].copy(),
            "test2": self.expected_json["test"].copy(),
        }
        expected_json["test1"]["name"] = "test1"
        expected_json["test2"]["name"] = "test2"
        model_names = ["test1", "test2"]
        with NamedTemporaryFile(mode="w+b", delete=False) as f:
            path = f.name
            write_rt_spectrum_from_dataframe(
                data,
                2,
                path,
                model_names=model_names,
                sources=self.sources,
                units=self.units,
                overwrite=True,
            )

    def test_write_rt_spectrum_from_dict(self):
        with NamedTemporaryFile(mode="w+b", delete=False) as f:
            path = f.name
            write_rt_spectrum_from_dict(
                self.data,
                1,
                path,
                model_names=self.model_names,
                sources=self.sources,
                units=self.units,
                overwrite=True,
            )
        with open(path, "r") as f:
            data = json.load(f)
        os.unlink(path)
        self.assertEqual(data, self.expected_json)

    def test_write_rt_spectrum_from_numpy(self):
        time = [1, 2]
        wavelength = [np.array([1, 2, 3]), np.array([4, 5, 6])]
        flux = [np.array([1, 2, 3]), np.array([4, 5, 6])]
        with NamedTemporaryFile(mode="w+b", delete=False) as f:
            path = f.name
            write_rt_spectrum_from_numpy(
                time,
                wavelength,
                flux,
                path,
                model_names=self.model_names,
                sources=self.sources,
                units=self.units,
                overwrite=True,
            )
        with open(path, "r") as f:
            data = json.load(f)
        os.unlink(path)
        self.assertEqual(data, self.expected_json)
