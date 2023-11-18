from yt_dlp import YoutubeDL
from urllib.parse import urlparse
from urllib.request import urlopen
import requests

from bs4 import BeautifulSoup
import json
import re
import time

from ast import literal_eval
from contextlib import suppress
from tqdm.auto import tqdm
from typing import Any, Callable, Dict, List, Optional, TypeVar
import datetime as dt
import eyed3
import logging
import os
import shutil
import sys
import traceback

DOWNLOAD_DIR = "download/"
IMAGE_DIR = "images/"
LOG_FILE = "log.json"

JSON_LOG = '{"levelname":"%(levelname)s", "funcName":"%(funcName)s", "message":"%(message)s", "asctime":"%(asctime)s"},'

HEADERS = lambda url: {
    "authority": urlparse(url).hostname,
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "accept-language": "ja-JP,ja;en-US,en;q=0.9,ko-KR;q=0.8,ko;q=0.7",
    "sec-ch-ua": '"Google Chrome";v="107", "Chromium";v="107", "Not=A?Brand";v="24"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"macOS"',
    "sec-fetch-dest": "document",
    "sec-fetch-mode": "navigate",
    "sec-fetch-site": "same-origin",
    "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36",
}

_KT = TypeVar("_KT")
_VT = TypeVar("_VT")

ydl_opts = {
    'format': 'bestaudio/best',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '320',
    }],
}


class YtDlpDownloader:
    def __init__(self, urls: List[str]):
        self.logger = CustomLogger("ytdlp", file='_'.join([self.get_name(),LOG_FILE]))
        self.urls = urls
        self.results = list()
        self.errors = list()

    def download(self):
        session = requests.Session()
        for url in tqdm(self.urls, desc=f"downloading {self.get_name()}"):
            try:
                with YoutubeDL(ydl_opts) as ydl:
                    ydl.download(url)
                with suppress(Exception):
                    info = self.fetch(session, url)
                    if info: self.tag(info)
            except Exception as exception:
                with suppress(Exception):
                    self.fetch(session, url)
                error_msg = ' '.join(traceback.format_exception(*sys.exc_info()))
                error_msg = error_msg.replace('\\','\\\\').replace('\n','\\n').replace('\"','\\"')
                self.errors.append({"url":url, "error":error_msg})
            time.sleep(1)
        session.close()
        self.save_results()
        self.logger.fit_json_log()

    def fetch(self, session: requests.Session, url: str) -> Dict[str,str]:
        response = session.get(url, headers=HEADERS(url))
        self.logger.info({"url":url, "status":response.status_code, "length":len(response.text)})
        info = self.parse(response.text)
        self.results.append(info)
        return info

    def parse(self, response: str) -> Dict[str,str]:
        return {"response": response}

    def tag(self, info: Dict[str,str]):
        title = info.get("title").replace(' ','')
        mp3files = [file for file in os.listdir() if file.endswith(".mp3")]
        mp3files += [file for file in os.listdir() if title in file and file.endswith(".mp3")]
        if mp3files:
            mp3file = mp3files[-1]
            audiofile = eyed3.load(mp3file)
            audiofile.tag.title = info.get("title")
            audiofile.tag.artist = info.get("artist")
            audiofile.tag.album = info.get("album")
            audiofile.tag.recording_date = info.get("year")
            audiofile.tag.genre = "Utaite" if "歌ってみた" in info.get("title") else "Vocaloid"
            audiofile.tag.composer = info.get("composer")
            with suppress(Exception):
                image = self.fetch_image(url=info.get("thumb"), file=IMAGE_DIR+re.sub(".mp3",".jpg",mp3file))
                audiofile.tag.images.set(type_=3, img_data=image, mime_type="image/jpeg")
            audiofile.tag.save()
        for mp3file in set(mp3files):
            shutil.move(mp3file, re.sub("\s*\[[^]]*\]\.mp3$", ".mp3", DOWNLOAD_DIR+mp3file))

    def fetch_image(self, url: str, file: str) -> bytes:
        response = urlopen(url)
        image = response.read()
        self.logger.info({"name":file, "status":response.status, "length":len(image)})
        with open(file, "wb") as handler:
            handler.write(image)
        return image

    def hier_get(self, __m: Dict, __path: List[_KT], default=None, apply: Optional[Callable]=None, **kwargs) -> _VT:
        try:
            for key in __path:
                __m = __m[key]
            value = __m if __m else default
            return apply(value) if apply else value
        except Exception:
            return default

    def save_results(self):
        results = {"results":self.results, "errors":self.errors}
        now = dt.datetime.now().strftime("%Y%m%d%H%M%S")
        with open('_'.join([self.get_name(),now])+".json", "w", encoding="utf-8") as f:
            json.dump(results, f, indent=2, ensure_ascii=False)

    def get_name(self) -> str:
        return "music"


class BiliDownloader(YtDlpDownloader):
    def parse(self, response: str) -> Dict[str,str]:
        source = BeautifulSoup(response, 'html.parser')
        script = source.find("script", text=re.compile(".*window\.__INITIAL_STATE__.*")).text
        script = re.sub("window\.__INITIAL_STATE__=", "", script)
        script = re.sub(";\(function\(\).*;$", "", script)
        data = json.loads(script)
        return self.map_info(data) if data else dict()

    def map_info(self, data: Dict[str,Any]) -> Dict[str,str]:
        info = dict()
        info["type"] = "bilibili"
        info["id"] = str(self.hier_get(data, ["videoData","bvid"], str()))
        info["url"] = "https://www.bilibili.com/video/"+info["id"]
        info["title"] = info["album"] = str(self.hier_get(data, ["videoData","title"], str()))
        info["desc"] = str(self.hier_get(data, ["videoData","desc"], str()))
        info["date"] = self.hier_get(data, ["videoData","pubdate"], apply=dt.datetime.fromtimestamp)
        if isinstance(info.get("date"), dt.datetime):
            info["year"] = info["date"].year
            info["date"] = info["date"].strftime("%Y-%m-%d %H:%M:%S")
        info["thumb"] = self.hier_get(data, ["videoData","pic"], str())
        info["composer"] = ', '.join([f'[{staff.get("title")}]{staff.get("name")}'
            for staff in data.get("staffData", list()) if isinstance(staff, dict)])
        info["tags"] = [tag.get("tag_name") for tag in data.get("tags", list())
            if isinstance(tag, dict) and tag.get("tag_name") in VOCALOIDS]
        artist = re.search("(?<=【)(.*?)(?=原创曲】)", info["title"])
        artist = ', '.join(artist.group().split('·') if artist else info.get("tags", list()))
        owner = str(self.hier_get(data, ["videoData","owner","name"], str()))
        info["artist"] = " feat. ".join([owner, artist]).strip()
        self.logger.debug(info)
        return info

    def get_name(self) -> str:
        return "bili"


class NicoDownloader(YtDlpDownloader):
    def parse(self, response: str) -> Dict[str,str]:
        source = BeautifulSoup(response, 'html.parser')
        raw_data = source.select_one("div#js-initial-watch-data").attrs.get("data-api-data",str())
        data = json.loads(raw_data)
        return self.map_info(data) if data else dict()

    def map_info(self, data: Dict[str,Any]) -> Dict[str,str]:
        info = dict()
        info["type"] = "nicovideo"
        info["id"] = str(self.hier_get(data, ["video","id"], str()))
        info["url"] = "https://www.nicovideo.jp/watch/"+info["id"]
        info["title"] = info["album"] = str(self.hier_get(data, ["video","title"], str()))
        info["desc"] = str(self.hier_get(data, ["video","description"], str()))
        strptime = lambda date: dt.datetime.strptime(date, "%Y-%m-%dT%H:%M:%S%z")
        info["date"] = self.hier_get(data, ["video","registeredAt"], apply=strptime)
        if isinstance(info.get("date"), dt.datetime):
            info["year"] = info["date"].year
            info["date"] = info["date"].strftime("%Y-%m-%d %H:%M:%S")
        info["thumb"] = self.hier_get(data, ["video","thumbnail","ogp"], str())
        info["composer"] = str(self.hier_get(data, ["owner","nickname"], str()))
        if not info["composer"]: info["composer"] = str(self.hier_get(data, ["channel","name"], str()))
        info["tags"] = [tag.get("name") for tag in self.hier_get(data, ["tag","items"], list())
            if isinstance(tag, dict) and tag.get("name") in VOCALOIDS]
        artist = ', '.join(info["tags"] if info["tags"] else [voca for voca in VOCALOIDS if voca in info["title"]])
        info["artist"] = info.pop("composer") if True in [match in info["title"] for match in UTAITE] else \
                            " feat. ".join([info["composer"], artist]).strip()
        self.logger.debug(info)
        return info

    def get_name(self) -> str:
        return "nico"


class CustomLogger(logging.Logger):
    def __init__(self, name=__name__, level=logging.INFO, file=str()):
        super().__init__(name, level)
        self.file = file
        formatter = logging.Formatter(fmt=JSON_LOG, datefmt="%Y-%m-%d %H:%M:%S")
        handler = logging.FileHandler(file, encoding="utf-8") if file else logging.StreamHandler()
        handler.setLevel(level)
        handler.setFormatter(formatter)
        self.addHandler(handler)

    def parse_message(self, message: str):
        msg_part = re.search('"message":"\{.*\}",', message)
        if msg_part:
            dict_msg = str(literal_eval(re.search('(?<="message":")(\{.*\})(?=",)', message).group()))
            dict_msg = dict_msg.replace('\'','\"').replace("\": ","\":")[1:-1]+','
            message = message.replace(msg_part.group(), dict_msg)
        return message.replace(": True",": true").replace(": False",": false").replace(": None",": null")

    def fit_json_log(self, log_file=str()):
        log_file = log_file if log_file else self.file
        if not os.path.exists(log_file): return
        with open(log_file, "r", encoding="utf-8") as f:
            log = f.readlines()
            if '}\n' in log:
                new_index = log.index('}\n')+1
                if len(log) == new_index: return
                new_log = [' '*4+line for line in log[new_index:]]
                new_log = [self.parse_message(line) for line in new_log]
                new_log[-1] = re.sub(",$", "", new_log[-1])
                log[new_index-3] = log[new_index-3].replace("\n", ",\n").replace("[,","[")
                log = log[:new_index-2]+new_log+log[new_index-2:new_index]
            else:
                log = [self.parse_message(line) for line in log]
                log = ["{\n", '  "log": [\n']+[' '*4+line for line in log]+["  ]\n","}\n"]
                log[-3] = re.sub(",$", "", log[-3])
        with open(log_file, "w", encoding="utf-8") as f:
            f.writelines(log)


VOCALOIDS = [
    '#kzn', 'AiSuu', 'Flower', 'Fukase', 'Fιφne', 'GUMI', 'GUMI English', 'GUMI sweet', 'Gumi English',
    'IA', 'IA ROCKS', 'KAFU', 'KAITO', 'Kaora', 'Kaori', 'Ken', 'Kevin', 'LOLA', 'LUMi', 'Lily', 'MEIKO',
    'Mai', 'Mew', 'Minus', 'ONE', 'Oliver', 'POPY', 'Rana', 'Ruby', 'Saki AI', 'SeeU', 'UNI', 'VY1',
    'VY1V3', 'VY1V4', 'VY2', 'VY2V3', 'flower', 'kaori', '시우', '시유', '유니', '이지음', '카일린',
    'さとうささら', 'すずきつづみ', 'すずきつづみ', 'ずんだもん', 'ついなちゃん', 'りむる', 'ギャラ子', 'ギャラ子 NEO', 'ダイナミック自演ズ',
    'ネネロボ', 'マユ', '东方栀子', '乐正兄妹', '乐正绫', '乐正龙牙', '健音テイ', '冥鳴ひまり', '初音ミク', '叁琏', '可不',
    '墨清弦', '夏色花梨', '夏语遥', '天碎瓷', '宮下遊', '小春六花', '巡音ルカ', '幻晓伊', '弦巻マキ', '徴羽摩柯', '徵羽摩柯',
    '心华', '星尘', '星尘Infinity', '星尘Minus', '星界', '暗鳴ニュイ', '東北きりたん', '東北ずん子', '東北イタコ', '极光体',
    '桜乃そら', '歌愛ユキ', '泠鸢', '洛天依', '海伊', '牧心', '狐子', '狐狸座', '猫村いろは', '琴葉茜', '琴葉葵',
    '留音ロッカ', '知声', '神威がくぽ', '神威がくぽ', '紲星あかり', '結月ゆかり', '羽累', '花隈千冬', '苍穹', '草薙寧々',
    '裏命', '言和', '诗岸', '赤羽', '重音テト', '鏡音リン', '鏡音レン', '铃霜', '闇音レンリ', '青溯', '音街ウナ', '香鈴',
    '鳴花ヒメ', '鳴花ミコト', '鸾明']

UTAITE = ["歌って", "歌ってみた", "歌いました"]


def main():
    if not os.path.exists(DOWNLOAD_DIR): os.mkdir(DOWNLOAD_DIR)
    if not os.path.exists(IMAGE_DIR): os.mkdir(IMAGE_DIR)
    if os.path.exists("urls.txt"):
        with open("urls.txt", "r", encoding="utf-8") as f:
            urls = [url.strip() for url in f.readlines()]
        bili_urls = [url for url in urls if "www.bilibili.com" in url]
        nico_urls = [url for url in urls if "www.nicovideo.jp" in url]
        bili = BiliDownloader(bili_urls)
        nico = NicoDownloader(nico_urls)
        bili.download()
        nico.download()


if __name__ == "__main__":
    main()
