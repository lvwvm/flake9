.. _formatting-plugins:

===========================================
 Developing a Formatting Plugin for Flake9
===========================================

|Flake9| allowed for custom formatting plugins in version
3.0.0. Let's write a plugin together:

.. code-block:: python

    from flake9.formatting import base


    class Example(base.BaseFormatter):
        """Flake9's example formatter."""

        pass

We notice, as soon as we start, that we inherit from |Flake9|'s
:class:`~flake9.formatting.base.BaseFormatter` class. If we follow the
:ref:`instructions to register a plugin <register-a-plugin>` and try to use
our example formatter, e.g., ``flake9 --format=example`` then
|Flake9| will fail because we did not implement the ``format`` method.
Let's do that next.

.. code-block:: python

    class Example(base.BaseFormatter):
        """Flake9's example formatter."""

        def format(self, error):
            return 'Example formatter: {0!r}'.format(error)

With that we're done. Obviously this isn't a very useful formatter, but it
should highlight the simplicity of creating a formatter with Flake9. If we
wanted to instead create a formatter that aggregated the results and returned
XML, JSON, or subunit we could also do that. |Flake9| interacts with the
formatter in two ways:

#. It creates the formatter and provides it the options parsed from the
   configuration files and command-line

#. It uses the instance of the formatter and calls ``handle`` with the error.

By default :meth:`flake9.formatting.base.BaseFormatter.handle` simply calls
the ``format`` method and then ``write``. Any extra handling you wish to do
for formatting purposes should override the ``handle`` method.

API Documentation
=================

.. autoclass:: flake9.formatting.base.BaseFormatter
    :members:
