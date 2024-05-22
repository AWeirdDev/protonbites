# protonbites
Most sane way to store JSON data. Simple, light, and secure. Rust as backend.

Not suggested by Google because they said "Protobuf is the solution." And no, I do not believe in gRPC. I believe in Neo is The One.


## Turorial

Follow this 5-step tutorial.

**Step 1.** Create a dataclass.

```python
from dataclasses import dataclass

@dataclass
class Person:
    name: str
    age: int
    has_bugatti: bool
```

> [!TIP]
> Add `typing.Annotated[int, 'u16']` to the type if you wish to use unsigned int 16.

**Step 2.** Save/load the schema. The JSON schema is only visible to you, this can reduce the chance of being attacked with queries or payloads.

```python
from protonbites import get_schema

# Get and save the schema
schema = get_schema(Person)
schema.save("bugatti.proton")

# ...or load from disk
schema = get_schema("bugatti.proton")
```

**Step 3.** Encode your data. Encoding is done easier with Protonbites. Plus, at minimum!

```python
# Define a person (data)
data = {
    "name": "Jesse Pinkman",
    "age": 24,
    "has_bugatti": False
}

# Encode the data
encoded = schema.encode(data)

print(encoded)
# => b'\x01 (…) \x02'
```

**Step 4.** Decode your data. Decoding is also at high speeds!

```python
decoded = schema.decode(encoded)

print(decoded)
# => { "name": "Jesse Pinkman", … }
```

**Step 5.** Use from anywhere. Protonbites will be available for both Python and Javascript. Potential **WASM** (WebAssembly) usage will be considered.

