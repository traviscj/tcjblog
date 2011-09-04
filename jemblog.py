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

dates = {}
byMonthDict = {}
categories = {}
for entry in blogEntries:
	entryNum, title, author, date, category, content = entry
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
	f=open("entry%0.4d.jemdoc"%entryNum,'w')
	f.write("# jemdoc: menu{MENU2}{index.html}\n")
	f.write("= %s\n"%(title))
	f.write("== from %s\n\n"%(date))
	f.write(content)
	f.write("\n")
	if entryNum != 0:
		f.write("[entry%0.4d.html older]\n"%(entryNum-1));
	else:
		f.write("older\n");
	#print entryNum, len(blogEntries)
	if entryNum+1 != len(blogEntries):
		f.write("[entry%0.4d.html newer]\n"%(entryNum+1));
	else:
		f.write("newer\n");
	f.close()
	
# Setup the menu file.
MENU = open("MENU2", 'w')
MENU.write("navigation\n")
MENU.write("\tback to main site		[..]\n")
MENU.write("\tfirst blog page		[blog0.html]\n")
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
		f.write("== [entry%0.4d.html %s] (from %s)\n"%(entryNum, title, date))
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
	first, last = "newest", "[blog%d.html oldest]"%(lastPage)
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
		f.write("== [entry%0.4d.html %s] (from %s)\n"%(entryNum, title, date))
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
		f.write("== [entry%0.4d.html %s] (from %s)\n"%(entryNum, title, date))
		f.write(content)
		f.write("\n")
	f.close()

