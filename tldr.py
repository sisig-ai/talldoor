import os
import zipfile

import aiohttp


def tldr_pages_downloaded() -> bool:
    return os.path.exists("tldr-pages.en.zip")


def tldr_pages_unzipped() -> bool:
    return os.path.exists("tldr-pages")


async def download_tldr_pages():
    print("Downloading tldr-pages.en.zip")
    async with aiohttp.ClientSession() as session:
        async with session.get(
            "https://github.com/tldr-pages/tldr/releases/latest/download/tldr-pages.en.zip"
        ) as resp:
            with open("tldr-pages.en.zip", "wb") as f:
                f.write(await resp.read())
                print("Downloaded tldr-pages.en.zip")


def unzip_tldr_pages():
    print("Unzipping tldr-pages.en.zip")
    with zipfile.ZipFile("tldr-pages.en.zip", "r") as zip_ref:
        zip_ref.extractall("tldr-pages")
        print("Unzipped tldr-pages.en.zip")
