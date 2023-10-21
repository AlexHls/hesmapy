import unittest
import os
import json
from tempfile import NamedTemporaryFile
from hesmapy.base import load_hydro_1d, Hydro1D


class TestLoadHydro1D(unittest.TestCase):
    def setUp(self):
        self.valid_data = {"model": {"name": "test", "schema": "test_schema"}}

    def test_load_hydro_1d(self):
        with NamedTemporaryFile(mode="w", delete=False) as f:
            json.dump(self.valid_data, f)
            path = f.name
        hydro = load_hydro_1d(path)
        os.unlink(path)
        self.assertIsInstance(hydro, Hydro1D)


if __name__ == "__main__":
    unittest.main()
