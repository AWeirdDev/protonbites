import ast
import gzip
import struct
from typing import Any, Tuple, TypeGuard, Union

from .types import PythonBackendDataTypes
from .datatypes import (
    FLOAT32,
    FLOAT64,
    FLOATS,
    START,
    END,
    ARRAY_HEAD,
    ARRAY_NIL,
    INT8,
    UINT8,
    INT16,
    UINT16,
    INT32,
    UINT32,
    INT64,
    UINT64,
    INTS,
    TRUE,
    FALSE,
    STRING,
    SPLITTER,
    Proton,
)


def encode(obj: PythonBackendDataTypes, /, *, force_keep_str: bool = False) -> bytes:
    if isinstance(obj, dict):
        data = START
        for v in obj.values():
            data += encode(v, force_keep_str=force_keep_str) + SPLITTER
        return data + END

    elif isinstance(obj, list):
        data = ARRAY_HEAD
        for v in obj:
            data += encode(v, force_keep_str=force_keep_str) + SPLITTER

        return data + ARRAY_NIL

    elif isinstance(obj, str):
        t = f"{obj!r}".encode("utf-8")

        if not force_keep_str:
            keep_text = len(t) <= 100 + 2
        else:
            keep_text = True

        return STRING + (t if keep_text else gzip.compress(t).hex().encode("utf-8"))

    elif isinstance(obj, bool):
        return TRUE if obj else FALSE

    elif isinstance(obj, int):
        return encode_number(obj, "int64")

    elif isinstance(obj, float):
        return encode_number(obj, "float64")

    elif isinstance(obj, Proton):
        return encode_number(obj.v, obj.dt)

    else:
        raise RuntimeError(f"Unexpected type {type(obj)!r}")


def encode_number(value: Union[int, float], dtype: str) -> bytes:
    if dtype == "int8":
        d = INT8 + struct.pack("b", value).hex().encode("utf-8")

    elif dtype == "uint8":
        d = UINT8 + struct.pack("B", value).hex().encode("utf-8")

    elif dtype == "int16":
        d = INT16 + struct.pack("h", value).hex().encode("utf-8")

    elif dtype == "uint16":
        d = UINT16 + struct.pack("H", value).hex().encode("utf-8")

    elif dtype == "int32":
        d = INT32 + struct.pack("i", value).hex().encode("utf-8")

    elif dtype == "uint32":
        d = UINT32 + struct.pack("I", value).hex().encode("utf-8")

    elif dtype == "int64":
        d = INT64 + struct.pack(">q", value).hex().encode("utf-8")

    elif dtype == "uint64":
        d = UINT64 + struct.pack("<Q", value).hex().encode("utf-8")

    elif dtype == "float32":
        d = FLOAT32 + struct.pack("f", value).hex().encode("utf-8")

    elif dtype == "float64":
        d = FLOAT64 + struct.pack("d", value).hex().encode("utf-8")

    else:
        raise ValueError("Unsupported data type")

    return d


def is_number(t: Tuple[Any, ...]) -> TypeGuard[Tuple[Union[int, float]]]:
    return len(t) == 1 and (isinstance(t[0], int) or isinstance(t[0], float))


def decode_number(dtype_header: bytes, val: bytes, /):
    value = bytes.fromhex(val.decode("utf-8"))

    if dtype_header == INT8:
        return struct.unpack("b", value)

    elif dtype_header == UINT8:
        return struct.unpack("B", value)

    elif dtype_header == INT16:
        return struct.unpack("h", value)

    elif dtype_header == UINT16:
        return struct.unpack("H", value)

    elif dtype_header == INT32:
        return struct.unpack("i", value)

    elif dtype_header == UINT32:
        return struct.unpack("I", value)

    elif dtype_header == INT64:
        return struct.unpack(">q", value)

    elif dtype_header == UINT64:
        return struct.unpack("<Q", value)

    elif dtype_header == FLOAT32:
        return struct.unpack("f", value)

    elif dtype_header == FLOAT64:
        return struct.unpack("d", value)

    else:
        raise ValueError("Unsupported data type", dtype_header)


def decode(__c: bytes, /) -> PythonBackendDataTypes:
    data = [chr(i).encode("utf-8") for i in __c]

    # Onto my rust journey again...
    # Tokenizers, tokenizers, tokenizers.
    char: bytes = data[0]

    if char == START or char == ARRAY_HEAD:
        i = 1
        depths = [0 if char == START else 1]
        d = bytes()
        items = []

        while i < len(data) and len(depths) > 0:
            char = data[i]

            if char == START:
                depths.append(0)
            elif char == ARRAY_HEAD:
                depths.append(1)
            elif char == END:
                assert depths.pop() == 0
            elif char == ARRAY_NIL:
                assert depths.pop() == 1
            elif char == SPLITTER and len(depths) == 1:
                items.append(decode(d))
                i += 1
                d = bytes()
                continue

            d += char
            i += 1
        return items

    item = __c
    header = chr(item[0]).encode("utf-8")

    if header == STRING:
        if bytes(item[1:]).startswith(b"1f"):
            # gzip-compressed string
            return gzip.decompress(bytes.fromhex(item[1:].decode("utf-8"))).decode(
                "utf-8"
            )

        else:
            mod = ast.parse(bytes(item[1:]))
            body = mod.body[0]

            # Expects error
            return body.value.value  # type: ignore

    elif header in {TRUE, FALSE}:
        return True if header == TRUE else False

    elif header in INTS or header in FLOATS:
        num = decode_number(header, item[1:])
        assert is_number(num)  # type guard
        return num[0]

    else:
        dtype = chr(item[0]).encode("utf-8")
        raise NotImplementedError(
            f"Unknown dtype symbol {dtype!r}.\nRaw data: {bytes(item[1:])!r}"
        )


def decoded_safely(d: PythonBackendDataTypes) -> TypeGuard[list]:
    return isinstance(d, list)
