from copyreg import constructor
import json
import requests
from datetime import datetime
from time import sleep
import sqlite3

def time(out='date_time'):
    # dd/mm/YY H:M:S
    now = datetime.now()
    match out:
        case "time":
            return now.strftime("%H:%M:%S")
        case "date":
            return now.strftime("%d/%m/%Y")
        case "min":
            return int(now.strftime("%M"))
    return now.strftime("%d/%m/%Y %H:%M:%S")
#testers
def setScoreCheck(setScore="0:0",out="diff"):
    state = 1
    homeScore =""
    awayScore =""
    diff = 0
    for str in setScore:
        if str == ":":
            state = 0
            continue
        if state == 1:
            homeScore += str
        else:
            awayScore += str
    homeScore=int(homeScore)
    awayScore=int(awayScore)
    if out == "homeScore":
        return homeScore
    elif out =="awayScore":
        return awayScore
    if homeScore > awayScore:
        diff = homeScore - awayScore
        winning = "Home"
    else:
        diff = awayScore - homeScore
        if homeScore < awayScore:
            winning = "Away"
        else:
            winning = "Draw"
    if out == "win":
        return winning
    return diff

def playedTimeCheck(playedSeconds ="00:00",out="rem"):
    state = 1
    playedTimeMin =""
    playedTimeSec =""
    for str in playedSeconds:
        if str == ":":
            state = 0
            continue
        if state == 1:
            playedTimeMin += str
        else:
            playedTimeSec += str
    playedTimeMin = int(playedTimeMin)
    playedTimeSec = int(playedTimeSec)
    if out == "min":
        return playedTimeMin
    elif out == "minsec": 
        return (playedTimeMin + (playedTimeSec/60))
    elif out == "extraTimeRem":
        if playedTimeMin>90:
            return playedTimeMin - 90
        else:
            return 0
    elif out == "extraTime":
        if playedTimeMin>90:
            return True
        else:
            return False
    return 90 - playedTimeMin

def matchDatabase(instruction='',list ={},updateDb=False):
    table='matchshistory'
    conn = sqlite3.connect('livematchs.db')
    match instruction:
        case 'createTable':
            conn.execute('''CREATE TABLE '''+table+'''
                            (	
                                date TIMESTAMP  NOT NULL,
                                time TIMESTAMP NOT NULL,
  								gameId INT     NOT NULL,
                                link           TEXT    NOT NULL,
                                mod   INT NOT NULL,
                            	homeTeamName	TEXT NOT NULL,
                            	awayTeamName	TEXT NOT NULL,
                            	league	TEXT NOT NULL,
                            	country	TEXT NOT NULL,
                            	setScore         TEXT    NOT NULL,
                            	scoreDiff         INT    NOT NULL,
                                playedTime         TEXT    NOT NULL,
                            	playedTimemin         INT    NOT NULL,
                            	remTime         INT    NOT NULL,
                            	extraTime       BOOL    NOT NULL,
                            	extraTimeRem     INT    NOT NULL,
                            	winning         TEXT    NOT NULL,
                                out1X2  TEXT,
                                outOverUnder   TEXT,
                                finalOutcome   TEXT,
                                finalScore TEXT,
                                finalScoreTotal INT
                            );
                        '''
                        )
        case 'insert':
            #constructor out1X2 and outOverUnder
            try:
                list['out1X2'] ="{\"outcome_"+str(list['mod'])+"\":["+list['out1X2'].rstrip(list['out1X2'][-1])+"]}"
            except:
                list['out1X2'] ="{\"outcome_"+str(list['mod'])+"\":[]}"
            try:
                list['outOverUnder'] ="{\"outcome_"+str(list['mod'])+"\":["+list['outOverUnder'].rstrip(list['outOverUnder'][-1])+"]}"
            except:
                list['outOverUnder'] ="{\"outcome_"+str(list['mod'])+"\":[]}"
            #chech if existing
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM '+table+';')
            rows = cursor.fetchall()
            for row in rows:
                if (int(row[2]) == int(list["gameId"])):
                    list['mod'] = int(row[4])+1
                    if not(updateDb):
                        return 0
            #mod
            list['out1X2'] ="{\"mod\":"+str(list['mod'])+",\"data\":"+list['out1X2']+"}"
            list['outOverUnder'] ="{\"mod\":"+str(list['mod'])+",\"data\":"+list['outOverUnder']+"}"
            dateTimeTuple=(time('date'),time('time'))
            conn.execute("""INSERT INTO """+table+"""
                            (
                                date,
                                time,
  								gameId,
                                link,
                                mod,
                            	homeTeamName,
                            	awayTeamName,
                            	league,
                            	country,
                            	setScore,
                            	scoreDiff,
                                playedTime,
                            	playedTimemin,
                            	remTime,
                            	extraTime,
                            	extraTimeRem,
                            	winning,
                                out1X2,
                                outOverUnder,
                                finalOutcome,
                                finalScore,
                                finalScoreTotal
                            )
                            VALUES
                            (
                                ?,
                                ?,
  								"""+ str(list['gameId'])+""",
                                """+"""'"""+str(list['link'])+"""'"""+""",
                                """+str(list['mod'])+""",
                            	"""+"""'"""+str(list['homeTeamName'])+"""'"""+""",
                            	"""+"""'"""+str(list['awayTeamName'])+"""'"""+""",
                            	"""+"""'"""+str(list['league'])+"""'"""+""",
                            	"""+"""'"""+str(list['country'])+"""'"""+""",
                            	"""+"""'"""+str(list['setScore'])+"""'"""+""",
                            	"""+"""'"""+str(list['scoreDiff'])+"""'"""+""",
                                """+"""'"""+str(list['playedTime'])+"""'"""+""",
                            	"""+str(list['playedTimemin'])+""",
                            	"""+str(list['remTime'])+""",
                            	"""+str(list['extraTime'])+""",
                            	"""+str(list['extraTimeRem'])+""",
                            	"""+"""'"""+str(list['winning'])+"""'"""+""",
                                """+"""'"""+str(list['out1X2'])+"""'"""+""",
                                """+"""'"""+str(list['outOverUnder'])+"""'"""+""",
                                """+"""'"""+str(list['finalOutcome'])+"""'"""+""",
                                """+"""'"""+str(list['finalScore'])+"""'"""+""",
                                """+str(list['finalScoreTotal'])+"""
                            )
                            ;
                        """
                ,dateTimeTuple)
               


            
    conn.commit()
    conn.close()      
def matchJsonToDatabase(updateDb=False):
    # api
    URL = "https://www.sportybet.com/api/ke/factsCenter/liveOrPrematchEvents?sportId=sr%3Asport%3A1"
    try:
        response = requests.get(url = URL)
    except:
        print('No internet')
        return 0
    #raw extraction json
    data = json.loads((response.text))
    for data in data["data"]:
        toDb ={
              	"gameId":0,
                "link":"",
                "mod":1,
                "homeTeamName":"",
                "awayTeamName":"",
                "league":(data["name"]),
                "country":(data["categoryName"]),
                "setScore":"",
                "scoreDiff":0,
                "playedTime":"",
                "playedTimemin":0,
                "remTime":0,
                "extraTime":bool,
                "extraTimeRem":0,
                "winning":"",
                "out1X2":"",
                "outOverUnder":"",
                "finalOutcome":"notSet",
                "finalScore":"0",
                "finalScoreTotal":0
        }
        for event in data["events"]:
            try:            
                toDb["gameId"]=(event["gameId"])
            except:
                continue
            toDb["link"]="https://www.sportybet.com/ke/sport/football/live/"+(data["categoryId"])+"/"+(data["id"])+"/"+(event["eventId"])
            toDb["homeTeamName"]=(event["homeTeamName"])
            toDb["awayTeamName"]=(event["awayTeamName"])
            toDb["setScore"]=(event["setScore"])
            toDb["scoreDiff"]=int(setScoreCheck(event["setScore"],out=""))
            toDb["playedTime"]=(event["playedSeconds"])
            toDb["playedTimemin"]=int(playedTimeCheck(event["playedSeconds"],out="min"))
            toDb["remTime"]=int(playedTimeCheck(event["playedSeconds"],out="rem"))
            toDb["extraTime"]=bool(playedTimeCheck(event["playedSeconds"],out="extraTime"))
            toDb["extraTimeRem"]=int(playedTimeCheck(event["playedSeconds"],out="extraTimeRem"))
            toDb["winning"]=(setScoreCheck(event["setScore"],out="win"))
            webholderEventID=""
            for str in (event["eventId"]):
                if str == ":":
                   webholderEventID +="%3A"
                   continue
                else:
                    webholderEventID += str
                # api
            URL_mk = "https://www.sportybet.com/api/ke/factsCenter/event?eventId="+(webholderEventID)
            try:
                response_mk = requests.get(url = URL_mk)
            except:
                print('No internet')
                return             
            #raw extraction json
            data_mk = json.loads(response_mk.text)
            for markets in data_mk["data"]["markets"]:
                placeHolder_mk =""
                if markets["desc"] == "1X2":
                    for outcomes in markets["outcomes"]:
                        st = json.dumps(outcomes)
                        placeHolder_mk =placeHolder_mk + st +","
                    toDb["out1X2"] = placeHolder_mk
                    placeHolder_mk =""
                if markets["desc"] == "Over/Under":
                    for outcomes in markets["outcomes"]:
                        st = json.dumps(outcomes)
                        placeHolder_mk =placeHolder_mk + st +","
                toDb["outOverUnder"] = toDb["outOverUnder"] + placeHolder_mk 
            matchDatabase('insert',toDb,updateDb=updateDb)
def main():
    timestart = time()
    timeMinWatch = int(time("min"))
    updateDb=False
    updateInterval = 15
    try:
        matchDatabase('createTable')
    except:
        pass
    while True:
        print("Running FROM: "+timestart+" NOW: "+time())
        matchJsonToDatabase(updateDb)
        #manage time and updateDb
        if time("min")<timeMinWatch:
            timeMinWatch = time("min")
        if time("min")>timeMinWatch:
            if (int(time("min"))-int(timeMinWatch))>updateInterval:
                timeMinWatch = time("min")
                updateDb = True                
            else:
                updateDb = False
                
        print("diff:"+str(int(time("min"))-int(timeMinWatch)))
        print(updateDb)


if __name__ == "__main__":
    main()