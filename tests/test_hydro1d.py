import unittest
import os
import json
from tempfile import NamedTemporaryFile
import pandas as pd
from hesmapy.hydro.base import Hydro1D


class TestHydro1D(unittest.TestCase):
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
        self.invalid_data = {"invalid": "data"}

    def test_load_data_valid(self):
        with NamedTemporaryFile(mode="w", delete=False) as f:
            json.dump(self.valid_data, f)
            path = f.name
        hydro = Hydro1D(path)
        os.unlink(path)
        self.assertEqual(hydro.data, self.valid_data)

    def test_load_data_invalid(self):
        with NamedTemporaryFile(mode="w", delete=False) as f:
            f.write("invalid json")
            path = f.name
        with self.assertRaises(IOError):
            Hydro1D(path)
        os.unlink(path)

    def test_validate_data_valid(self):
        with NamedTemporaryFile(mode="w", delete=False) as f:
            json.dump(self.valid_data, f)
            path = f.name
        hydro = Hydro1D(path)
        os.unlink(path)
        self.assertTrue(hydro.valid)

    def test_validate_data_invalid_schema(self):
        with NamedTemporaryFile(mode="w", delete=False) as f:
            json.dump(self.invalid_data, f)
            path = f.name
        hydro = Hydro1D(path)
        os.unlink(path)
        self.assertFalse(hydro.valid)

    def test_validate_data_multiple_objects(self):
        with NamedTemporaryFile(mode="w", delete=False) as f:
            json.dump([self.valid_data, self.valid_data], f)
            path = f.name
        hydro = Hydro1D(path)
        os.unlink(path)
        self.assertTrue(hydro.valid)

    def test_validate_data_invalid_multiple_objects(self):
        with NamedTemporaryFile(mode="w", delete=False) as f:
            json.dump([self.valid_data, self.invalid_data], f)
            path = f.name
        hydro = Hydro1D(path)
        os.unlink(path)
        self.assertFalse(hydro.valid)

    def test_get_model_empty(self):
        with NamedTemporaryFile(mode="w", delete=False) as f:
            json.dump([self.valid_data, self.valid_data], f)
            path = f.name
        hydro = Hydro1D(path)
        os.unlink(path)
        self.assertEqual(hydro._get_model(), list(self.valid_data.keys())[0])

    def test_get_model_string(self):
        with NamedTemporaryFile(mode="w", delete=False) as f:
            json.dump([self.valid_data, self.valid_data], f)
            path = f.name
        hydro = Hydro1D(path)
        os.unlink(path)
        self.assertEqual(hydro._get_model("model"), list(self.valid_data.keys())[0])

    def test_get_model_integer(self):
        with NamedTemporaryFile(mode="w", delete=False) as f:
            json.dump([self.valid_data, self.valid_data], f)
            path = f.name
        hydro = Hydro1D(path)
        os.unlink(path)
        self.assertEqual(hydro._get_model(0), list(self.valid_data.keys())[0])

    def test_get_model_invalid(self):
        with NamedTemporaryFile(mode="w", delete=False) as f:
            json.dump([self.valid_data, self.valid_data], f)
            path = f.name
        hydro = Hydro1D(path)
        os.unlink(path)
        with self.assertRaises(TypeError):
            hydro._get_model(1.2)

    def test_get_unique_times_valid(self):
        with NamedTemporaryFile(mode="w", delete=False) as f:
            json.dump([self.valid_data, self.valid_data], f)
            path = f.name
        hydro = Hydro1D(path)
        os.unlink(path)
        self.assertEqual(hydro.get_unique_times(), [1, 2])

    def test_get_unique_times_invalid(self):
        with NamedTemporaryFile(mode="w", delete=False) as f:
            json.dump([self.invalid_data, self.invalid_data], f)
            path = f.name
        hydro = Hydro1D(path)
        os.unlink(path)
        self.assertEqual(hydro.get_unique_times(), [])

    def test_get_data_valid(self):
        with NamedTemporaryFile(mode="w", delete=False) as f:
            json.dump([self.valid_data, self.valid_data], f)
            path = f.name
        hydro = Hydro1D(path)
        os.unlink(path)
        pd.testing.assert_frame_equal(
            hydro.get_data(),
            pd.DataFrame(self.valid_data["model"]["data"]),
        )

    def test_get_data_valid_with_time(self):
        with NamedTemporaryFile(mode="w", delete=False) as f:
            json.dump([self.valid_data, self.valid_data], f)
            path = f.name
        hydro = Hydro1D(path)
        os.unlink(path)
        ref = pd.DataFrame(self.valid_data["model"]["data"])
        ref = ref[ref["time"] == 1]
        pd.testing.assert_frame_equal(
            hydro.get_data(1),
            ref,
        )

    def test_get_data_invalid(self):
        with NamedTemporaryFile(mode="w", delete=False) as f:
            json.dump([self.invalid_data, self.invalid_data], f)
            path = f.name
        hydro = Hydro1D(path)
        os.unlink(path)
        with self.assertRaises(NotImplementedError):
            hydro.get_data()

    def test_get_units_valid(self):
        with NamedTemporaryFile(mode="w", delete=False) as f:
            json.dump(self.valid_data, f)
            path = f.name
        hydro = Hydro1D(path)
        os.unlink(path)
        self.assertEqual(
            hydro.get_units(),
            self.valid_data["model"]["units"],
        )

    def test_get_units_invalid(self):
        with NamedTemporaryFile(mode="w", delete=False) as f:
            json.dump(self.invalid_data, f)
            path = f.name
        hydro = Hydro1D(path)
        os.unlink(path)
        with self.assertRaises(NotImplementedError):
            hydro.get_units()

    def test_plot_valid(self):
        # TODO: Figure out how to test this
        # Right now this just makes sure it doesn't crash
        with NamedTemporaryFile(mode="w", delete=False) as f:
            json.dump(self.valid_data, f)
            path = f.name
        hydro = Hydro1D(path)
        os.unlink(path)
        hydro.plot()


if __name__ == "__main__":
    unittest.main()
