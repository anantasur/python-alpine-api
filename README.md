Python SDK for Chorus
=====================

# Project structure

* README.md
* LICENSE
* api/
* doc/
* examples/
* tests/

# Code style guide:

Placeholder

# Documentation style guide:
Documentation will be automatically generated by Sphinx from the function comments. Please use the following example as a guide for each function. You must include a description of the function, expected type(s) of parameters, expected return types and any Exceptions that may be raised.

~~~
def fake_function(self, user_name, another_one):
    """
    Get one user's metadata

    :param str user_name: A Unique user name.
    :param another_one: A second param, used to illustrate that you can have multiple expected types.
    :type: int or str
    :return: User's id plus 1
    :rtype: int or None
    :exception UserNotFoundException: The user_name does not exist.
    """
~~~

## Creating the docs locally:

The .gitignore is setup to not track the generated documentation files. To build it locally (and open it) you can run the following commands from the doc directory:

~~~
make clean
make html
open _build/html/index.html
~~~

## Editing the documentation

The files that create the documentation are located in the doc folder. See Sphinx documentation or the examples I've created.

For example, to create and introduction page you must create a file called introduction.rst. You must also insert the name of the file into the table of contents in index.rst.

There are lots of [tutorials online](https://pythonhosted.org/an_example_pypi_project/sphinx.html#function-definitions).
