# Templates
Job templates allow users to programmatically define job descriptions in Python. They are ordered dictionaries and are utilised by the `job` class. Currently, available are a `base` template and `vanilla python` template.

## Example Usage - Vanilla Python
The following example shows how to define a Python job description that will run in a Vanilla HTCondor universe.

```
templates = Templates()
my_job_description = templates.vanilla_python
my_job_description['python_file'] = "python_program.py"
```

## Defining a description from scratch
Of course, it may be easier to define your job description from scratch, which can be done as follows

```
from collections import OrderedDict
description = OrderedDict()
description['universe'] = "vanilla"
description['executable'] = "my_executable"
description['...'] = "..."
```