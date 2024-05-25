import pprint
from dataclasses import Field, is_dataclass
from typing import (
    Annotated,
    Any,
    ClassVar,
    Concatenate,
    Dict,
    Generic,
    Mapping,
    Protocol,
    Type,
    TypeGuard,
    TypeVar,
    Union,
    get_origin,
)
from .datatypes import DATATYPES
from .core import decode, decoded_safely, encode

SchemaMapping = Mapping[str, Union[Field, "Schema", str]]


class DataclassProtocol(Protocol):
    __dataclass_fields__: ClassVar[Dict[str, Any]]


T = TypeVar("T", bound=DataclassProtocol)


class Schema(Generic[T]):
    mapping: SchemaMapping

    def __init__(self, __dataclass: Type[T], __mapping: dict, /):
        self.mapping = __mapping
        self.dataclass = __dataclass

    def fit(self, array: list) -> T:
        """Fit the given array data to fit the mapping."""
        kwargs = {}

        for index, (k, field) in enumerate(self.mapping.items()):
            data = array[index]
            if isinstance(field, Schema):
                kwargs[k] = field.fit(data)

            elif isinstance(field, Field):
                assert data is field.type or isinstance(data, field.type)
                kwargs[k] = data

            elif field in DATATYPES:
                kwargs[k] = field

        # type guarded?
        # assert is_dataclass(self.dataclass)
        return self.dataclass(**kwargs)

    def encode(self, __dc_instance: T, /, *, force_keep_str: bool = False) -> bytes:
        """Encode the given dataclass instance to bytes."""
        return encode(__dc_instance.__dict__, force_keep_str=force_keep_str)

    def decode(self, __c: bytes) -> T:
        """Decode the given bytes to a dataclass instance."""
        d = decode(__c)
        assert decoded_safely(d)
        return self.fit(d)

    def __repr__(self):
        return "Schema(" + pprint.pformat(self.mapping) + ")"


def get_schema(__dc: Type[T]) -> Schema[T]:
    """🐣 Creates a schema from a dataclass. (type safe)

    ```python
    @dataclass
    class Person:
        name: str
        age: int

    schema = get_schema(Person)
    person = schema.fit(your_encoded_data)

    reveal_type(person)
    #           ^^^^^^
    # Type of "person" is "Person"
    # => Runtime type is 'Person'
    ```
    """
    mapping = {}

    for name, field in __dc.__dataclass_fields__.items():
        if isinstance(field, Field):
            if get_origin(field.type) is Annotated:
                t = mapping[name] = field.type.__metadata__[0]
                assert t in DATATYPES
                mapping[name] = t

            elif is_dataclass(field.type):
                mapping[name] = get_schema(field.type)

            else:
                mapping[name] = field

        else:
            raise NotImplementedError(
                f"Not implemented for {type(field)!r} (field name {name!r})"
            )

    return Schema(__dc, mapping)
