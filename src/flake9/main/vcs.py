"""Module containing some of the logic for our VCS installation logic."""
from __future__ import print_function

import argparse
import sys

from flake9 import exceptions as exc
from flake9.main import git
from flake9.main import mercurial


# NOTE(sigmavirus24): In the future, we may allow for VCS hooks to be defined
# as plugins, e.g., adding a flake9.vcs entry-point. In that case, this
# dictionary should disappear, and this module might contain more code for
# managing those bits (in conjuntion with flake9.plugins.manager).
_INSTALLERS = {"git": git.install, "mercurial": mercurial.install}


class InstallAction(argparse.Action):
    """argparse action to run the hook installation."""

    def __call__(self, parser, namespace, value, option_string=None):
        """Perform the argparse action for installing vcs hooks."""
        installer = _INSTALLERS[value]
        errored = False
        successful = False
        try:
            successful = installer()
        except exc.HookInstallationError as hook_error:
            print(str(hook_error))
            errored = True

        if not successful:
            print("Could not find the {0} directory".format(value))

        print(
            "\nWARNING: flake9 vcs hooks integration is deprecated and "
            "scheduled for removal in 4.x.  For more information, see "
            "https://gitlab.com/pycqa/flake9/issues/568",
            file=sys.stderr,
        )

        raise SystemExit(not successful and errored)


def choices():
    """Return the list of VCS choices."""
    return list(_INSTALLERS)
