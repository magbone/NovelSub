# coding: utf-8


import argparse
import json
import abc
import re

import requests
from apscheduler.schedulers.background import BackgroundScheduler
from requests import ConnectionError, HTTPError, Timeout, TooManyRedirects

from novelsub.lib.mail import MailRss, MailContentText
from novelsub.lib.logger import logger

class HtmlFilterImp(metaclass=abc.ABCMeta):

    @abc.abstractclassmethod
    def parse_arg(self):
        pass


class Request(HtmlFilterImp):

    headers = {
        "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:69.0) Gecko/20100101 Firefox/69.0"
    }


    def __init__(self, chapter_url, timeout=2):

        self._chapter_url = chapter_url
        self._timeout = timeout
        self._chapters = []

    def parse_arg(self):
        try:
            r = requests.get(self._chapter_url, headers=self.headers, timeout=self._timeout)
            r.encoding = "utf-8"

            if r.text:
                self._chapters = re.findall(r'[\u7B2C][^<>\s]*[\u7AE0]', r.text, re.I| re.M)

        except (ConnectionError, HTTPError, Timeout, TooManyRedirects) as e:
            logger.debug(e.strerror)
        else:
            return self._chapters


class ChapterParser(object):

    number_table = {
        '零': 0,
        '0' : 0,
        '一': 1,
        '1':  1,
        '二': 2,
        '两': 2,
        '2' : 2,
        '三': 3,
        '3':  3,
        '四': 4,
        '4':  4,
        '五': 5,
        '5':  5,
        '六': 6,
        '6':  6,
        '七': 7,
        '7':  7,
        '八': 8,
        '8':  8,
        '九': 9,
        '9':  9,
        '十': 10,
        '百': 100,
        '千': 1000,
        '万': 10000
    }


    def __init__(self, chapter):
        self._chapter = chapter[::-1]
        self._index = 0

    def _next(self):
        if self._index >= len(self._chapter):
            return None
        self._dict_value = self._chapter[self._index]
        self._index += 1
        return self._dict_value

    def parse_chapter(self):
        try:
            return int(self._chapter[::-1][1:len(self._chapter) -1])
        except ValueError:
            number = 0
            times = 1
            while self._next():
                if self._dict_value == "第" or self._dict_value == "章":
                    continue
                else:
                    try:
                        if int(self.__dict__[self._dict_value]) <= 9 and self.__dict__[self._dict_value] >= 0:
                            number += self.__dict__[self._dict_value] * times
                        else:
                            times = self.__dict__[self._dict_value]
                    except KeyError:
                        return None
            return number


class FilterGroup(object):
    pass



class Subscribe:


    def __init__(self, conf_path):
        '''

        :param conf_path: the conf path
        '''
        # conf demo
        #
        # mail(Obj):
        #     smtp_host: smtp defines address
        #     smtp_port: smtp defines port (25 is default and 476 is used SSL)
        #     sender: sender mail address(String)
        #     receivers: receiver mail addresses(String array)
        # timeout(Number): request the html timeout
        # schedule(Number): the task execute time (hour)
        # novels(Array Obj):
        #     link: the novel chapter address(String)
        #     name: the novel name(String)
        #     author: the novel author name(String)
        #     begin_chapter: the novel chapter you want to begin subscribe
        self._conf_path = conf_path
        self._conf_json = json.load(open(conf_path, "r"))
    def __job__(self):
        mail_content_text = MailContentText()
        for i in range(0, len(self._conf_json['novels'])):
            novel = self._conf_json['novels'][i]
            update_chapters = []
            r = Request(novel['link'], timeout=self._conf_json['timeout'])
            chapters = list(set(r.parse_arg()))
            newest_chapter = 0
            for chapter in  chapters:
                parser = ChapterParser(chapter)
                parsed_chapter = parser.parse_chapter()
                if novel['begin_chapter'] < parsed_chapter:
                    update_chapters.append(chapter)
                if parsed_chapter >= newest_chapter:
                    newest_chapter = parsed_chapter
            logger.info(update_chapters)
            mail_content_text.add(novel_name=novel['name'],
                             novel_author=novel['author'],
                             novel_link="link",
                             update_chapters=update_chapters)

            #Update chapter
            self._conf_json['novels'][i]['begin_chapter'] = newest_chapter

        mail_rss = MailRss(sender=self._conf_json['sender'],
                            receivers=self._conf_json['receiver'],
                            text=mail_content_text.parse_text())
        logger.info(mail_content_text.parse_text())
        mail_rss.smtp_server(host=self._conf_json['mail']['smtp_server'],
                            user=self._conf_json['mail']['user'],
                            password=self._conf_json['mail']['password'],
                            port=self._conf_json['mail']['smtp_port'])
        mail_rss.send()

        #Update json file
        json.dump(self._conf_json, open(self._conf_path, "w"))

    def run(self):
        self.__job__()
        logger.info(
            "Novel Subscribe started."
        )
        scheduler = BackgroundScheduler()
        scheduler.add_job(self.__job__, 'interval', seconds= 3600 * self._conf_json['schedule'])
        scheduler.start()

        while 1:
            pass


def main():
    parse = argparse.ArgumentParser(description="A novel subscribe tool")
    parse.add_argument("-c", help="conf path")
    args = parse.parse_args()
    if args.c:
        s = Subscribe(args.c)
        s.run()





