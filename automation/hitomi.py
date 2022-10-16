from typing import Dict, List
from contextlib import suppress
from pathlib import Path
import argparse
import json
import time
import re
import os

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager

from tqdm.asyncio import tqdm
import asyncio
import aiohttp
import aiofiles

DRIVER_LOG = "log.json"
DOWNLOAD_LOG = "log_image.json"

HEADERS = lambda id=str(): {
    "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36",
    "authority": "ba.hitomi.la",
    "accept": "image/avif, image/webp, image/apng, */*",
    "accept-language": "en-US,en;q=0.9,ko-KR;q=0.8,ko;q=0.7",
    "sec-ch-ua": '"Google Chrome";v="105", "Not)A;Brand";v="8", "Chromium";v="105"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"macOS"',
    "sec-fetch-dest": "document",
    "sec-fetch-mode": "navigate",
    "sec-fetch-site": "same-origin",
    "referer": f"https://hitomi.la/reader/{id}.html",
}


class HitomiDriver(webdriver.Chrome):
    def __init__(self, history: str, path: str):
        try: service = Service(executable_path=ChromeDriverManager().install())
        except: service = Service(executable_path="./chromedriver")
        super().__init__(service=service)
        self.root = Path(path)
        self.root.mkdir(exist_ok=True)
        self.history = str(history)
        self.page = 1
        self.images = list()
        self.results = list()
        self.errors = list()

    def start_requests(self):
        try:
            while True:
                self.fetch_index()
                self.page += 1
        except KeyboardInterrupt:
            self.close()

    def fetch_index(self) -> List[Dict[str,str]]:
        self.get(f"https://hitomi.la/index-korean.html?page={str(self.page)}")
        time.sleep(2)

        for manga in self.parse_manga():
            if manga.get("id") == self.history:
                raise KeyboardInterrupt()
            try:
                self.parse_image(**manga)
            except NoSuchElementException:
                self.errors.append(manga.get("id"))

    def parse_manga(self) -> List[Dict[str,str]]:
        manga_list = self.find_elements(By.CSS_SELECTOR, "div.gallery-content > div")
        manga_info = list()
        for manga in manga_list:
            with suppress(NoSuchElementException):
                manga_info.append({
                    "id": re.search("(\d+)(?=\.html)", manga.find_element(By.CSS_SELECTOR, 'a').get_attribute('href')).group(),
                    "title": manga.find_element(By.CSS_SELECTOR, 'h1').text.strip(),
                    "artist": manga.find_element(By.CSS_SELECTOR, 'div.artist-list').text.strip(),
                })
        return manga_info

    def parse_image(self, id: str, title: str, artist: str):
        self.get(f"https://hitomi.la/reader/{id}.html")
        time.sleep(1)
        pages = len(self.find_elements(By.CSS_SELECTOR, "select#single-page-select > option"))

        artist = f"[{artist}]" if '/' not in artist else str()
        invalid = re.compile("[\\/:*?\"<>|]")
        dir = self.root / invalid.sub("", " ".join([artist, title, f"({id})"])).strip()
        dir.mkdir(exist_ok=True)

        for page in range(1, pages+1):
            self.get(f"https://hitomi.la/reader/{id}.html#{str(page)}")
            time.sleep(0.1)
            self.images.append({
                "id": id,
                "url": self.find_element(By.CSS_SELECTOR, 'picture > img').get_attribute("src"),
                "path": str(dir / f"{str(page)}.webp")
            })
        self.results.append(id)

    def log_json(self):
        path = self.root / DRIVER_LOG
        history = max([int(image["id"]) for image in self.images])
        log = {"history":history, "images":self.images, "results":self.results, "errors":self.errors}
        with open(path, "w", encoding="utf-8") as f:
            json.dump(log, f, ensure_ascii=False, indent=2)
        print(f"Driver log saved at {str(path)}")


class HitomiDownloader():
    def __init__(self, images: List[Dict[str,str]], path: str):
        self.root = Path(path)
        self.root.mkdir(exist_ok=True)
        self.images = images
        self.errors = list()

    async def download(self):
        async with aiohttp.ClientSession() as session:
            await tqdm.gather(*[self.fetch_image(session, **image) for image in self.images])

    async def fetch_image(self, session: aiohttp.ClientSession, id: str, url: str, path: str):
        try:
            while not os.path.exists(path):
                async with session.get(url, headers=HEADERS(id=id)) as response:
                    if response.status != 200:
                        await asyncio.sleep(0.5)
                        continue
                    async with aiofiles.open(path, mode='wb') as f:
                        await f.write(await response.read())
        except Exception as e:
            self.errors.append({"id":id, "url":url, "path":path, "error":str(e)})

    def log_json(self):
        if self.errors:
            path = self.root / DOWNLOAD_LOG
            with open(path, "w", encoding="utf-8") as f:
                json.dump({"images":self.errors}, f, ensure_ascii=False, indent=2)
            print(f"Download log saved at {str(path)}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Hitomi Downloader')
    parser.add_argument("--h", "--history", dest="history", type=str)
    parser.add_argument("--m", "--mode", dest="mode", type=str, default="default", required=False)
    args = parser.parse_args()
    download_path = os.path.join(os.getcwd(), "hitomi_downloaded")

    if args.mode in ["default"]:
        print("Start Collecting image links on web browser")
        start = time.time()
        driver = HitomiDriver(history=args.history, path=download_path)
        driver.start_requests()
        print("Completely collected image links")
        print(f"Elapsed time: {round(time.time()-start,1)}s")
        driver.log_json()

    driver_log = os.path.join(download_path, DRIVER_LOG)
    download_log = os.path.join(download_path, DOWNLOAD_LOG)
    if args.mode in ["default"]:
        images = driver.images
    elif args.mode in ["recovery"] and os.path.exists(driver_log):
        with open(driver_log, "r", encoding="utf-8") as f:
            log = json.loads("".join([line for line in f.readlines()]))
            images = log["images"]
    elif args.mode in ["download"] and os.path.exists(download_log):
        with open(download_log, "r", encoding="utf-8") as f:
            log = json.loads("".join([line for line in f.readlines()]))
            images = log["images"]
    else: raise Exception("Invalid mode entered:", args.mode)

    print("Start downloading images")
    start = time.time()
    downloader = HitomiDownloader(images=images, path=download_path)
    asyncio.run(downloader.download())
    downloader.log_json()
    print("Completely downloaded images")
    print(f"Elapsed time: {round(time.time()-start,1)}s")
