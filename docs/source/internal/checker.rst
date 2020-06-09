====================
 How Checks are Run
====================

In |Flake9| 2.x, |Flake9| delegated check running to pep8. In 3.0 |Flake9|
takes on that responsibility. This has allowed for simpler
handling of the ``--jobs`` parameter (using :mod:`multiprocessing`) and
simplified our fallback if something goes awry with concurrency.
At the lowest level we have a |FileChecker|. Instances of |FileChecker| are
created for *each* file to be analyzed by |Flake9|. Each instance, has a copy
of all of the plugins registered with setuptools in the ``flake9.extension``
entry-point group.

The |FileChecker| instances are managed by an instance of |Manager|. The
|Manager| instance handles creating sub-processes with
:mod:`multiprocessing` module and falling back to running checks in serial if
an operating system level error arises. When creating |FileChecker| instances,
the |Manager| is responsible for determining if a particular file has been
excluded.


Processing Files
----------------

Unfortunately, since |Flake9| took over check running from pep8/pycodestyle,
it also had to take over parsing and processing files for the checkers
to use. Since it couldn't reuse pycodestyle's functionality (since it did not
separate cleanly the processing from check running) that function was isolated
into the :class:`~flake9.processor.FileProcessor` class. We moved
several helper functions into the :mod:`flake9.processor` module (see also
:ref:`Processor Utility Functions <processor_utility_functions>`).


API Reference
-------------

.. autoclass:: flake9.checker.FileChecker
    :members:

.. autoclass:: flake9.checker.Manager
    :members:

.. autoclass:: flake9.processor.FileProcessor
    :members:


.. _processor_utility_functions:

Utility Functions
`````````````````

.. autofunction:: flake9.processor.count_parentheses

.. autofunction:: flake9.processor.expand_indent

.. autofunction:: flake9.processor.is_eol_token

.. autofunction:: flake9.processor.is_multiline_string

.. autofunction:: flake9.processor.log_token

.. autofunction:: flake9.processor.mutate_string

.. autofunction:: flake9.processor.token_is_newline

.. Substitutions
.. |FileChecker| replace:: :class:`~flake9.checker.FileChecker`
.. |Manager| replace:: :class:`~flake9.checker.Manager`
