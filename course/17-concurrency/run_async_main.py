"""Run an async main from a script. Notebooks use top-level await instead."""
import asyncio


async def main() -> None:
    await asyncio.sleep(0)
    print("script loop finished")


if __name__ == "__main__":
    asyncio.run(main())
