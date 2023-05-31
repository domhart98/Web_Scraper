import sqlite3

conn = sqlite3.connect('fight_prophet.db')
cursor = conn.cursor()

## Function to delete the duplicate records of each fight.
def deleteDuplicateFights():
    cursor.execute('''DELETE FROM fights 
        WHERE EXISTS (
            SELECT 1 FROM fights f2
            WHERE fights.fightId = f2.fightId 
            )'''
        )
    
def addBoxerColumns():
    return

def addFightColumns():
    cursor.execute('''ALTER TABLE fights
    ADD COLUMN boxer2KOwins
    ''')

    cursor.execute('''ALTER TABLE fights
    ADD COLUMN boxer2KOlosses
    ''')

    cursor.execute('''ALTER TABLE fights
    ADD COLUMN boxer2OppCombinedWins
    ''')

    cursor.execute('''ALTER TABLE fights
    ADD COLUMN boxer2OppCombinedLosses
    ''')

    cursor.execute('''ALTER TABLE fights
    ADD COLUMN boxer2TotalRounds
    ''')

    cursor.execute('''ALTER TABLE fights
    ADD COLUMN boxer2TotalRoundsScheduled
    ''')


## Function to insert relevant data into newly added fields in the boxers table.
def updateBoxers():
    return

## Function to insert relevant data into newly added fields in the fights table.
def updateFights():
    cursor.execute('''UPDATE fights AS f0
    SET boxer2KOwins = f2.boxer1KOwins, boxer2KOlosses = f2.boxer1KOlosses, boxer2OppCombinedWins = f2.boxer1OppCombinedWins, boxer2OppCombinedLosses = f2.boxer1OppCombinedLosses, boxer2totalRounds = f2.boxer1TotalRounds, boxer2TotalRoundsScheduled = f2.boxer1TotalRoundsScheduled
    FROM (SELECT f.fightId, f.boxer1KOwins, f.boxer1KOlosses, f.boxer1OppCombinedWins, f.boxer1OppCombinedLosses, f.boxer1TotalRounds, f.boxer1TotalRoundsScheduled
    FROM fights f1 INNER JOIN fights f 
    ON f1.fightId = f.fightId
    WHERE f1.boxer1 = f.boxer2
    GROUP BY f.fightId) AS f2
    WHERE f0.fightId = f2.fightId
    ''')

    

##addFightColumns()
updateFights()


cursor.execute('''SELECT * from fights
                WHERE fightId = "2701260" OR fightId="2863721" OR fightId="2289759"
                GROUP BY fightId
            ''')
query_result = cursor.fetchall()
print(len(query_result))
print(query_result)

names = list(map(lambda x: x[0], cursor.description))
print(names)



## Uncomment to finalize changes to db
##conn.commit()