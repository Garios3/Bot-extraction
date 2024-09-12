
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
def extraccion(comuna, word1, word2, word3, n_tweets, df):
      
    driver.get(url) # Navegar en pagina
    time.sleep(random.randint(7,12))
    buscar = driver.find_element('xpath', '/html/body/div[1]/div/div/div[2]/main/div/div/div/div[2]/div/div[2]/div/div/div/div[1]/div/div/div/form/div[1]/div/div/div/div/div[2]/div/input ') # Boton de busqueda
    buscar.click()
    time.sleep(random.randint(1,5))
    # Generacion de consulta
    sql_consulta = json.dumps(comuna) + ' (' + json.dumps(word1) + ' OR ' + json.dumps(word2) + ' OR ' + json.dumps(word3) + ')' + ' lang:es until:2022-12-31 since:2022-01-01 -filter:links'

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

    for i in range(999):
        try:
            tweets = driver.find_elements(By.CSS_SELECTOR, 'div[data-testid=cellInnerDiv]')
            is_a_tweet = tweets[0].find_elements(By.XPATH, './/article[@data-testid="tweet"]')
           
            # check if list is not empty (i.e. check if element is a tweet or a "who to follow" element)
            if is_a_tweet:
                date = tweets[0].find_element(By.XPATH, './/time').get_attribute('datetime').split('T')[0]
                tweet_text = is_a_tweet[0].text.replace('\n','')
                publisher = re.search('@(.*)·',tweet_text).group(1)
                df = pd.concat([df, pd.DataFrame.from_records([{'comuna': comuna, 'word1': word1, 'word2': word2, 'word3': word3, 'publisher': publisher, 'date': date, 'texto': tweet_text, 'query': sql_consulta}])], ignore_index=True)                                          
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

'''
user = gonzalo.rios60@gmail.com
pass = G@rv527572
'''

# Definicion del DataFrame
tweets_df = pd.DataFrame(columns = ['comuna','word1','word2','word3','publisher','date','texto','query'])

# Solo comunas Region Metropolitana
comunas = ['santiago centro',
           'cerrillos',
           'cerro navia',
           'conchali',
           'el bosque',
           'estacion central',
           'huechuraba',
           'comuna independencia',
           'la cisterna',
           'la florida',
           'la granja',
           'la pintana',
           'comuna la reina',
           'las condes',
           'lo barnechea',
           'lo espejo',
           'lo prado',
           'macul',
           'maipu',
           'ñuñoa',
           'pedro aguirre cerda',
           'peñalolen',
           'providencia',
           'pudahuel',
           'quilicura',
           'quinta normal',
           'recoleta',
           'renca',
           'san joaquin',
           'san miguel',
           'san ramon',
           'vitacura',
           'puente alto',
           'pirque',
           'san jose de maipo',
           'colina',
           'lampa',
           'tiltil',
           'san bernardo',
           'buin',
           'calera de tango',
           'paine',
           'melipilla',
           'alhue',
           'curacavi',
           'comuna maria pinto',
           'san pedro',
           'talagante',
           'el monte',
           'isla de maipo',
           'padre hurtado',
           'peñaflor']

Educacion = ['educacion', 'universidad', 'trabajador', 'estudiantes', 'profesor', 'empleo']
Salud = ['salud', 'hospital', 'doctor', 'bienestar', 'deporte', 'salud mental', 'medicina']
Seguridad = ['corrupcion', 'policia', 'privacidad', 'seguridad', 'libertad', 'inseguridad', 'violencia', 'asalto', 'robo', 'delincuencia']

random.seed(12345)
Educacion_words = random.sample(Educacion, 2)
print(Educacion_words)

random.seed(12345)
Salud_words = random.sample(Salud, 2)
print(Salud_words)

random.seed(12345)
Seguridad_words = random.sample(Seguridad, 2)
print(Seguridad_words)

import itertools

a = [Educacion_words, Salud_words, Seguridad_words]
combinaciones = list(itertools.product(*a))

# Ejemplo de prueba
i = 0
j = 0
tweets_df = extraccion(comunas[i], word1 = combinaciones[j][0], word2 = combinaciones[j][1], word3 = combinaciones[j][2], n_tweets = 999, df = tweets_df)

#for i in range(8,len(comunas)):
#    for j in range(len(combinaciones)):
#        try:
#            tweets_df = extraccion(comunas[i], word1 = combinaciones[j][0], word2 = combinaciones[j][1], word3 = combinaciones[j][2], n_tweets = 999, df = tweets_df)
#            time.sleep(random.randint(10, 60))
#        except:
#            continue

#tweets_df = extraccion(comunas[i], word1 = combinaciones[j][0], word2 = combinaciones[j][1], word3 = combinaciones[j][2], n_tweets = 999, df = tweets_df)
