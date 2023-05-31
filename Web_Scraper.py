from bs4 import BeautifulSoup
import os
import time
import re
import sqlite3
from boxer import Boxer
from fight import Fight
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# Replace special characters, to insert into SQLite database without failure
normalMap = {'Ñ': 'N', 'ñ': 'n', 'ń': 'n', 'ó': 'o'}
normalize = str.maketrans(normalMap)

# Connect to SQLite database
conn = sqlite3.connect('fight_prophet.db')
cursor = conn.cursor()

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
boxers = []
fights = []

cursor.execute('''DROP TABLE boxers''')
cursor.execute('''DROP TABLE fights''')
cursor.execute('''CREATE TABLE boxers(
    boxerId INTEGER,
    name TEXT,
    age INTEGER,
    alias TEXT,
    nationality TEXT,
    residence TEXT,
    height TEXT,
    reach TEXT,
    stance TEXT,
    weightClass TEXT,
    sex TEXT,
    titles TEXT,
    rank TEXT,
    debut TEXT,
    wins INTEGER,
    losses INTEGER,
    draws INTEGER, 
    KOwins INTEGER,
    KOlosses INTEGER,
    totalRounds INTEGER,
    totalRoundsScheduled INTEGER,
    oppCombinedWins INTEGER,
    oppCombinedLosses INTEGER
    )''')
cursor.execute('''CREATE TABLE fights(
    fightId INTEGER,
    boxer1 INTEGER,
    weight1 TEXT,
    boxer1Wins INTEGER,
    boxer1Losses INTEGER,
    boxer1Draws INTEGER,
    boxer1KOwins INTEGER,
    boxer1KOlosses INTEGER,
    boxer1OppCombinedWins INTEGER,
    boxer1OppCombinedLosses INTEGER,
    boxer1TotalRounds INTEGER,
    boxer1TotalRoundsScheduled INTEGER,
    boxer2 INTEGER,
    weight2 TEXT,
    boxer2Wins INTEGER,
    boxer2Losses INTEGER,
    boxer2Draws INTEGER,
    date TEXT,
    location TEXT,
    winner TEXT,
    methodOfVictory TEXT,
    rounds INTEGER,
    roundsScheduled INTEGER,
    titles TEXT,
    rating INTEGER
)''')
conn.commit() 

for i in range(50):
    time.sleep(4)
    id = "se" + str(i)
    link = driver.find_element(By.ID, id).find_element(By.CLASS_NAME, "personLink")
    print(link)
    ##for link in links:
    ##driver.execute_script("arguments[0].scrollIntoView(true);",link)
    
    link.send_keys(Keys.ENTER)
    time.sleep(10)
    ## Click each link, scrape the boxers information, then return to the ratings page
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    ## Consolidate all data from fighter page into fighter_data
    fighter_data = soup.find_all('td')
    ## Consolidate all fight data from said fighter into fight_data, using regex
    fighter_bouts = soup.find_all(id=re.compile("^[0-9]{7}$"))

    rank_regex = re.compile("#")
    fighter_ranks = soup.find_all("a", string=rank_regex)

    boxer = Boxer()
    boxer.name = soup.h1.text.strip()
    wins = 0
    losses = 0
    draws = 0
    KOwins = 0
    KOlosses = 0
    boxer1CombinedOppWins = 0
    boxer1CombinedOppLosses = 0
    boxer1TotalRounds = 0
    boxer1TotalRoundsScheduled = 0

    ## For each fight on the fighters' resume, create fight() object and add to fight data
    fighter_bouts.reverse()
    for index, tr in enumerate(fighter_bouts):
        
        fight_data = tr.find_all('td')
        bout = Fight()
        bout.boxer1Wins = wins
        bout.boxer1Losses = losses
        bout.boxer1Draws = draws
        bout.boxer1KOwins = KOwins
        bout.boxer1KOlosses = KOlosses
        bout.boxer1CombinedOppWins = boxer1CombinedOppWins
        bout.boxer1CombinedOppLosses = boxer1CombinedOppLosses
        bout.boxer1TotalRounds = boxer1TotalRounds
        bout.boxer1TotalRoundsScheduled = boxer1TotalRoundsScheduled
        bout.fightId = tr.get('id')
        bout.date = fight_data[1].a.text.strip()
        bout.weight1 = fight_data[2].text.strip()
        bout.weight2 = fight_data[3].text.strip()
        bout.boxer1 = boxer.name
        if(fight_data[5].a):
            bout.boxer2 = fight_data[5].a.text.strip()
        bout.location = fight_data[8].text.strip().translate(normalize)
        if(fight_data[6].find('span', class_="textWon")):
            bout.boxer2Wins = int(fight_data[6].find('span', class_="textWon").text.strip())
            bout.boxer2Losses = int(fight_data[6].find('span', class_="textLost").text.strip())
            bout.boxer2Draws = int(fight_data[6].find('span', class_="textDraw").text.strip())
        else:
            bout.boxer2Wins = 0
            bout.boxer2Losses = 0 
            bout.boxer2Draws = 0
        
        if('-' in fight_data[9].text.strip()):
            result, methodOfVictory = fight_data[9].text.strip().split("-")
        else:
            result = 'TBD'
            methodOfVictory = 'TBD'
        
        if(result == "W"):
            bout.winner = bout.boxer1
            if(methodOfVictory == "RTD" or methodOfVictory == "KO" or methodOfVictory == "TKO"):
                KOwins += 1
            wins += 1
        elif(result == "L"):
            bout.winner = bout.boxer2
            if(methodOfVictory == "RTD" or methodOfVictory == "KO" or methodOfVictory == "TKO"):
                KOlosses += 1
            losses += 1
        elif(result == "D"):
            draws += 1
        bout.methodOfVictory = methodOfVictory
        
        if('/' in fight_data[10].text.strip()):
            bout.rounds, bout.roundsScheduled = fight_data[10].text.strip().split('/')
        else:
            bout.rounds = 0
            bout.roundsScheduled = fight_data[10].text.strip()
        

        bout.rating = len(list(fight_data[11].next_element.find_all("i", class_="fas")))
        if(tr.next_sibling):
            bout.titles = [title.text for title in tr.next_sibling.find_all("a", class_="titleLink")]
        fights.append(bout)
        cursor.execute('''INSERT INTO fights VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''', (bout.fightId,
            bout.boxer1,
            bout.weight1,
            int(bout.boxer1Wins),
            int(bout.boxer1Losses),
            int(bout.boxer1Draws),
            int(bout.boxer1KOwins),
            int(bout.boxer1KOlosses),
            int(boxer1CombinedOppWins),
            int(boxer1CombinedOppLosses),
            int(boxer1TotalRounds),
            int(boxer1TotalRoundsScheduled),
            bout.boxer2,
            bout.weight2,
            int(bout.boxer2Wins),
            int(bout.boxer2Losses),
            int(bout.boxer2Draws),
            bout.date,
            bout.location,
            bout.winner,
            bout.methodOfVictory,
            int(bout.rounds),
            int(bout.roundsScheduled),
            str(bout.titles),
            int(bout.rating),
            
            )) #25 values provided
        
        bout.boxer1Wins = wins
        bout.boxer1Losses = losses
        bout.boxer1Draws = draws
        bout.boxer1KOwins = KOwins
        bout.boxer1KOlosses = KOlosses
        boxer1CombinedOppWins += bout.boxer2Wins
        boxer1CombinedOppLosses += bout.boxer2Losses
        boxer1TotalRounds += int(bout.rounds)
        boxer1TotalRoundsScheduled += int(bout.roundsScheduled)
        conn.commit()
        print(bout.boxer1 + " vs " + bout.boxer2 + ": successfully added")

    ## Create boxer() object, and fill with fighter data
    field = ""
    wins = int(soup.find("td", class_="bgW").text.strip())
    boxer.wins = wins
    losses = int(soup.find("td", class_="bgL").text.strip())
    boxer.losses = losses
    draws = int(soup.find("td", class_="bgD").text.strip())
    boxer.draws = draws
    KOwins, x =  soup.find("th", class_="textWon").text.strip().split(" ")
    KOwins = int(KOwins)
    boxer.KOwins = KOwins
    KOlosses, x = soup.find("th", class_="textLost").text.strip().split(" ")
    KOlosses = int(KOlosses)
    boxer.KOlosses = KOlosses
    boxer.rank = fighter_ranks[0].text.strip()
    boxer.oppCombinedWins = boxer1CombinedOppWins
    boxer.oppCombinedLosses = boxer1CombinedOppLosses
    boxer.totalRounds = boxer1TotalRounds
    boxer.totalRoundsScheduled = boxer1TotalRoundsScheduled
    for index, td in enumerate(fighter_data):
        field = td.text.strip()
        match field:
            case 'ID#':
                boxer.boxerId = fighter_data[index+1].text.strip()
            case 'rank':
                boxer.rank = fighter_data[index+1].text.strip()
            case 'bouts':
                boxer.bouts = fighter_data[index+1].text.strip()
            case 'debut':
                boxer.debut = fighter_data[index+1].text.strip()
            case 'titles':
                boxer.titles = [title.text for title in fighter_data[index+1].find_all("a", class_="titleLink")]
            case 'sex':
                boxer.sex = fighter_data[index+1].text.strip()
            case 'alias':
                boxer.alias = fighter_data[index+1].text.strip()
            case 'age':
                boxer.age = fighter_data[index+1].text.strip()
            case 'nationality':
                boxer.nationality = fighter_data[index+1].text.strip()
            case 'height':
                boxer.height = fighter_data[index+1].text.strip()[+5:]
            case 'reach':
                boxer.reach = fighter_data[index+1].text.strip()[+5:]
            case 'residence':
                boxer.residence = fighter_data[index+1].text.strip()
            case 'stance':
                boxer.stance = fighter_data[index+1].text.strip()
            case 'division':
                boxer.weightClass = fighter_data[index+1].text.strip()
    boxers.append(boxer)

    ## Replace '' with 0 for integer values, before insertion into table
    
    ## Insert boxer data into table
    cursor.execute('''INSERT INTO boxers VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''', (boxer.boxerId,
        boxer.name,
        boxer.age,
        boxer.alias,
        boxer.nationality,
        boxer.residence,
        boxer.height,
        boxer.reach,
        boxer.stance,
        boxer.weightClass,
        boxer.sex,
        str(boxer.titles),
        boxer.rank,
        boxer.debut,
        int(boxer.wins),
        int(boxer.losses),
        int(boxer.draws),
        int(boxer.KOwins),
        int(boxer.KOlosses),
        int(boxer.totalRounds),
        int(boxer.totalRoundsScheduled),
        int(boxer.oppCombinedWins),
        int(boxer.oppCombinedLosses)
        )) 
    ## 23 values provided
    conn.commit()
    print(boxer.name + "(" + boxer.boxerId +"): successfully added")
    
    
    
    driver.back()


conn.close()
##TODO: Add boxer data to excel spreadsheet & PostgreSQL database

