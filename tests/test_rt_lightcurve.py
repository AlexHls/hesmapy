import unittest
import os
import json
from tempfile import NamedTemporaryFile
import pandas as pd
from hesmapy.rt.lightcurves import RTLightcurve


class TestRTLightcurve(unittest.TestCase):
    def setUp(self):
        self.valid_data = {
            "model": {
                "name": "model",
                "schema": "test_schema",
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
        self.invalid_data = {"invalid": "data"}

    def test_load_data_valid(self):
        with NamedTemporaryFile(mode="w", delete=False) as f:
            json.dump(self.valid_data, f)
            path = f.name
        rt_lightcurve = RTLightcurve(path)
        os.unlink(f.name)
        self.assertEqual(rt_lightcurve.data, self.valid_data)

    def test_load_data_invalid(self):
        with NamedTemporaryFile(mode="w", delete=False) as f:
            f.write("invalid json")
            path = f.name
        with self.assertRaises(IOError):
            RTLightcurve(path)
        os.unlink(f.name)

    def test_validate_data_valid(self):
        with NamedTemporaryFile(mode="w", delete=False) as f:
            json.dump(self.valid_data, f)
            path = f.name
        rt_lightcurve = RTLightcurve(path)
        os.unlink(f.name)
        self.assertTrue(rt_lightcurve.valid)

    def test_validate_data_invalid_schema(self):
        with NamedTemporaryFile(mode="w", delete=False) as f:
            json.dump(self.invalid_data, f)
            path = f.name
        rt_lightcurve = RTLightcurve(path)
        os.unlink(f.name)
        self.assertFalse(rt_lightcurve.valid)

    def test_validate_data_multiple_objects(self):
        with NamedTemporaryFile(mode="w", delete=False) as f:
            json.dump([self.valid_data, self.valid_data], f)
            path = f.name
        rt_lightcurve = RTLightcurve(path)
        os.unlink(f.name)
        self.assertTrue(rt_lightcurve.valid)

    def test_validate_data_invalid_multiple_objects(self):
        with NamedTemporaryFile(mode="w", delete=False) as f:
            json.dump([self.valid_data, self.invalid_data], f)
            path = f.name
        rt_lightcurve = RTLightcurve(path)
        os.unlink(f.name)
        self.assertFalse(rt_lightcurve.valid)

    def test_get_model_empty(self):
        with NamedTemporaryFile(mode="w", delete=False) as f:
            json.dump([self.valid_data, self.valid_data], f)
            path = f.name
        rt_lightcurve = RTLightcurve(path)
        os.unlink(f.name)
        self.assertEqual(rt_lightcurve._get_model(), list(self.valid_data.keys())[0])

    def test_get_model_string(self):
        with NamedTemporaryFile(mode="w", delete=False) as f:
            json.dump(self.valid_data, f)
            path = f.name
        rt_lightcurve = RTLightcurve(path)
        os.unlink(f.name)
        self.assertEqual(
            rt_lightcurve._get_model("model"), list(self.valid_data.keys())[0]
        )

    def test_get_model_integer(self):
        with NamedTemporaryFile(mode="w", delete=False) as f:
            json.dump(self.valid_data, f)
            path = f.name
        rt_lightcurve = RTLightcurve(path)
        os.unlink(f.name)
        self.assertEqual(rt_lightcurve._get_model(0), list(self.valid_data.keys())[0])

    def test_get_model_invalid(self):
        with NamedTemporaryFile(mode="w", delete=False) as f:
            json.dump([self.valid_data, self.valid_data], f)
            path = f.name
        rt_lightcurve = RTLightcurve(path)
        os.unlink(f.name)
        with self.assertRaises(TypeError):
            rt_lightcurve._get_model(1.2)

    def test_get_unique_viewing_angles_valid(self):
        with NamedTemporaryFile(mode="w", delete=False) as f:
            json.dump(self.valid_data, f)
            path = f.name
        rt_lightcurve = RTLightcurve(path)
        os.unlink(f.name)
        self.assertEqual(rt_lightcurve.get_unique_viewing_angles(), [1])

    def test_get_unique_viewing_angles_invalid(self):
        with NamedTemporaryFile(mode="w", delete=False) as f:
            json.dump([self.invalid_data, self.invalid_data], f)
            path = f.name
        rt_lightcurve = RTLightcurve(path)
        os.unlink(f.name)
        self.assertEqual(rt_lightcurve.get_unique_viewing_angles(), [])

    def test_get_unique_bands_valid(self):
        with NamedTemporaryFile(mode="w", delete=False) as f:
            json.dump(self.valid_data, f)
            path = f.name
        rt_lightcurve = RTLightcurve(path)
        os.unlink(f.name)
        self.assertEqual(rt_lightcurve.get_unique_bands(), ["B"])

    def test_get_unique_bands_invalid(self):
        with NamedTemporaryFile(mode="w", delete=False) as f:
            json.dump([self.invalid_data, self.invalid_data], f)
            path = f.name
        rt_lightcurve = RTLightcurve(path)
        os.unlink(f.name)
        self.assertEqual(rt_lightcurve.get_unique_bands(), [])

    def test_get_data_valid(self):
        with NamedTemporaryFile(mode="w", delete=False) as f:
            json.dump(self.valid_data, f)
            path = f.name
        rt_lightcurve = RTLightcurve(path)
        os.unlink(f.name)
        pd.testing.assert_frame_equal(
            rt_lightcurve.get_data(),
            pd.DataFrame(self.valid_data["model"]["data"]),
        )

    def test_get_data_valid_with_viewing_angle(self):
        with NamedTemporaryFile(mode="w", delete=False) as f:
            json.dump(self.valid_data, f)
            path = f.name
        rt_lightcurve = RTLightcurve(path)
        os.unlink(f.name)
        ref = pd.DataFrame(self.valid_data["model"]["data"])
        ref = ref[ref["viewing_angle"] == 1]
        pd.testing.assert_frame_equal(
            rt_lightcurve.get_data(viewing_angle=1),
            ref,
        )

    def test_get_data_invalid(self):
        with NamedTemporaryFile(mode="w", delete=False) as f:
            json.dump([self.invalid_data, self.invalid_data], f)
            path = f.name
        rt_lightcurve = RTLightcurve(path)
        os.unlink(f.name)
        with self.assertRaises(NotImplementedError):
            rt_lightcurve.get_data()

    def test_get_derived_data_valid(self):
        with NamedTemporaryFile(mode="w", delete=False) as f:
            json.dump(self.valid_data, f)
            path = f.name
        rt_lightcurve = RTLightcurve(path)
        os.unlink(f.name)
        pd.testing.assert_frame_equal(
            rt_lightcurve.get_derived_data(),
            pd.DataFrame(self.valid_data["model"]["derived_data"]),
        )

    def test_get_derived_data_valid_with_viewing_angle(self):
        with NamedTemporaryFile(mode="w", delete=False) as f:
            json.dump(self.valid_data, f)
            path = f.name
        rt_lightcurve = RTLightcurve(path)
        os.unlink(f.name)
        ref = pd.DataFrame(self.valid_data["model"]["derived_data"])
        ref = ref[ref["viewing_angle"] == 1]
        pd.testing.assert_frame_equal(
            rt_lightcurve.get_derived_data(viewing_angle=1),
            ref,
        )

    def test_get_derived_data_invalid(self):
        with NamedTemporaryFile(mode="w", delete=False) as f:
            json.dump([self.invalid_data, self.invalid_data], f)
            path = f.name
        rt_lightcurve = RTLightcurve(path)
        os.unlink(f.name)
        with self.assertRaises(NotImplementedError):
            rt_lightcurve.get_derived_data()

    def test_get_units_valid(self):
        with NamedTemporaryFile(mode="w", delete=False) as f:
            json.dump(self.valid_data, f)
            path = f.name
        rt_lightcurve = RTLightcurve(path)
        os.unlink(f.name)
        self.assertEqual(
            rt_lightcurve.get_units(),
            self.valid_data["model"]["units"],
        )

    def test_get_units_invalid(self):
        with NamedTemporaryFile(mode="w", delete=False) as f:
            json.dump(self.invalid_data, f)
            path = f.name
        rt_lightcurve = RTLightcurve(path)
        os.unlink(f.name)
        with self.assertRaises(NotImplementedError):
            rt_lightcurve.get_units()

    def test_plot_valid(self):
        # TODO: Figure out how to test this
        # Right now this just makes sure it doesn't crash
        with NamedTemporaryFile(mode="w", delete=False) as f:
            json.dump(self.valid_data, f)
            path = f.name
        rt_lightcurve = RTLightcurve(path)
        os.unlink(f.name)
        rt_lightcurve.plot()


if __name__ == "__main__":
    unittest.main()
