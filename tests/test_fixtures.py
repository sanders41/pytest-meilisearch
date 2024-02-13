from uuid import uuid4

import pytest


async def test_async_client(async_meilisearch_client):
    result = await async_meilisearch_client.health()
    assert result.status == "available"


async def test_async_empty_index(async_empty_index):
    uid = str(uuid4())
    index = await async_empty_index(uid)
    assert index.uid == uid


async def test_async_empty_index_default(async_empty_index):
    index = await async_empty_index()
    assert index.uid is not None


@pytest.mark.parametrize("index_name", [str(uuid4()), None])
async def test_async_index_with_documents(index_name, async_index_with_documents):
    docs = [{"id": 1, "title": "Title 1"}, {"id": 2, "title": "Title 2"}]
    index = await async_index_with_documents(docs, index_name)
    if index_name:
        assert index.uid == index_name
    else:
        assert index.uid is not None
    result = await index.get_documents()
    assert len(result.results) == 2
    assert result.results == docs


def test_client(meilisearch_client):
    result = meilisearch_client.health()
    assert result.status == "available"


def test_empty_index(empty_index):
    uid = str(uuid4())
    index = empty_index(uid)
    assert index.uid == uid


def test_empty_index_default(empty_index):
    index = empty_index()
    assert index.uid is not None


@pytest.mark.parametrize("index_name", [str(uuid4()), None])
def test_index_with_documents(index_name, index_with_documents):
    docs = [{"id": 1, "title": "Title 1"}, {"id": 2, "title": "Title 2"}]
    index = index_with_documents(docs, index_name)
    if index_name:
        assert index.uid == index_name
    else:
        assert index.uid is not None
    result = index.get_documents()
    assert len(result.results) == 2
    assert result.results == docs
