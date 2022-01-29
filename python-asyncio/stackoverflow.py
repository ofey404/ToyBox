import asyncio
import json


data = ({"large": "data"},) * 3  # large
stacked_jsons = ""


async def transform(d: dict, q: asyncio.Queue) -> None:
    # `do_some_transformation`: long IO bound task
    await asyncio.sleep(1)
    await q.put(d)


# WARNING: incremental concatination of string would be slow,
# since string is immutable.
async def join(q: asyncio.Queue):
    global stacked_jsons
    while True:
        d = await q.get()
        stacked_jsons += json.dumps(d, separators=(",", ":")) + "\n"
        q.task_done()


async def main():
    q = asyncio.Queue()
    producers = [asyncio.create_task(transform(d, q)) for d in data]
    consumer = asyncio.create_task(join(q))
    await asyncio.gather(*producers)
    await q.join()  # Implicitly awaits consumers, too
    consumer.cancel()
    print(stacked_jsons)


if __name__ == "__main__":
    import time

    s = time.perf_counter()
    asyncio.run(main())
    elapsed = time.perf_counter() - s
    print(f"{__file__} executed in {elapsed:0.2f} seconds.")
