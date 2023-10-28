from uuid import uuid4


async def test_async_client(async_client):
    result = await async_client.health()
    assert result.status == "available"


async def test_async_empty_index(async_empty_index):
    uid = str(uuid4())
    index = await async_empty_index(uid)
    assert index.uid == uid


def test_client(client):
    result = client.health()
    assert result.status == "available"


def test_empty_index(empty_index):
    uid = str(uuid4())
    index = empty_index(uid)
    assert index.uid == uid
