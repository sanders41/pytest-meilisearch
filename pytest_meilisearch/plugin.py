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
    start_meilisearch,
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
    group.addoption(
        "--start-meilisearch",
        action="store_true",
        default=False,
        help="Start Meilisearch before running tests. Default: False.",
    )
    group.addoption(
        "--meilisearch-start-timeout",
        action="store",
        default=120,
        type=int,
        help="The number of seconds to wait for Meilisearch to start before timing out. Default: 120.",
    )
    group.addoption(
        "--meilisearch-version",
        action="store",
        default="latest",
        type=str,
        help="The version of Meilisearch to use when start-meilisearch is True. Default: latest.",
    )
    parser.addini(
        "meilisearch_client_scope",
        "Modify the scope of the async_client and client fixtures. Default: function.",
        default="function",
    )
    parser.addini(
        "meilisearch_clear_indexes",
        "Modify the autouse setting for the async_clear_indexes and clear_indexes fixtures.",
        default="none",
    )
