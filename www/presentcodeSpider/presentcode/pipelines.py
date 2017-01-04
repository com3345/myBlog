# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from datetime import datetime as dt
import re
from scrapy.exceptions import DropItem
import logging


MAP = {
    "メンテナンス": "维护",
    "日": "周日",
    "月": "周一",
    "火": "周二",
    "水": "周三",
    "木": "周四",
    "金": "周五",
    "土": "周六",
    "メンテナンスまで": "维护开始前",
    "まで": "为止",
    "終了後": "结束后",
    "開始時": "开始时",
    "※": "",
    "アイテムをお受け取り頂けます。": "。",
    " ": "",
    "\r\n■有効期限：": "2017"  # \r\n■有効期限：/1/4(周三)维护开始时为止
}


class PresentcodePipeline(object):
    def process_item(self, item, spider):
        for key, value in MAP.items():
            item["timestr"] = item["timestr"].replace(key, value)
        if "～" in item["timestr"]:
            endtimestr = item["timestr"].split("～")[1]
            endtime_month, endtime_day = endtimestr.split("(")[0].split("/")
            endtime_year = item["timestr"][:4]
        else:
            endtime_year, endtime_month, endtime_day = item["timestr"].split("(")[0].split("/")

        re_result = re.findall(r"\d+:\d+", item["timestr"])
        if re_result:
            endtime_hour, endtime_minute = re_result[-1].split(":")
        else:
            endtime_hour, endtime_minute = 8, 30
        endtimedate = dt(*map(int, (endtime_year, endtime_month, endtime_day, endtime_hour, endtime_minute)))

        item["endtimestamp"] = endtimedate.timestamp()
        item["timestr"] = "/".join(item["timestr"].split("/")[1:])
        logging.info(item)
        # if dt.today() > endtimedate:
        #     raise DropItem("礼物代码过期了")
        return item
