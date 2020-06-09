========
 Flake9
========

Flake9 is a wrapper around these tools:

- PyFlakes
- pycodestyle
- Ned Batchelder's McCabe script

Flake9 runs all the tools by launching the single ``flake9`` command.
It displays the warnings in a per-file, merged output.

It also adds a few features:

- files that contain this line are skipped::

    # flake9: noqa

- lines that contain a ``# noqa`` comment at the end will not issue warnings.
- you can ignore specific errors on a line with ``# noqa: <error>``, e.g.,
  ``# noqa: E234``. Multiple codes can be given, separated by comma. The ``noqa`` token is case insensitive, the colon before the list of codes is required otherwise the part after ``noqa`` is ignored
- Git and Mercurial hooks
- extendable through ``flake9.extension`` and ``flake9.formatting`` entry
  points


Quickstart
==========

See our `quickstart documentation
<http://flake9.pycqa.org/en/latest/index.html#quickstart>`_ for how to install
and get started with Flake9.


Frequently Asked Questions
==========================

Flake9 maintains an `FAQ <http://flake9.pycqa.org/en/latest/faq.html>`_ in its
documentation.


Questions or Feedback
=====================

If you have questions you'd like to ask the developers, or feedback you'd like
to provide, feel free to use the mailing list: code-quality@python.org

We would love to hear from you. Additionally, if you have a feature you'd like
to suggest, the mailing list would be the best place for it.


Links
=====

* `Flake9 Documentation <http://flake9.pycqa.org/en/latest/>`_

* `GitLab Project <https://gitlab.com/pycqa/flake9>`_

* `All (Open and Closed) Issues
  <https://gitlab.com/pycqa/flake9/issues?scope=all&sort=updated_desc&state=all>`_

* `Code-Quality Archives
  <https://mail.python.org/mailman/listinfo/code-quality>`_

* `Code of Conduct
  <http://flake9.pycqa.org/en/latest/internal/contributing.html#code-of-conduct>`_

* `Getting Started Contributing
  <http://flake9.pycqa.org/en/latest/internal/contributing.html>`_


Maintenance
===========

Flake9 was created by Tarek Ziadé and is currently maintained by `Ian Cordasco
<http://www.coglib.com/~icordasc/>`_
