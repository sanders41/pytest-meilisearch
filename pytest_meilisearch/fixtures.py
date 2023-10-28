import asyncio
from uuid import uuid4

import pytest
from meilisearch_python_sdk import AsyncClient, Client

from pytest_meilisearch._internal import determine_clear_indexes, determine_client_scope


@pytest.fixture(scope="session")
def meilisearch_url(pytestconfig):
    return (
        f"{pytestconfig.getvalue('meilisearch_host')}:{pytestconfig.getvalue('meilisearch_port')}"
    )


@pytest.fixture(scope=determine_client_scope)  # type: ignore
async def async_client(pytestconfig, meilisearch_url):
    """Creates a meilisearch_python_sdk.AsyncClient for asyncronous testing."""
    async with AsyncClient(
        meilisearch_url, pytestconfig.getvalue("meilisearch_master_key")
    ) as client:
        yield client


@pytest.fixture(scope=determine_client_scope)  # type: ignore
def client(pytestconfig, meilisearch_url):
    """Creates a meilisearch_python_sdk.Client for testing."""
    yield Client(meilisearch_url, pytestconfig.getvalue("meilisearch_master_key"))


@pytest.fixture
async def async_empty_index(async_client):
    """Create an empty meilisearch_python_sdk.AsyncIndex.

    A name for the index uid can be passed in. By default the id will be created with a uuid
    """

    async def index_maker(uid=str(uuid4())):
        return await async_client.create_index(uid=uid)

    return index_maker


@pytest.fixture
def empty_index(client):
    """Create an empty meilisearch_python_sdk.Index.

    A name for the index uid can be passed in. By default the id will be created with a uuid
    """

    def index_maker(uid=str(uuid4())):
        return client.create_index(uid=uid)

    return index_maker


@pytest.fixture(autouse=True)
async def async_clear_indexes(async_client, request):
    """Asyncronously clears all indexes."""

    yield
    if determine_clear_indexes(request.config) == "async":
        indexes = await async_client.get_indexes()
        if indexes:
            tasks = await asyncio.gather(*[async_client.index(x.uid).delete() for x in indexes])
            await asyncio.gather(*[async_client.wait_for_task(x.task_uid) for x in tasks])


@pytest.fixture(autouse=True)
def clear_indexes(client, request):
    """Clears all indexes."""

    yield
    if determine_clear_indexes(request.config) == "sync":
        indexes = client.get_indexes()
        if indexes:
            for index in indexes:
                client.index(index.uid).delete()
