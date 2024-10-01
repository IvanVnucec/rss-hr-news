import xml.etree.ElementTree as ET
import urllib.request
import json
import re
from datetime import datetime

def fetch_rss(feed):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
    }
    req = urllib.request.Request(feed, headers=headers)
    xml = urllib.request.urlopen(req).read()
    root = ET.fromstring(xml)
    items = root.findall(".//item")
    articles = []
    for item in items:
        try:
            datetime_now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            title = item.find("title").text
            link = item.find("link").text
            description = item.find("description").text
            description = re.sub(r"<.*?>", "", description)
            articles.append({
                "datetime": datetime_now,
                "title": title,
                "link": link,
                "description": description,
            })
        except Exception as e:
            print(f"Error '{feed}': {e}")
    return articles

def dump_to_jsonl(file, feed):
    with open(file, "a+", encoding="utf-8") as f:
        for item in feed:
            json.dump(item, f, ensure_ascii=False)
            f.write("\n")

feeds = [
    "https://feed.hrt.hr/vijesti/page.xml",
    "https://www.index.hr/rss",
    "https://net.hr/feed",
    "https://www.24sata.hr/feeds/news.xml",
    "http://www.vecernji.hr/rss/",
    "https://n1info.hr/feed/",
    "http://www.tportal.hr/rss/naslovnicarss.xml",
    "http://rss.dnevnik.hr/index.rss",
    "https://www.slobodnadalmacija.hr/feed/category/119",
]

for feed in feeds:
    try:
        feed = fetch_rss(feed)
    except Exception as e:
        print(f"Error '{feed}': {e}")
    else:
        dump_to_jsonl("articles.jsonl", feed)
