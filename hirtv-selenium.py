from selenium import webdriver
import pandas as pd
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from re import search
import os.path



getLink = input("Type in the Hir TV link without the current_page count number: ")
numberOfPages = int(input("How many pages would you like to collect? "))
getKeyword = input("What keyword did you search for? ")
driver = webdriver.Chrome(executable_path='C:/Users/shiro/Downloads/chromedriver_win32/chromedriver')

driver.get(getLink)
driver.implicitly_wait(3)
driver.find_element(By.CLASS_NAME, "css-1k8602u").click()
driver.implicitly_wait(3)


#  20cikk van egy oldalon
# TODO: DUPKLIKACIOK MIKOR GYORSAN LEMENT. TOBBSZOR MENNT LE SOROKAT

saveHeadlines = []
saveArticleText = []
saveLeadArticle = []
saveArticleDate = []
webPageName = 'Hir TV'
pageIndex = 51

while pageIndex <= numberOfPages:
    currentPage = getLink + str(pageIndex)
    driver.get(currentPage)
    hirTvArticles = driver.find_elements(By.CLASS_NAME, 'focuspoint')
    print((len(hirTvArticles)))
    for i in range(len(hirTvArticles)):
        try:
            correctUrl = 'hirtv'
            strUrl = driver.current_url
            if search(correctUrl, strUrl):
                pass
            else:
                print('It got redirected to a different webpage.')
                driver.close()
                continue

            WebDriverWait(driver, 50).until(
                EC.presence_of_element_located((By.CLASS_NAME, 'focuspoint'))
                )
            hirTvArticles = driver.find_elements(By.CLASS_NAME, 'focuspoint')
            driver.implicitly_wait(16)
            actions = ActionChains(driver)
            actions.click(hirTvArticles[i])
            actions.perform()
            # hirTvArticles[i].click()
            driver.implicitly_wait(5)
            insideAnArticle = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.TAG_NAME, "article"))
            )
            saveHeadlines.append(driver.find_element(By.TAG_NAME, "h1").text)
            saveArticleText.append(driver.find_element(By.CLASS_NAME, 'article-content').text)
            saveLeadArticle.append(driver.find_element(By.CLASS_NAME, 'font-weight-bold.article-lead').text)
            saveArticleDate.append(driver.find_element(By.CLASS_NAME, 'small.article-date').text)
            driver.back()
            driver.implicitly_wait(15)

                
        except IndexError:
            print('out of range inside loop')
            continue
        
    pageIndex+= 1
    file_exists = os.path.exists('articlesfromhirtv.csv')
    if file_exists:
        dict = {'Title':saveHeadlines, 'Lead text': saveLeadArticle, 'Text':saveArticleText, 'Date':saveArticleDate, 'News site': webPageName, 'Keyword': getKeyword}
        df= pd.DataFrame(dict)
        df.to_csv('articlesfromhirtv.csv', mode='a', index=False, header=None, encoding='utf-8-sig')
    else:
        dict = {'Title':saveHeadlines, 'Lead text': saveLeadArticle, 'Text':saveArticleText, 'Date':saveArticleDate, 'News site': webPageName, 'Keyword': getKeyword}
        df= pd.DataFrame(dict)
        df.to_csv('articlesfromhirtv.csv', index=False, encoding='utf-8-sig')
    
driver.quit()



