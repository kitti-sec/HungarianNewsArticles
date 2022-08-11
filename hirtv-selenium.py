from selenium import webdriver
import pandas as pd
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC



getLink = input("Type in the Hir TV link without the current_page count number: ")
numberOfPages = int(input("How many pages would you like to collect? "))
getKeyword = input("What keyword did you search for? ")
driver = webdriver.Chrome(executable_path='C:/Users/shiro/Downloads/chromedriver_win32/chromedriver')

driver.get(getLink)
driver.implicitly_wait(3)
driver.find_element(By.CLASS_NAME, "css-1k8602u").click()
driver.implicitly_wait(3)


#  20cikk van egy oldalon

saveHeadlines = []
saveArticleText = []
saveLeadArticle = []
saveArticleDate = []
webPageName = 'Hir TV'
pageIndex = 1

while pageIndex <= numberOfPages:
    currentPage = getLink + str(pageIndex)
    driver.get(currentPage)
    hirTvArticles = driver.find_elements(By.CLASS_NAME, 'focuspoint')
    for i in range(len(hirTvArticles)):
        try:
            hirTvArticles = driver.find_elements(By.CLASS_NAME, 'focuspoint')
            driver.implicitly_wait(16)
            hirTvArticles[i].click()
            driver.implicitly_wait(3)
            saveHeadlines.append(driver.find_element(By.CSS_SELECTOR, "h1").text)
            saveArticleText.append(driver.find_element(By.CLASS_NAME, 'article-content').text)
            saveLeadArticle.append(driver.find_element(By.CLASS_NAME, 'font-weight-bold.article-lead').text)
            saveArticleDate.append(driver.find_element(By.CLASS_NAME, 'small.article-date').text)
            driver.back()
            driver.implicitly_wait(3)
            pageIndex+= 1
        except IndexError:
            print('out of range inside loop')
            continue


dict = {'Title':saveHeadlines, 'Lead text': saveLeadArticle, 'Text':saveArticleText, 'Date':saveArticleDate, 'News site': webPageName, 'Keyword': getKeyword}
df= pd.DataFrame(dict)
df.to_csv('articlesfromhirtv.csv', index=False, encoding='utf-8-sig')
driver.quit()
