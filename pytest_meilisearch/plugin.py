from pytest_meilisearch.fixtures import (  # noqa: F401
    async_clear_documents,
    async_clear_indexes,
    async_empty_index,
    async_index_with_documents,
    async_meilisearch_client,
    clear_documents,
    clear_indexes,
    empty_index,
    index_with_documents,
    meilisearch_client,
    meilisearch_url,
)


def pytest_addoption(parser):
    group = parser.getgroup("meilisearch")
    group.addoption(
        "--meilisearch-host",
        action="store",
        default="http://127.0.0.1",
        type=str,
        help="The host where Meilisearch is running. Default: http://127.0.0.1",
    )
    group.addoption(
        "--meilisearch-port",
        action="store",
        default=7700,
        type=int,
        help="The port Meilisearch is running on. Default: 7700",
    )
    group.addoption(
        "--meilisearch-master-key",
        action="store",
        type=str,
        help="The master key for Meilisearch.",
    )
    parser.addini(
        "meilisearch_client_scope",
        "Modify the scope of the async_meilisearch_client and meilisearch_client fixtures. Default: function.",
        default="function",
    )
    parser.addini(
        "meilisearch_clear",
        "Modify the autouse setting for the async_clear_documents, async_clear_indexes, clear_documents, and clear_indexes fixtures.",
        default="none",
    )
