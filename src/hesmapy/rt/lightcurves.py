import json
from jsonschema import ValidationError, validate

from hesmapy.json_base import HesmaBaseJSONFile
from hesmapy.constants import RT_LIGHTCURVE_JSON_SCHEMA


class RTLightcurve(HesmaBaseJSONFile):
    def __init__(self, path) -> None:
        self.schema = RT_LIGHTCURVE_JSON_SCHEMA
        super().__init__(path)
