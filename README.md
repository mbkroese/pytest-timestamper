# pytest-timestamper

![CI Status](https://github.com/mbkroese/pytest-timestamper/actions/workflows/main.yml/badge.svg)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)


Plugin to add a timestamp prefix to the pytest output.

```
➜ myproject python3 -m pytest -v
==================================== test session starts ====================================
platform darwin -- Python 3.9.4, pytest-6.3.0.dev494+g43faea832.d20210528, py-1.10.0, ...
cachedir: .pytest_cache
rootdir: /Users/mbk/git_tree/myproject
plugins: timestamper-0.1.dev14+gaacde4a
collected 3 items

[2021-06-06 12:19:06] tests/test_one.py::test_dummy PASSED                            [ 33%]
[2021-06-06 12:19:06] tests/test_one.py::test_dummy_two PASSED                        [ 66%]
[2021-06-06 12:19:06] tests/test_two.py::test_another_dummy PASSED                    [100%]

===================================== 3 passed in 0.02s =====================================
```

## Motivation

For various reasons tests can be slower on some runs than other.
However, without a timestamp in front of the test it is not clear to the user how long the current test has been taking.
This plugin adds a simple timestamp in front of the pytest output.

## Installation

```
pip install pytest-timestamper
```

## Usage

To activate the plugin one simply needs to install it.
The user can update the format of the prefix with the `--prefixfmt` and the datetime format with `--datefmt`.
