"""Package containing the option manager and config management logic.

- :mod:`flake9.options.config` contains the logic for finding, parsing, and
  merging configuration files.

- :mod:`flake9.options.manager` contains the logic for managing customized
  Flake9 command-line and configuration options.

- :mod:`flake9.options.aggregator` uses objects from both of the above modules
  to aggregate configuration into one object used by plugins and Flake9.

"""
