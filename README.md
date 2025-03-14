# vidtoolz-add-sound

[![PyPI](https://img.shields.io/pypi/v/vidtoolz-add-sound.svg)](https://pypi.org/project/vidtoolz-add-sound/)
[![Changelog](https://img.shields.io/github/v/release/sukhbinder/vidtoolz-add-sound?include_prereleases&label=changelog)](https://github.com/sukhbinder/vidtoolz-add-sound/releases)
[![Tests](https://github.com/sukhbinder/vidtoolz-add-sound/workflows/Test/badge.svg)](https://github.com/sukhbinder/vidtoolz-add-sound/actions?query=workflow%3ATest)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/sukhbinder/vidtoolz-add-sound/blob/main/LICENSE)

Add sound to a video

## Installation

First install [vidtoolz](https://github.com/sukhbinder/vidtoolz).

```bash
pip install vidtoolz
```

Then install this plugin in the same environment as your vidtoolz application.

```bash
vidtoolz install vidtoolz-add-sound
```
## Usage

type ``vid addsound --help`` to get help



## Development

To set up this plugin locally, first checkout the code. Then create a new virtual environment:
```bash
cd vidtoolz-add-sound
python -m venv venv
source venv/bin/activate
```
Now install the dependencies and test dependencies:
```bash
pip install -e '.[test]'
```
To run the tests:
```bash
python -m pytest
```
