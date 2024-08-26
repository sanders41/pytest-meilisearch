# pytest-meilisearch

[![Tests Status](https://github.com/sanders41/pytest-meilisearch/actions/workflows/testing.yml/badge.svg?branch=main&event=push)](https://github.com/sanders41/pytest-meilisearch/actions?query=workflow%3ATesting+branch%3Amain+event%3Apush)
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
  `http://localhost`. Default = `http://127.0.0.1` (This is the same as `http://localhost`).
- `--meilisearch-port`: Port where the Meilisearch test server is running. For example `7700`.
  Default = `7700`.
- `--meilisearch-master-key`: The master key for the Meilisearch test server. Default = `None`.

#### Settings

- `meilisearch_client_scope`: Modify the scope of the async_meilisearch_client and
  meilisearch_client fixtures. Valid settings are `function`, `module`, `package`, or `session`.
  Default = `function`.
- `meilisearch_clear`: Controls if either documents or indexes are deleted after each tests. This
  can be useful to ensure that tests don't interfer with each other. Valid options are
  `none` = documents and indexes are not deleted, `async_document` = documents are asyncronously
  deleted after each test, `async_index` = indexes are asyncronously deleted after each test,
  `document` = documents are syncronously deleted after each test, or `index` = indexes are
  syncronously deleted between each test. Default = `none`.

## Examples

- Testing that your function that adds documents to an index is successful:

  - async:

    ```py
    async def test_my_func(async_meilisearch_client):
        docs = [
            {"id": 1, "title": "Ready Player One"},
            {"id": 2, "title": "The Hitchhiker's Guide to the Galaxy"},
        ]
        index_name = "books"
        await my_func(index_name, docs)
        index = async_meilisearch_client.index(index_name)
        result = await index.get_documents()
        assert result.results == docs
    ```

  - sync:

    ```py
    def test_my_func(meilisearch_client):
        docs = [
            {"id": 1, "title": "Ready Player One"},
            {"id": 2, "title": "The Hitchhiker's Guide to the Galaxy"},
        ]
        index_name = "books"
        my_func(index_name, docs)
        index = meilisearch_client.index(index_name)
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
