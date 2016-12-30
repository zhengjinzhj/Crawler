#!/usr/bin/env python
# -*- coding: utf-8 -*-

from HTMLParser import HTMLParser
import urlparse
import re


class LinkFinder(HTMLParser, object):
    def __init__(self, base_url, page_url):
        super(LinkFinder, self).__init__()
        self.base_url = base_url
        self.page_url = page_url
        self.links = set()

    # Call HTMLParser.feed(), this function is called when it encounters an opening tag <a>
    def handle_starttag(self, tag, attrs):
        if tag == 'a':
            for attribute, value in attrs:
                if attribute == 'href':
                    url = urlparse.urljoin(self.base_url, value)
                    self.links.add(url)
                if attribute == 'onclick':
                    value = self.modify(value)
                    pre_url = value.split(',')[1]
                    url = urlparse.urljoin(self.base_url, pre_url)
                    self.links.add(url)

    def page_links(self):
        return self.links

    def error(self, message):
        pass

    @staticmethod
    def modify(url):
        return re.sub('\"', '', url)

# finder = LinkFinder()
# finder.feed('<html><head><title>Test</title></head>'
#             '<body><h1>Parse me!</h1></body></html>')
