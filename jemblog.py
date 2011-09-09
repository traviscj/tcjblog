#!/usr/bin/python

# author: travis johnson (traviscj@traviscj.com)
# date: sept 4, 2011
# 
# Copyright (C) 2011 Travis Johnson
# jemblog is free software; you can redistribute it and/or modify it under the
# terms of the GNU General Public License as published by the Free Software
# Foundation; either version 3 of the License, or (at your option) any later
# version.
#
# jemblog is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR
# A PARTICULAR PURPOSE. See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with
# this program. If not, see <http://www.gnu.org/licenses/>.
import glob
short_months = ["", "jan", "feb", "mar", "apr", "may", "jun", "jul", "aug", "sep", "oct", "nov", "dec"]
really_short_months = " JFMAMJJASOND"

# first, just read in the entry files
blogEntries = []
entryNum = 0
for fileName in glob.glob("entry*.txt"):
	f = open(fileName)
	title = f.readline()
	author = f.readline()
	date = f.readline()
	category = f.readline()
	content = f.readlines()[1:]
	junk, title = title[:-1].split(": ",1)
	junk, author = author[:-1].split(": ",1)
	junk, date = date[:-1].split(": ",1)
	junk, category = category[:-1].split(": ",1)

	blogEntries.append( (entryNum, title, author, date, category, "".join(content)) )
	entryNum += 1

# need to reverse so that newest blog posts show up at the top
blogEntries.reverse()
# figure out how many pages are needed
pageNum,entryNum = 0,0
pageDict = {}
for entry in blogEntries:
	# do blog0...n
	if pageNum in pageDict:
		pageDict[pageNum].append(entry)
	else:
		pageDict[pageNum] = [entry]
	if entryNum % 10 == 9:
		pageNum += 1
	entryNum += 1
	
lastPage = len(blogEntries)/10

def friendly(str):
	from re import sub
	return sub("'|:|!|&|/|\/|\(|\)|\?|,", "", str).replace(" ", "_").replace("__","_").lower()
	#return str.replace(" ", "_").replace("'","").replace(":","").replace("!","").replace("&", "and").replace("/","_or_").lower()

dates = {}
byMonthDict = {}
categories = {}
#for entry in blogEntries:
for i in range(len(blogEntries)):
	entryNum, title, author, date, category, content = blogEntries[i]
	year, month, day = date.split("/")
	#print year, month, day
	if year in dates:
		if month not in dates[year]:
			dates[year].append(month)
	else:
		dates[year] = [month]
	byMonth = "%s_%s"%(year, short_months[int(month)])
	#print "from %s %s %s, I got %d then %s"%(year,month,day,int(month),byMonth)
	if byMonth in byMonthDict:
		byMonthDict[byMonth].append(entry)
	else:
		byMonthDict[byMonth] = [entry]
	if category in categories:
		categories[category].append(entry)
	else:
		categories[category] = [entry]
		
	date = date.replace("/", "\/")
	filetitle = friendly(title)
	f=open(filetitle+".jemdoc",'w')
	f.write("# jemdoc: menu{MENU2}{index.html}\n")
	f.write("= %s\n"%(title))
	f.write("== from %s\n\n"%(date))
	f.write(content)
	f.write("\n")
	if i+1 != len(blogEntries):
		prevtitle = friendly(blogEntries[i+1][1])
		f.write("[%s.html older]\n"%(prevtitle))
	else:
		f.write("older\n");
	#print entryNum, len(blogEntries)
	if i != 0:
		nexttitle = friendly(blogEntries[i-1][1])
		f.write("[%s.html newer]\n"%(nexttitle))
	else:
		f.write("newer\n");
	f.close()
	
# Setup the menu file.
MENU = open("MENU2", 'w')
MENU.write("navigation\n")
MENU.write("\tback to main site		[..]\n")
MENU.write("\tfirst blog page		[index.html]\n")
MENU.write("by month\n")
years = dates.keys()
years.sort()
for year in years:
	MENU.write("\t" + year + ": ")
	for month in range(1,13):
		mStr = "%0.2d"%(month)
		if mStr in dates[year]:
			MENU.write("[%s_%s.html %s] "%(year, short_months[month],really_short_months[month]))
		else:
			MENU.write(really_short_months[month] + " ")
	MENU.write("\n")
MENU.write("by category\n")
for cat in categories.iterkeys():
	MENU.write("\t%s\t\t[category_%s.html]\n"%(cat,cat))
MENU.write("other\n")
MENU.write("\tjemblog [https://github.com/traviscj/jemblog]\n")
MENU.write("\trss [rss.xml]\n")

# setup the main blog layout
for page, entries in pageDict.iteritems():
	if page==0:
		fileName = "index.jemdoc"
	else:
		fileName = "index%d.jemdoc"%page
	f=open(fileName,'w')
	f.write("# jemdoc: menu{MENU2}{index.html}\n")
	f.write("= Blog, page %d\n"%(page))
	f.write("from the desk of travis johnson.\n\n");
	for entry in entries:
		entryNum, title, author, date, category, content = entry
		date = date.replace("/", "\/")
		f.write("== [%s.html %s] (from %s)\n"%(friendly(title), title, date))
		f.write(content)
		f.write("\n")
	f.write("\n\n")
	f.write("~~~\n")
	f.write("{}{table}{bottomnav}\n")
	if page > 1:
		f.write("[index%d.html newer page]\n"%(page-1))
	elif page == 1:
		f.write("[index.html newer page]\n")
	else:
		f.write("newer page\n")
	first, last = "newest", "[index%d.html oldest]"%(lastPage)
	if page != 0:
		first = "[index.html newest]"
	if page == lastPage:
		last = "last"
	f.write(" | %s %s  | "%(first,last))
	if page != lastPage:
		f.write("[index%d.html older page]\n"%(page+1))
	else:
		f.write("older page")
	f.write("\n")
	f.write("~~~\n")
	f.close()

#print byMonthDict
# month view... last thing!
yearmonthList = byMonthDict.keys()
for yearmonth in yearmonthList:
	entries = byMonthDict[yearmonth]
	#print yearmonth
	f=open("%s.jemdoc"%(yearmonth),'w')
	f.write("# jemdoc: menu{MENU2}{%s.html}\n"%(yearmonth))
	f.write("= Blog, by date: %s\n"%(yearmonth))
	f.write("from the desk of travis johnson.\n\n")
	for entry in entries:
		entryNum, title, author, date, category, content = entry
		date = date.replace("/", "\/")
		f.write("== [%s.html %s] (from %s)\n"%(friendly(title), title, date))
		f.write(content)
		f.write("\n")
	f.close()
catList = categories.keys()
catList.sort()
for category in catList:
	entries = categories[category]
	#print yearmonth
	f=open("category_%s.jemdoc"%(category),'w')
	f.write("# jemdoc: menu{MENU2}{%s.html}\n"%(category))
	f.write("= Blog, by category: %s\n"%(category))
	f.write("from the desk of travis johnson.\n\n")
	for entry in entries:
		entryNum, title, author, date, category, content = entry
		date = date.replace("/", "\/")
		f.write("== [%s.html %s] (from %s)\n"%(friendly(title), title, date))
		f.write(content)
		f.write("\n")
	f.close()

html_escape_table = {
	"&": "&amp;",
	'"': "&quot;",
	"'": "&apos;",
	">": "&gt;",
	"<": "&lt;",
	}
def html_escape(text):
	"""Produce entities within text."""
	return "".join(html_escape_table.get(c,c) for c in text)

import datetime, tempfile
rss = open("html/rss.xml",'w')
rssDate = "%a, %d %b %Y %X +0000"
lastYearS,lastMonthS,lastDayS = blogEntries[0][3].split("/")
lastYear,lastMonth,lastDay = int(lastYearS), int(lastMonthS), int(lastDayS)
rss.write("""<?xml version="1.0" encoding="UTF-8" ?>
<rss version="2.0">
<channel>
        <title>%s</title>
        <description>%s</description>
        <link>%s</link>
        <lastBuildDate>%s</lastBuildDate>
        <pubDate>%s</pubDate>""" % ("~traviscj/", "feed for traviscj.com/blog", "http://traviscj.com/blog",
								datetime.datetime.utcnow().strftime(rssDate),datetime.date(lastYear,lastMonth,lastDay).strftime(rssDate)))
import subprocess,os
from xml.sax.saxutils import escape
for entry in blogEntries[0:10]:
	entryNum, title, author, date, category, content = entry
	yearS, monthS, dayS = date.split("/")
	year,month,day = int(yearS), int(monthS), int(dayS)

	print title
	title = escape(title)
	print title
	#content = html_escape(content)

	tmpfd,tmpFileName = tempfile.mkstemp()
	parsedfd,parsedFileName = tempfile.mkstemp()
	tmpFile = open(tmpFileName,'w')
	parsedFile = open(parsedFileName)
	tmpFile.write("# jemdoc: \n")
	tmpFile.write(content)
	tmpFile.close()
	subprocess.call(['/usr/bin/python','jemdoc.py','-o',parsedFile.name,tmpFile.name])
	formattedLines = parsedFile.readlines()
	parsedFile.close()
	#print parsedFileName, tmpFileName
	os.remove(parsedFileName)
	os.remove(tmpFileName)
	formattedcontent = "\n".join(formattedLines[10:-2])
	formattedcontent = escape(formattedcontent)
	rss.write("""
        <item>
                <title>%s</title>
                <description>%s</description>
                <link>%s</link>
                <guid>%s</guid>
                <pubDate>%s </pubDate>
        </item>
	""" % (title, formattedcontent, "http://traviscj.com/blog/"+friendly(title)+".html", friendly(title), datetime.date(year,month,day).strftime(rssDate)))
 
rss.write("""
</channel>
</rss>""")

