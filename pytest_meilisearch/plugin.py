from pytest_meilisearch.fixtures import (  # noqa: F401
    async_clear_indexes,
    async_client,
    async_empty_index,
    async_index_with_documents,
    clear_indexes,
    client,
    empty_index,
    index_with_documents,
    meilisearch_url,
)


def pytest_addoption(parser):
    group = parser.getgroup("meilisearch")
    group.addoption(
        "--meilisearch-host",
        action="store",
        default="http://127.0.0.1",
        type=str,
        help="The host where Meilisearch is running.",
    )
    group.addoption(
        "--meilisearch-port",
        action="store",
        default=7700,
        type=int,
        help="The port Meilisearch is running on.",
    )
    group.addoption(
        "--meilisearch-master-key",
        action="store",
        type=str,
        help="The master key for Meilisearch.",
    )
    parser.addini(
        "meilisearch_client_scope",
        "Modify the scope of the async_client and client fixtures.",
        default="session",
    )
    parser.addini(
        "meilisearch_clear_indexes",
        "Modify the autouse setting for the async_clear_indexes and clear_indexes fixtures.",
        default="none",
    )
