import re
import bs4
import requests


class HTMLScanner:

    def __init__(self, url_meta):
        super().__init__()
        self.url_meta = url_meta
        url_page = requests.get(self.url_meta.url)
        self.html = url_page.text
        self.soup = bs4.BeautifulSoup(self.html, 'html.parser')

    def find_video(self):
        return self.find_urls_regex()[0]

    # Uses regex to find all .mp4 links in the file.
    def find_urls_regex(self):
        # Find all .mp4 links in the html.
        raw_urls = re.findall("https.*.mp4\\s", self.html)
        return raw_urls
