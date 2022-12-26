from selenium import webdriver
from bs4 import BeautifulSoup
import constants as const
from selenium.webdriver.common.by import By
import time
import requests
import books
import books

driver = webdriver.Chrome(executable_path='C:/Users/atiya/Downloads/chromedriver_win32 (2)/chromedriver.exe')
azTitleCheck=()
class Amazon:

    def loadPage ():
        driver.get("https://www.amazon.ca/b/?ie=UTF8&node=17450799011&ref_=sv_b_7")
        azPage = requests.get("https://www.amazon.ca/b/?ie=UTF8&node=17450799011&ref_=sv_b_7")
        azSoup = BeautifulSoup(azPage.content, 'html.parser')
        azPrices = azSoup.find_all('li', class_="a-carousel-card acswidget-carousel__card")
        return azPrices

    def getList (prices):
        for price in prices:
            type = price.find('span', class_="acs-product-block__binding-value").text
            titles = price.find('span', class_="a-truncate-full").text
            bookPrice = price.find('span', class_="a-offscreen")
            if bookPrice is not None:
                bookPrice = float(bookPrice.text.replace('$',''))
            bookInfo = [type, titles, bookPrice]
            books.checkBook(titles.lower(), type, bookPrice, books.azBooks)

    def searchBook(title):
        book_search = driver.find_element(By.ID, 'twotabsearchtextbox')
        book_search.clear()
        book_search.send_keys(title)
        search_button = driver.find_element(By.ID, 'nav-search-submit-button')
        search_button.click()
        soups = BeautifulSoup(driver.page_source, features="html.parser")
        try:
            title = soups.find('div', class_="s-result-item s-asin sg-col-0-of-12 sg-col-16-of-20 sg-col s-widget-spacing-small sg-col-12-of-16").find('span',class_="a-size-medium a-color-base a-text-normal").text
            #title = soups.find('div',class_="s-result-item").find(
             #   'span', class_="a-size-medium a-color-base a-text-normal").text
            book_search = driver.find_element(By.LINK_TEXT, f'{title}').click()
            soups = BeautifulSoup(driver.page_source, features="html.parser")
            paperback = soups.find_all('li', class_="swatchElement")

            for cost in paperback:
                bookType = cost.find('span', class_="a-button-inner").find('span').text
                if bookType is None:
                    bookType = cost.find('span', class_="audible_mm_title ").find('span')
                bookPrice = cost.find('span', class_="a-color-secondary")
                if bookPrice is None:
                    bookPrice = cost.find('span', class_="a-color-base")
                bookPrice = bookPrice.text.replace('\n', "")
                bookPrices = bookPrice.replace('$', '').replace('from','')
                books.azBooks.append(books.Book(title, bookType, float(bookPrices)))
        except:
            books.azBooks.append(books.Book(title, None, None))


    def __exit__(self, exc_type, exc_val, exc_tb):
        driver.quit()

