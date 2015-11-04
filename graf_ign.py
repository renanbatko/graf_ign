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

def convert_date(text_date, dic_dates):
    months = {'Janeiro': 1, 'Fevereiro': 2, 'Março': 3, 'Abril': 4, 'Maio': 5,
    'Junho': 6, 'Julho': 7, 'Agosto': 8, 'Setembro': 9, 'Outubro': 10,
    'Novembro': 11, 'Dezembro': 12};

    post_date = text_date.split(" ", 2)
    day = post_date[1]
    day = day.replace(",", "")
    month = months[post_date[0]]
    year = post_date[2]
    #print "%d/%d/%d" % (int(day), int(month), int(year))
    date = str(day) + "/" + str(month) + "/" + str(year)
    if date in dic_dates:
        dic_dates[date] += 1
    else:
        dic_dates[date] = 1

def compare_dates(data1, data2):
	dia1 = int(data1.split("/", 1)[0])
	mes1 = int(data1.split("/", 2)[1])
	ano1 = int(data1.split("/", 3)[2])
	dia2 = int(data2.split("/", 1)[0])
	mes2 = int(data2.split("/", 2)[1])
	ano2 = int(data2.split("/", 3)[2])

	#print dia1+" "+mes1+" "+ano1+" "+dia2+" "+mes2+" "+ano2

	if (ano1 > ano2):
		return 1
	if (ano1 == ano2):
		if (mes1 > mes2):
			return 1
		if (mes1 == mes2):
				if (dia1 >= dia2):
					return 1
	return 0

def sort_file(file_name):
    arq = open(file_name, "r")
    dates = []

    for line in arq:
        temp01 = line.split("\t", 1)[0]
        dates.append(temp01)
    arq.close()

    for i in range(0, len(dates)):
        for j in range(len(dates)-1, i, -1):
            if (compare_dates(dates[i], dates[j]) == 1):
                aux = dates[i]
                dates[i] = dates[j]
                dates[j] = aux

    fp = open("sorted_dates.txt", "w")
    arq = open(file_name, "r")
    for date in dates:
        arq.seek(0)
        for lin in arq:
            col1 = lin.split("\t", 1)[0]
            col2 = lin.split("\t", 2)[1]
            if (date == col1):
                fp.write(date + "\t" + col2)

    arq.close()
    fp.close()

#inicio
url_base = raw_input("URL do tópico: ")
#tpc_name = raw_input("Título do tópico: ")

page = urllib.urlopen(url_base)
n_pages = number_of_pages(page)

dic_dates = {}
for index in range(1, n_pages+1):
    url_now = url_base + "/page-" + str(index)
    page = urllib.urlopen(url_now)
    for line in page:
        if line.find('title="Permalink" class="datePermalink"') != -1:
            post_date = line.split('title="Permalink" class="datePermalink"', 2)[1]
            if post_date.find('DateTime" title="') != -1:
                post_date = post_date.split('DateTime" title="', 1)[1]
                post_date = post_date.split("às", 1)[0]
                #print post_date
                convert_date(post_date, dic_dates)
            else:
                post_date = post_date.split('data-datestring="', 1)[1]
                post_date = post_date.split('"', 1)[0]
                #print post_date
                convert_date(post_date, dic_dates)
            #print post_date

#print dic_dates
arq = open("unsorted_dates.txt", "w")
for w in dic_dates:
    arq.write(w + "\t" + str(dic_dates[w]) + "\n")
    #print w + "\t" + str(dic_dates[w])
arq.close()

sort_file("unsorted_dates.txt")

page.close()
