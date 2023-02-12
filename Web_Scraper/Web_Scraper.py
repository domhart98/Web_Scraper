from bs4 import BeautifulSoup
import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

def scrape_boxer():
    name = driver.find_element(By.ID, "name")
    age = driver.find_element(By.ID, "")
    bouts = driver.find_element(By.ID, "age")
    wins = driver.find_element(By.ID, "age"), 
    losses = driver.find_element(By.ID, "age"), 
    KOs = driver.find_element(By.ID, "age"), 
    TKOs = driver.find_element(By.ID, "age"), 
    KOlosses = driver.find_element(By.ID, "age"), 
    TKOlosses = driver.find_element(By.ID, "age"), 
    debut = driver.find_element(By.ID, "age"), 
    height = driver.find_element(By.ID, "age"), 
    reach = driver.find_element(By.ID, "age"), 
    nationality = driver.find_element(By.ID, "age"), 
    lastFight = driver.find_element(By.ID, "age"), 
    activityLevel = driver.find_element(By.ID, "age"), 
    titles = driver.find_element(By.ID, "age"), 
    opponents = driver.find_element(By.ID, "age"), 
    fights = driver.find_element(By.ID, "age"), 
    weightClass = driver.find_element(By.ID, "age"), 
    worldRank = driver.find_element(By.ID, "age"), 
    rounds = driver.find_element(By.ID, "age")

    boxer = Boxer(age, name, bouts, wins, losses, KOs, TKOs, KOlosses, TKOlosses, debut, height, reach, nationality, lastFight, activityLevel, titles, opponents, fights, weightClass, worldRank, rounds)
    
    

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
baseURL = "https://boxrec.com"
driver.get(baseURL)

driver.find_element(By.CLASS_NAME, "lozengeButton").click()
time.sleep(2)
driver.find_element(By.ID, "username").send_keys("domhart98@hotmail.com")
driver.find_element(By.ID, "password").send_keys("Spronk1s/Spronk1s/")
driver.find_element(By.CLASS_NAME, "submitButton").click()
driver.find_element(By.LINK_TEXT, "ratings").click()
driver.find_element(By.ID, "select2-r_division-container").click()
driver.find_element(By.CLASS_NAME, "select2-search__field").send_keys("heavy")
driver.find_element(By.CLASS_NAME, "select2-search__field").send_keys(Keys.RETURN)
time.sleep(2)
driver.execute_script("window.scrollTo(0, 100)")
time.sleep(2)
driver.find_element(By.CLASS_NAME, "submitButton").click()




##
links = driver.find_elements(By.CLASS_NAME,"personLink")
##driver.execute_script("window.scrollTo(0, 200)")
for link in links:
    print(link)
    link.click()
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    fighter_data = soup.find_all('td')
    print(fighter_data)
    driver.back()
    


##TODO: Add boxer data to excel spreadsheet & PostgreSQL database


