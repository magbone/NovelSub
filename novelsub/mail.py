#coding: utf-8

from builtins import NotImplementedError
from email.mime.text import MIMEText
from email.header import Header
import smtplib


class HTMLParser(object):

    def parse_html(self):

        raise NotImplementedError

    def _container_tag(self, str1):

        return "<div class=\"container\">" + str1 + "</div>"

    def _author_tag(self, str1):
        return "<h3>" + str1 + "</h3>"

    def _name_tag(self, str1):
        return "<h3>" + str1 + "</h3>"

    def _count_tag(self, str1):
        return "<h4>" + str1 + "</h4>"

    def _chapter_tag(self, str1):
        return "".join(("<h4>", str1,"</h4>"))

    def _link_tag(self, str1="#"):
        return "<a href=\"" + str1 + "\"></a>"

    def _row_tag(self, str1):
        return "<div class=\"row\">" + str1 + "</div>"

class MailContent(HTMLParser):

    begin_body = """<!DOCTYPE html><html><head><meta charset="utf-8"/><title></title><link rel="stylesheet" href="//cdnjs.loli.net/ajax/libs/mdui/0.4.3/css/mdui.min.css">
<script src="//cdnjs.loli.net/ajax/libs/mdui/0.4.3/js/mdui.min.js"></script></head><body>"""

    end_body = "</body></html>"
    def __init__(self):
        self._novels = []
        pass

    def add(self, novel_name, novel_author, novel_link, update_chapters):
        self._novels.append({'novel_name':novel_name,
                             'novel_author': novel_author,
                             'novel_link': novel_link,
                             'update_chapters_count': len(update_chapters),
                             'update_chapters': update_chapters})

    def _container_tag(self, str1):
        return "<div class=\"mdui-container\">" + str1 + "</div>"

    def _author_tag(self, str1):
        return "<div class=\"mdui-col-xs-6 mdui-col-sm-4\"><div class=\"mdui-typo-display-1\">"+ str1 + "</div></div>"

    def _name_tag(self, str1):
        return "<div class=\"mdui-col-xs-6 mdui-col-sm-4\"><div class=\"mdui-typo-display-1\">" + str1 + "</div></div>"

    def _count_tag(self, str1):
        return "<div class=\"mdui-col-xs-6 mdui-col-sm-4\"><div class=\"mdui-typo-display-1\">" + str(str1) + "</div></div>"

    def _chapter_tag(self, str1):
        return "<div class=\"mdui-col-xs-6 mdui-col-sm-4\"><div class=\"mdui-typo-display-1\">" +  " ".join((tuple([str(chapter) for chapter in str1]))) + "</div></div>"

    def _link_tag(self, str1="#"):
        return "<div class=\"mdui-col-xs-6 mdui-col-sm-4\"><div class=\"mdui-typo\"><a href=\"" + str1 + "\">前往官网</a></div></div>"

    def _row_tag(self, str1):

        return "<div class=\"mdui-row\">" + str1 + "</div>"
    def parse_html(self):
        html = ""
        html += self.begin_body

        novels = ""

        for novel in self._novels:
            novel_item = self._name_tag(novel['novel_name']) \
                        + self._author_tag(novel['novel_author'])\
                        + self._chapter_tag(novel['update_chapters'])\
                        + self._count_tag(novel['update_chapters_count'])\
                        + self._link_tag(novel['novel_link'])
            novels += self._row_tag(novel_item)
        html += self._container_tag(novels)
        html += self.end_body
        return html

class MailContentText:
    def __init__(self):
        self._novels = []
        pass

    def add(self, novel_name, novel_author, novel_link, update_chapters):
        self._novels.append({'novel_name':novel_name,
                             'novel_author': novel_author,
                             'novel_link': novel_link,
                             'update_chapters_count': len(update_chapters),
                             'update_chapters': update_chapters})
    def parse_text(self):
        text = ""
        for novel in self._novels:
            if len(novel['update_chapters_count']) == 0:
                chapters = "暂无更新"
            else:
                chapters = " ".join(tuple([str(chapter) for chapter in novel['update_chapters']]))

            update_msg = "书名：%s，作者：%s，更新章节： %s, 更新章数 %d" % (novel['novel_name'],
                                                            novel['novel_author'],
                                                            chapters,
                                                            novel['update_chapters_count'])
            text += update_msg

        return text


class MailRss:

    def __init__(self, sender, receivers, text):
        self._sender = sender
        self._receivers = receivers
        self._text = text
        self._message = None

    def smtp_server(self, host, user, password, port=25):
        self._host = host
        self._user = user
        self._password = password
        self._port = port

    def send(self):
        self._message = MIMEText(self._text, 'html' 'utf-8')
        subject = "我的小说订阅"
        self._message['From'] = self._sender
        self._message['To'] = self._receivers
        self._message['Subject'] = Header(subject, "utf-8")
        self._message.add_header('Content-Type', "text/html")
        try:
            if self._port == 25:
                smtp_obj = smtplib.SMTP(self._host, self._port)
            else:
                # smtp use ssl protocol
                smtp_obj = smtplib.SMTP_SSL(self._host, self._port)
            smtp_obj.login(self._user, self._password)
            smtp_obj.set_debuglevel(1)
            smtp_obj.sendmail(self._sender, self._receivers, self._message.as_string())
        except smtplib.SMTPException as e:
            print(e)
        else:
            smtp_obj.quit()
# Test block
if __name__ == '__main__':
    content = MailContent()
    content.add("xhy", "xhy", "http://sss.com", [123, 124])
    content.add("xhy", "xhy", "https://www.com", [123])
    print(content.parse_html())
