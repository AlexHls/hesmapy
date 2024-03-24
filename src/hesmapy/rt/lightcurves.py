import json
from jsonschema import ValidationError, validate

from hesmapy.constants import RT_LIGHTCURVE_JSON_SCHEMA


class RTLightcurve:
    def __init__(self, path) -> None:
        self.schema = RT_LIGHTCURVE_JSON_SCHEMA

        self.path = path
        self.data = self._load_data()

        # Naively assume that the data is valid
        self.valid = True

        self.models = []

        self.valid = self._validate_data()

    def _load_data(self) -> dict:
        with open(self.path) as f:
            try:
                data = json.load(f)
            except json.decoder.JSONDecodeError:
                raise IOError("Invalid JSON file")
        return data

    def _validate_data(self) -> bool:
        for model in self.models:
            try:
                validate(self.data[model], schema=self.schema)
            except ValidationError:
                return False

        return True
