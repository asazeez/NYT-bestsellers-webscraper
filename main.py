import indigo
import amazon
import books
import time
import constants as const
import tables

nyt = books.scrapeNYT()
azDriver = amazon.driver
azObject = amazon.Amazon
azPrice = azObject.loadPage()
azObject.getList(azPrice)
time.sleep(3)
new = books.compBooks(books.books, books.azTitleCheck,books.azSearch)
for key in books.books:
  azObject.searchBook(key)

indDriver = indigo.driver
indObject = indigo.Indigo

indFicPrice = indObject.loadPage(const.INDFIC)
indObject.getList(indFicPrice)

indNFPrice = indObject.loadPage(const.INDNONFIC)
indObject.getList(indNFPrice)

indADPrice = indObject.loadPage(const.INDADV)
indObject.getList(indADPrice)

time.sleep(3)
indNew = books.compBooks(books.books, books.indTitleCheck,books.indSearch)
for title in indNew:
    indObject.bookSearch(title)

books.sortAzBooks(books.books)
books.sortIndBooks(books.books)
books.convertPD()
tables.newTable()