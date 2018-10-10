A replacement for Python virtualenv that uses a container-based environment manager that conforms to virtualenv's interface.

The Contain Project Contract:
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

I think contain has a contract with the User that says:

You give me a directory structure with source code, and meta-source code

I'll give you:

an image config (including entrypoint and runner)
an image
