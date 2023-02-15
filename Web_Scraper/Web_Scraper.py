from bs4 import BeautifulSoup
import os
import time
import re
from boxer import Boxer
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
    
def populate(text):  
    match text:
        case "division":
            return "Bad request"
        case "":
            return "Not found"
        case "":
            return "I'm a teapot"

        # If an exact match is not confirmed, this last case will be used if provided
        case _:
            return "Something's wrong with the internet"
  
## Use Chrome webdriver from selenium to access boxrec initially
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
baseURL = "https://boxrec.com"
driver.get(baseURL)

## Login and navigate to ratings section, which contains list of boxers
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

## Get list of links to different boxers (50) from the first page
links = driver.find_elements(By.CLASS_NAME, "personLink")
boxers = []

for link in links:
    driver.execute_script("arguments[0].scrollIntoView(true);", link)
    time.sleep(2)
    link.click()
    
    ## Click each link, scrape the boxers information, then return to the ratings page
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    fighter_data = soup.find_all('td')

    my_regex = re.compile("#")
    fighter_ranks = soup.find_all("a", text=my_regex)

    current_field = ""
    boxer = Boxer()
    boxer.name = soup.h1.text.strip()
    boxer.wins = soup.find("td", class_="bgW").text.strip()
    boxer.losses = soup.find("td", class_="bgL").text.strip()
    boxer.draws = soup.find("td", class_="bgD").text.strip()
    boxer.KOW = soup.find("th", class_="textWon").text.strip()
    boxer.KOL = soup.find("th", class_="textLost").text.strip()
    boxer.rank = fighter_ranks[0].text.strip()
    for index, td in enumerate(fighter_data):
        current_field = td.text.strip()
        match current_field:
            case 'rank':
                print[fighter_data[index+1].text.strip()]
                boxer.rank = fighter_data[index+1].text.strip()
            case 'bouts':
                boxer.bouts = fighter_data[index+1].text.strip()
            case 'rounds':
                boxer.rounds = fighter_data[index+1].text.strip()
            case 'debut':
                boxer.debut = fighter_data[index+1].text.strip()
            case 'titles':
                boxer.titles = fighter_data[index+1].text.strip()
            case 'sex':
                boxer.sex = fighter_data[index+1].text.strip()
            case 'alias':
                boxer.alias = fighter_data[index+1].text.strip()
            case 'age':
                boxer.age = fighter_data[index+1].text.strip()
            case 'nationality':
                boxer.nationality = fighter_data[index+1].text.strip()
            case 'height':
                boxer.height = fighter_data[index+1].text.strip()
            case 'reach':
                boxer.reach = fighter_data[index+1].text.strip()
            case 'residence':
                boxer.residence = fighter_data[index+1].text.strip()
            case 'stance':
                boxer.stance = fighter_data[index+1].text.strip()
            case 'division':
                boxer.weightclass = fighter_data[index+1].text.strip()
        
    boxers.append(boxer)
    driver.back()




    


##TODO: Add boxer data to excel spreadsheet & PostgreSQL database

