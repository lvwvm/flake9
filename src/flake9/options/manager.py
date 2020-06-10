"""Option handling and Option management logic."""
import argparse
import collections
import contextlib
import enum
import functools
import logging
from typing import Any, Callable, cast, Dict, Generator, List, Mapping
from typing import Optional, Sequence, Set, Tuple, Union

from flake9 import utils

if False:  # TYPE_CHECKING
    from typing import NoReturn
    from typing import Type

LOG = logging.getLogger(__name__)

# represent a singleton of "not passed arguments".
# an enum is chosen to trick mypy
_ARG = enum.Enum("_ARG", "NO")


_optparse_callable_map = {
    "int": int,
    "long": int,
    "string": str,
    "float": float,
    "complex": complex,
    "choice": _ARG.NO,
    # optparse allows this but does not document it
    "str": str,
}  # type: Dict[str, Union[Type[Any], _ARG]]


class _CallbackAction(argparse.Action):
    """Shim for optparse-style callback actions."""

    def __init__(self, *args, **kwargs):
        # type: (*Any, **Any) -> None
        self._callback = kwargs.pop("callback")
        self._callback_args = kwargs.pop("callback_args", ())
        self._callback_kwargs = kwargs.pop("callback_kwargs", {})
        super(_CallbackAction, self).__init__(*args, **kwargs)

    def __call__(
        self,
        parser,  # type: argparse.ArgumentParser
        namespace,  # type: argparse.Namespace
        values,  # type: Optional[Union[Sequence[str], str]]
        option_string=None,  # type: Optional[str]
    ):
        # type: (...) -> None
        if not values:
            values = None
        elif isinstance(values, list) and len(values) > 1:
            values = tuple(values)
        self._callback(
            self,
            option_string,
            values,
            parser,
            *self._callback_args,
            **self._callback_kwargs
        )


def _flake9_normalize(value, *args, **kwargs):
    # type: (str, *str, **bool) -> Union[str, List[str]]
    comma_separated_list = kwargs.pop("comma_separated_list", False)
    normalize_paths = kwargs.pop("normalize_paths", False)
    if kwargs:
        raise TypeError("Unexpected keyword args: {}".format(kwargs))

    ret = value  # type: Union[str, List[str]]
    if comma_separated_list and isinstance(ret, utils.string_types):
        ret = utils.parse_comma_separated_list(value)

    if normalize_paths:
        if isinstance(ret, utils.string_types):
            ret = utils.normalize_path(ret, *args)
        else:
            ret = utils.normalize_paths(ret, *args)

    return ret


class Option(object):
    """Our wrapper around an argparse argument parsers to add features."""

    def __init__(
        self,
        short_option_name=_ARG.NO,  # type: Union[str, _ARG]
        long_option_name=_ARG.NO,  # type: Union[str, _ARG]
        # Options below here are taken from the optparse.Option class
        action=_ARG.NO,  # type: Union[str, Type[argparse.Action], _ARG]
        default=_ARG.NO,  # type: Union[Any, _ARG]
        type=_ARG.NO,  # type: Union[str, Callable[..., Any], _ARG]
        dest=_ARG.NO,  # type: Union[str, _ARG]
        nargs=_ARG.NO,  # type: Union[int, str, _ARG]
        const=_ARG.NO,  # type: Union[Any, _ARG]
        choices=_ARG.NO,  # type: Union[Sequence[Any], _ARG]
        help=_ARG.NO,  # type: Union[str, _ARG]
        metavar=_ARG.NO,  # type: Union[str, _ARG]
        # deprecated optparse-only options
        callback=_ARG.NO,  # type: Union[Callable[..., Any], _ARG]
        callback_args=_ARG.NO,  # type: Union[Sequence[Any], _ARG]
        callback_kwargs=_ARG.NO,  # type: Union[Mapping[str, Any], _ARG]
        # Options below are taken from argparse.ArgumentParser.add_argument
        required=_ARG.NO,  # type: Union[bool, _ARG]
        # Options below here are specific to Flake9
        parse_from_config=False,  # type: bool
        comma_separated_list=False,  # type: bool
        normalize_paths=False,  # type: bool
    ):  # type: (...) -> None
        """Initialize an Option instance.

        The following are all passed directly through to argparse.

        :param str short_option_name:
            The short name of the option (e.g., ``-x``). This will be the
            first argument passed to ``ArgumentParser.add_argument``
        :param str long_option_name:
            The long name of the option (e.g., ``--xtra-long-option``). This
            will be the second argument passed to
            ``ArgumentParser.add_argument``
        :param default:
            Default value of the option.
        :param dest:
            Attribute name to store parsed option value as.
        :param nargs:
            Number of arguments to parse for this option.
        :param const:
            Constant value to store on a common destination. Usually used in
            conjuntion with ``action="store_const"``.
        :param iterable choices:
            Possible values for the option.
        :param str help:
            Help text displayed in the usage information.
        :param str metavar:
            Name to use instead of the long option name for help text.
        :param bool required:
            Whether this option is required or not.

        The following options may be passed directly through to :mod:`argparse`
        but may need some massaging.

        :param type:
            A callable to normalize the type (as is the case in
            :mod:`argparse`).  Deprecated: you can also pass through type
            strings such as ``'int'`` which are handled by :mod:`optparse`.
        :param str action:
            Any action allowed by :mod:`argparse`.  Deprecated: this also
            understands the ``action='callback'`` action from :mod:`optparse`.
        :param callable callback:
            Callback used if the action is ``"callback"``.  Deprecated: please
            use ``action=`` instead.
        :param iterable callback_args:
            Additional positional arguments to the callback callable.
            Deprecated: please use ``action=`` instead (probably with
            ``functools.partial``).
        :param dictionary callback_kwargs:
            Keyword arguments to the callback callable. Deprecated: please
            use ``action=`` instead (probably with ``functools.partial``).

        The following parameters are for Flake9's option handling alone.

        :param bool parse_from_config:
            Whether or not this option should be parsed out of config files.
        :param bool comma_separated_list:
            Whether the option is a comma separated list when parsing from a
            config file.
        :param bool normalize_paths:
            Whether the option is expecting a path or list of paths and should
            attempt to normalize the paths to absolute paths.
        """
        if (
            long_option_name is _ARG.NO
            and short_option_name is not _ARG.NO
            and short_option_name.startswith("--")
        ):
            short_option_name, long_option_name = _ARG.NO, short_option_name

        # optparse -> argparse `%default` => `%(default)s`
        if help is not _ARG.NO and "%default" in help:
            LOG.warning(
                "option %s: please update `help=` text to use %%(default)s "
                "instead of %%default -- this will be an error in the future",
                long_option_name,
            )
            help = help.replace("%default", "%(default)s")

        # optparse -> argparse for `callback`
        if action == "callback":
            LOG.warning(
                "option %s: please update from optparse `action='callback'` "
                "to argparse action classes -- this will be an error in the "
                "future",
                long_option_name,
            )
            action = _CallbackAction
            if type is _ARG.NO:
                nargs = 0

        # optparse -> argparse for `type`
        if isinstance(type, utils.string_types):
            LOG.warning(
                "option %s: please update from optparse string `type=` to "
                "argparse callable `type=` -- this will be an error in the "
                "future",
                long_option_name,
            )
            type = _optparse_callable_map[type]

        # flake9 special type normalization
        if comma_separated_list or normalize_paths:
            type = functools.partial(
                _flake9_normalize,
                comma_separated_list=comma_separated_list,
                normalize_paths=normalize_paths,
            )

        self.short_option_name = short_option_name
        self.long_option_name = long_option_name
        self.option_args = [
            x
            for x in (short_option_name, long_option_name)
            if x is not _ARG.NO
        ]
        self.action = action
        self.default = default
        self.type = type
        self.dest = dest
        self.nargs = nargs
        self.const = const
        self.choices = choices
        self.callback = callback
        self.callback_args = callback_args
        self.callback_kwargs = callback_kwargs
        self.help = help
        self.metavar = metavar
        self.required = required
        self.option_kwargs = {
            "action": self.action,
            "default": self.default,
            "type": self.type,
            "dest": self.dest,
            "nargs": self.nargs,
            "const": self.const,
            "choices": self.choices,
            "callback": self.callback,
            "callback_args": self.callback_args,
            "callback_kwargs": self.callback_kwargs,
            "help": self.help,
            "metavar": self.metavar,
            "required": self.required,
        }  # type: Dict[str, Union[Any, _ARG]]

        # Set our custom attributes
        self.parse_from_config = parse_from_config
        self.comma_separated_list = comma_separated_list
        self.normalize_paths = normalize_paths

        self.config_name = None  # type: Optional[str]
        if parse_from_config:
            if long_option_name is _ARG.NO:
                raise ValueError(
                    "When specifying parse_from_config=True, "
                    "a long_option_name must also be specified."
                )
            self.config_name = long_option_name[2:].replace("-", "_")

        self._opt = None

    @property
    def filtered_option_kwargs(self):  # type: () -> Dict[str, Any]
        """Return any actually-specified arguments."""
        return {
            k: v for k, v in self.option_kwargs.items() if v is not _ARG.NO
        }

    def __repr__(self):  # type: () -> str  # noqa: D105
        parts = []
        for arg in self.option_args:
            parts.append(arg)
        for k, v in self.filtered_option_kwargs.items():
            parts.append("{}={!r}".format(k, v))
        return "Option({})".format(", ".join(parts))

    def normalize(self, value, *normalize_args):
        # type: (Any, *str) -> Any
        """Normalize the value based on the option configuration."""
        if self.comma_separated_list and isinstance(
            value, utils.string_types
        ):
            value = utils.parse_comma_separated_list(value)

        if self.normalize_paths:
            if isinstance(value, list):
                value = utils.normalize_paths(value, *normalize_args)
            else:
                value = utils.normalize_path(value, *normalize_args)

        return value

    def normalize_from_setuptools(self, value):
        # type: (str) -> Union[int, float, complex, bool, str]
        """Normalize the value received from setuptools."""
        value = self.normalize(value)
        if self.type is int or self.action == "count":
            return int(value)
        elif self.type is float:
            return float(value)
        elif self.type is complex:
            return complex(value)
        if self.action in ("store_true", "store_false"):
            value = str(value).upper()
            if value in ("1", "T", "TRUE", "ON"):
                return True
            if value in ("0", "F", "FALSE", "OFF"):
                return False
        return value

    def to_argparse(self):
        # type: () -> Tuple[List[str], Dict[str, Any]]
        """Convert a Flake9 Option to argparse ``add_argument`` arguments."""
        return self.option_args, self.filtered_option_kwargs

    @property
    def to_optparse(self):  # type: () -> NoReturn
        """No longer functional."""
        raise AttributeError("to_optparse: flake9 now uses argparse")


PluginVersion = collections.namedtuple(
    "PluginVersion", ["name", "version", "local"]
)


class OptionManager(object):
    """Manage Options and OptionParser while adding post-processing."""

    def __init__(
        self,
        prog,
        version,
        usage="%(prog)s [options] file file ...",
        parents=None,
    ):  # type: (str, str, str, Optional[List[argparse.ArgumentParser]]) -> None  # noqa: E501
        """Initialize an instance of an OptionManager.

        :param str prog:
            Name of the actual program (e.g., flake9).
        :param str version:
            Version string for the program.
        :param str usage:
            Basic usage string used by the OptionParser.
        :param argparse.ArgumentParser parents:
            A list of ArgumentParser objects whose arguments should also be
            included.
        """
        if parents is None:
            parents = []

        self.parser = argparse.ArgumentParser(
            prog=prog, usage=usage, parents=parents
        )  # type: argparse.ArgumentParser
        self._current_group = None  # type: Optional[argparse._ArgumentGroup]
        self.version_action = cast(
            "argparse._VersionAction",
            self.parser.add_argument(
                "--version", action="version", version=version
            ),
        )
        self.parser.add_argument("filenames", nargs="*", metavar="filename")
        self.config_options_dict = {}  # type: Dict[str, Option]
        self.options = []  # type: List[Option]
        self.program_name = prog
        self.version = version
        self.registered_plugins = set()  # type: Set[PluginVersion]
        self.extended_default_ignore = set()  # type: Set[str]
        self.extended_default_select = set()  # type: Set[str]

    @contextlib.contextmanager
    def group(self, name):  # type: (str) -> Generator[None, None, None]
        """Attach options to an argparse group during this context."""
        group = self.parser.add_argument_group(name)
        self._current_group, orig_group = group, self._current_group
        try:
            yield
        finally:
            self._current_group = orig_group

    def add_option(self, *args, **kwargs):  # type: (*Any, **Any) -> None
        """Create and register a new option.

        See parameters for :class:`~flake9.options.manager.Option` for
        acceptable arguments to this method.

        .. note::

            ``short_option_name`` and ``long_option_name`` may be specified
            positionally as they are with argparse normally.
        """
        option = Option(*args, **kwargs)
        option_args, option_kwargs = option.to_argparse()
        if self._current_group is not None:
            self._current_group.add_argument(*option_args, **option_kwargs)
        else:
            self.parser.add_argument(*option_args, **option_kwargs)
        self.options.append(option)
        if option.parse_from_config:
            name = option.config_name
            assert name is not None  # nosec (for mypy)
            self.config_options_dict[name] = option
            self.config_options_dict[name.replace("_", "-")] = option
        LOG.debug('Registered option "%s".', option)

    def remove_from_default_ignore(self, error_codes):
        # type: (Sequence[str]) -> None
        """Remove specified error codes from the default ignore list.

        :param list error_codes:
            List of strings that are the error/warning codes to attempt to
            remove from the extended default ignore list.
        """
        LOG.debug("Removing %r from the default ignore list", error_codes)
        for error_code in error_codes:
            try:
                self.extended_default_ignore.remove(error_code)
            except (ValueError, KeyError):
                LOG.debug(
                    "Attempted to remove %s from default ignore"
                    " but it was not a member of the list.",
                    error_code,
                )

    def extend_default_ignore(self, error_codes):
        # type: (Sequence[str]) -> None
        """Extend the default ignore list with the error codes provided.

        :param list error_codes:
            List of strings that are the error/warning codes with which to
            extend the default ignore list.
        """
        LOG.debug("Extending default ignore list with %r", error_codes)
        self.extended_default_ignore.update(error_codes)

    def extend_default_select(self, error_codes):
        # type: (Sequence[str]) -> None
        """Extend the default select list with the error codes provided.

        :param list error_codes:
            List of strings that are the error/warning codes with which
            to extend the default select list.
        """
        LOG.debug("Extending default select list with %r", error_codes)
        self.extended_default_select.update(error_codes)

    def generate_versions(
        self, format_str="%(name)s: %(version)s", join_on=", "
    ):
        # type: (str, str) -> str
        """Generate a comma-separated list of versions of plugins."""
        return join_on.join(
            format_str % plugin._asdict()
            for plugin in sorted(self.registered_plugins)
        )

    def update_version_string(self):  # type: () -> None
        """Update the flake9 version string."""
        self.version_action.version = "{} ({}) {}".format(
            self.version, self.generate_versions(), utils.get_python_version()
        )

    def generate_epilog(self):  # type: () -> None
        """Create an epilog with the version and name of each of plugin."""
        plugin_version_format = "%(name)s: %(version)s"
        self.parser.epilog = "Installed plugins: " + self.generate_versions(
            plugin_version_format
        )

    def parse_args(
        self,
        args=None,  # type: Optional[List[str]]
        values=None,  # type: Optional[argparse.Namespace]
    ):
        # type: (...) -> Tuple[argparse.Namespace, List[str]]
        """Proxy to calling the OptionParser's parse_args method."""
        self.generate_epilog()
        self.update_version_string()
        if values:
            self.parser.set_defaults(**vars(values))
        parsed_args = self.parser.parse_args(args)
        # TODO: refactor callers to not need this
        return parsed_args, parsed_args.filenames

    def parse_known_args(self, args=None):
        # type: (Optional[List[str]]) -> Tuple[argparse.Namespace, List[str]]
        """Parse only the known arguments from the argument values.

        Replicate a little argparse behaviour while we're still on
        optparse.
        """
        self.generate_epilog()
        self.update_version_string()
        return self.parser.parse_known_args(args)

    def register_plugin(self, name, version, local=False):
        # type: (str, str, bool) -> None
        """Register a plugin relying on the OptionManager.

        :param str name:
            The name of the checker itself. This will be the ``name``
            attribute of the class or function loaded from the entry-point.
        :param str version:
            The version of the checker that we're using.
        :param bool local:
            Whether the plugin is local to the project/repository or not.
        """
        self.registered_plugins.add(PluginVersion(name, version, local))