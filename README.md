# Python Project

Example project to test building a Python app with the following:

* Linting
* Tests
* Documentation
* Automation

See the following for information about structure Python projects:

* https://dev.to/codemouse92/dead-simple-python-project-structure-and-imports-38c6
* [Structuring Your Project](https://docs.python-guide.org/writing/structure/)
* [Python Application Layouts: A Reference](https://realpython.com/python-application-layouts/)

## Automation

Automation of linting, testing and documentation is provided by [Nox](https://nox.thea.codes/en/stable/). Configuration is managed by the file [noxfile](./noxfile.py).

To run all sessions use `nox`.

To specify a specific session use, for example, `nox --sessions lint`. To get a list of a sessions use `nox --list`.

## Documentation

Using Sphinx with autodoc

See 

https://pythonhosted.org/an_example_pypi_project/sphinx.html