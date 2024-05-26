# protonbites <kbd>🧪 EXPR1</kbd>
Most sane way to store JSON data. Simple, light, strongly-typed and secure. (Probably, overall)

**Step 1.** Create a dataclass.

```python
from dataclasses import dataclass

@dataclass
class Person:
    name: str
    age: int
```

> For floats and ints, you can use `typing.Annotated[int, '<dtype>']` where `<dtype>` is the desired datatype.
> Below are the avilable dtypes:
> 
> **ints**
> - int8 / uint8
> - int16 / uint16
> - int32 / uint32
> - int64 / uint64
> 
> **floats**
> - float32
> - float64


**Step 2.** Create a schema from the dataclass.

```python
from protonbites import get_schema

schema = get_schema(Person)
```

**Step 3.** Use the schema to encode/decode data.

```python
# Init a new dataclass
person = Person(name="Jesse Pinkman", age=28)

encoded = schema.encode(person)
decoded = schema.decode(encoded)

assert isinstance(decoded, Person)
```

## API Documentation <kbd>incomplete</kbd>

Oopsy daisy.

### <kbd>def</kbd> encode

```python
def encode(
    obj: PythonBackendDataTypes, 
    /, 
    *,
    force_keep_str: bool = False
) -> bytes
```

Encode data to a proton.

**Args**:
- obj (`PythonBackendDataTypes`): Object.
- force_keep_str (`bool`): Force keep the string? Usually, when the expected text length is more than 102 characters, we use `gzip` to compress the text data. If you wish to keep the string, set this to `True`.

**Simple Example:**
```python
encode({
    "name": "Mr. Penguin",
    "tags": ["depressed"],
    "friends": [
        {
            "name": "Fernando Miguel",
            "tags": ["dancing", "noot"]
        }
    ]
})
# => b"\x01\x0f'Mr. Penguin'\x11\x03\x0f'depressed'\x11\x04\x11\x03\x01\x0f'Fernando Miguel'\x11\x03\x0f'dancing'\x11\x0f'noot'\x11\x04\x11\x02\x11\x04\x11\x02"

encode({ "text": "what the fish " * 9_999 })
# => b'\x01\x0f1f8b0800a6ed516602ffe…bf2c1f2a24c7aad4220200\x11\x02'
```

**Example using custom ints and floats:**
```python
from protonbites import uint8, float32

encode({
    "a": uint8(10),
    "b": float32(10.98535)
})
```

<br />

### <kbd>def</kbd> decode

```python
def decode(__c: bytes, /) -> PythonBackendTypes
```

Decode the data.

**Args:**
- \_\_c: The encoded data.

**Example:**
```python
a = decode(b"\x01…\x02")
# => [ …, …, … ]

reveal_type(a)  # PythonBackendDataTypes (type_checking)

# To ensure the decoded data is the entrypoint
b = decoded_safely(a)
reveal_type(b)  # list (type_checking)
```

<br />

### <kbd>def</kbd> get_schema

```python
def get_schema(__dc: type[T], /) -> Schema[T]
```

<details>
    <summary><code>where T:</code></summary>
<p>

```haskell
where T: DataclassProtocol
```

```python
T = TypeVar('T', bound=DataclassProtocol)
# get_schema(__dc: type[T@get_schema], /) -> Schema[T@get_schema]
```

</p>
</details>

**Args:**
- \_\_dc: The dataclass.

```python
@dataclass
class Person:
    name: str
    age: int

schema = get_schema()
schema.encode(Person(name="Jesse Pinkman", age=28))
```

<br />

<details>
<summary>Were you looking for Mr. Penguin?</summary>
<p>

<img src="https://github.com/AWeirdDev/protonbites/assets/90096971/26303b62-3ffe-4665-ab2b-36f331ec2f04" alt="What you're looking for is here" align="left" />
<p>I'm standing in a void. No light. No sound. And as I stand there... In front of me, a penguin manifests. He merely stands. Observing. But I. I am filled with dread. I dare think it, but not say it. Are you the embodiment of my end? His gaze, so vacant, pierces my very soul. Then, from the all-encompassing abyss itself, the noots of a hundred penguins billow out. The noots coalesce, forming bodies. But from those bodies, arise not life, but... flames. Their joyful noots mutate into agonized screams. Suddenly, they're engulfed by the void. Yet, the most haunting realization? In their fleeting, fiery visages, I glimpse my own reflection.</p><br /><br />
</p>
</details>

***

(c) 2024 AWeirdDev
