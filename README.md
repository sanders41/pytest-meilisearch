# pytest-meilisearch

[![Test Status](https://github.com/sanders41/pytest-meilisearch/workflows/Testing/badge.svg?branch=main&event=push)](https://github.com/sanders41/pytest-meilisearch/actions?query=workflow%3ATesting+branch%3Amain+event%3Apush)
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
[pytest-asyncio](https://github.com/pytest-dev/pytest-asyncio). In order to use
`--start-meilisearch` [Docker](https://www.docker.com/) has to be installed.

### Configuration

#### Flags

- `--meilisearch-host`: Host where the Meilisearch test server is running. For example
  `http://localhost`. Default = `http://127.0.0.1` (This is the same as `http://localhost`).
- `--meilisearch-port`: Port where the Meilisearch test server is running. For example `7700`.
  Default = `7700`.
- `--meilisearch-master-key"`: The master key for the Meilisearch test server. Default = `None`.
- `--start-meilisearch`: Start a Meilisearch Docker container before running the tests. For this to
  work Docker has to be installed first. Default = `False`.
- `--meilisearch-version`: When using `--start-meilisearch` the this flag will set the version of
  Meilisearch to start. Default = `latest`.
- `--meilisearch-start-timeout`: The number of seconds to wait for Meilisearch to start before
  timing out. Default = 120.

#### Settings

- `meilisearch_client_scope`: Modify the scope of the async_client and client fixtures. Valid
  settings are `function`, `module`, `package`, or `session`. Default = `function`.
- `meilisearch_clear_indexes`: Controls is indexes are deleted after each tests. This can be useful
  to ensure that tests don't interfer with each other. Valid options are `none` = indexes are not
  deleted, `async` = indexes are asyncronously deleted after each test, or `sync` = indexes are
  syncronously deleted between each test. Default = `none`.

## Examples

- Testing that your function that adds documents to an index is successful:

  - async:

    ```py
    async def test_my_func(async_client):
        docs = [
            {"id": 1, "title": "Ready Player One"},
            {"id": 2, "title": "The Hitchhiker's Guide to the Galaxy"},
        ]
        index_name = "books"
        await my_func(index_name, docs)
        index = async_client.index(index_name)
        result = await index.get_documents()
        assert result.results == docs
    ```

  - sync:

    ```py
    def test_my_func(client):
        docs = [
            {"id": 1, "title": "Ready Player One"},
            {"id": 2, "title": "The Hitchhiker's Guide to the Galaxy"},
        ]
        index_name = "books"
        my_func(index_name, docs)
        index = client.index(index_name)
        result = index.get_documents()
        assert result.results == docs
    ```

- Testing that your search is successful:

  - async:

    ```py
    async def test_my_func(async_index_with_documents):
        docs = [
            {"id": 1, "title": "Ready Player One"},
            {"id": 2, "title": "The Hitchhiker's Guide to the Galaxy"},
        ]
        index_name = "books"
        index = await async_index_with_documents(docs, index_name)
        results = await my_func("Ready Player One")
        expected = "Ready Player One"  # Whatever you expect to be returned
        assert result == expected
    ```

  - sync:

    ```py
    def test_my_func(index_with_documents):
        docs = [
            {"id": 1, "title": "Ready Player One"},
            {"id": 2, "title": "The Hitchhiker's Guide to the Galaxy"},
        ]
        index_name = "books"
        index = index_with_documents(docs, index_name)
        results = my_func("Ready Player One")
        expected = "Ready Player One"  # Whatever you expect to be returned
        assert result == expected
    ```

## Contributing

If you are interested in contributing to this project please see our
[contributing guide](CONTRIBUTING.md).
