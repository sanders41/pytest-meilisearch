import asyncio
from uuid import uuid4

import pytest
from meilisearch_python_sdk import AsyncClient, Client

from pytest_meilisearch._internal import (
    determine_clear,
    determine_client_scope,
)


@pytest.fixture(autouse=True)
async def async_clear_documents(async_meilisearch_client, request):
    """Asyncronously clears all documents in an indexes.

    This fixture runs if `meilisearch_clear` is set to `async_document`.
    """
    yield
    if determine_clear(request.config) == "async_document":
        indexes = await async_meilisearch_client.get_indexes()
        if indexes:
            tasks = await asyncio.gather(
                *[async_meilisearch_client.index(x.uid).delete_all_documents() for x in indexes]
            )
            await asyncio.gather(
                *[async_meilisearch_client.wait_for_task(x.task_uid) for x in tasks]
            )


@pytest.fixture(autouse=True)
async def async_clear_indexes(async_meilisearch_client, request):
    """Asyncronously clears all indexes.

    This fixture runs if `meilisearch_clear` is set to `async_index`.
    """
    yield
    if determine_clear(request.config) == "async_index":
        indexes = await async_meilisearch_client.get_indexes()
        if indexes:
            tasks = await asyncio.gather(
                *[async_meilisearch_client.index(x.uid).delete() for x in indexes]
            )
            await asyncio.gather(
                *[async_meilisearch_client.wait_for_task(x.task_uid) for x in tasks]
            )


@pytest.fixture(scope=determine_client_scope)  # type: ignore
async def async_meilisearch_client(pytestconfig, meilisearch_url):
    """Creates a meilisearch_python_sdk.AsyncClient for asyncronous testing."""

    async with AsyncClient(
        meilisearch_url, pytestconfig.getvalue("meilisearch_master_key")
    ) as client:
        yield client


@pytest.fixture
async def async_empty_index(async_meilisearch_client):
    """Create an empty meilisearch_python_sdk.AsyncIndex.

    A name for the index uid can be passed in. By default the id will be created with a uid to
    ensure it is unique.
    """
    uid = str(uuid4())

    async def index_maker(uid=uid):
        return await async_meilisearch_client.create_index(uid=uid)

    return index_maker


@pytest.fixture
async def async_index_with_documents(async_meilisearch_client, async_empty_index):
    """Creates a meilisearch_python_sdk.AsyncIndex that contains documents.

    The documents to populate the index need to be passed in when using the fixture.
    """

    async def index_maker(documents, index_name=None):
        if index_name:
            index = await async_empty_index(index_name)
        else:
            index = await async_empty_index()
        response = await index.add_documents(documents)
        await async_meilisearch_client.wait_for_task(response.task_uid)
        return index

    return index_maker


@pytest.fixture(autouse=True)
def clear_documents(meilisearch_client, request):
    """Clears all documents.

    This fixture runs if `meilisearch_clear` is set to `document`.
    """
    yield
    if determine_clear(request.config) == "document":
        indexes = meilisearch_client.get_indexes()
        if indexes:
            for index in indexes:
                task = meilisearch_client.index(index.uid).delete_all_documents()
                meilisearch_client.wait_for_task(task.task_uid)


@pytest.fixture(autouse=True)
def clear_indexes(meilisearch_client, request):
    """Clears all indexes.

    This fixture runs if `meilisearch_clear` is set to `index`.
    """

    yield
    if determine_clear(request.config) == "index":
        indexes = meilisearch_client.get_indexes()
        if indexes:
            for index in indexes:
                task = meilisearch_client.index(index.uid).delete()
                meilisearch_client.wait_for_task(task.task_uid)


@pytest.fixture(scope=determine_client_scope)  # type: ignore
def meilisearch_client(pytestconfig, meilisearch_url):
    """Creates a meilisearch_python_sdk.Client for testing."""

    yield Client(meilisearch_url, pytestconfig.getvalue("meilisearch_master_key"))


@pytest.fixture
def empty_index(meilisearch_client):
    """Create an empty meilisearch_python_sdk.Index.

    A name for the index uid can be passed in. By default the id will be created with a uid to
    ensure it is unique.
    """
    uid = str(uuid4())

    def index_maker(uid=uid):
        return meilisearch_client.create_index(uid=uid)

    return index_maker


@pytest.fixture
def index_with_documents(meilisearch_client, empty_index):
    """Creates a meilisearch_python_sdk.Index that contains documents.

    The documents to populate the index need to be passed in when using the fixture.
    """

    def index_maker(documents, index_name=None):
        if index_name:
            index = empty_index(index_name)
        else:
            index = empty_index()
        response = index.add_documents(documents)
        meilisearch_client.wait_for_task(response.task_uid)
        return index

    return index_maker


@pytest.fixture(scope=determine_client_scope)  # type: ignore
def meilisearch_url(pytestconfig):
    """Combines the `meilisearch_host` and `meilisearch_port` into an URL."""

    return _create_meilisarch_url(pytestconfig)


def _create_meilisarch_url(pytestconfig):
    return (
        f"{pytestconfig.getvalue('meilisearch_host')}:{pytestconfig.getvalue('meilisearch_port')}"
    )
