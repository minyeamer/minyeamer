from typing import Any, Dict, List, Optional, Union
from pathlib import Path
from urllib.parse import urlparse
import argparse
import datetime as dt
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
import requests

ROOT = os.path.join(os.getcwd(), "downloaded")
URLS_LOG = "urls.txt"
DRIVER_LOG = "log.json"
DOWNLOAD_LOG = "log_image.json"

HEADERS = lambda url, referer: {
    "authority": urlparse(url).hostname,
    "accept": "image/avif, image/webp, image/apng, */*",
    "accept-language": "en-US,en;q=0.9,ko-KR;q=0.8,ko;q=0.7",
    "sec-ch-ua": '"Google Chrome";v="105", "Not)A;Brand";v="8", "Chromium";v="105"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"macOS"',
    "sec-fetch-dest": "document",
    "sec-fetch-mode": "navigate",
    "sec-fetch-site": "same-origin",
    "referer": referer,
    "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36",
}

INDEX_URL = lambda page: f"https://hitomi.la/index-korean.html?page={str(page)}"
GALLERY_PATTERN = re.compile("https://ltn.hitomi.la/galleryblock/(\d+).html")
GALLERY_URL = lambda id, page=1: f"https://hitomi.la/doujinshi/-{str(id)}.html#{str(page)}"
READER_URL = lambda id: f"https://hitomi.la/reader/{id}.html"

THUMB_PATTERN = re.compile("https://([ab])tn\.hitomi\.la/avifsmallsmalltn/([\w\d+]+)/([\w\d+]+)/([\w\d+]+)\.avif")
IMAGE_URL = lambda a, b, s, i: f"https://{a}a.hitomi.la/webp/{b}/{s}/{i}.webp"
TIMESTAMP_PATTERN = "b: '(\d+)/'"
TIMESTAMP_URL = lambda t=str(dt.datetime.now().timestamp()): f"https://ltn.hitomi.la/gg.js?_={t}"
TIMESTAMP_SUB_PATTERN = re.compile("(?<=webp/)(\d+)(?=/)")

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
    def __init__(self, path: str, urls: Optional[List[str]]=list(), **kwargs):
        try: service = Service(executable_path=ChromeDriverManager().install())
        except: service = Service(executable_path="./chromedriver")
        super().__init__(service=service, **kwargs)
        self.implicitly_wait(3)
        self.root = Path(path)
        self.root.mkdir(exist_ok=True)
        self.urls = [id if id.isdigit() else re_get("\d+",id) for id in urls]
        self.images = list()
        self.results = list()
        self.errors = list()

    def fetch_urls(self, history: str):
        for page in range(1, 100):
            print(f"Gathering urls from page {str(page)}")
            self.execute_script(CLEAR_SCRIPT)
            self.get(INDEX_URL(page))
            self.refresh()
            time.sleep(0.5)
            logs = self.execute_script(LOG_SCRIPT)
            for log in logs:
                id = re_get(GALLERY_PATTERN, get(log,"name"))
                if id == history: return self.save_urls()
                if id: self.urls.append(id)

    def read_urls(self):
        with open(os.path.join(os.getcwd(), URLS_LOG), "r", encoding="utf-8") as f:
            self.urls = [url.strip() for url in f.readlines()]

    def save_urls(self):
        with open(os.path.join(os.getcwd(), URLS_LOG), "w", encoding="utf-8") as f:
            f.writelines(self.urls)

    def gather_images(self):
        for id in tqdm(self.urls, desc="Gathering images from urls"):
            self.execute_script(CLEAR_SCRIPT)
            try:
                self.fetch_images(id)
                self.parse_images(id)
                self.download_images()
            except Exception as e:
                self.errors.append({"id":id, "url":GALLERY_URL(id), "path":str(), "error":str(e)})

    def fetch_images(self, id: str):
        prev = 0
        for page in range(1, 100):
            self.get(GALLERY_URL(id, page))
            self.refresh()
            time.sleep(0.5)
            logs = self.execute_script(LOG_SCRIPT)
            cur = len([get(log,"name") for log in logs if THUMB_PATTERN.search(get(log,"name"))])
            if (cur-prev) < 50: break
            prev = cur

    def parse_images(self, id: str):
        dir = self.get_image_dir(id)
        logs = self.execute_script(LOG_SCRIPT)
        thumbs = [re_get(THUMB_PATTERN, get(log,"name")) for log in logs
                if THUMB_PATTERN.search(get(log,"name"))]
        b = fetch_timestamp(id)
        for idx, (a, m1, m2, i) in enumerate(thumbs, start=1):
            self.images.append({"id":id, "url":IMAGE_URL(a,b,int(m1+m2,16),i), "path":str(dir/f"{str(idx)}.webp")})

    def get_image_dir(self, id: str) -> Path:
        title = self.find_element(By.CSS_SELECTOR, "h1#gallery-brand").text
        artist = self.find_element(By.CSS_SELECTOR, "h2#artists").text
        artist = f"[{artist}]" if 'N/A' not in artist else str()
        dir = self.root / INVALID_PATTERN.sub('', ' '.join([artist,title,f"({id})"])).strip()
        dir.mkdir(exist_ok=True)
        return dir

    def download_images(self):
        downloader = HitomiDownloader(self.images, self.root)
        downloader.download()
        self.images = list()
        self.results += downloader.results
        self.errors += downloader.errors

    def log_json(self, name: str, file: str, filter: Optional[List]=list()):
        path = os.path.join(os.getcwd(), file)
        history = max(*self.urls, str())
        log = {"history":history, "results":self.results, "errors":self.errors}
        log = {k:v for k,v in log.items() if k in filter} if filter else log
        with open(path, "w", encoding="utf-8") as f:
            json.dump(log, f, ensure_ascii=False, indent=2)
        print(f"{name} log saved at {str(path)}")


class HitomiDownloader():
    def __init__(self, images: List[Dict[str,str]], path: str):
        self.root = Path(path)
        self.root.mkdir(exist_ok=True)
        self.images = images
        self.results = list()
        self.errors = list()

    def download(self, timestamp=False):
        b = fetch_timestamp() if timestamp else str()
        asyncio.run(self.gather_images(b=b))

    async def gather_images(self, b=str()):
        async with aiohttp.ClientSession() as session:
            await tqdm.gather(*[self.fetch_image(session, b=b, **image) for image in self.images], desc="Downloading images")

    async def fetch_image(self, session: aiohttp.ClientSession, id: str, url: str, path: str, b=str(), **kwargs):
        try:
            if b: url = TIMESTAMP_SUB_PATTERN.sub(b, url)
            for i in range(5):
                if os.path.exists(path):
                    self.results.append({"id":id, "url":url, "path":path})
                    break
                if i > 1: url = TIMESTAMP_SUB_PATTERN.sub(fetch_timestamp(id), url)
                async with session.get(url, headers=HEADERS(url, READER_URL(id))) as response:
                    if response.status != 200:
                        await asyncio.sleep(i/5)
                        continue
                    async with aiofiles.open(path, mode='wb') as f:
                        await f.write(await response.read())
        except Exception as e:
            self.errors.append({"id":id, "url":url, "path":path, "error":str(e)})

    def log_json(self, name: str, file: str, filter: Optional[List]=list()):
        path = os.path.join(os.getcwd(), file)
        log = {"results":self.results, "errors":self.errors}
        log = {k:v for k,v in log.items() if k in filter} if filter else log
        with open(path, "w", encoding="utf-8") as f:
            json.dump(log, f, ensure_ascii=False, indent=2)
        print(f"{name} log saved at {str(path)}")


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


def fetch_timestamp(id: str) -> str:
    url = TIMESTAMP_URL()
    response = requests.get(url, headers=HEADERS(url, GALLERY_URL(id)))
    return re_get(TIMESTAMP_PATTERN, response.text)


def run_driver(history=str(), debug=False):
    options = set_chrome_options(debug)
    name, log, filter = "Download", DOWNLOAD_LOG, ["results", "errors"]
    print("Start requests")
    start = time.time()
    driver = HitomiDriver(path=ROOT, chrome_options=options)
    if history:
        driver.fetch_urls(history)
        name, log, filter = "Driver", DRIVER_LOG, ["history"]+filter
    else: driver.read_urls()
    driver.gather_images()
    driver.close()
    print("Finish requests")
    print(f"Elapsed time: {round(time.time()-start,1)}s")
    driver.log_json(name, log, filter)


def run_downloader():
    images = list()
    driver_log = os.path.join(os.getcwd(), DRIVER_LOG)
    download_log = os.path.join(os.getcwd(), DOWNLOAD_LOG)
    log_file = download_log if os.path.exists(download_log) else driver_log
    with open(log_file, "r", encoding="utf-8") as f:
        images = json.loads(''.join([line for line in f.readlines()]))["errors"]
    downloader = HitomiDownloader(images, path=ROOT)
    downloader.download()
    downloader.log_json("Downloader", DOWNLOAD_LOG)


if __name__ == "__main__":
    args = set_arguments()
    if args.mode in ["default", "urls"]:
        run_driver(args.history, debug=(args.debug=="debug"))
    elif args.mode in ["images"]:
        run_downloader()
    else: raise Exception("Invalid mode entered:", args.mode)
