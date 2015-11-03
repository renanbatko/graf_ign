#/usr/bin/env python
# -*- coding: utf-8 -*-
import urllib
import time
import re
import os

def number_of_pages(page):
    c = 0
    for line in page:
        if line.find("page-") != -1:
            c += 1
            if (c == 8):
                n_pages = line.split("page-", 1)[1]
                n_pages = n_pages.split('"', 1)[0]
                n_pages = int(n_pages)
                return n_pages

#inicio
url_base = raw_input("URL do tópico: ")
#tpc_name = raw_input("Título do tópico: ")

page = urllib.urlopen(url_base)
n_pages = number_of_pages(page)

for index in range(1, n_pages+1):
    url_now = url_base + "/page-" + str(index)
    page = urllib.urlopen(url_now)
    for line in page:
        if line.find('title="Permalink" class="datePermalink"') != -1:
            post_date = line.split('title="Permalink" class="datePermalink"', 2)[1]
            if post_date.find('DateTime" title="') != -1:
                post_date = post_date.split('DateTime" title="', 1)[1]
                post_date = post_date.split("às", 1)[0]
            else:
                post_date = post_date.split('data-datestring="', 1)[1]
                post_date = post_date.split('"', 1)[0]
            print post_date


page.close()
