import os
import requests
import json
import time
from datetime import datetime as dt
#from app.helpers.helpers import get_proposals
#from app.helpers.proposals import proposals

#snapshot_proposals= proposals()
githubData= requests.get("https://raw.githubusercontent.com/mmmgtc/stewards/main/assets/json/data.json").json()
karmaData= requests.get("https://api.showkarma.xyz/api/dao/delegates?name=gitcoin&pageSize=250&offset=0&workstreamId=6,4,3,7,1,2,5").json()


def getKarmaDataStats(EthAddress, timeVal, variableName):
    for steward in karmaData["data"]["delegates"]:
        if steward["publicAddress"].lower() == EthAddress.lower():
            for stewardStat in steward["stats"]: # [0], [1]
                if stewardStat["period"] == timeVal:
                    return stewardStat[variableName] 
            return 0    
    return 0
                
                               
def checkStewardPosition(EthAddress):
    for steward in githubData:
        if steward["address"] == EthAddress and steward["workstream"]!= "":
            if (steward["workstream"].split(" ")[1]).lower() == "lead":
                return 5 #w value then is used as 5 for score calculation
            elif (steward["workstream"].split(" ")[1]).lower() == "contributor":
                return 3 #w value then is used as 5 for score calculation
            else: return 0
    return 0
        


def getHealthScore(EthAddress, timeVal):
    """
    time_value= 30days / lifetime 
    
    score = offChainVotesPct * 0.07 + proposalsInitiated * 1.5 + proposalsDiscussed * 0.7 + 
            (forumTopicCount - proposalsInitiated) * 1.1 + (forumPostCount - proposalsDiscussed)*0.6 
            + workstreamInvolvement
    finalScore = Min(score, 10)
    """
    W= checkStewardPosition(EthAddress=EthAddress)
    score= getKarmaDataStats(EthAddress, timeVal, variableName="offChainVotesPct")*0.07 + \
             getKarmaDataStats(EthAddress, timeVal, variableName="proposalsInitiated")*1.5 + \
                 getKarmaDataStats(EthAddress, timeVal, variableName="proposalsDiscussed")*0.7 + \
                    (getKarmaDataStats(EthAddress, timeVal, variableName="forumTopicCount") - getKarmaDataStats(EthAddress, timeVal, variableName="proposalsInitiated"))*1.1 + \
                        (getKarmaDataStats(EthAddress, timeVal, variableName="forumPostCount") - getKarmaDataStats(EthAddress, timeVal, variableName="proposalsDiscussed"))*0.60 + \
                            W
    health_score= int(min(score, 10)) #as we are rating out of 10
    return health_score
    
def getStewardDays(steward_since):
    t1= dt.strptime(steward_since, "%Y-%m-%d")
    t2= dt.strptime(dt.now().strftime("%Y-%m-%d"), "%Y-%m-%d")
    delta_t= t2 - t1
    return int(abs(delta_t).days)

def preprocess():
    #proposals_data = get_proposals()
    #length_proposals = len(proposals_data)

    #if length_proposals==snapshot_proposals.number:
    #    return stewards_data

    #else:      
    data= []  
    for steward in githubData:
        steward_data= {
                "name": steward["name"],
                "address": steward["address"],
                "profile_image": steward["image"],
                "workstream": steward["workstream"],
                "gitcoin_username": steward["handle_gitcoin"],
                "discourse_username": steward["handle_forum"],
                "steward_since": steward["steward_since"],
                "steward_days": getStewardDays(steward_since= steward["steward_since"]),
                "statement_post": f"https://gov.gitcoin.co/t/introducing-stewards-governance/41/{steward['statement_post_id']}",
                "forum_activity": {
                    "30d": (getKarmaDataStats(EthAddress=steward['address'], timeVal='30d', variableName="forumPostCount",) + getKarmaDataStats(EthAddress=steward['address'], timeVal='30d', variableName="forumTopicCount")),
                    "lifetime": (getKarmaDataStats(EthAddress=steward['address'], timeVal='lifetime', variableName="forumPostCount") + getKarmaDataStats(EthAddress=steward['address'], timeVal='lifetime', variableName="forumTopicCount")),
                    }, 
                "vote_participation": {
                    "30d": getKarmaDataStats(EthAddress=steward['address'], timeVal='30d', variableName="offChainVotesPct"),
                    "lifetime": getKarmaDataStats(EthAddress=steward['address'], timeVal='lifetime', variableName="offChainVotesPct"),
                    },
                "voting_weight": steward["votingweight"],
                "snapshot_votes": getKarmaDataStats(EthAddress=steward['address'], timeVal='lifetime', variableName="delegatedVotes"),
                "health": {
                    "30d": getHealthScore(EthAddress=steward['address'], timeVal='30d'), 
                    "lifetime": getHealthScore(EthAddress=steward['address'], timeVal='lifetime'), 
                    }, 
            }
        data.append(steward_data)
        stewards_data= {"data": data}
    
    #snapshot_proposals.change(length_proposals)
    # the json file where the output must be stored 
    output_file = open("static/json/stewards_data.json", "w")      
    json.dump(stewards_data, output_file, indent = 6)     
    output_file.close()
    
    return stewards_data



    