from email.header import Header
import time
from selenium import webdriver
import pandas as pd
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os.path
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException

from selenium.webdriver.chrome.options import Options

path_to_extension = r'C:\All\projects\future\Charles Study\MA thesis\app\propagandaanalysis\1.44.4_3'
chrome_options = Options()
chrome_options.add_argument('load-extension=' + path_to_extension)



getLink = input("Type in the Magyar Nemzet link without the current_page count number: ")
pageIndex = int(input('From (page) '))
numberOfPages = int(input("To (page) "))
getKeyword = input("What keyword did you search for? ")

driver = webdriver.Chrome(executable_path='C:/Users/shiro/Downloads/chromedriver_win32/chromedriver',chrome_options=chrome_options)
driver.create_options()
driver.get(getLink)

webPageName = 'Magyar Nemzet'


driver.implicitly_wait(3)
driver.find_element(By.CSS_SELECTOR, "body > div.fc-consent-root > div.fc-dialog-container > div.fc-dialog.fc-choice-dialog > div.fc-footer-buttons-container > div.fc-footer-buttons > button.fc-button.fc-cta-consent.fc-primary-button").click()

while pageIndex <= numberOfPages:
    saveHeadlines = []
    saveArticleText = []
    saveLeadArticle = []
    saveArticleDate = []
    saveLink = []
    currentPage = getLink + str(pageIndex)
    driver.get(currentPage)
    # articles = driver.find_elements(By.CSS_SELECTOR, "body > app-root > app-base > app-search > div > div.search-feature > div.result-list > app-article-card > article > div.article-right.ng-star-inserted > a")
    articles = driver.find_elements(By.CSS_SELECTOR, "body > app-root > app-base > app-search > div > div.search-feature > div.result-list > app-article-card > article > a")
    articlesWithPics = driver.find_elements(By.CSS_SELECTOR, "body > app-root > app-base > app-search > div > div.search-feature > div.result-list > app-article-card > article > div.article-right.ng-star-inserted > a")
    articles.extend(articlesWithPics)
    lengthofList = len(articles)
    for i in range(lengthofList):
        saveSearchPage = driver.current_url
        try:

            WebDriverWait(driver, 50).until(
                EC.presence_of_element_located((By.CLASS_NAME, 'result-list'))
            )
            
            # articles = driver.find_elements(By.CSS_SELECTOR, "body > app-root > app-base > app-search > div > div.search-feature > div.result-list > app-article-card > article > div.article-right.ng-star-inserted > a")
            articles = driver.find_elements(By.CSS_SELECTOR, "body > app-root > app-base > app-search > div > div.search-feature > div.result-list > app-article-card > article > a")
            articlesWithPics = driver.find_elements(By.CSS_SELECTOR, "body > app-root > app-base > app-search > div > div.search-feature > div.result-list > app-article-card > article > div.article-right.ng-star-inserted > a")
            articles.extend(articlesWithPics)


            articles[i].click()
            driver.implicitly_wait(4)
               
            handle404 = driver.find_element(By.CLASS_NAME, "title").text
            if handle404 == 'A keresett oldal nem található.':
                raise NoSuchElementException('404')

            saveHeadlines.append(driver.find_element(By.CLASS_NAME, "title").text)

            # /// Add together different sections to one article ///
            articleTextList = driver.find_elements(By.TAG_NAME, 'app-article-text')
            articleTextCombined = ''
            for i in articleTextList:
                articleTextCombined = articleTextCombined + i.text
            saveArticleText.append(articleTextCombined)

            if driver.find_element(By.CLASS_NAME, 'mbm-subtitle'):
                saveLeadArticle.append(driver.find_element(By.CLASS_NAME, 'mbm-subtitle').text)
            else:
                saveLeadArticle.append('none')
            saveArticleDate.append(driver.find_element(By.XPATH, "//div[@class='info-line']//div[@class='right']").text)

            saveLink.append(driver.current_url)

            driver.back()
        except (NoSuchElementException, TimeoutException) as err:
            print("No such element exception or Timeout Exception")
            driver.get(saveSearchPage)
            continue

    pageIndex+= 1
    # /// Save data to .csv, append after every page (21 articles)
    file_exists = os.path.exists('articlesfrommagyarnemzet' + getKeyword + '.csv')
    if file_exists:
        dict = {'Title':saveHeadlines, 'Lead text': saveLeadArticle, 'Text':saveArticleText, 'Date':saveArticleDate, 'News site': webPageName, 'Keyword': getKeyword, 'URL': saveLink}
        df= pd.DataFrame(dict)
        df.to_csv('articlesfrommagyarnemzet' + getKeyword + '.csv', index=False, header=None, encoding='utf-8-sig', mode='a')
    else:
        dict = {'Title':saveHeadlines, 'Lead text': saveLeadArticle, 'Text':saveArticleText, 'Date':saveArticleDate, 'News site': webPageName, 'Keyword': getKeyword,  'URL': saveLink}
        df= pd.DataFrame(dict)
        df.to_csv('articlesfrommagyarnemzet' + getKeyword + '.csv', index=False, encoding='utf-8-sig', mode='a')


driver.quit()

