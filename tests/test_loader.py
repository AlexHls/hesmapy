import unittest
import os
import json
from tempfile import NamedTemporaryFile
from hesmapy.base import load_hydro_1d, Hydro1D


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


if __name__ == "__main__":
    unittest.main()
