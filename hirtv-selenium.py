from keyword import kwlist
from lib2to3.pgen2.pgen import DFAState
from operator import index
from xml.dom.minidom import Element
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait 
import pandas as pd
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import csv

getLink = input("Type in the Hir TV link: ")
# numberOfPages = input("How many pages would you like to collect?")
getKeyword = input("What did you searched for?")
driver = webdriver.Chrome(executable_path='C:/Users/shiro/Downloads/chromedriver_win32/chromedriver')

driver.get(getLink)
driver.implicitly_wait(3)
driver.find_element(By.CLASS_NAME, "css-1k8602u").click()
driver.implicitly_wait(3)

#  20cikk van egy oldalon

saveHeadlines = []
saveArticleText = []
saveLeadArticle = []
webPageName = 'Hir TV'

hirTvArticles = driver.find_elements(By.CLASS_NAME, 'focuspoint')
driver.implicitly_wait(2)
articleLinks = [elem.get_attribute('href') for elem in hirTvArticles]

driver.implicitly_wait(3)
# 0,20,1 a jo
for i in range(0,2,1):
    hirTvArticles = driver.find_elements(By.CLASS_NAME, 'focuspoint')
    hirTvArticles[i].click()
    saveHeadlines.append(driver.find_element(By.CSS_SELECTOR, "h1").text)
    saveArticleText.append(driver.find_element(By.CLASS_NAME, 'article-content').text)
    saveLeadArticle.append(driver.find_element(By.CLASS_NAME, 'font-weight-bold.article-lead').text)
    driver.back()
    driver.implicitly_wait(3)

print(saveHeadlines)
print(saveArticleText)
print(saveLeadArticle)

dict = {'Title':saveHeadlines, 'Lead text': saveLeadArticle, 'Text':saveArticleText, 'News site': webPageName, 'Keyword': getKeyword}
df= pd.DataFrame(dict)
df.to_csv('articles.csv', index=False, encoding='utf-8-sig')
driver.quit()
