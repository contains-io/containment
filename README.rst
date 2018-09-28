containment
===========

|PyPI| |Python Versions| |Build Status| |Coverage Status| |Code Quality|

*Automate the creation and management of development containers.*

``containment`` makes it easy to create and share reusable container images that
provide a consistent, yet familiar, development environment.

``containment`` was inspired by Python's virtualenv_ package. Like
``virtualenv``, ``containment`` separates project dependencies from packages
installed on the development machine but additionally separates your project's
operating system dependencies to guarantee that all developers are using a
consistent set of dependencies.

Unlike with traditional container-based approaches, ``containment`` creates an
additional layer to make the use of the development container more seamless.
``containment`` tries to be as invisible to the user as possible, by using the
same shell, development tools, and configuration already defined by the user.
``containment`` should never feel like it hinders or slows the development process.


Installation
------------

Currently, the easiest method is to install it using pip:

.. code-block:: bash

    $ pip3 install containment


In the future, there will be operating system packages to simplify the
installation of ``containment``.


Basic Usage
-----------

.. code-block:: bash

    $ cd path/to/project
    $ containment


.. _virtualenv: https://github.com/pypa/virtualenv


.. |Build Status| image:: https://travis-ci.org/contains-io/containment.svg?branch=master
   :target: https://travis-ci.org/contains-io/containment
.. |Coverage Status| image:: https://coveralls.io/repos/github/contains-io/containment/badge.svg?branch=master
   :target: https://coveralls.io/github/contains-io/containment?branch=master
.. |PyPI| image:: https://img.shields.io/pypi/v/containment.svg
   :target: https://pypi.python.org/pypi/containment/
.. |Python Versions| image:: https://img.shields.io/pypi/pyversions/containment.svg
   :target: https://pypi.python.org/pypi/containment/
.. |Code Quality| image:: https://api.codacy.com/project/badge/Grade/f6306cdc0276428fbbbed44386aeb1b6
   :target: https://www.codacy.com/app/contains-io/containment?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=contains-io/containment&amp;utm_campaign=Badge_Grade
