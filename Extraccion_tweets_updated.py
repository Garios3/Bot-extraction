
# Scraper Twitter

from selenium import webdriver
import pandas as pd
import time
from selenium.webdriver.common.keys import Keys
import random
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import re
import json

'''
Función extracción de tweets
'''

# Extraccion de tweets
def extraccion(comuna, df):
      
    driver.get(url) # Navegar en pagina
    time.sleep(random.randint(7,12))
    buscar = driver.find_element('xpath', '/html/body/div[1]/div/div/div[2]/main/div/div/div/div[2]/div/div[2]/div/div/div/div[1]/div/div/div/form/div[1]/div/div/div/div/div[2]/div/input ') # Boton de busqueda
    buscar.click()
    time.sleep(random.randint(1,5))
    # Generacion de consulta
    sql_consulta = comuna + ' (' + 'Tormenta' + ' OR ' + 'corte de luz' + ' OR ' + ')' + ' lang:es until:2024-08-31 since:2024-08-01 -filter:links'

    buscar.send_keys(sql_consulta)
    buscar.send_keys(Keys.ENTER)
    time.sleep(random.randint(5, 10))
   
    # Mas recientes
    driver.find_element('xpath', '/html/body/div[1]/div/div/div[2]/main/div/div/div/div/div/div[1]/div[1]/div[2]/nav/div/div[2]/div/div[2]/a/div/div/span').click()
    time.sleep(random.randint(5,10))

    # Otro approach
    # wait for tweets to appear in the page
    first_tweet = WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "div[data-testid=cellInnerDiv]")))
    # scroll to first tweet
    driver.execute_script('arguments[0].scrollIntoView({block: "center", behavior: "smooth"});', first_tweet)
    time.sleep(1)
   
    date_for_deletion = '2023-12-31'
#    stop_condition = 999

    for i in range(100):
        try:
            tweets = driver.find_elements(By.CSS_SELECTOR, 'div[data-testid=cellInnerDiv]')
            is_a_tweet = tweets[0].find_elements(By.XPATH, './/article[@data-testid="tweet"]')
           
            # check if list is not empty (i.e. check if element is a tweet or a "who to follow" element)
            if is_a_tweet:
                date = tweets[0].find_element(By.XPATH, './/time').get_attribute('datetime').split('T')[0]
                tweet_text = is_a_tweet[0].text.replace('\n','')
                publisher = re.search('@(.*)·',tweet_text).group(1)
                df = pd.concat([df, pd.DataFrame.from_records([{'publisher': publisher, 'date': date, 'texto': tweet_text, 'query': sql_consulta}])], ignore_index=True)                                          
                if date == date_for_deletion:
                    # delete the tweet
                    ...
                    time.sleep(random.randint(1,4))

            # delete element from HTML
            driver.execute_script('var element = arguments[0]; element.remove();', tweets[0])
#            if i == stop_condition:
#                break
            time.sleep(random.randint(1,4)) # Tiempo de espera entre cada extraccion (fijo)
        except:
            try:
                hidde = driver.find_element('xpath', '/html/body/div[1]/div/div/div[2]/main/div/div/div/div/div/div[3]/section/div/div/div[1]/div/div/div/article/div/div/div[2]/div[2]/div[1]/div/div[2]')
                hidde.click()
                driver.find_element('xpath', '//*[@id="layers"]/div[2]/div/div/div/div[2]/div/div[3]/div/div/div/div[1]/div[2]').click()
                time.sleep(random.randint(1,3))
            except:
                continue

    return df

service = Service(executable_path = 'C:\\Users\\gonza\\Desktop\\Doctorado\\Papers\\Paper Diana - Hanns\\chromedriver.exe')
driver = webdriver.Chrome(service = service)
url = 'https://twitter.com/home?lang=es'

driver.get(url)

# Definicion del DataFrame
tweets_df = pd.DataFrame(columns = ['publisher','date','texto','query'])

tweets_df = extraccion(df = tweets_df, comuna = 'maipu')

