from selenium import webdriver
import pandas as pd
from selenium.webdriver.common.by import By


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
webPageName = 'Hir TV'
pageIndex = 1
while pageIndex <= numberOfPages:
    currentPage = getLink + str(pageIndex)
    driver.get(currentPage)
    for i in range(0,20,1):
        hirTvArticles = driver.find_elements(By.CLASS_NAME, 'focuspoint')
        hirTvArticles[i].click()
        saveHeadlines.append(driver.find_element(By.CSS_SELECTOR, "h1").text)
        saveArticleText.append(driver.find_element(By.CLASS_NAME, 'article-content').text)
        saveLeadArticle.append(driver.find_element(By.CLASS_NAME, 'font-weight-bold.article-lead').text)
        driver.back()
        driver.implicitly_wait(3)
    pageIndex+= 1

dict = {'Title':saveHeadlines, 'Lead text': saveLeadArticle, 'Text':saveArticleText, 'News site': webPageName, 'Keyword': getKeyword}
df= pd.DataFrame(dict)
df.to_csv('articlesfromhirtv.csv', index=False, encoding='utf-8-sig')
driver.quit()
