import unittest
import numpy as np

from hesmapy.utils.writer_utils import (
    _check_numpy_array,
    _check_model_names,
    _check_units,
)


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
        self.valid_model_names_list = ["test", "test"]
        self.invalid_model_names = "test"
        self.invalid_model_names_list = ["test", "test"]

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
        self.assertEqual(_check_units(self.valid_units), self.valid_units)

    def test_check_units_empty(self):
        self.assertEqual(_check_units(None), self.empty_units)

    def test_check_units_invalid_units(self):
        with self.assertRaises(TypeError):
            _check_units("invalid_units")

    def test_ckeck_units_incomplete_units(self):
        self.assertEqual(
            _check_units({"radius": "cm", "density": "g/cm^3"}), self.partial_units
        )


if __name__ == "__main__":
    unittest.main()
