import re
import urllib.error
import urllib.parse
import urllib.request
import http.client

from lxml import etree

apiQuery = "http://de.wikipedia.org/w/api.php?action=query&"
catQuery = "list=categorymembers&format=xml&cmlimit=max&cmtitle="
imgQuery = "prop=revisions&rvlimit=1&rvprop=content&format=xml&titles="


def open_url(url):
    print("Getting " + url)
    request = urllib.request.Request(url)
    request.add_header("User-Agent", "http://wikifeedme.openthesaurus.de/")
    try:
        page = urllib.request.urlopen(request)
    # TODO log errors instead of printing
    except urllib.error.HTTPError as e:
        print("ERROR urllib2.HTTPError for " + url + ": " + str(e))
        page = e
    except http.client.BadStatusLine:
        print("ERROR httplib.BadStatusLine for " + url)
        page = "<nopage></nopage>"
    except urllib.error.URLError:
        print("ERROR urllib2.URLError for " + url)
        page = "<nopage></nopage>"
    return page


def get_title_from_link(link_string):
    # TODO deprecated?
    title_from_link_matcher = re.compile("(/wiki/|/zh-tw/|/zh-cn/)([^.]*)")
    brackets = re.compile("( \(|\()([^(]+)\)")
    title = urllib.parse.unquote(re.search(title_from_link_matcher, link_string).group(2).replace("_", " "))
    clean_title = re.sub(brackets, "", title)
    return clean_title


def get_all_pages_starting_from(cat):
    pages = set()
    recurse_categories(cat, pages, set())
    return pages


def recurse_categories(cat, pages, categories):
    parsed_url = etree.parse(open_url(apiQuery + catQuery + quote(cat)))
    for page in get_page_links(parsed_url):
        pages.add(page)
    for category in get_category_links(parsed_url):
        if category not in categories:
            categories.add(category)
            recurse_categories(category, pages, categories)


def get_category_links(root):
    return [i for i in root.xpath('//cm [contains(@title, "Kategorie:") and not(contains(@title, "Liste"))]/@title')]


def get_page_links(root):
    return [i for i in root.xpath('//cm [not(contains(@title, ":")) and not(contains(@title, "Liste"))]/@title')]


def found_no_pictures_in(title):
    query = apiQuery + imgQuery + quote(title)
    content = open_url(query)
    parse_result = etree.parse(content)
    redirect = parse_result.xpath(
        '//rev[starts-with(text(), "#WEITERLEITUNG") '
        'or starts-with(text(), "#redirect") '
        'or starts-with(text(), "#REDIRECT")]')

    if redirect:
        print("skipping redirect")
        return False

    pix = parse_result.xpath(
        '//rev [contains(text(), "Image:") '
        'or (contains(text(), "Bild:")) '
        'or (contains(text(), "Bild1")) '
        'or (contains(text(), "Bildname")) '
        'or (contains(text(), "<gallery>")) '
        'or (contains(text(), "Datei:")) '
        'or (contains(text(), "File:"))]')
    print("pix: ", len(pix))
    return pix == []


def generate_link_from_title(title):
    return "http://de.wikipedia.org/wiki/%s" % quote(title)


def quote(title):
    return urllib.parse.quote(title.encode("utf-8"))


# for debugging:
# if __name__ == "__main__":
#    found_no_pictures_in("Rossiki salata")

#   #foundNoPicturesIn("Dessert")
#   foundNoPicturesIn(u"Steckrübeneintopf")
