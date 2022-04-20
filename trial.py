import requests
import json
import time
import math
from datetime import datetime as dt
#from app.helpers.helpers import get_proposals
#from app.helpers.proposals import proposals

#snapshot_proposals= proposals()
githubData= requests.get("https://raw.githubusercontent.com/mmmgtc/stewards/main/assets/json/stewards_data.json").json()
karmaData= requests.get("https://api.showkarma.xyz/api/dao/delegates?name=gitcoin&pageSize=250&offset=0&workstreamId=6,4,3,7,1,2,5").json()

def checkStewardPosition(EthAddress):
    for steward in githubData["data"]:
        if steward["address"] == EthAddress and steward["workstream"]!= "":
            if (steward["workstream"].split(" ")[1]).lower() == "lead":
                return 5 #w value then is used as 5 for score calculation
            elif (steward["workstream"].split(" ")[1]).lower() == "contributor":
                return 3 #w value then is used as 5 for score calculation
            else: return 0
    return 0
        
        
def getKarmaDataStats(EthAddress, timeVal, variableName):
    #print(variableName)
    for steward in karmaData["data"]["delegates"]:
        if steward["publicAddress"].lower() == EthAddress.lower():
            for stewardStat in steward["stats"]: # [0], [1]
                if stewardStat["period"] == timeVal:
                    if(stewardStat[variableName]):
                        print(stewardStat[variableName])
                        return stewardStat[variableName] 
                    else: return 0
            return 0    
    return 0


def getHealth_30d(EthAddress, timeVal):
    W= checkStewardPosition(EthAddress=EthAddress)
    """
    time_value= 30days OR lifetime 
    
    #30days score
    score = offChainVotesPct * 0.07 + proposalsInitiated * 1.5 + proposalsDiscussed * 0.7 + 
            (forumTopicCount - proposalsInitiated) * 1.1 + (forumPostCount - proposalsDiscussed)*0.6 
            + workstreamInvolvement
    finalScore = Min(score, 10)
    """
    score_30d= getKarmaDataStats(EthAddress, timeVal, variableName="offChainVotesPct")*0.07 + \
            getKarmaDataStats(EthAddress, timeVal, variableName="proposalsInitiated")*1.5 + \
                getKarmaDataStats(EthAddress, timeVal, variableName="proposalsDiscussed")*0.7 + \
                    (getKarmaDataStats(EthAddress, timeVal, variableName="forumTopicCount") - getKarmaDataStats(EthAddress, timeVal="30d", variableName="proposalsInitiated"))*1.1 + \
                        (getKarmaDataStats(EthAddress, timeVal, variableName="forumPostCount") - getKarmaDataStats(EthAddress, timeVal="30d", variableName="proposalsDiscussed"))*0.60 + \
                            W
    health_30d= int(min(score_30d, 10)) #as we are rating out of 10
    print(health_30d)
    return health_30d

def getHealth_lifetime(EthAddress, timeVal, steward_days):
    #W= checkStewardPosition(EthAddress=EthAddress)
    """
    #lifetime score 
    score = offChainVotesPct* 0.07 + (proposalsInitiated * 1.5 + proposalsDiscussed * 1
                + (forumTopicCount - proposalsInitiated) * 1.1 
                + (forumPostCount - proposalsDiscussed)*0.7) / SQRT(Steward_days) + workstreamInvolvement
    finalScore = Min(score, 10) 
    """
    score_lifetime= getKarmaDataStats(EthAddress, timeVal, variableName="offChainVotesPct")*0.07 + \
            ((getKarmaDataStats(EthAddress, timeVal, variableName="proposalsInitiated")*1.5 + \
                getKarmaDataStats(EthAddress, timeVal, variableName="proposalsDiscussed")*1 + \
                    (getKarmaDataStats(EthAddress, timeVal, variableName="forumTopicCount") - getKarmaDataStats(EthAddress, timeVal="lifetime", variableName="proposalsInitiated"))*1.1 + \
                        (getKarmaDataStats(EthAddress, timeVal, variableName="forumPostCount") - getKarmaDataStats(EthAddress, timeVal="lifetime", variableName="proposalsDiscussed"))*0.7) / math.sqrt(steward_days)) + \
                            0
    health_lifetime= int(min(score_lifetime, 10))
    return health_lifetime

address= githubData['data'][7]['address']
score= getHealth_30d(EthAddress="0x66b1de0f14a0ce971f7f248415063d44caf19398", timeVal="30d")
#print(score)
a= null
