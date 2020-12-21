Search for code duplication in your python codebase inspecting its abstract syntax
tree.

---

This project is in a very early phase, expect bugs and/or sub-optimal behaviour.

Feedbacks, issues, pull requests are welcome!


#### Requirements
- [`astunparse`](https://github.com/simonpercivall/astunparse)

#### Usage
```
usage: pydups.py [-h] path

Search for duplicate functions looking at code's AST.

positional arguments:
  path        path of the python module to inspect

optional arguments:
  -h, --help  show this help message and exit
```

**Examples:**
```
$ python3 pydups.py tests/pyfoo
Found duplicates 💥

================================================================================

def f(x0, x1):
    x0 += 3
    x1 = (x1 + 1)
    return (x0 + x1)

tests/pyfoo/foo.py::foo
tests/pyfoo/boo/boo.py::boo

================================================================================

def f(x0, x1, x2):
    return (x1 * x2)

tests/pyfoo/foo.py::FooClass.coo
tests/pyfoo/foo.py::GooClass.doo
tests/pyfoo/boo/boo.py::HooClass.hoo

$ python3 pydups.py pydups.py 
No duplicates! ✨
```

