import unittest
import os
import json
from tempfile import NamedTemporaryFile
from hesmapy.hydro.base import Hydro1D


class TestHydro1D(unittest.TestCase):
    def setUp(self):
        self.valid_data = {"model": {"name": "test", "schema": "test_schema"}}
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
        with self.assertRaises(ValueError):
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
        self.assertFalse(hydro.valid)


if __name__ == "__main__":
    unittest.main()
