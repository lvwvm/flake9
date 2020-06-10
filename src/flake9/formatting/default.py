"""Default formatting class for Flake9."""
from typing import Optional, Set

from flake9.formatting import base

if False:  # `typing.TYPE_CHECKING` was introduced in 3.5.2
    from flake9.style_guide import Violation


class SimpleFormatter(base.BaseFormatter):
    """Simple abstraction for Default and Pylint formatter commonality.

    Sub-classes of this need to define an ``error_format`` attribute in order
    to succeed. The ``format`` method relies on that attribute and expects the
    ``error_format`` string to use the old-style formatting strings with named
    parameters:

    * code
    * text
    * path
    * row
    * col

    """

    error_format = None  # type: str

    def format(self, error):  # type: (Violation) -> Optional[str]
        """Format and write error out.

        If an output filename is specified, write formatted errors to that
        file. Otherwise, print the formatted error to standard out.
        """
        return self.error_format % {
            "code": error.code,
            "text": error.text,
            "path": error.filename,
            "row": error.line_number,
            "col": error.column_number,
        }


class Default(SimpleFormatter):
    """Default formatter for Flake9.

    This also handles backwards compatibility for people specifying a custom
    format string.
    """

    error_format = "%(path)s:%(row)d:%(col)d: %(code)s %(text)s"

    def after_init(self):  # type: () -> None
        """Check for a custom format string."""
        if self.options.format.lower() != "default":
            self.error_format = self.options.format


class Pylint(SimpleFormatter):
    """Pylint formatter for Flake9."""

    error_format = "%(path)s:%(row)d: [%(code)s] %(text)s"


class FilenameOnly(SimpleFormatter):
    """Only print filenames, e.g., flake9 -q."""

    error_format = "%(path)s"

    def after_init(self):  # type: () -> None
        """Initialize our set of filenames."""
        self.filenames_already_printed = set()  # type: Set[str]

    def show_source(self, error):  # type: (Violation) -> Optional[str]
        """Do not include the source code."""

    def format(self, error):  # type: (Violation) -> Optional[str]
        """Ensure we only print each error once."""
        if error.filename not in self.filenames_already_printed:
            self.filenames_already_printed.add(error.filename)
            return super(FilenameOnly, self).format(error)
        else:
            return None


class Nothing(base.BaseFormatter):
    """Print absolutely nothing."""

    def format(self, error):  # type: (Violation) -> Optional[str]
        """Do nothing."""

    def show_source(self, error):  # type: (Violation) -> Optional[str]
        """Do not print the source."""