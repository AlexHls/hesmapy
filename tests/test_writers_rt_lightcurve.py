import unittest
import os
import json
from tempfile import NamedTemporaryFile
import pandas as pd
import numpy as np

from hesmapy.writers.rt_lightcurve import (
    write_rt_lightcurve_from_dataframe,
    write_rt_lightcurve_from_dict,
    write_rt_lightcurve_from_numpy,
)
from hesmapy.constants import RT_LIGHTCURVE_SCHEMA


class TestRTLightcurveWriter(unittest.TestCase):
    def setUp(self):
        self.data = {
            "time": [1.0, 2.0, 3.0],
            "band": ["B", "B", "B"],
            "magnitude": [1.0, 2.0, 3.0],
            "e_magnitude": [0.1, 0.2, 0.3],
            "viewing_angle": [1, 1, 1],
        }
        self.df = pd.DataFrame(self.data)
        self.derived_data = {
            "peak_mag": [1.0],
            "peak_time": [1.0],
            "rise_time": [1.0],
            "decline_rate_15": [1.0],
            "decline_rate_40": [1.0],
            "band": ["B"],
            "viewing_angle": [1],
        }
        self.derived_df = pd.DataFrame(self.derived_data)
        self.model_names = "test"
        self.sources = {
            "bibcode": "2018ApJ...853..107S",
            "reference": "Shen et al. (2018)",
            "url": "https://ui.adsabs.harvard.edu/abs/2018ApJ...853..107S/abstract",
        }
        self.units = {
            "time": "s",
            "B": "mag",
        }
        self.expected_json = {
            "test": {
                "name": "test",
                "schema": RT_LIGHTCURVE_SCHEMA,
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
        self.maxDiff = None

    def test_write_rt_lightcurve_from_dataframe(self):
        with NamedTemporaryFile(mode="w+b", delete=False) as f:
            path = f.name
            write_rt_lightcurve_from_dataframe(
                self.df,
                path,
                self.derived_df,
                self.model_names,
                self.sources,
                self.units,
                overwrite=True,
            )
        with open(path, "r") as f:
            json_data = json.load(f)
        os.unlink(path)
        self.assertEqual(json_data, self.expected_json)

    def test_write_rt_lightcurve_form_dataframe_2(self):
        df = [self.df, self.df]
        derived_df = [self.derived_df, self.derived_df]
        expected_json = {
            "test1": self.expected_json["test"].copy(),
            "test2": self.expected_json["test"].copy(),
        }
        expected_json["test1"]["name"] = "test1"
        expected_json["test2"]["name"] = "test2"
        model_names = ["test1", "test2"]
        with NamedTemporaryFile(mode="w+b", delete=False) as f:
            path = f.name
            write_rt_lightcurve_from_dataframe(
                df,
                path,
                derived_df,
                model_names,
                self.sources,
                self.units,
                overwrite=True,
            )
        with open(path, "r") as f:
            json_data = json.load(f)
        os.unlink(path)
        self.assertEqual(json_data, expected_json)

    def test_write_rt_lightcurve_from_dict(self):
        with NamedTemporaryFile(mode="w+b", delete=False) as f:
            path = f.name
            write_rt_lightcurve_from_dict(
                self.data,
                path,
                self.derived_data,
                self.model_names,
                self.sources,
                self.units,
                overwrite=True,
            )
        with open(path, "r") as f:
            json_data = json.load(f)
        os.unlink(path)
        self.assertEqual(json_data, self.expected_json)

    def test_write_rt_lightcurve_from_numpy(self):
        time = np.array(self.data["time"])
        band = np.array(self.data["band"])
        magnitude = np.array(self.data["magnitude"])
        e_magnitude = np.array(self.data["e_magnitude"])
        viewing_angle = np.array(self.data["viewing_angle"])
        peak_mag = np.array(self.derived_data["peak_mag"])
        peak_time = np.array(self.derived_data["peak_time"])
        rise_time = np.array(self.derived_data["rise_time"])
        decline_rate_15 = np.array(self.derived_data["decline_rate_15"])
        decline_rate_40 = np.array(self.derived_data["decline_rate_40"])
        derived_band = np.array(self.derived_data["band"])
        derived_viewing_angle = np.array(self.derived_data["viewing_angle"])
        with NamedTemporaryFile(mode="w+b", delete=False) as f:
            path = f.name
            write_rt_lightcurve_from_numpy(
                time,
                magnitude,
                band,
                viewing_angle,
                path,
                e_magnitude=e_magnitude,
                peak_mag=peak_mag,
                peak_time=peak_time,
                rise_time=rise_time,
                decline_rate_15=decline_rate_15,
                decline_rate_40=decline_rate_40,
                derived_band=derived_band,
                derived_viewing_angle=derived_viewing_angle,
                model_names=self.model_names,
                sources=self.sources,
                units=self.units,
                overwrite=True,
            )
        with open(path, "r") as f:
            json_data = json.load(f)
        os.unlink(path)
        self.assertEqual(json_data, self.expected_json)


if __name__ == "__main__":
    unittest.main()
