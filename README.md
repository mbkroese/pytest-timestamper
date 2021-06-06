# pytest-timestamper

Plugin to add a timestamp prefix to the pytest output

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
