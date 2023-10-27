from __future__ import annotations

import asyncio
from uuid import uuid4

import pytest
from meilisearch_python_sdk import AsyncClient, Client


@pytest.fixture
async def async_test_client():
    """Creates a meilisearch_python_sdk.AsyncClient for asyncronous testing."""
    async with AsyncClient() as client:
        yield client


@pytest.fixture
def test_client():
    """Creates a meilisearch_python_sdk.Client for testing."""
    yield Client()


@pytest.fixture
async def async_empty_index(async_test_client):
    """Create an empty meilisearch_python_sdk.AsyncIndex with a uuid for the name.

    The use of a uuid prevents name clashes between tests.
    """

    async def index_maker():
        return await async_test_client.create_index(uid=str(uuid4()))

    return index_maker


@pytest.fixture
def empty_index(test_client):
    """Create an empty meilisearch_python_sdk.Index with a uuid for the name.

    The use of a uuid prevents name clashes between tests.
    """

    def index_maker():
        return test_client.create_index(uid=str(uuid4()))

    return index_maker


@pytest.fixture
async def async_clear_indexes(async_test_client):
    """Asyncronously clears all indexes."""
    yield
    indexes = await async_test_client.get_indexes()
    if indexes:
        tasks = await asyncio.gather(*[async_test_client.index(x.uid).delete() for x in indexes])
        await asyncio.gather(*[async_test_client.wait_for_task(x.task_uid) for x in tasks])


@pytest.fixture
async def clear_indexes(test_client):
    """Clears all indexes."""
    yield
    indexes = test_client.get_indexes()
    if indexes:
        for index in indexes:
            test_client.index(index.uid).delete()
