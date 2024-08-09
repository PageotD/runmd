
# CHANGELOG

All notable changes to this project will be documented in this file.
 
The format is based on [Keep a Changelog](http://keepachangelog.com/)
and this project adheres to [Semantic Versioning](http://semver.org/).
 
## [Unreleased]
 
### Added
* add `show`option to show the code block in terminal
* show `(<lang>)` or `(<lang>: not configured)` next to the code block name
* add config file validation

### Changed
* add type hints to functions
* move functions related to configuration to config.py
* move parse_markdown function to parser.py
* move run_code_block function to runner.py
* move process_markdown_files function to process.py

### Fixed
* prevent running code block for not configured languages