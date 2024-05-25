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

<details>
<summary>Were you looking for Mr. Penguin?</summary>
<p>

<img src="https://github.com/AWeirdDev/protonbites/assets/90096971/26303b62-3ffe-4665-ab2b-36f331ec2f04" alt="What you're looking for is here" align="left" />
<p>I'm standing in a void. No light. No sound. And as I stand there... In front of me, a penguin manifests. He merely stands. Observing. But I. I am filled with dread. I dare think it, but not say it. Are you the embodiment of my end? His gaze, so vacant, pierces my very soul. Then, from the all-encompassing abyss itself, the noots of a hundred penguins billow out. The noots coalesce, forming bodies. But from those bodies, arise not life, but... Flames. Their joyful noots mutate into agonized screams. Suddenly, they're engulfed by the void. Yet, the most haunting realization? In their fleeting, fiery visages, I glimpse my own reflection.</p><br /><br />
</p>
</details>

***

(c) 2024 AWeirdDev
