from uuid import uuid4


async def test_async_client(async_client):
    result = await async_client.health()
    assert result.status == "available"


async def test_async_empty_index(async_empty_index):
    uid = str(uuid4())
    index = await async_empty_index(uid)
    assert index.uid == uid


async def test_async_index_with_documents(async_index_with_documents):
    docs = [{"id": 1, "title": "Title 1"}, {"id": 2, "title": "Title 2"}]
    index = await async_index_with_documents(docs)
    result = await index.get_documents()
    assert len(result.results) == 2
    titles = [x["title"] for x in result.results]
    assert docs[0]["title"] in titles
    assert docs[1]["title"] in titles


def test_client(client):
    result = client.health()
    assert result.status == "available"


def test_empty_index(empty_index):
    uid = str(uuid4())
    index = empty_index(uid)
    assert index.uid == uid


def test_index_with_documents(index_with_documents):
    docs = [{"id": 1, "title": "Title 1"}, {"id": 2, "title": "Title 2"}]
    index = index_with_documents(docs)
    result = index.get_documents()
    assert len(result.results) == 2
    titles = [x["title"] for x in result.results]
    assert docs[0]["title"] in titles
    assert docs[1]["title"] in titles
