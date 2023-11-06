import asyncio
from uuid import uuid4

import pytest
from meilisearch_python_sdk import AsyncClient, Client

from pytest_meilisearch._internal import determine_clear_indexes, determine_client_scope
from pytest_meilisearch._meilisearch_server import MeilisearchServer


@pytest.fixture(autouse=True)
async def async_clear_indexes(async_client, request):
    """Asyncronously clears all indexes.

    This fixture runs if `meilisearch_clear_indexes` is set to `async`.
    """

    yield
    if determine_clear_indexes(request.config) == "async":
        indexes = await async_client.get_indexes()
        if indexes:
            tasks = await asyncio.gather(*[async_client.index(x.uid).delete() for x in indexes])
            await asyncio.gather(*[async_client.wait_for_task(x.task_uid) for x in tasks])


@pytest.fixture(scope=determine_client_scope)  # type: ignore
async def async_client(pytestconfig, meilisearch_url):
    """Creates a meilisearch_python_sdk.AsyncClient for asyncronous testing."""

    async with AsyncClient(
        meilisearch_url, pytestconfig.getvalue("meilisearch_master_key")
    ) as client:
        yield client


@pytest.fixture
async def async_empty_index(async_client):
    """Create an empty meilisearch_python_sdk.AsyncIndex.

    A name for the index uid can be passed in. By default the id will be created with a uid to
    ensure it is unique.
    """

    async def index_maker(uid=str(uuid4())):
        return await async_client.create_index(uid=uid)

    return index_maker


@pytest.fixture
async def async_index_with_documents(async_client, async_empty_index):
    """Creates a meilisearch_python_sdk.AsyncIndex that contains documents.

    The documents to populate the index need to be passed in when using the fixture.
    """

    async def index_maker(documents, index_name=None):
        if index_name:
            index = await async_empty_index(index_name)
        else:
            index = await async_empty_index()
        response = await index.add_documents(documents)
        await async_client.wait_for_task(response.task_uid)
        return index

    return index_maker


@pytest.fixture(autouse=True)
def clear_indexes(client, request):
    """Clears all indexes.

    This fixture runs if `meilisearch_clear_indexes` is set to `sync`.
    """

    yield
    if determine_clear_indexes(request.config) == "sync":
        indexes = client.get_indexes()
        if indexes:
            for index in indexes:
                client.index(index.uid).delete()


@pytest.fixture(scope=determine_client_scope)  # type: ignore
def client(pytestconfig, meilisearch_url):
    """Creates a meilisearch_python_sdk.Client for testing."""

    yield Client(meilisearch_url, pytestconfig.getvalue("meilisearch_master_key"))


@pytest.fixture
def empty_index(client):
    """Create an empty meilisearch_python_sdk.Index.

    A name for the index uid can be passed in. By default the id will be created with a uid to
    ensure it is unique.
    """

    def index_maker(uid=str(uuid4())):
        return client.create_index(uid=uid)

    return index_maker


@pytest.fixture
def index_with_documents(client, empty_index):
    """Creates a meilisearch_python_sdk.Index that contains documents.

    The documents to populate the index need to be passed in when using the fixture.
    """

    def index_maker(documents, index_name=None):
        if index_name:
            index = empty_index(index_name)
        else:
            index = empty_index()
        response = index.add_documents(documents)
        client.wait_for_task(response.task_uid)
        return index

    return index_maker


@pytest.fixture(scope=determine_client_scope)  # type: ignore
def meilisearch_url(pytestconfig):
    """Combines the `meilisearch_host` and `meilisearch_port` into an URL."""

    return _create_meilisarch_url(pytestconfig)


@pytest.fixture(scope="session", autouse=True)
def start_meilisearch(pytestconfig):
    if pytestconfig.getvalue("start_meilisearch"):
        server = MeilisearchServer(
            url=_create_meilisarch_url(pytestconfig),
            port=pytestconfig.getvalue("meilisearch_port"),
            meilisearch_version=pytestconfig.getvalue("meilisearch_version"),
            start_timeout=pytestconfig.getvalue("meilisearch_start_timeout"),
            api_key=pytestconfig.getvalue("meilisearch_master_key"),
        )
        server.start()
    yield
    if pytestconfig.getvalue("start_meilisearch"):
        server.stop()


def _create_meilisarch_url(pytestconfig):
    return (
        f"{pytestconfig.getvalue('meilisearch_host')}:{pytestconfig.getvalue('meilisearch_port')}"
    )
