import json
from jsonschema import ValidationError, validate


class Hydro1D:
    def __init__(self, path) -> None:
        self.schema = {
            "type": "object",
            "properties": {
                "name": {"type": "string"},
                "schema": {"type": "string"},
            },
            "required": ["name"],
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
        except ValidationError as e:
            return False
        return True
