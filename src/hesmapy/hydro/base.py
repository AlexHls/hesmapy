import json
from jsonschema import ValidationError, validate


class Hydro1D:
    def __init__(self, path) -> None:
        self.schema = {
            "type": "object",
            "properties": {
                "name": {"type": "string"},
                "schema": {"type": "string"},
                "sources": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "bibcode": {"type": "string"},
                            "reference": {"type": "string"},
                            "url": {"type": "string"},
                        },
                    },
                },
                "units": {
                    "type": "object",
                    "properties": {
                        "radius": {"type": "string"},
                        "density": {"type": "string"},
                        "pressure": {"type": "string"},
                        "temperature": {"type": "string"},
                        "mass": {"type": "string"},
                        "velocity": {"type": "string"},
                        "time": {"type": "string"},
                    },
                },
                "data": {
                    "type": "array",
                    "minItems": 2,
                    "items": {
                        "type": "object",
                        "properties": {
                            "radius": {"type": "number"},
                            "density": {"type": "number"},
                            "pressure": {"type": "number"},
                            "temperature": {"type": "number"},
                            "mass": {"type": "number"},
                            "velocity": {"type": "number"},
                            "time": {"type": "number"},
                            "\bx[A-Z][a-z][0-9]{0,3}\b": {"type": "number"},
                        },
                        "required": ["radius", "density"],
                    },
                },
            },
            "required": ["name", "data"],
        }

        self.path = path
        self.data = self.load_data()
        self.valid = self.validate_data()

    def load_data(self) -> dict:
        with open(self.path) as f:
            try:
                data = json.load(f)
            except json.decoder.JSONDecodeError:
                # TODO Implement propper error handling
                raise ValueError("Invalid JSON file")
        return data

    def validate_data(self) -> bool:
        if len(self.data) > 1:
            return False
        try:
            obj = list(self.data.keys())[0]
            validate(self.data[obj], schema=self.schema)
        except ValidationError:
            return False
        return True
