import sqlite3
import random
from itertools import chain
import wiki_crawler

starters = [u"Kategorie:Salat",
            u"Kategorie:Suppe",
            u"Kategorie:Vorspeise",
           ]
mainCourses = [u"Kategorie:Gemüsegericht",
               u"Kategorie:Käsegericht",
               u"Kategorie:Kartoffelgericht",
               u"Kategorie:Speise_aus_Teigwaren",
               u"Kategorie:Reisgericht",
               u"Kategorie:Fondue",
               u"Kategorie:Fleischgericht",
               u"Kategorie:Fischgericht",
               u"Kategorie:Eierspeise",
               u"Kategorie:Brotgericht",
               u"Kategorie:Speise_aus_Getreideprodukten",
              ]
sides = [u"Kategorie:Beilage"]
desserts = [u"Kategorie:Süßspeise"]
cheeses = [u"Kategorie:Käsesorte"]


def grab_food():
    starters = get_mouthwatering_starters()
    mains = get_delightful_main_courses()
    desserts = get_yummylicious_desserts()
    cheeses = get_cheezburgerworthy_cheeses()

    conn = sqlite3.connect('nomnom.db')
    conn.rollback()
    c = conn.cursor()
    c.execute('create table if not exists nom (kind text, link text, name text)')
    for starter in starters:
        c.execute("insert into nom values ('Starter',?,?)", starter)
    for mainCourse in mains:
        c.execute("insert into nom values ('MainCourse',?,?)", mainCourse)
    for dessert in desserts:
        c.execute("insert into nom values ('Dessert',?,?)", dessert)
    for cheese in cheeses:
        c.execute("insert into nom values ('Cheese',?,?)", cheese)
    conn.commit()
    c.close()


def spit_it_out():
    random_starter = get_random_dish("Starter")
    random_main = get_random_dish("MainCourse")
    random_dessert = get_random_dish("Dessert")
    random_cheeses = [get_random_dish("Cheese") for _ in range(3)]
    return random_starter, random_main, random_dessert, random_cheeses


def get_mouthwatering_starters():
    mouthwatering_starters = [get_pages_with_no_pictures(starter) for starter in starters]
    return list(chain.from_iterable(mouthwatering_starters))


def get_delightful_main_courses():
    delightful_main_courses = [get_pages_with_no_pictures(mainCourse) for mainCourse in mainCourses]
    return list(chain.from_iterable(delightful_main_courses))


def get_yummylicious_desserts():
    yummylicious_desserts = [get_pages_with_no_pictures(dessert) for dessert in desserts]
    return list(chain.from_iterable(yummylicious_desserts))


def get_cheezburgerworthy_cheeses():
    cheezbugerworthy_cheeses = [get_pages_with_no_pictures(cheese) for cheese in cheeses]
    return list(chain.from_iterable(cheezbugerworthy_cheeses))


def get_pages_with_no_pictures(start):
    pages = wiki_crawler.get_all_pages_starting_from(start)
    pages_with_no_pictures = []
    for page in pages:
        if wiki_crawler.found_no_pictures_in(page):
            print(u"No images:", page.encode('utf-8'))
            pages_with_no_pictures.append((wiki_crawler.generate_link_from_title(page), page))
        else:
            print(u"Has images, ignoring page:", page.encode('utf-8'))
    return pages_with_no_pictures


def get_random_dish(kind):
    conn = sqlite3.connect('nomnom.db')
    c = conn.cursor()
    c.execute('select * from nom where kind=?', (kind,))
    nom = random.choice(c.fetchall())
    c.close()
    return nom


def print_recommendation(menu):
    print("Empfehlung des Chefs!\nVorspeise: %s\nHauptspeise: %s\nNachtisch: %s\n" % (
        menu[0][2], menu[1][2], menu[2][2]))
    print(u"\n... Und eine Käseplatte aus würzigem %s, sahnigem %s, und %s nach altem schweizer Rezept." % (
        menu[3][0][2], menu[3][1][2], menu[3][2][2]))


if __name__ == "__main__":
    grab_food()
    print_recommendation(spit_it_out())
