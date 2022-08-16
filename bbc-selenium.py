from email.header import Header
from selenium import webdriver
import pandas as pd
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os.path
from selenium.common.exceptions import NoSuchElementException

getLink = input("Type in the BBC link without the current_page count number: ")
pageIndex = int(input('From (page) '))
numberOfPages = int(input("To (page) "))
getKeyword = input("What keyword did you search for? ")
webPageName = 'BBC'

driver = webdriver.Chrome(executable_path='C:/Users/shiro/Downloads/chromedriver_win32/chromedriver')
driver.get(getLink)
WebDriverWait(driver, 50).until(
    EC.presence_of_element_located((By.XPATH, '//*[@id="main-content"]'))
)

driver.implicitly_wait(4)

while pageIndex <= numberOfPages:
    saveHeadlines = []
    saveArticleText = []
    saveLeadArticle = []
    saveArticleDate = []
    saveLink = []
    currentPage = getLink + str(pageIndex)
    driver.get(currentPage)
    articles = driver.find_elements(By.XPATH, "//div[@spacing='2']//a")
    driver.implicitly_wait(3)
    lengthofList = len(articles)
    for i in range(lengthofList):
        saveSearchPage = driver.current_url
        try:

            WebDriverWait(driver, 50).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="main-content"]'))
            )
            articles = driver.find_elements(By.XPATH, "//div[@spacing='2']//a")
            articles[i].click()
            driver.implicitly_wait(4)
            # //// inside the article ///
            if i == 0:
                driver.find_element(By.XPATH, "//p[@class='fc-button-label']").click()
                driver.implicitly_wait(3)
            
            saveHeadlines.append(driver.find_element(By.ID, "main-heading").text)
            saveLink.append(driver.current_url)
            saveArticleDate.append(driver.find_element(By.TAG_NAME, "time").text)
            driver.implicitly_wait(15)
            articleTextList = driver.find_elements(By.XPATH, "//div[@data-component='text-block']")
            # articleTextList = driver.find_elements(By.TAG_NAME, 'p')
            articleTextCombined = ''
            for i in articleTextList:
                articleTextCombined = articleTextCombined + ' ' + i.text
            saveArticleText.append(articleTextCombined)
            driver.back()

        except (NoSuchElementException):
            print("No such element exception")
            driver.get(saveSearchPage)
            continue
    pageIndex+= 1

       # /// Save data to .csv, append after every page (21 articles)
    file_exists = os.path.exists('articlesfrombbc' + getKeyword + '.csv')
    if file_exists:
        dict = {'Title':saveHeadlines, 'Text':saveArticleText, 'Date':saveArticleDate, 'News site': webPageName, 'Keyword': getKeyword, 'URL': saveLink}
        df= pd.DataFrame(dict)
        df.to_csv('articlesfrombbc' + getKeyword + '.csv', index=False, header=None, encoding='utf-8-sig', mode='a')
    else:
        dict = {'Title':saveHeadlines,  'Text':saveArticleText, 'Date':saveArticleDate, 'News site': webPageName, 'Keyword': getKeyword,  'URL': saveLink}
        df= pd.DataFrame(dict)
        df.to_csv('articlesfrombbc' + getKeyword + '.csv', index=False, encoding='utf-8-sig', mode='a')


driver.quit()
