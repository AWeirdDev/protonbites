import struct


class Number:
    fmt: str
    v: int

    def __init_subclass__(cls, fmt: str) -> None:
        cls.fmt = fmt

    def __init__(self, v: int):
        self.v = v

    def pack(self) -> bytes:
        return struct.pack(self.fmt, self.v)


class Int8(Number, fmt="b"): ...


class Uint8(Number, fmt="B"): ...


class Int16(Number, fmt="h"): ...


class Uint16(Number, fmt="H"): ...


class Int32(Number, fmt="i"): ...


class Uint32(Number, fmt="I"): ...


DATATYPES = {"int8", "uint8", "int16", "uint16", "int32", "uint32"}
