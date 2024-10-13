
# CHANGELOG

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](http://keepachangelog.com/)
and this project adheres to [Semantic Versioning](http://semver.org/).

## [0.13.0] - 2024-10-13

### Added 
* add environment manager

## [0.12.0] - 2024-10-03

### Added
* add the capacity to interact with user

### Changed
* move command name constants in an Enum class

## [0.11.0] - 2024-09-21

### Added
* add vault command to encrypt/decrypt markdown files

## [0.10.1] - 2024-09-15

### Fixed
* add rootpath to history to locate the original md file

## [0.10.0] - 2024-09-10

### Added
* add shebang detection in code blocks
* add package upload to PYPI
* add commands module to create the CLI parser

### Removed
* remove cliargs function from cli module

## [0.9.0] 2024-09-06

### Added
* add run command to CLI shell (experimental)
* add show command to CLI shell (experimental)
* add list command to CLI shell (experimental)
* add input markdown file handling
* add color to code block displayed with the show command
* add pygments as a dependency
* add vault features to encrypt/decrypt markdown files (experimental)
* add sandbox dockerfiles for alpine and debian

## [0.8.0] 2024-09-02

### Added
* create get_configuration fonction to simplify the load and validate in cli.py
* add expirimental CLI shell for runmd

### Changed
* change print/return with a FileNotFoundError in copy_config()
* remove useless variable in copy_config()
* raise error instead of returining empty list if error reading history file
* change read_history to load_history for coherence with load_config

## [0.7.0] - 2024-08-25

## Added
* add __version__ in __init__.py
* add --version command
* add compile_pattern function (refactoring parser module)

## Changed
* add tag flag for the run command instead of @+tagname argument
* add tag flag for the list command instead of @+tagname argument
* add status for history (success/fail) and collect history only for the run command
* migrate from pkg_resources to importlib.resources (python min version 3.7)
* remove unecessary `blocklist` argument in `process_markdown` function

## [0.6.0] - 2024-08-19

### Added
* add hist command to print runmd history command and replay commands

## [0.5.1] - 2024-08-19

### Changed
* huge refactoring of cli.py

### Fixed
* tag option is now working with list command

## [0.5.0] - 2024-08-17

### Added
* add function dedicated to language settings validation

### Changed
* remove duplicated code in runner.py
* drop config.json for config.ini

## [0.4.2] - 2024-08-16

### Fixed
* fix the print error when using the run command for a block name which does not exist

## [0.4.1] - 2024-08-16

### Changed
* move call to valid_config() from load_config() to cli.py

### Fixed
* fix error related to the --file option

## [0.4.0] - 2024-08-13

### Added
* add `tag` attribute
* add the possibility to run all code blocks with a given tag using `runmd run @<tag>`

### Changed
* rework on runner.py to print STDERR outputs in terminal
* refactor cli.py for lisibility and control

## [0.3.0] - 2024-08-12

### Changed
* cli and all functions in process.py have been refactored to gain in lisibility and usability

## [0.2.0] - 2024-08-11

### Added
* add support for environment variables
* add --file option to specifiy the markdown file to process

### Changed
* change `ls` command to `list` for homogeneity

### Removed
* remove --dir option since it creates too much complexity for very small benefits

## [0.1.0] - 2024-08-09

### Added
* add `show`option to show the code block in terminal
* show `(<lang>)` or `(<lang>: not configured)` next to the code block name
* add config file validation
* add init command and copy_config function to copy the config file to destination

### Changed
* add type hints to functions
* move functions related to configuration to config.py
* move parse_markdown function to parser.py
* move run_code_block function to runner.py
* move process_markdown_files function to process.py

### Fixed
* prevent running code block for not configured languages
