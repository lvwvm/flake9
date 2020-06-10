import toml
import logging
import os.path


LOG = logging.getLogger(__name__)

# max depth to search for
MAX_RECURSION = 25


def parse_py_project_toml():
    path = "pyproject.toml"
    for _ in range(MAX_RECURSION):
        try:
            with open(path) as f:
                try:
                    LOG.info("loading config from pyproject.toml")
                    loaded = toml.load(f)
                    break
                except toml.TomlDecodeError as e:
                    LOG.error("failed to parse pyproject.toml at %s" % os.path.abspath(path), exc_info=e)
        except FileNotFoundError:
            path = "../" + path
        except OSError as e:
            LOG.error("failed to open pyproject.toml at %s: %s" % (os.path.abspath(path), e), exc_info=e)
            path = "../" + path
    else:
        LOG.debug("no pyproject.toml found")
        return {}
    return {k.replace("-", "_"): v for k, v in loaded["tool"]["flake9"].items()}
