import unittest
import os
import json
from tempfile import NamedTemporaryFile
import pandas as pd
from hesmapy.rt.spectra import RTSpectrum


class TestRTSpectrum(unittest.TestCase):
    def setUp(self):
        self.valid_data = {
            "model": {
                "name": "test",
                "schema": "rt_spectrum",
                "sources": [
                    {
                        "bibcode": "2018ApJ...853..107S",
                        "reference": "Shen et al. (2018)",
                        "url": "https://ui.adsabs.harvard.edu/abs/2018ApJ...853..107S/abstract",
                    }
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
            }
        }
        self.invalid_data = {"invalid": "data"}
        self.df1 = pd.DataFrame(
            {
                "wavelength": [1, 2, 3],
                "flux": [1, 2, 3],
            }
        )
        self.df2 = pd.DataFrame(
            {
                "wavelength": [4, 5, 6],
                "flux": [4, 5, 6],
            }
        )

    def test_load_data_valid(self):
        with NamedTemporaryFile(mode="w", delete=False) as f:
            json.dump(self.valid_data, f)
            path = f.name
        rt_spectrum = RTSpectrum(path)
        os.unlink(path)
        self.assertEqual(rt_spectrum.data, self.valid_data)

    def test_load_data_invalid(self):
        with NamedTemporaryFile(mode="w", delete=False) as f:
            f.write("invaldi json")
            path = f.name
        with self.assertRaises(IOError):
            RTSpectrum(path)
        os.unlink(path)

    def test_validate_data_valid(self):
        with NamedTemporaryFile(mode="w", delete=False) as f:
            json.dump(self.valid_data, f)
            path = f.name
        rt_spectrum = RTSpectrum(path)
        os.unlink(path)
        self.assertTrue(rt_spectrum.valid)

    def test_validate_data_invalid_schema(self):
        with NamedTemporaryFile(mode="w", delete=False) as f:
            json.dump(self.invalid_data, f)
            path = f.name
        rt_spectrum = RTSpectrum(path)
        os.unlink(path)
        self.assertFalse(rt_spectrum.valid)

    def test_validate_data_multiple_objects(self):
        with NamedTemporaryFile(mode="w", delete=False) as f:
            json.dump([self.valid_data, self.valid_data], f)
            path = f.name
        rt_spectrum = RTSpectrum(path)
        os.unlink(path)
        self.assertTrue(rt_spectrum.valid)

    def test_validate_data_invalid_multiple_objects(self):
        with NamedTemporaryFile(mode="w", delete=False) as f:
            json.dump([self.valid_data, self.invalid_data], f)
            path = f.name
        rt_spectrum = RTSpectrum(path)
        os.unlink(path)
        self.assertFalse(rt_spectrum.valid)

    def test_get_model_empty(self):
        with NamedTemporaryFile(mode="w", delete=False) as f:
            json.dump([self.valid_data, self.valid_data], f)
            path = f.name
        rt_spectrum = RTSpectrum(path)
        os.unlink(path)
        self.assertEqual(rt_spectrum._get_model(), list(self.valid_data.keys())[0])

    def test_get_model_string(self):
        with NamedTemporaryFile(mode="w", delete=False) as f:
            json.dump([self.valid_data, self.valid_data], f)
            path = f.name
        rt_spectrum = RTSpectrum(path)
        os.unlink(path)
        self.assertEqual(
            rt_spectrum._get_model("model"), list(self.valid_data.keys())[0]
        )

    def test_get_model_integer(self):
        with NamedTemporaryFile(mode="w", delete=False) as f:
            json.dump([self.valid_data, self.valid_data], f)
            path = f.name
        rt_spectrum = RTSpectrum(path)
        os.unlink(path)
        self.assertEqual(rt_spectrum._get_model(0), list(self.valid_data.keys())[0])

    def test_get_model_invalid(self):
        with NamedTemporaryFile(mode="w", delete=False) as f:
            json.dump([self.valid_data, self.valid_data], f)
            path = f.name
        rt_spectrum = RTSpectrum(path)
        os.unlink(path)
        with self.assertRaises(TypeError):
            rt_spectrum._get_model(1.2)

    def test_get_unique_times_valid(self):
        with NamedTemporaryFile(mode="w", delete=False) as f:
            json.dump([self.valid_data, self.valid_data], f)
            path = f.name
        rt_spectrum = RTSpectrum(path)
        os.unlink(path)
        self.assertEqual(rt_spectrum.get_unique_times(), [1, 2])

    def test_get_unique_times_invalid(self):
        with NamedTemporaryFile(mode="w", delete=False) as f:
            json.dump([self.invalid_data, self.invalid_data], f)
            path = f.name
        rt_spectrum = RTSpectrum(path)
        os.unlink(path)
        self.assertEqual(rt_spectrum.get_unique_times(), [])

    def test_get_data_valid(self):
        with NamedTemporaryFile(mode="w", delete=False) as f:
            json.dump([self.valid_data, self.valid_data], f)
            path = f.name
        rt_spectrum = RTSpectrum(path)
        os.unlink(path)
        data = rt_spectrum.get_data()
        self.assertEqual(len(data), 2)
        pd.testing.assert_frame_equal(
            data[0],
            self.df1,
        )
        pd.testing.assert_frame_equal(
            data[1],
            self.df2,
        )

    def test_get_data_valid_with_time(self):
        with NamedTemporaryFile(mode="w", delete=False) as f:
            json.dump([self.valid_data, self.valid_data], f)
            path = f.name
        rt_spectrum = RTSpectrum(path)
        os.unlink(path)
        pd.testing.assert_frame_equal(
            rt_spectrum.get_data(1),
            self.df1,
        )

    def test_get_data_invalid(self):
        with NamedTemporaryFile(mode="w", delete=False) as f:
            json.dump([self.invalid_data, self.invalid_data], f)
            path = f.name
        rt_spectrum = RTSpectrum(path)
        os.unlink(path)
        with self.assertRaises(NotImplementedError):
            rt_spectrum.get_data()

    def test_get_units_valid(self):
        with NamedTemporaryFile(mode="w", delete=False) as f:
            json.dump(self.valid_data, f)
            path = f.name
        rt_spectrum = RTSpectrum(path)
        os.unlink(path)
        self.assertEqual(
            rt_spectrum.get_units(),
            self.valid_data["model"]["units"],
        )

    def test_get_units_invalid(self):
        with NamedTemporaryFile(mode="w", delete=False) as f:
            json.dump(self.invalid_data, f)
            path = f.name
        rt_spectrum = RTSpectrum(path)
        os.unlink(path)
        with self.assertRaises(NotImplementedError):
            rt_spectrum.get_units()

    def test_plot_valid(self):
        # TODO: Figure out how to test this
        # Right now this just makes sure it doesn't crash
        with NamedTemporaryFile(mode="w", delete=False) as f:
            json.dump(self.valid_data, f)
            path = f.name
        rt_spectrum = RTSpectrum(path)
        os.unlink(path)
        rt_spectrum.plot()
