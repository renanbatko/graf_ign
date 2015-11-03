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

def convert_date(text_date, arq):
    months = {'Janeiro': 1, 'Fevereiro': 2, 'Março': 3, 'Abril': 4, 'Maio': 5,
    'Junho': 6, 'Julho': 7, 'Agosto': 8, 'Setembro': 9, 'Outubro': 10,
    'Novembro': 11, 'Dezembro': 12};

    post_date = text_date.split(" ", 2)
    day = post_date[1]
    day = day.replace(",", "")
    month = months[post_date[0]]
    year = post_date[2]
    print "%d/%d/%d" % (int(day), int(month), int(year))


#inicio
url_base = raw_input("URL do tópico: ")
#tpc_name = raw_input("Título do tópico: ")

page = urllib.urlopen(url_base)
n_pages = number_of_pages(page)


arq = open("sorted_dates.txt", "w")
for index in range(1, n_pages+1):
    url_now = url_base + "/page-" + str(index)
    page = urllib.urlopen(url_now)
    for line in page:
        if line.find('title="Permalink" class="datePermalink"') != -1:
            post_date = line.split('title="Permalink" class="datePermalink"', 2)[1]
            if post_date.find('DateTime" title="') != -1:
                post_date = post_date.split('DateTime" title="', 1)[1]
                post_date = post_date.split("às", 1)[0]
                convert_date(post_date, arq)
            else:
                post_date = post_date.split('data-datestring="', 1)[1]
                post_date = post_date.split('"', 1)[0]
                convert_date(post_date, arq)
            #print post_date


page.close()
