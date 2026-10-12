import asyncio


def shouted(names: list[str]) -> list[str]:
    return [name.upper() for name in names]


async def fetch_all(names: list[str]) -> list[str]:
    """Fetch every name at the same time. Keep the input order."""
    return list(await asyncio.gather(*(fetch(name) for name in names)))  # noqa: F821


async def first_done(fast: float, slow: float) -> str:
    async def nap(label: str, delay: float) -> str:
        await asyncio.sleep(delay)
        return label

    tasks = {
        asyncio.create_task(nap("fast", fast)),
        asyncio.create_task(nap("slow", slow)),
    }
    done, pending = await asyncio.wait(tasks, return_when=asyncio.FIRST_COMPLETED)
    for task in pending:
        task.cancel()
    return done.pop().result()
