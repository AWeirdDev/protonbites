import ast
import gzip
import struct

from .types import DataTypes

# Objects
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

# Booleans
TRUE = b"\x0d"
FALSE = b"\x0e"

# Strings
STRING = b"\x0f"

# Splitter
SPLITTER = b"\x11"


def encode(obj: DataTypes, /, *, force_keep_str: bool = False) -> bytes:
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
        if not force_keep_str:
            keep_text = len(obj) <= 100+2
        else:
            keep_text = True

        return STRING + (
            f"{obj!r}".encode("utf-8")
            if keep_text
            else gzip.compress(obj.encode("utf-8"))
        )

    elif isinstance(obj, int):
        return encode_number(obj, "int32")

    elif isinstance(obj, bool):
        return TRUE if obj else FALSE


def encode_number(value: int, dtype) -> bytes:
    if dtype == "int8":
        return b"\x05" + struct.pack("b", value)

    elif dtype == "uint8":
        return b"\x08" + struct.pack("B", value)

    elif dtype == "int16":
        return b"\x06" + struct.pack("h", value)

    elif dtype == "uint16":
        return b"\x09" + struct.pack("H", value)

    elif dtype == "int32":
        return b"\x07" + struct.pack("i", value)

    elif dtype == "uint32":
        return b"\x0a" + struct.pack("I", value)

    else:
        raise ValueError("Unsupported data type")


def decode(__c: bytes, /):
    if __c[0] != ord(START):
        raise NotImplementedError("Array-based PROTONs are not yet supported")

    data = [chr(i).encode("utf-8") for i in __c]

    # Onto my rust journey again...
    # Tokenizers, tokenizers, tokenizers.
    i = 0
    while i < len(__c):
        char: bytes = data[i]

        if char == START or char == ARRAY_HEAD:
            #is_array: bool = char == ARRAY_HEAD
            i += 1
            obj = []

            # 🤗 Explanation
            #
            # First, we get the next occurrence index of SPLITTER
            # => NEXT_OCCURR = data[i:].index(SPLITTER)
            #
            # We want to get the text between the already looped ones and -
            # the future ones.
            # The variable i is the current index (in other words looped contents' length)
            # => D = data[i : NEXT_OCCURR + 1]
            #
            # Then, we join the data so it becomes a complete utf-8 byte string
            # - Before joining: list[bytes]
            # - After joining:  bytes
            # => J = b''.join(D)
            #
            # Finally, split with SPLITTER to get all the elements inside of the 2d array
            # => J.split(SPLITTER)

            for item in b"".join(data[i : data[i:].index(SPLITTER) + 1]).split(
                SPLITTER
            ):
                if item[0] == ord(STRING):
                    mod = ast.parse(bytes(item[1:]))
                    print(ast.dump(mod))
                    body = mod.body[0]

                    # Expects error
                    obj.append(body.value.value)  # type: ignore


                else:
                    print("idk, but looks like", item[0])

            print(obj)

        i += 1


# gzip: \x1f
