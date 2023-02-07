import asyncio

from .logger import logger


async def shutdown(signal, loop):
    """Cleanup tasks tied to the service's shutdown."""
    logger.info(f"Received exit signal {signal.name}")
    tasks = [t for t in asyncio.all_tasks() if t is not asyncio.current_task()]

    [task.cancel() for task in tasks]

    logger.info(f"Cancelling {len(tasks)} outstanding tasks")
    await asyncio.gather(*tasks)
    loop.stop()
