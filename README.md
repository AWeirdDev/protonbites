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

***

(c) 2024 AWeirdDev
