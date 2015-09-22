from math import radians, sin, cos, atan, atan2, sqrt
from simplemapplot import make_us_state_map
from time import sleep

#######################
# Name:readStateCenterFile(stateCenterDict)
# Input:
# Output:
# Purpose: reads in the file of state centers as described in the handout
#
def readStateCenterFile(stateCenterDict):
    stateFile = open("stateCenters.txt")
    for line in stateFile:
        value = line.split(',')
        stateCenterDict[value[0]] = (float(value[1]), float(value[2]))    
    stateFile.close()
########################


########################
# Name:readTweetFile(tweetList)
# Input:
# Output:
# Purpose: reads the tweets from the file into a list.  The file is specified in
# the "open" command.  Change the "open" call when you want the big file. 
#
def readTweetFile(tweetList):
    tweetFile = open("allTweets.txt", encoding="utf-8")
    for line in tweetFile:
        try:
            value = line.split("\t")
            lat,long = value[0].split(",")
            lat = float(lat[1:])
            long = float(long[:-1])
            tweetList.append(((lat,long),str(value[3])))
        except:
            None
    tweetFile.close()
#########################

###########################
# Name:distance (lat1, lon1, lat2, lon2)
# Input:
# Output:
# Purpose:takes a latitude and longitude for two given points and returns
# the great circle distance between them in miles
#
def distance (lat1, lon1, lat2, lon2):
    earth_radius = 3963.2  # miles
    lat1 = radians(float(lat1))
    lat2 = radians(float(lat2))
    lon1 = radians(float(lon1))
    lon2 = radians(float(lon2))
    dlat, dlon = lat2-lat1, lon2-lon1
    a = sin(dlat/2) ** 2  + sin(dlon/2) ** 2 * cos(lat1) * cos(lat2)
    c = 2 * atan2(sqrt(a), sqrt(1-a));
    return earth_radius * c;
#
############################

############
# Function to assign frequency colors to map

def assignStateColor(stateCountDict, stateColor):
    dictMin = min(stateCountDict.values())
    dictMax = max(stateCountDict.values())
    lightest = dictMax*.1
    lighter = dictMax*.3
    light = dictMax*.5
    dark = dictMax*.7
    darker = dictMax*.8
    darkest = dictMax
    for i in stateCountDict:
        if stateCountDict[i] == 0:
            stateColor[i] = 0
        elif 0 <= stateCountDict[i] <= lightest:
            stateColor[i] = 1
        elif lightest <= stateCountDict[i] <= lighter:
            stateColor[i] = 2
        elif lighter <= stateCountDict[i] <= light:
            stateColor[i] = 3
        elif light <= stateCountDict[i] <= dark:
            stateColor[i] = 4
        elif dark <= stateCountDict[i]<= darker:
            stateColor[i] = 5
        elif darker <= stateCountDict[i]<= darkest:
            stateColor[i] = 6

    return(stateColor)
############


############################
#MAIN
############################
def main():
    stateCenterDict = {}        #Key: state abbrev  Value: 2-tuple of (lat,long) of state center
    tweetList = []              #list of two items, first is 2-tuple (lat,long), second is tweet

    stateCountDict = {}         #Key: state abbrev  Value: count for word
    stateColor = {}             #Key, state abbrev Value: frequency count

    readStateCenterFile(stateCenterDict)
    readTweetFile(tweetList)

    for key in stateCenterDict:
        stateCountDict[key] = 0
        stateColor[key] = 0

    wordOfInterest = input("what word are you looking for? ")
    wordOfInterest = wordOfInterest.lower()

    
    # find location of tweet and assign word count
    for item in tweetList:
        state= None
        minDist = 400
        pos = item[0]
        tweet = item[1]
        lat = pos[0]
        long = pos[1]
        if lat > 55:
            state = 'AK'
        elif lat < 26:
            state = 'HI'
        else:
            for s in stateCenterDict.keys():
                sLat = stateCenterDict[s][0]
                sLong = stateCenterDict[s][1]
                d = distance(sLat, sLong, lat, long)
                if d < minDist:
                    state = s
                    minDist = d
        # assign value and sentiment score to each state
        if wordOfInterest in tweet.lower():
            if state in stateCenterDict.keys():
                stateCountDict[state]+=1

            
    assignStateColor(stateCountDict, stateColor)
       

    
                        
    print(stateCountDict)
    print(stateColor)
    
    
    COLORS = ["#FFFFFF", "#EBAD99", "#E08566", "#D65C33", "#CC3300", "#A32900", "#7A1F00"]

    make_us_state_map(stateColor, COLORS)

#
#############################   
main()
    
