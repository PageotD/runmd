
# CHANGELOG

All notable changes to this project will be documented in this file.
 
The format is based on [Keep a Changelog](http://keepachangelog.com/)
and this project adheres to [Semantic Versioning](http://semver.org/).

## [unreleased] - 2024-08-13

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