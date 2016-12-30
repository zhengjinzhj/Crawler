#!/usr/bin/env python
# -*- coding: utf-8 -*-

from urlparse import urlparse


# Get domain name (example.com)
def get_domain_name(url):
    try:
        results = get_sub_domain_name(url).split('.')  # a list
        return results[-2] + '.' + results[-1]
        # return results[-3] + '.' + results[-2] + '.' + results[-1]

    except:
        return ''


# Get sub domain name (name.example.com)
def get_sub_domain_name(url):
    try:
        return urlparse(url).netloc
    except:
        return ''

print get_domain_name('https://twitter.com/intent/tweet?text=Videos&url=')
