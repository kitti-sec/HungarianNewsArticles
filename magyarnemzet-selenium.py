from email.header import Header
from selenium import webdriver
import pandas as pd
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os.path

getLink = input("Type in the Magyar Nemzet link without the current_page count number: ")
numberOfPages = int(input("How many pages would you like to collect? "))
getKeyword = input("What keyword did you search for? ")
driver = webdriver.Chrome(executable_path='C:/Users/shiro/Downloads/chromedriver_win32/chromedriver')

driver.get(getLink)

# saveHeadlines = []
# saveArticleText = []
# saveLeadArticle = []
# saveArticleDate = []
webPageName = 'Magyar Nemzet'
pageIndex = 1

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
    articles = driver.find_elements(By.XPATH, "//a[@class='article-link ng-star-inserted']")
    for i in range(21):
        # len(articles)
        WebDriverWait(driver, 50).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'result-list'))
        )
        
        articles = driver.find_elements(By.CSS_SELECTOR, "body > app-root > app-base > app-search > div > div.search-feature > div.result-list > app-article-card > article > div.article-right.ng-star-inserted > a")
        articles[i].click()
        driver.implicitly_wait(4)
        saveHeadlines.append(driver.find_element(By.CLASS_NAME, "title").text)

        articleTextList = driver.find_elements(By.TAG_NAME, 'app-article-text')
        for i in articleTextList:
            articleTextCombined = ''
            articleTextCombined = articleTextCombined + i.text
        saveArticleText.append(articleTextCombined)

        if driver.find_element(By.CLASS_NAME, 'mbm-subtitle'):
            saveLeadArticle.append(driver.find_element(By.CLASS_NAME, 'mbm-subtitle').text)
        else:
            saveLeadArticle.append('none')
        saveArticleDate.append(driver.find_element(By.XPATH, "//div[@class='info-line']//div[@class='right']").text)

        saveLink.append(driver.current_url)

        driver.back()
    pageIndex+= 1
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

