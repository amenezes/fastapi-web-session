import pytest


async def test_get(storage):
    with pytest.raises(NotImplementedError):
        await storage.get("key")


@pytest.mark.asyncio
async def test_set(storage):
    with pytest.raises(NotImplementedError):
        await storage.set("key", "value")


async def test_delete(storage):
    with pytest.raises(NotImplementedError):
        await storage.delete("key1", "key2")
