import asyncio
import logging
import pathlib
import sys
from dataclasses import dataclass
from urllib.parse import urljoin

import aiofiles
import aiohttp
from aiohttp import ClientSession
from bs4 import BeautifulSoup

logging.basicConfig(
    format="%(asctime)s %(levelname)s:%(name)s: %(message)s",
    level=logging.DEBUG,
    datefmt="%H:%M:%S",
    stream=sys.stderr,
)
logger = logging.getLogger("areq")
logging.getLogger("chardet.charsetprober").disabled = True

# Maximum link count
WORKER_COUNT = 10


class FetchFailure(Exception):
    """Raised when url fetch failed"""

    pass


@dataclass
class Meta:
    gallery_id: str
    img_url: str
    page_count: int


async def fetch(url: str, session: ClientSession, **kwargs) -> aiohttp.ClientResponse:
    """Get request wrapper to fetch pictures"""
    try:
        resp = await session.request(method="GET", url=url, **kwargs)
        resp.raise_for_status()
    except (
        aiohttp.ClientError,
        aiohttp.http_exceptions.HttpProcessingError,
    ) as e:
        logger.error(
            "aiohttp exception for %s [%s]: %s",
            url,
            getattr(e, "status", None),
            getattr(e, "message", None),
        )
    except Exception as e:
        logger.exception(
            "Non-aiohttp exception occured:  %s", getattr(e, "__dict__", {})
        )
    else:
        logger.info("Got response [%s] for URL: %s", resp.status, url)
        return resp
    raise FetchFailure("Fetch failed for URL {}".format(url))


async def fetch_jpg(url: str, session: ClientSession, **kwargs) -> bytes:
    """Get request wrapper to fetch pictures"""
    resp = await fetch(url=url, session=session, **kwargs)
    jpg = await resp.read()
    logger.info("Unpack jpg for URL: %s", url)
    return jpg


async def fetch_html(url: str, session: ClientSession, **kwargs) -> str:
    """Get request wrapper to fetch HTML"""
    resp = await fetch(url=url, session=session, **kwargs)
    html = await resp.text()
    logger.info("Unpack html for URL: %s", url)
    return html


async def write_one(filepath: str, url: str, **kwargs) -> None:
    try:
        jpg = await fetch_jpg(url, **kwargs)
    except FetchFailure:
        logger.error("Fetch failed for URL %s", url)
    else:
        async with aiofiles.open(filepath, "wb") as f:
            await f.write(jpg)
        logger.info("Wrote results for source URL: %s", url)


async def construct_task_queue(meta: Meta) -> asyncio.Queue:
    queue = asyncio.Queue()
    for i in range(1, meta.page_count + 1):
        await queue.put(i)
    logger.info("Constructed task queue for %s", meta)
    return queue


async def worker(
    queue: asyncio.Queue, meta: Meta, outpath: pathlib.Path, **kwargs
) -> None:
    while True:
        page = await queue.get()
        imgname = str(page) + ".jpg"
        url = urljoin(meta.img_url, imgname)
        filepath = outpath.joinpath(imgname)
        await write_one(filepath=filepath, url=url, **kwargs)
        queue.task_done()


async def crawl_and_write(nid: str, outpath: pathlib.Path, **kwargs) -> None:
    meta = await get_meta(nid)
    queue = await construct_task_queue(meta)

    async with ClientSession() as session:
        workers = [
            asyncio.create_task(worker(queue, meta, outpath, session=session, **kwargs))
            for _ in range(WORKER_COUNT)
        ]
        await queue.join()
        for c in workers:
            c.cancel()


async def get_meta(nid: str, **kwargs) -> Meta:
    url = urljoin("https://nhentai.net/g/", nid)

    async with ClientSession() as session:
        # if failed to fetch meta data, just die.
        html = await fetch_html(url=url, session=session, **kwargs)
        soup = BeautifulSoup(html, features="lxml")

        # WARNING: Dirty!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        #          I'm not quite into those front end stuff...
        cover_url = soup.find_all(attrs={"id": "cover"})[0].find_all(
            "img", attrs={"class": None}
        )[0]["src"]
        img_url = urljoin(cover_url, ".").replace("t.nhentai.net", "i.nhentai.net")
        page_count = int(soup.find_all("span", attrs={"class": "name"})[-1].text)

    return Meta(nid, img_url, page_count)


if __name__ == "__main__":
    import os
    import sys

    assert sys.version_info >= (3, 7), "Script requires Python 3.7+."
    assert (
        len(sys.argv) == 2 and sys.argv[1].isdigit()
    ), "\nUsage:\n$ python ncurl.py 383251"

    nid = sys.argv[1]
    here = pathlib.Path(__file__).parent
    outpath = here.joinpath(nid)
    if not os.path.exists(outpath):
        os.makedirs(outpath)

    asyncio.run(crawl_and_write(nid, outpath))
