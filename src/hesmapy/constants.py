# Description: Constants used in the project
import re

from hesmapy.__about__ import __version__

HYDRO1D_ABUNDANCE_REGEX = re.compile(r"\bx[a-zA-Z]{1,2}[0-9]{0,3}\b")
HYDRO1D_SCHEMA = "https://github.com/AlexHls/hesmapy/blob/v{:s}/SCHEMA.md".format(
    __version__
)
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

RT_LIGHTCURVE_JSON_SCHEMA = {
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
                "time": {"type": "string"},
            },
        },
        "data": {
            "type": "array",
            "minItems": 2,
            "items": {
                "type": "object",
                "properties": {
                    "time": {"type": "number"},
                    "magnitude": {"type": "number"},
                    "e_magnitude": {"type": "number"},
                    "band": {"type": "string"},
                    "viewing_angle": {"type": "number"},
                },
                "required": ["magnitude", "time"],
            },
        },
        "derived_data": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "peak_mag": {"type": "number"},
                    "peak_time": {"type": "number"},
                    "rise_time": {"type": "number"},
                    "decline_rate_15": {"type": "number"},
                    "decline_rate_40": {"type": "number"},
                    "band": {"type": "string"},
                    "viewing_angle": {"type": "number"},
                },
            },
        },
    },
    "required": ["name", "data"],
}
