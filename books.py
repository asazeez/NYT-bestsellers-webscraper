from bs4 import BeautifulSoup
from selenium import webdriver
import requests
from csv import writer
import pandas as pd
import amazon

# Fiction books
urlFEbook = "https://www.nytimes.com/books/best-sellers/combined-print-and-e-book-fiction/"
urlFHardcover = "https://www.nytimes.com/books/best-sellers/hardcover-fiction/"
urlFPaperback = "https://www.nytimes.com/books/best-sellers/trade-fiction-paperback/"

# Nonfiction books
urlNFEbook = "https://www.nytimes.com/books/best-sellers/combined-print-and-e-book-nonfiction/"
urlNFHardcover = "https://www.nytimes.com/books/best-sellers/hardcover-nonfiction/"
urlNFPaperback = "https://www.nytimes.com/books/best-sellers/paperback-nonfiction/"
urlMisc = "https://www.nytimes.com/books/best-sellers/advice-how-to-and-miscellaneous/"

# Bookstore urls
amzEBbook = "https://www.amazon.ca/b/?ie=UTF8&node=17450799011&ref_=sv_b_7"
indFic = "https://www.chapters.indigo.ca/en-ca/books/nyt-bestsellers/fiction/?mc=NYTBestsellers&lu=LeftNav_Fiction"
indNonFic = "https://www.chapters.indigo.ca/en-ca/books/nyt-bestsellers/non-fiction/?mc=NYTBestsellers&lu=LeftNav_Non-Fiction"
indAdv = "https://www.chapters.indigo.ca/en-ca/books/nyt-bestsellers/lifestyle/?mc=NYTBestsellers&lu=LeftNav_HowTo"

# List of URLs
urlList = [urlFEbook, urlFHardcover, urlFPaperback, urlNFEbook, urlNFHardcover, urlNFPaperback, urlMisc]
lists = []
indSearch = []
azSearch = []
azPrices = []
azBooks = []
azHard = []
azPaper = []
azEbook = []
indBooks = []
books = {}
new = []
indNew = []
indHard = []
indPaper = []
indEbook = []
azTitleCheck = set()
indTitleCheck = set()
class Book:

  def __init__(self, title, type, price):
    self.title = title
    self.type = type
    self.price= price

class infoBook:
    def __init__(self, title, hard, paper, ebook):
        self.title = title
        self.hard = hard
        self.paper = paper
        self.ebook = ebook


def copy(arr):
    for item in arr:
        lists.append(item)

#scrapes the books from the website list
def bookScrape(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    list = soup.find_all('li', class_="css-13y32ub")
    copy(list)

def checkBook (title, type, price, arr):
    for key in books:
        keyL = key.lower()
        if keyL in title:
            arr.append(Book(key, type, price))
            azTitleCheck.add(key)

def compBooks (books,checked, search):
    for key in books:
        if key not in checked:
            search.append(key)
    return search

def sortBook (books, title, arr):
    paperback= None
    hardcover= None
    ebook= None
    for book in books:
        if title.lower() in book.title.lower():
            if book.type == 'Paperback':
                paperback = book.price
            if book.type == 'Hardcover':
                hardcover = book.price
            if book.type =='Kindle Edition':
                ebook = book.price
    arr.append(infoBook(title, hardcover, paperback, ebook))
    print (title, hardcover, paperback, ebook)

def objectInfo(books, hardArr,paperArr,ebookArr):
    for book in books:
        hardArr.append(book.hard)
        paperArr.append (book.paper)
        ebookArr.append(book.ebook)

def changeDict (dict):
    titles = []
    blurb = []
    authour = []
    for key in dict:
        titles.append(key)
        value = dict[key]
        blurb.append(value[1])
        authour.append(value[0])
    new = {'Title':titles,
           'Authour': authour,
           'Description': blurb }
    return new

def scrapeNYT():
    for url in urlList:
        bookScrape(url)

    for list in lists:
        title = list.find('h3', class_="css-5pe77f").text
        authour = list.find('p', class_="css-hjukut").text.replace('by','')
        blurb = list.find ('p', class_= "css-14lubdp").text
        bookInfo = [title,authour]
        books[title] = [authour, blurb]
        print (bookInfo)

def prinlist():
    for item in azBooks:
        print (item.title)
        print(item.price)

def sortAzBooks (arrBooks):
    for key in arrBooks:
        sortBook(azBooks,key, new)

def sortIndBooks (arrBooks):
    for key in arrBooks:
        sortBook(indBooks,key, indNew)


def convertPD():
    newBook = changeDict(books)
    objectInfo(new, azHard, azPaper, azEbook)
    objectInfo(indNew, indHard, indPaper, indEbook)
    df = pd.DataFrame.from_dict(newBook)
    df['AzHardcover'] = azHard
    df['AzPaperback'] = azPaper
    df['AzEbook'] = azEbook
    df['IndHardcover'] = indHard
    df['IndPaperback'] = indPaper
    df['IndEbook'] = indEbook
    df.to_csv ('nyt-bestseller.csv', index=False, encoding='utf8')