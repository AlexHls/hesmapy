import unittest
import numpy as np
import pandas as pd

from hesmapy.utils.writer_utils import (
    _check_numpy_array,
    _check_model_names,
    _check_hydro1d_units,
    _check_sources,
    _hydro1d_dataframe_to_json_dict,
)
from hesmapy.constants import HYDRO1D_SCHEMA


class TestWriterUtilsCheckNumpyArray(unittest.TestCase):
    def setUp(self):
        self.valid_array = np.array([1, 2, 3])
        self.valid_list = [np.array([1, 2, 3]), np.array([1, 2, 3])]
        self.invalid_array = [1, 2, 3]
        self.invalid_list = [[1, 2, 3], [1, 2, 3]]

    def test_check_numpy_array_valid_array(self):
        self.assertEqual(_check_numpy_array(self.valid_array), [self.valid_array])

    def test_check_numpy_array_valid_list(self):
        self.assertEqual(_check_numpy_array(self.valid_list), self.valid_list)

    def test_check_numpy_array_invalid_array(self):
        with self.assertRaises(TypeError):
            _check_numpy_array(self.invalid_array)

    def test_check_numpy_array_invalid_list(self):
        with self.assertRaises(TypeError):
            _check_numpy_array(self.invalid_list)


class TestWriterUtilsCheckModelNames(unittest.TestCase):
    def setUp(self):
        self.valid_model_names = "test"
        self.valid_model_names_list = ["test1", "test2"]
        self.invalid_model_names = "test"
        self.invalid_model_names_list = ["test1", "test2"]
        self.dup_model_names_list = ["test1", "test1"]

    def test_check_model_names_empty(self):
        self.assertEqual(_check_model_names(None, 2), ["model_0", "model_1"])

    def test_check_model_names_valid_model_names(self):
        self.assertEqual(
            _check_model_names(self.valid_model_names, 1), [self.valid_model_names]
        )

    def test_check_model_names_invalid_model_names(self):
        with self.assertRaises(ValueError):
            _check_model_names(self.invalid_model_names, 2)

    def test_check_model_names_valid_model_names_list(self):
        self.assertEqual(
            _check_model_names(self.valid_model_names_list, 2),
            self.valid_model_names_list,
        )

    def test_check_model_names_invalid_model_names_list(self):
        with self.assertRaises(ValueError):
            _check_model_names(self.invalid_model_names_list, 3)

    def test_check_model_names_dup_model_names_list(self):
        with self.assertRaises(ValueError):
            _check_model_names(self.dup_model_names_list, 2)


class TestWriterUtilsCheckUnits(unittest.TestCase):
    def setUp(self):
        self.valid_units = {
            "radius": "cm",
            "density": "g/cm^3",
            "pressure": "g/cm^2",
            "temperature": "K",
            "mass": "g",
            "velocity": "cm/s",
            "time": "s",
        }
        self.empty_units = {
            "radius": "(arb. units)",
            "density": "(arb. units)",
            "pressure": "(arb. units)",
            "temperature": "(arb. units)",
            "mass": "(arb. units)",
            "velocity": "(arb. units)",
            "time": "(arb. units)",
        }
        self.partial_units = {
            "radius": "cm",
            "density": "g/cm^3",
            "pressure": "(arb. units)",
            "temperature": "(arb. units)",
            "mass": "(arb. units)",
            "velocity": "(arb. units)",
            "time": "(arb. units)",
        }

    def test_check_units_valid_units(self):
        self.assertEqual(_check_hydro1d_units(self.valid_units), self.valid_units)

    def test_check_units_empty(self):
        self.assertEqual(_check_hydro1d_units(None), self.empty_units)

    def test_check_units_invalid_units(self):
        with self.assertRaises(TypeError):
            _check_hydro1d_units("invalid_units")

    def test_check_units_incomplete_units(self):
        self.assertEqual(
            _check_hydro1d_units({"radius": "cm", "density": "g/cm^3"}),
            self.partial_units,
        )


class TestWriterUtilsCheckSources(unittest.TestCase):
    def setUp(self):
        self.valid_sources = {
            "bibcode": "2019ApJ...871..112S",
            "reference": "Shen et al. (2019)",
            "url": "https://ui.adsabs.harvard.edu/abs/2019ApJ...871..112S/abstract",
        }
        self.incomplete_sources = {
            "bibcode": "2019ApJ...871..112S",
            "reference": "Shen et al. (2019)",
        }
        self.invalid_sources = {
            "bibliography": "2019ApJ...871..112S",
        }

    def test_check_sources_valid_sources(self):
        self.assertEqual(_check_sources(self.valid_sources), [self.valid_sources])

    def test_check_sources_incomplete_sources(self):
        self.assertEqual(
            _check_sources(self.incomplete_sources), [self.incomplete_sources]
        )

    def test_check_sources_invalid_sources(self):
        with self.assertRaises(ValueError):
            _check_sources(self.invalid_sources)

    def test_check_sources_invalid_sources_2(self):
        with self.assertRaises(TypeError):
            _check_sources("invalid_sources")

    def test_check_sources_valid_sources_list(self):
        self.assertEqual(
            _check_sources([self.valid_sources, self.valid_sources]),
            [self.valid_sources, self.valid_sources],
        )

    def test_check_sources_invalid_sources_list(self):
        with self.assertRaises(ValueError):
            _check_sources([self.valid_sources, self.invalid_sources])

    def test_check_sources_invalid_sources_list_2(self):
        with self.assertRaises(TypeError):
            _check_sources([self.valid_sources, "invalid_sources"])


class TestWriterUtilsHydroDataFrameToJsonDict(unittest.TestCase):
    def setUp(self):
        self.df = pd.DataFrame(
            {
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
        )
        self.model = "test"
        self.sources = [
            {
                "bibcode": "2019ApJ...871..112S",
                "reference": "Shen et al. (2019)",
                "url": "https://ui.adsabs.harvard.edu/abs/2019ApJ...871..112S/abstract",
            }
        ]
        self.units = {
            "radius": "cm",
            "density": "g/cm^3",
            "pressure": "g/cm^2",
            "temperature": "K",
            "mass": "g",
            "velocity": "cm/s",
            "time": "s",
        }
        self.maxDiff = None

    def test_hydro_dataframe_to_json_dict(self):
        self.assertEqual(
            _hydro1d_dataframe_to_json_dict(
                self.df, self.model, self.sources, self.units
            ),
            {
                "test": {
                    "name": "test",
                    "schema": HYDRO1D_SCHEMA,
                    "sources": [
                        {
                            "bibcode": "2019ApJ...871..112S",
                            "reference": "Shen et al. (2019)",
                            "url": "https://ui.adsabs.harvard.edu/abs/2019ApJ...871..112S/abstract",
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
            },
        )


if __name__ == "__main__":
    unittest.main()
