# -*- coding: utf-8 -*-
import sqlite3
import random
from itertools import chain
import wikiCrawler

starters = [u"Kategorie:Salat",
            u"Kategorie:Suppe",
            u"Kategorie:Vorspeise"]
mainCourses = [u"Kategorie:Gemüsegericht",
            u"Kategorie:Käsegericht",
            u"Kategorie:Kartoffelgericht",
            u"Kategorie:Nudelgericht",
            u"Kategorie:Reisgericht",
            u"Kategorie:Fondue",
            u"Kategorie:Fleischgericht",
            u"Kategorie:Fischgericht",
            u"Kategorie:Eierspeise"]
sides = [u"Kategorie:Beilage"]
desserts = [u"Kategorie:Süßspeise"]
cheeses = [u"Kategorie:Käsesorte"]

def grabFood():
    starters = getMouthwateringStarters()
    mains = getDelightfulMainCourses()
    desserts = getYummyliciousDesserts()
    cheeses = getCheezburgerworthyCheeses()
    
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

def spitItOut():
    randomStarter = getRandomDish("Starter")
    randomMain = getRandomDish("MainCourse")
    randomDessert = getRandomDish("Dessert")
    randomCheeses = [getRandomDish("Cheese") for _ in range(3)]
    return (randomStarter, randomMain, randomDessert, randomCheeses)

def getMouthwateringStarters():
    mouthwateringStarters = [getPagesWithNoPictures(starter) for starter in starters]
    return list(chain.from_iterable(mouthwateringStarters))

def getDelightfulMainCourses():
    delightfulMainCourses = [getPagesWithNoPictures(mainCourse) for mainCourse in mainCourses]
    return list(chain.from_iterable(delightfulMainCourses))
    
def getYummyliciousDesserts():
    yummyliciousDesserts = [getPagesWithNoPictures(dessert) for dessert in desserts]
    return list(chain.from_iterable(yummyliciousDesserts))

def getCheezburgerworthyCheeses():
    cheezbugerworthyCheeses = [getPagesWithNoPictures(cheese) for cheese in cheeses]
    return list(chain.from_iterable(cheezbugerworthyCheeses))

def getPagesWithNoPictures(start):
    pages = wikiCrawler.getAllPagesStartingFrom(start)
    pagesWithNoPictures = [] 
    for page in pages:
        if wikiCrawler.foundNoPicturesIn(page):
            pagesWithNoPictures.append((wikiCrawler.generateLinkFromTitle(page), page))
    return pagesWithNoPictures

def getRandomDish(kind):
    conn = sqlite3.connect('nomnom.db')
    c = conn.cursor()
    c.execute('select * from nom where kind=?', (kind,))
    nom = random.choice(c.fetchall())
    c.close()
    return nom


def printRecommendation(menu):
    print "Empfehlung des Chefs!\nVorspeise: %s\nHauptspeise: %s\nNachtisch: %s\n"%(
        menu[0][2], menu[1][2], menu[2][2])
    print u"\n... Und eine Käseplatte aus würzigem %s, sahnigem %s, und %s nach altem schweizer Rezept."%(
        menu[3][0][2], menu[3][1][2], menu[3][2][2])
        
    

if __name__=="__main__":
    grabFood()
    printRecommendation(spitItOut())
