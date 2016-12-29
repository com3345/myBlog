# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import re
from datetime import datetime
from .items import BdItem
from scrapy.exceptions import DropItem


P_NUBE = "ぬ|ヌ|nube|nu"  # 1
P_KUTUMU = "つ|ツ|kutu|靴"  # 2
P_KUZAKA = "くざ|クザカ|kuza"  # 3
P_KARANDA = "カランダ"  # 4


def findbosstype(text):
    if any(re.findall(P_NUBE, text)):
        # return "努贝尔(ヌベール)"
        return "nube"
    if any(re.findall(P_KUTUMU, text)):
        # return "库图姆(クツム)"
        return "kutu"
    if any(re.findall(P_KUZAKA, text)):
        # return "库扎卡(クザカ)"
        return "kuza"
    if any(re.findall(P_KARANDA, text)):
        # return "卡兰达(カランダ)"
        return "kara"


class BdPipeline(object):
    def __init__(self):
        self.newest_nube = BdItem(boss="nube", last_time=0)
        self.newest_kutu = BdItem(boss="kutu", last_time=0)
        self.newest_kuza = BdItem(boss="kuza", last_time=0)
        self.newest_kara = BdItem(boss="kara", last_time=0)

    def process_item(self, item, spider):

        re_time = re.compile(
            r"\d{1,2}：\d{1,2}|\d{1,2}:\d{1,2}|\d{2,4}|\d{1,2}\w\d{1,2}")
        last_time = re_time.search(item["content"])

        if last_time:
            last_time = last_time.group(0)
        else:
            last_time = re_time.search(item["title"]).group(0)

        if ":" in last_time:
            hour, minute = last_time.split(":")
        elif "時" in last_time:
            hour, minute = last_time.split("時")
        else:
            hour, minute = last_time[:2], last_time[2:]

        ymd = datetime.strptime(item["create_time"], "%Y年%m月%d日")

        item["last_time"] = datetime(
            year=ymd.year,
            month=ymd.month,
            day=ymd.day,
            hour=int(hour),
            minute=int(minute)).timestamp()

        item["boss"] = findbosstype(item["content"] + item["title"])

        # print(self.newest_nube["last_time"], "\t", self.newest_kutu["last_time"], "\t", self.newest_kuza["last_time"], "\t", self.newest_kara["last_time"])
        # print(item["boss"], item["last_time"])
        if item["boss"] == "nube" and item["last_time"] > self.newest_nube["last_time"]:
            self.newest_nube = item
            return item
        elif item["boss"] == "kutu" and item["last_time"] > self.newest_kutu["last_time"]:
            self.newest_kutu = item
            return item
        elif item["boss"] == "kuza" and item["last_time"] > self.newest_kuza["last_time"]:
            self.newest_kuza = item
            return item
        elif item["boss"] == "kara" and item["last_time"] > self.newest_kara["last_time"]:
            self.newest_kara = item
            return item
        else:
            raise DropItem()
