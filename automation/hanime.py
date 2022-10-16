import argparse
import asyncio
import aiohttp

from collections import defaultdict
from contextlib import suppress
from typing import Dict, List
from tqdm.auto import tqdm
import json
import os

DEFAULT_TAGS = "tags.json"
DEFAULT_RENAME = "rename.json"
DEFAULT_RESULTS = "results.json"

URL = "https://search.htv-services.com/"
PAYLOAD = lambda query: {"search_text":query,"tags":[],"tags_mode":"AND","brands":[],"blacklist":[],"order_by":"created_at_unix","ordering":"desc","page":0}

HEADERS = {
    "authority": "search.htv-services.com",
    "accept": "application/json, text/plain, */*",
    "accept-encoding": "gzip, deflate, br",
    "accept-language": "en-US,en;q=0.9",
    "content-type": "application/json;charset=UTF-8",
    "origin": "https://hanime.tv",
    "sec-ch-ua": '"Chromium";v="106", "Google Chrome";v="106", "Not;A=Brand";v="99"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "\"macOS\"",
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "cross-site",
    "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36"
}


def read_json(file: str) -> Dict:
    if os.path.exists(file):
        with open(file, "r", encoding="utf-8") as f:
            return json.loads("".join([line for line in f.readlines()]))


def write_json(file: str, __d: Dict):
    with open(file, "w", encoding="utf-8") as f:
        json.dump(__d, f, indent=2, ensure_ascii=False)


async def crawl(query: List[str]) -> Dict[str,List]:
    async with aiohttp.ClientSession() as session:
        return map_dict(chain_dict(await tqdm.gather(*[fetch(session, __q) for __q in query])))


async def fetch(session: aiohttp.ClientSession, query: str) -> List[Dict]:
    response = await session.post(URL, json=PAYLOAD(query), headers=HEADERS)
    try:
        data = json.loads(await response.text())
        hits = json.loads(data["hits"])
        return [{query:{"name":hit["name"],"tags":hit["tags"]}} for hit in hits]
    except:
        return list()


def chain_dict(data: List[List[Dict]]) -> Dict[str,List]:
    __d = defaultdict(list)
    for records in data:
        for record in records:
            for key, values in record.items():
                __d[key].append(values)
    return __d


def map_dict(data: Dict[str,List]) -> Dict[str,List]:
    return {key: sorted(values, key=lambda value: value["name"]) for key, values in data.items()}


def tag_templates(root: str) -> Dict[str,Dict]:
    templates = dict()
    ROOT, DIRS, FILES = 0, 1, 2
    for sub_root in os.listdir(root):
        childs = list(os.walk(os.path.join(root,sub_root)))
        templates[sub_root] = dict()
        for dir, sub_child in zip(childs[0][DIRS],childs[1:]):
            templates[sub_root][dir] = [{"name":file,"tags":list(),"path":os.path.join(sub_child[ROOT],file)}
                                        for file in sub_child[FILES] if not is_image(file)]
        templates[sub_root]["Others"] = [{"name":file,"tags":list(),"path":os.path.join(childs[0][ROOT],file)}
                                for file in childs[0][FILES] if not is_image(file)]
    return templates


def is_image(file: str):
    return file.endswith(".jpg") or file.endswith(".png") or file.endswith(".gif") or file.endswith(".webp")


def match_templates(templates: Dict[str,Dict], tags: Dict[str,List]) -> Dict[str,Dict]:
    for sub_root, childs in templates.items():
        for sub_child, files in childs.items():
            for idx, tag in enumerate(tags.get(sub_child, list())[:len(files)]):
                with suppress(Exception):
                    if not templates[sub_root][sub_child][idx]["tags"]:
                        templates[sub_root][sub_child][idx]["tags"] = ", ".join(
                            sorted([str(keyword).replace(" ","_") for keyword in tag["tags"]]))
    return templates


def main(args: argparse.Namespace):
    if args.mode == "search" and args.query:
        search(args)
    elif args.mode == "update":
        update(args)
    elif args.mode == "upsert":
        search(args)
        update(args)
    else:
        raise ValueError("Invalid mode entered:", args.mode)


def search(args: argparse.Namespace):
    rename = read_json(os.path.join(args.root, args.rename))
    query = args.query.split(",")
    query = [rename[__q] for __q in query] if rename else query
    tags = asyncio.run(crawl(query))
    if rename:
        revert = {value:key for key,value in rename.items()}
        tags = {revert[key]:values for key,values in tags.items()}
        for key, values in tags.items():
            tags[key] = [{"name":value["name"].replace(rename[key],key),"tags":value["tags"]}
                            for value in values if value["name"].startswith(rename[key])]
    write_json(DEFAULT_TAGS, tags)


def update(args: argparse.Namespace):
    templates = read_json(os.path.join(args.root, args.templates))
    tags = read_json(os.path.join(args.root, args.tags))
    if templates and tags:
        templates[args.key] = match_templates(templates[args.key], tags)
        write_json(DEFAULT_RESULTS, templates)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Hanime Search')
    parser.add_argument("--m", "--mode", dest="mode", type=str, default="search")
    parser.add_argument("--p", "--path", dest="root", type=str, default=os.getcwd())
    parser.add_argument("--q", "--query", dest="query", type=str, default=str())
    parser.add_argument("--k", "--key", dest="key", type=str, default="Anime")
    parser.add_argument("--t", "--templates", dest="templates", type=str, default=DEFAULT_TAGS)
    parser.add_argument("--h", "--history", dest="tags", type=str, default=DEFAULT_TAGS)
    parser.add_argument("--r", "--rename", dest="rename", type=str, default=DEFAULT_RENAME)
    args = parser.parse_args()
    main(args)
