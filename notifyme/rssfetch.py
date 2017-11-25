from bs4 import BeautifulSoup
import requests
import os
import re

RSS_FEED_URL = "https://www.worldcubeassociation.org/rss.html"


class RSSParser(object):

    def __init__(self):
        r = requests.get(RSS_FEED_URL)
        self.soup = BeautifulSoup(r.text, "xml")

    def get_events(self):
        items = self.soup.rss.channel.find_all('item')
        items = [BeautifulSoup(i.description.string) for i in items if "Check out" in i.description.string]
        links = [i.find_all('a') for i in items]
        d = {i[0].string: i[1]['href'] for i in links}
        for event in d:
            if re.match('^https?:\/\/(www\.)?worldcubeassociation\.org\/competitions\/[^\/]*\/?$', d[event]) is not None:
                r = requests.get(os.path.join(d[event], 'register'))
                soup = BeautifulSoup(r.text)
                reg_time = soup.find(class_="wca-local-time")
                if reg_time is not None:
                    time = reg_time['data-utc-time']
                    d[event] = (d[event], time)
                else:
                    d[event] = (d[event], 'open')
            else:
                d[event] = (d[event], None)
        return d
