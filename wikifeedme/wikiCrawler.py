#!/usr/bin/python
# -*- coding: utf-8 -*-

from lxml import html, etree
import re
import urllib
import urllib2
import httplib

apiQuery = "http://de.wikipedia.org/w/api.php?action=query&"
catQuery = "list=categorymembers&format=xml&cmlimit=max&cmtitle="
imgQuery = "prop=revisions&rvlimit=1&rvprop=content&format=xml&titles="

def openUrl(url):
    print "Getting " + url
    request=urllib2.Request(url)
    request.add_header("User-Agent","http://wikifeedme.openthesaurus.de/")
    try:
        page=urllib2.urlopen(request)
    except urllib2.HTTPError as e:
        print "ERROR urllib2.HTTPError for " + url + ": " + e
        page=e
    except httplib.BadStatusLine:
        print "ERROR httplib.BadStatusLine for " + url
        page="<nopage></nopage>"
    except urllib2.URLError:
        print "ERROR urllib2.URLError for " + url
        page="<nopage></nopage>"
    return page
    
def getTitleFromLink(linkString):
    titleFromLinkMatcher = re.compile("(/wiki/|/zh-tw/|/zh-cn/)([^\.]*)")
    brackets = re.compile("( \(|\()([^(]+)\)")
    title = urllib.unquote(re.search(titleFromLinkMatcher, linkString).group(2).replace("_"," "))
    cleanTitle = re.sub(brackets, "", title.decode("utf-8"))
    return cleanTitle

def getAllPagesStartingFrom(cat):
    pages = set()
    recurseCategories(cat, pages, set())
    return pages

def recurseCategories(cat, pages, categories):
    parsedUrl=etree.parse(openUrl(apiQuery+catQuery+quote(cat)))
    for page in getPageLinks(parsedUrl):
            pages.add(page)
    for category in getCategoryLinks(parsedUrl):
        if category not in categories:
            categories.add(category)
            recurseCategories(category, pages, categories)

def getCategoryLinks(root):
    return [i for i in root.xpath('//cm [contains(@title, "Kategorie:") and not(contains(@title, "Liste"))]/@title')]

def getPageLinks(root):
    return [i for i in root.xpath('//cm [not(contains(@title, ":")) and not(contains(@title, "Liste"))]/@title')]

def foundNoPicturesIn(title):
    query = apiQuery+imgQuery+quote(title)
    content = openUrl(query)
    parseResult = etree.parse(content)
    #print "=================================================="
    #print parseResult
    pix = parseResult.xpath(
        '//rev [contains(text(), "Image:") or (contains(text(), "Bild:")) or (contains(text(), "Datei:")) or (contains(text(), "File:"))]')
    print "pix: ", len(pix)
    return pix == []

def generateLinkFromTitle(title):
    return "http://de.wikipedia.org/wiki/%s"%quote(title)

def quote(title):
    return urllib.quote(title.encode("utf-8"))

# for debugging:
#if __name__=="__main__":
#   #foundNoPicturesIn("Dessert")
#   foundNoPicturesIn(u"Steckrübeneintopf")
