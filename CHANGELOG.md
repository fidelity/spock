# Spock CHANGELOG

## August 7th, 2020 - v1.0
* Initial open source release

## June 18, 2020 - vPre-Release
* New Features:
    * Added support for more config file types (TOML and JSON in additon to YAML)
    * Added a new parameter type ChoiceArg for parameters that muse be chosen from a
    fixed set

* Additional unit test and linting

* Complete documentation overhaul with examples

* General code clean-up and doc-strings

## June 01, 2020 - vPreRelease
* New Features:
    * Forked dataclass to remove order requirements for class inheritance

* General bug fixes, clean-up, and doc updates

## January 30, 2020 - vPreRelease
* New Features:
    * Multiple configs with the same options
    * Setting config specific options with YAML namespaces
    * Python overrride/extension of YAML file path in ConfigArgBuilder with kwarg

* Removed:
    * Ability to specify args at the command line (for now...)
    * configargparse dependency

## January 6, 2020 - vPreRelease
* New Features:
    * YAML inheritance -- composing from multiple YAML configuration files

* Additional unit tests

* Enhanced documentation

## October 15, 2019 - vPreRelease

* Initial release with all base functionality, documentation, and unit tests.

## September-October 2019 - vDev

* Dev period.
