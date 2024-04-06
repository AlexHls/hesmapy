import json
from jsonschema import validate, ValidationError

from hesmapy.constants import HESMA_BASE_JSON_SCHEMA


class HesmaBaseJSONFile:
    def __init__(self, path) -> None:
        self.schema = (
            HESMA_BASE_JSON_SCHEMA if not hasattr(self, "schema") else self.schema
        )

        self.path = path
        self.data = self._load_data()

        # Naively assume that the data is valid
        self.valid = True

        self.models = []
        self.multi_model = self._multiple_models()

        self.valid = self._validate_data()

    def _multiple_models(self) -> bool:
        # This is a hacky way to deal with multiple models and individual
        # models at the same time
        if isinstance(self.data, dict):
            self.models = list(self.data.keys())
        elif isinstance(self.data, list):
            for item in self.data:
                if isinstance(item, dict):
                    self.models.append(list(item.keys())[0])
                else:
                    self.valid = False
                    break
            else:
                # Put all data in a single dict so we don't have to deal with
                # with a list of dicts
                data = {}
                for i, item in enumerate(self.data):
                    modelname = self.models[i]
                    # Avoid duplicate keys
                    if modelname in data:
                        modelname = f"{modelname}_{i}"
                    data[modelname] = item[self.models[i]]
                    self.models[i] = modelname
                self.data = data
        else:
            # This collects all the edge cases I can't think of
            self.models = []
            self.valid = False
        return len(self.models) > 1

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

        # TODO: Check if all data has the same length
        return True

    def _get_model(self, model: str | int = None) -> str:
        if model is None:
            model = self.models[0]
        elif isinstance(model, int):
            assert model < len(self.models), "Invalid model index"
            model = self.models[model]
        elif isinstance(model, str):
            assert model in self.models, "Invalid model name"
        else:
            raise TypeError("Invalid model type")
        return model
