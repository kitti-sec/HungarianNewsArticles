from selenium import webdriver
import pandas as pd
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

getLink = input("Type in the Magyar Nemzet link without the current_page count number: ")
numberOfPages = int(input("How many pages would you like to collect? "))
getKeyword = input("What keyword did you search for? ")
driver = webdriver.Chrome(executable_path='C:/Users/shiro/Downloads/chromedriver_win32/chromedriver')

driver.get(getLink)

saveHeadlines = []
saveArticleText = []
saveLeadArticle = []
saveArticleDate = []
webPageName = 'Magyar Nemzet'
pageIndex = 0

driver.implicitly_wait(3)
driver.find_element(By.LINK_TEXT, "Beleegyezés").click()

while pageIndex <= numberOfPages:
    currentPage = getLink + str(pageIndex)
    driver.get(currentPage)
    articles = driver.find_elements(By.XPATH, "//a[@class='article-link ng-star-inserted']")
    for i in range(len(articles)):
        WebDriverWait(driver, 50).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'result-list'))
        )
        articles = driver.find_elements(By.XPATH, "//a[@class='article-link ng-star-inserted']")
        articles[i].click()
        driver.implicitly_wait(4)
        saveHeadlines.append(driver.find_element(By.CLASS_NAME, "title").text)
        saveArticleText.append(driver.find_element(By.TAG_NAME, 'app-article-text').text)
        if driver.find_element(By.CLASS_NAME, 'mbm-subtitle'):
            saveLeadArticle.append(driver.find_element(By.CLASS_NAME, 'mbm-subtitle').text)
        else:
            saveLeadArticle.append('none')
        saveArticleDate.append(driver.find_element(By.CLASS_NAME, 'right').text)
        driver.back()
    pageIndex+= 1

dict = {'Title':saveHeadlines, 'Lead text': saveLeadArticle, 'Text':saveArticleText, 'Date':saveArticleDate, 'News site': webPageName, 'Keyword': getKeyword}
df= pd.DataFrame(dict)
df.to_csv('articlesfrommagyarnemzet' + getKeyword + '.csv', index=False, encoding='utf-8-sig')
driver.quit()

