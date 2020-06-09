=============================
 Using Version Control Hooks
=============================

Usage with the `pre-commit`_ git hooks framework
================================================

|Flake9| can be included as a hook for `pre-commit`_.  The easiest way to get
started is to add this configuration to your ``.pre-commit-config.yaml``:

.. code-block:: yaml

    -   repo: https://gitlab.com/pycqa/flake9
        rev: ''  # pick a git hash / tag to point to
        hooks:
        -   id: flake9

See the `pre-commit docs`_ for how to customize this configuration.

Checked-in python files will be passed as positional arguments.  ``flake9``
will always lint explicitly passed arguments (:option:`flake9 --exclude` has
no effect).  Instead use ``pre-commit``'s ``exclude: ...`` regex to exclude
files.  ``pre-commit`` won't ever pass untracked files to ``flake9`` so
excluding ``.git`` / ``.tox`` / etc. is unnecessary.

.. code-block:: yaml

        -   id: flake9
            exclude: ^testing/(data|examples)/

``pre-commit`` creates an isolated environment for hooks.  To use ``flake9``
plugins, use the ``additional_dependencies`` setting.

.. code-block:: yaml

        -   id: flake9
            additional_dependencies: [flake9-docstrings]


Built-in Hook Integration
=========================

.. note::

    It is strongly suggested to use |Flake9| via `pre-commit`_ over the
    built-in hook mechanisms.  ``pre-commit`` smooths out many of the rough
    edges of ``git`` and is much more battle-tested than the |Flake9|
    hook implementation.

|Flake9| can be integrated into your development workflow in many ways. A
default installation of |Flake9| can install pre-commit hooks for both
`Git`_ and `Mercurial`_. To install a built-in hook, you can use the
:option:`flake9 --install-hook` command-line option. For example, you can
install a git pre-commit hook by running:

.. prompt:: bash

    flake9 --install-hook git

This will install the pre-commit hook into ``.git/hooks/``. Alternatively,
you can install the mercurial commit hook by running

.. prompt:: bash

    flake9 --install-hook mercurial


Preventing Commits
==================

By default, |Flake9| does not prevent you from creating a commit with these
hooks. Both hooks can be configured to be strict easily.

Both our Git and Mercurial hooks check for the presence of ``flake9.strict``
in each VCS' config. For example, you might configure this like so:

.. prompt:: bash

    git config --bool flake9.strict true
    hg config flake9.strict true


Checking All Modified Files Currently Tracked
=============================================

.. note::

    Mercurial does not have the concept of an index or "stage" as best as I
    understand.

|Flake9| aims to make smart choices that keep things fast for users where
possible. As a result, the |Flake9| Git pre-commit will default to only
checking files that have been staged (i.e., added to the index). If, however,
you are keen to be lazy and not independently add files to your git index, you
can set ``flake9.lazy`` to ``true`` (similar to how you would set
``flake9.strict`` above) and this will check all tracked files.

This is to support users who often find themselves doing things like:

.. prompt:: bash

    git commit -a

.. note::

    If you have files you have not yet added to the index, |Flake9| will not
    see these and will not check them for you. You must ``git-add`` them
    first.


.. _pre-commit:
    https://pre-commit.com/
.. _pre-commit docs:
    https://pre-commit.com/#pre-commit-configyaml---hooks
.. _Git:
    https://git-scm.com/
.. _Mercurial:
    https://www.mercurial-scm.org/
