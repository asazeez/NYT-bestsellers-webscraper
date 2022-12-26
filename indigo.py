from selenium import webdriver
from bs4 import BeautifulSoup
import constants as const
from selenium.webdriver.common.by import By
import time
import books

driver = webdriver.Chrome(executable_path='C:/Users/atiya/Downloads/chromedriver_win32 (2)/chromedriver.exe')

class Indigo:

    def loadPage(url):
        driver.get(url)
        driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
        time.sleep(1)
        content = driver.page_source
        soup = BeautifulSoup(content,features="html.parser")
        indPrices = soup.find_all('div', class_="product-list__product product-list__product-container")
        return indPrices

    def getList (prices):
        for price in prices:
            titles = price.find('a', class_="product-list__product-title").text
            bookPrice = price.find('p', class_="product-list__price--orange")
            type = price.find('div', class_="product-list__product-format").text
            if bookPrice is not None:
                bookPrice = bookPrice.text.replace('online',"").replace('$','')
            bookInfo = [titles, type, bookPrice]
            books.checkBook(titles.lower(), type, bookPrice, books.indBooks)
            print(bookInfo)

    def bookSearch (title):
        book_search= driver.find_element(By.ID, 'header__quick-search')
        book_search.clear()
        book_search.send_keys(title)
        search_button = driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]')
        search_button.click()
        soups = BeautifulSoup(driver.page_source,features="html.parser")
        verity = soups.find('div', class_="product-list__product product-list__product-container")
        paperback = verity.find_all('span', class_="product-list__format-text-wrapper")
        for cost in paperback:
            #print(cost.text)
            costArr = (cost.text.split('$'))
            bookType = costArr[0]
            if 'sold out' in bookType:
                costArr = cost.text.split('sold out')
                bookType=costArr[0]
                bookPrice = None
            else:
                bookPrice = float(costArr[1])
            if bookType == 'Kobo ebook':
                bookType = 'Kindle Edition'
            books.indBooks.append(books.Book(title, bookType, bookPrice))

    def __exit__(self, exc_type, exc_val, exc_tb):
        driver.quit()

