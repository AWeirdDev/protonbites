from typing import Any, Mapping, Union
from .datatypes import int8, uint8, int16, uint16, int32, uint32, int64, uint64

PythonBackendDataTypes = Union[
    Mapping[str, Any], list, str, int, float, bool, int8, uint8, int16, uint16, int32, uint32, int64, uint64
]
