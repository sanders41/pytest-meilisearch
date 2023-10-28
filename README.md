# pytest-meilisearch

[![Test Status](https://github.com/sanders41/pytest-meilisearch/workflows/Testing/badge.svg?branch=main&event=push)](https://github.com/sanders41/pytest-meilisearch/actions?query=workflow%3CI+branch%3Amain+event%3Apush)
[![pre-commit.ci status](https://results.pre-commit.ci/badge/github/sanders41/pytest-meilisearch/main.svg)](https://results.pre-commit.ci/latest/github/sanders41/pytest-meilisearch/main)
[![PyPI version](https://badge.fury.io/py/pytest-meilisearch.svg)](https://badge.fury.io/py/pytest-meilisearch)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/pytest-meilisearch?color=5cc141)](https://github.com/sanders41/pytest-meilisearch)

pytest helpers for testing Python projects using Meilisearch.

## Installation

Using a virtual environment is recommended for installing this package. Once the virtual
environment is created and activated, install the package with:

```sh
pip install pytest-meilisearch
```

## Usage

Note that to use any of the async options you also need to install an async test helper such as
[pytest-asyncio](https://github.com/pytest-dev/pytest-asyncio).

### Configuration

#### Flags

- `--meilisearch-host`: Host where the Meilisearch test server is running. For example
  `http://localhost`. Default = "http://127.0.0.1" (This is the same as http://localhost).
- `--meilisearch-port`: Port where the Meilisearch test server is running. For example `7700`.
  Default = `7700`.
  group.addoption(
- `--meilisearch-master-key"`: The master key for the Meilisearch test server. Default = `None`.

#### Settings

- `meilisearch_client_scope`: Modify the scope of the async_client and client fixtures. Valid
  settings are `function`, `module`, `package`, or `session`. Default = `session`.
- `meilisearch_clear_indexes`: Controls is indexes are deleted after each tests. This can be useful
  to ensure that tests don't interfer with each other. Valid options are `none` = indexes are not
  deleted, `async` = indexes are asyncronously deleted after each test, or `sync` = indexes are
  syncronously deleted between each test. Default = `none`.
