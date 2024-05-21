# protonbites
Most sane way to store JSON data. Simple, light, and secure.

Not suggested by Google because they said "Protobuf is the solution." And no, I do not believe in gRPC. I believe in Neo is The One.


## Turorial

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

**Step 2.** Save/get the schema. The JSON schema is only visible to you, this can reduce the chance of being attacked with queries or payloads.

```python
from protonbites import get_schema

# Get and save the schema
schema = get_schema(Person)
schema.save("bugatti.proton")

# Load from disk
# schema = get_schema("bugatti.proton")
```


