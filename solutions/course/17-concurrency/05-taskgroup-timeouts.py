import asyncio


async def pair():
    async with asyncio.TaskGroup() as group:
        a = group.create_task(asyncio.sleep(0, result=1))
        b = group.create_task(asyncio.sleep(0, result=2))
    return a.result(), b.result()


async def bounded_sleep(delay: float, limit: float) -> str:
    try:
        async with asyncio.timeout(limit):
            await asyncio.sleep(delay)
            return "ok"
    except TimeoutError:
        return "timed out"


async def sibling_cancelled() -> bool:
    async def boom():
        await asyncio.sleep(0.01)
        raise RuntimeError("nope")

    async def slow():
        await asyncio.sleep(1)
        return "late"

    try:
        async with asyncio.TaskGroup() as group:
            group.create_task(boom())
            slow_task = group.create_task(slow())
    except Exception:
        return slow_task.cancelled()
    return False
