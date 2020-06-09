.. flake9 documentation master file, created by
   sphinx-quickstart on Tue Jan 19 07:14:10 2016.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

===============================================
 Flake9: Your Tool For Style Guide Enforcement
===============================================

Quickstart
==========

.. _installation-guide:

Installation
------------

To install |Flake9|, open an interactive shell and run:

.. code::

    python<version> -m pip install flake9

If you want |Flake9| to be installed for your default Python installation, you
can instead use:

.. code::

    python -m pip install flake9

.. note::

    It is **very** important to install |Flake9| on the *correct* version of
    Python for your needs. If you want |Flake9| to properly parse new language
    features in Python 3.5 (for example), you need it to be installed on 3.5
    for |Flake9| to understand those features. In many ways, Flake9 is tied to
    the version of Python on which it runs.

Using Flake9
------------

To start using |Flake9|, open an interactive shell and run:

.. code::

    flake9 path/to/code/to/check.py
    # or
    flake9 path/to/code/

.. note::

    If you have installed |Flake9| on a particular version of Python (or on
    several versions), it may be best to instead run ``python<version> -m
    flake9``.

If you only want to see the instances of a specific warning or error, you can
*select* that error like so:

.. code::

    flake9 --select E123,W503 path/to/code/

Alternatively, if you want to *ignore* only one specific warning or error:

.. code::

    flake9 --ignore E24,W504 path/to/code/

Please read our user guide for more information about how to use and configure
|Flake9|.

FAQ and Glossary
================

.. toctree::
    :maxdepth: 2

    faq
    glossary

User Guide
==========

All users of |Flake9| should read this portion of the documentation. This
provides examples and documentation around |Flake9|'s assortment of options
and how to specify them on the command-line or in configuration files.

.. toctree::
    :maxdepth: 2

    user/index
    Flake9 man page <manpage>

Plugin Developer Guide
======================

If you're maintaining a plugin for |Flake9| or creating a new one, you should
read this section of the documentation. It explains how you can write your
plugins and distribute them to others.

.. toctree::
    :maxdepth: 2

    plugin-development/index

Contributor Guide
=================

If you are reading |Flake9|'s source code for fun or looking to contribute,
you should read this portion of the documentation. This is a mix of documenting
the internal-only interfaces |Flake9| and documenting reasoning for Flake9's
design.

.. toctree::
    :maxdepth: 2

    internal/index

Release Notes and History
=========================

.. toctree::
    :maxdepth: 2

    release-notes/index

General Indices
===============

* :ref:`genindex`
* :ref:`Index of Documented Public Modules <modindex>`
* :ref:`Glossary of terms <glossary>`
