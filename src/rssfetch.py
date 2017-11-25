from bs4 import BeautifulSoup
import requests

RSS_FEED_URL = "https://www.worldcubeassociation.org/rss.html"


class RSSParser(object):

    def __init__(self):
        r = requests.get(RSS_FEED_URL)
        self.soup = BeautifulSoup(r.text, "xml")

    def get_events(self):
        items = self.soup.rss.channel.find_all('item')
        items = [BeautifulSoup(i.description.string) for i in items if "Check out" in i.description.string]
        links = [i.find_all('a') for i in items]
        return {i[0].string: i[1]['href'] for i in links}
