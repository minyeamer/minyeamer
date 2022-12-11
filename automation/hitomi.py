from typing import Any, Dict, List, Optional, Union
from pathlib import Path
from urllib.parse import urlparse
import argparse
import json
import os
import re

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import time
import warnings
warnings.filterwarnings("ignore")

from tqdm.asyncio import tqdm
import asyncio
import aiohttp
import aiofiles
import functools
import requests

ROOT = os.path.join(os.getcwd(), "downloaded")
URLS_LOG = "urls.txt"
DRIVER_LOG = "log.json"
DOWNLOAD_LOG = "log_image.json"

HEADERS = lambda url, referer=str(): dict({
    "authority": urlparse(url).hostname,
    "accept": "image/avif, image/webp, image/apng, */*",
    "accept-language": "en-US,en;q=0.9,ko-KR;q=0.8,ko;q=0.7",
    "sec-ch-ua": '"Google Chrome";v="105", "Not)A;Brand";v="8", "Chromium";v="105"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"macOS"',
    "sec-fetch-dest": "document",
    "sec-fetch-mode": "navigate",
    "sec-fetch-site": "same-origin",
    "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36",
}, **({"referer": referer} if referer else dict()))

INDEX_URL = lambda page: f"https://hitomi.la/index-korean.html?page={str(page)}"
GALLERY_PATTERN = re.compile("https://ltn.hitomi.la/galleryblock/(\d+).html")
GALLERY_URL = lambda id, page=1: f"https://hitomi.la/doujinshi/-{str(id)}.html#{str(page)}"
READER_URL = lambda id: f"https://hitomi.la/reader/{id}.html"

THUMB_PATTERN = re.compile("https://([ab])tn\.hitomi\.la/(avif|webp)(small){1,6}tn/([\w\d+]+)/([\w\d+]+)/([\w\d+]+)\.(avif|webp)")
IMAGE_URL = lambda a, b, s, i: f"https://{a}a.hitomi.la/webp/{b}/{s}/{i}.webp"
TIMESTAMP_PATTERN = "b: '(\d+)/'"
TIMESTAMP_URL = "https://ltn.hitomi.la/gg.js"
TIMESTAMP_SUB_PATTERN = re.compile("(?<=webp/)(\d+)(?=/)")
DEFAULT_TIMEOUT = 30

LOG_SCRIPT = "return network = window.performance.getEntries();"
CLEAR_SCRIPT = "window.performance.clearResourceTimings();"

INVALID_PATTERN = re.compile("[\\/:*?\"<>|]")

def get(_dict: Dict, key: str, default=str()) -> Any:
    try: return _dict[key]
    except: return default

def re_get(pattern: Union[re.Pattern,str], string: str) -> Union[List[str],str]:
    pattern = pattern if isinstance(pattern,re.Pattern) else re.compile(pattern)
    match = pattern.search(string)
    return (match.groups() if len(match.groups())>1 else match[1]) if match else str()


class HitomiDriver(webdriver.Chrome):
    def __init__(self, path: str, urls: Optional[List[str]]=list(), history=str(), download=True, **kwargs):
        try: service = Service(executable_path=ChromeDriverManager().install())
        except: service = Service(executable_path="./chromedriver")
        super().__init__(service=service, **kwargs)
        self.root = Path(path)
        self.root.mkdir(exist_ok=True)
        self.history = history
        self.download = download
        self.urls = [id if id.isdigit() else re_get("\d+",id) for id in urls]
        self.images = list()
        self.messages = list()
        self.results = list()
        self.errors = list()

    def fetch_urls(self, history=str()):
        history = history if history else self.history
        for page in range(1, 100):
            print(f"Gathering urls from page {str(page)}")
            self.execute_script(CLEAR_SCRIPT)
            self.get(INDEX_URL(page))
            self.refresh()
            time.sleep(1)
            logs = self.execute_script(LOG_SCRIPT)
            self.messages.append(f"page {(str(page))} has {str(len(logs))} logs")
            for log in logs:
                id = re_get(GALLERY_PATTERN, get(log,"name"))
                if id == history:
                    if self.urls: self.history = self.urls[0]
                    return self.save_urls()
                if id: self.urls.append(id)

    def read_urls(self):
        with open(URLS_LOG, "r", encoding="utf-8") as f:
            self.urls = [id.strip() if id.strip().isdigit() else re_get("\d+",id) 
                for id in f.readlines()]
        self.messages.append(f"read {str(len(self.urls))} urls")

    def save_urls(self):
        with open(URLS_LOG, "w", encoding="utf-8") as f:
            f.write('\n'.join(self.urls))
        self.messages.append(f"saved {str(len(self.urls))} urls")

    def gather_images(self):
        for id in tqdm(set(self.urls), desc="Gathering images from urls"):
            self.execute_script(CLEAR_SCRIPT)
            try:
                self.fetch_images(id)
                images = self.parse_images(id)
                if self.download: self.download_images(images)
                self.images += images
            except Exception as e:
                self.errors.append({"id":id, "url":GALLERY_URL(id), "path":str(), "error":str(e)})

    def fetch_images(self, id: str):
        prev = 0
        for page in range(1, 100):
            self.get(GALLERY_URL(id, page))
            self.refresh()
            time.sleep(1)
            logs = self.execute_script(LOG_SCRIPT)
            cur = len([get(log,"name") for log in logs if THUMB_PATTERN.search(get(log,"name"))])
            if (cur-prev) < 50:
                self.messages.append(f"{id} has {str(page)} pages and {str(cur)} images")
                break
            prev = cur

    def parse_images(self, id: str) -> List[Dict]:
        images = list()
        dir = self.get_image_dir(id)
        logs = self.execute_script(LOG_SCRIPT)
        thumbs = [re_get(THUMB_PATTERN, get(log,"name")) for log in logs
                if THUMB_PATTERN.search(get(log,"name"))]
        b = fetch_timestamp(id)
        for idx, (a, _, _, m1, m2, i, _) in enumerate(thumbs, start=1):
            images.append({"id":id, "url":IMAGE_URL(a,b,int(m1+m2,16),i), "path":str(dir/f"{str(idx)}.webp")})
        return images

    def get_image_dir(self, id: str) -> Path:
        title = self.find_element(By.CSS_SELECTOR, "h1#gallery-brand").text
        artist = self.find_element(By.CSS_SELECTOR, "h2#artists").text
        artist = f"[{artist}]" if 'N/A' not in artist else str()
        dir = self.root / INVALID_PATTERN.sub('', ' '.join([artist,title,f"({id})"])).strip()
        dir.mkdir(exist_ok=True)
        return dir

    def download_images(self, images: List[Dict]):
        downloader = HitomiDownloader(images, self.root, loop=False, timeout=DEFAULT_TIMEOUT)
        downloader.download()
        self.results += downloader.results
        # self.errors += downloader.errors

    def log_json(self, name: str, file: str, filter: Optional[List]=list()):
        filter = filter if filter else ["images","messages","errors"]
        filter = ["history"]+filter if self.history else filter
        logs = {k:v for k,v in self.__dict__.items() if k in filter}
        with open(file, "w", encoding="utf-8") as f:
            json.dump(logs, f, ensure_ascii=False, indent=2, default=(lambda _:"Non-serializable text"))
        print(f"{name} log saved at {file}")


class HitomiDownloader():
    def __init__(self, images: List[Dict[str,str]], path: str, loop=True, timeout=0):
        self.root = Path(path)
        self.root.mkdir(exist_ok=True)
        self.loop = loop
        self.timeout = timeout
        self.timestamp = str()
        self.images = images
        self.results = list()
        self.errors = list()

    def download(self):
        asyncio.run(self.gather_images())

    async def gather_images(self):
        while self.images:
            self.timestamp = fetch_timestamp()
            async with aiohttp.ClientSession() as session:
                await tqdm.gather(*[self.fetch_image(session, **image) for image in self.images], desc="Downloading images")
            if not self.loop: break
            self.log_json("Downloader", DOWNLOAD_LOG)
            self.refresh_images()
            asyncio.sleep(1)

    async def fetch_image(self, session: aiohttp.ClientSession,
                            id: str, url: str, path: str, **kwargs):
        try:
            if (os.path.exists(path) and (os.stat(path).st_size > 1024)): return
            url = TIMESTAMP_SUB_PATTERN.sub(self.timestamp, url)
            timeout = {"timeout":self.timeout} if self.timeout else dict()
            async with session.get(url, headers=HEADERS(url, READER_URL(id)), **timeout) as response:
                if response.status == 200:
                    async with aiofiles.open(path, mode='wb') as f:
                        await f.write(await response.read())
            if not (os.path.exists(path) and (os.stat(path).st_size > 1024)):
                error = aiohttp.ClientError(f"Response status {response.status}")
                self.errors.append({"id":id, "url":url, "path":path, "error":error})
            else: self.results.append({"id":id, "url":url, "path":path})
        except Exception as e:
            self.errors.append({"id":id, "url":url, "path":path,"error":str(e)})

    def refresh_images(self):
        self.images = list()
        for _ in range(len(self.errors)):
            error = self.errors.pop()
            error["url"] = self.toggle_hostname(error["url"])
            self.images.append(error)

    def toggle_hostname(self, url: str) -> str:
        toggle = {"aa.hitomi.la":"ba.hitomi.la","ba.hitomi.la":"aa.hitomi.la"}
        hostname = urlparse(url).hostname
        return url.replace(hostname,toggle.get(hostname,hostname))

    def log_json(self, name: str, file: str, filter: Optional[List]=list()):
        filter = filter if filter else ["results","errors"]
        log = {k:v for k,v in self.__dict__.items() if k in filter}
        with open(file, "w", encoding="utf-8") as f:
            json.dump(log, f, ensure_ascii=False, indent=2, default=(lambda _:"Non-serializable text"))
        print(f"{name} log saved at {file}")


def set_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Hitomi Downloader")
    parser.add_argument("--d", "--debug", dest="debug", type=str, default="debug")
    parser.add_argument("--h", "--history", dest="history", type=str, default=str(), required=False)
    parser.add_argument("--m", "--mode", dest="mode", type=str, default="default")
    return parser.parse_args()


def set_chrome_options(debug=False) -> Options:
    options = Options()
    options.headless = True
    if debug: options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
    return options


def fetch_timestamp(id=str()) -> str:
    referer = GALLERY_URL(id) if id else str()
    response = requests.get(TIMESTAMP_URL, headers=HEADERS(TIMESTAMP_URL, referer))
    return re_get(TIMESTAMP_PATTERN, response.text)


def run_driver(history=str(), download=False, debug=False):
    options = set_chrome_options(debug)
    print("Start requests")
    start = time.time()
    driver = HitomiDriver(path=ROOT, history=history, download=download, chrome_options=options)
    if history: driver.fetch_urls()
    else: driver.read_urls()
    driver.gather_images()
    driver.log_json("Driver", DRIVER_LOG)
    images = driver.images.copy()
    driver.close()
    run_downloader(images)
    print("Finish requests")
    print(f"Elapsed time: {round(time.time()-start,1)}s")


def run_downloader(images: Optional[List]=list()):
    if not images:
        log_file, key = (DOWNLOAD_LOG,"errors") if os.path.exists(DOWNLOAD_LOG) else (DRIVER_LOG,"images")
        with open(log_file, "r", encoding="utf-8") as f:
            images = json.loads(''.join([line for line in f.readlines()]))[key]
    downloader = HitomiDownloader(images, path=ROOT)
    downloader.download()
    downloader.log_json("Downloader", DOWNLOAD_LOG)


if __name__ == "__main__":
    args = set_arguments()
    if args.mode in ["default", "download", "urls"]:
        run_driver(args.history, download=(args.mode=="download"), debug=(args.debug=="debug"))
    elif args.mode in ["images"]:
        run_downloader()
    else: raise Exception("Invalid mode entered:", args.mode)
