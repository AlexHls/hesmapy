# Description: Constants used in the project

HYDRO1D_ABUNDANCE_REGEX = r"\bx[a-zA-Z]{1,2}[0-9]{0,3}\b"
HYDRO1D_SCHEMA = "https://github.com/AlexHls/hesmapy/blob/v0.1.0/SCHEMA.md"
HYDRO1D_JSON_SCHEMA = {
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
                    HYDRO1D_ABUNDANCE_REGEX: {"type": "number"},
                },
                "required": ["radius", "density", "time"],
            },
        },
    },
    "required": ["name", "data"],
}
