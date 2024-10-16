# Structure for Python Project & how to run files
You can still follow the [*Cookie-cutter* project structure](https://skaftenicki.github.io/dtu_mlops/s2_organisation_and_version_control/code_structure/), you just have to run your *main.py* a little differently.

## Structure
Currently I have an *\app* directory that functions virtually the same as a *\src* directory. In here lies the *main.py* file. This has to be run from the terminal at ROOT level, with the following command: `py -m app.main`.

This way you also have to ensure that every single *Python module* (file), imports from other files as if it were called from the ROOT level. This means e.g. that all files in *\app* has to call on other files from *\app* with an import beginning like: `from app.(some-package)`.

Then *pytest* can also be run from ROOT level, simply with something like: `pytest .` or `pytest -v .`.