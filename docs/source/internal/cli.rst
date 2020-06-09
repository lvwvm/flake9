Command Line Interface
======================

The command line interface of |Flake9| is modeled as an application via
:class:`~flake9.main.cli.Application`. When a user runs ``flake9`` at their
command line, :func:`~flake9.main.cli.main` is run which handles
management of the application.

User input is parsed *twice* to accommodate logging and verbosity options
passed by the user as early as possible.
This is so as much logging can be produced as possible.

The default |Flake9| options are registered by
:func:`~flake9.main.options.register_default_options`. Trying to register
these options in plugins will result in errors.


API Documentation
-----------------

.. autofunction:: flake9.main.cli.main

.. autoclass:: flake9.main.application.Application
    :members:

.. autofunction:: flake9.main.options.register_default_options
