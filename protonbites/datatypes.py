# Objects
from typing import Generic, TypeVar, Union


START = b"\x01"
END = b"\x02"

# List
ARRAY_HEAD = b"\x03"
ARRAY_NIL = b"\x04"

# Raw data
INT8 = b"\x05"
UINT8 = b"\x08"
INT16 = b"\x06"
UINT16 = b"\x09"
INT32 = b"\x07"
UINT32 = b"\x0a"
INT64 = b"\x0b"
UINT64 = b"\x0c"

FLOAT32 = b"\x0e"
FLOAT64 = b"\x1e"

INTS = {INT8, UINT8, INT16, UINT16, INT32, UINT32, INT64, UINT64}
FLOATS = {FLOAT32, FLOAT64}

# Booleans
TRUE = b"\x1b"
FALSE = b"\x1c"

# Strings
STRING = b"\x0f"

# Splitter
SPLITTER = b"\x11"

DATATYPES = {
    "int8",
    "uint8",
    "int16",
    "uint16",
    "int32",
    "uint32",
    "int64",
    "uint64",
    "float32",
    "float64",
}

T = TypeVar("T", bound=Union[int, float])


class Proton(Generic[T]):
    dt: str
    v: T

    def __init_subclass__(cls, dt: str) -> None:
        assert dt in DATATYPES
        cls.dt = dt

    def __init__(self, v: T):
        self.v = v


class int8(Proton[int], dt="int8"): ...


class uint8(Proton[int], dt="uint8"): ...


class int16(Proton[int], dt="int16"): ...


class uint16(Proton[int], dt="uint16"): ...


class int32(Proton[int], dt="int32"): ...


class uint32(Proton[int], dt="uint32"): ...


class int64(Proton[int], dt="int64"): ...


class uint64(Proton[int], dt="uint64"): ...


class float32(Proton[float], dt="float32"): ...


class float64(Proton[float], dt="float64"): ...
