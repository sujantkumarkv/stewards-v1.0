import os
import requests
import json
import time
import numpy as np
#from app.helpers.helpers import get_proposals
#from app.helpers.proposals import proposals

#snapshot_proposals= proposals()
githubData= requests.get("https://raw.githubusercontent.com/mmmgtc/stewards/main/assets/json/data.json").json()
karmaData= requests.get("https://api.karmaprotocol.io/api/dao/delegates?name=gitcoin&pageSize=10000&offset=0").json()


def getKarmaDataStats(EthAddress, timeVal, variableName):
    for steward in karmaData["data"]["delegates"]:
        if steward["publicAddress"].lower() == EthAddress.lower():
            for stewardStat in steward["stats"]: # [0], [1]
                if stewardStat["period"] == timeVal:
                    return stewardStat[variableName]
                else: return 0
        else: continue
                
                               
def checkStewardPosition(EthAddress):
    for steward in githubData:
        if steward["address"] == EthAddress and steward["workstream"]!= "":
            if (steward["workstream"].split(" ")[1]).lower() == "lead":
                return 5 #w value then is used as 5 for score calculation
            elif (steward["workstream"].split(" ")[1]).lower() == "contributor":
                return 3 #w value then is used as 5 for score calculation
    return 0
        


def getHealthScore(EthAddress, timeVal):
    """
    score = offChainVotesPct * 0.7 + proposalsInitiated * 1.5 + proposalsDiscussed * 0.7 + 
            (forumTopicCount - proposalsInitiated) * 1.1 + (forumPostCount - proposalsDiscussed)*0.6 
            + workstreamInvolvement
    finalScore = Min(score, 10)
    """
    W= checkStewardPosition(EthAddress=EthAddress)
    score= getKarmaDataStats(EthAddress, timeVal, variableName="offChainVotesPct")*0.7 \
            + getKarmaDataStats(EthAddress, timeVal, variableName="proposalsInitiated")*1.5 \
                + getKarmaDataStats(EthAddress, timeVal, variableName="proposalsDiscussed")*0.7 + (getKarmaDataStats(EthAddress, timeVal, variableName="forumTopicCount") - getKarmaDataStats(EthAddress, timeVal, variableName="proposalsInitiated"))*1.1 + (getKarmaDataStats(EthAddress, timeVal, variableName="forumPostCount") - getKarmaDataStats(EthAddress, timeVal, variableName="proposalsDiscussed"))*0.60 + W
    health_score= int(min(score, 10)) #as we are rating out of 10
    return health_score
    
    
def preprocess():
    #proposals_data = get_proposals()
    #length_proposals = len(proposals_data)

    #if length_proposals==snapshot_proposals.number:
    #    return stewards_data

    #else:      
    stewards_data= []  
    for steward in githubData:
        steward_data= {
                "name": steward["name"],
                "address": steward["address"],
                "profile_image": steward["image"],
                "workstream": steward["workstream"],
                "gitcoin_username": steward["handle_gitcoin"],
                "discourse_username": steward["handle_forum"],
                "steward_since": steward["steward_since"],
                "statement_post": f"https://gov.gitcoin.co/t/introducing-stewards-governance/41/{steward['statement_post_id']}",
                "forum_activity_30d": (getKarmaDataStats(EthAddress=steward['address'], timeVal='30d', variableName="forumPostCount") + getKarmaDataStats(EthAddress=steward['address'], timeVal='30d', variableName="forumTopicCount")),
                "forum_activity_lifetime": (getKarmaDataStats(EthAddress=steward['address'], timeVal='lifetime', variableName="forumPostCount") + getKarmaDataStats(EthAddress=steward['address'], timeVal='lifetime', variableName="forumTopicCount")),
                "vote_participation_30d": getKarmaDataStats(EthAddress=steward['address'], timeVal='30d', variableName="offChainVotesPct"),
                "vote_participation_lifetime": getKarmaDataStats(EthAddress=steward['address'], timeVal='lifetime', variableName="offChainVotesPct"),
                "voting_weight": steward["votingweight"],
                "snapshot_votes": getKarmaDataStats(EthAddress=steward['address'], timeVal='lifetime', variableName="delegatedVotes"),
                "health_score_30d": getHealthScore(EthAddress=steward['address'], timeVal='30d'),
                "health_score_lifetime": getHealthScore(EthAddress=steward['address'], timeVal='lifetime'),
            }
        stewards_data.append(steward_data)
    
    #snapshot_proposals.change(length_proposals)
    # the json file where the output must be stored 
    output_file = open("app/static/json/stewards_data.json", "w")      
    json.dump(stewards_data, output_file, indent = 6)     
    output_file.close()
    
    return stewards_data



    