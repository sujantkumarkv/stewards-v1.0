import requests
import pandas as pd
s = requests.get(
                f"https://gov.gitcoin.co/u/owocki.json",
                headers={
                "Api-key": "7cdc9c114d516ecaa8181485fa16cfddcb058221e9f93af26f04825a82db6214",
                "Api-Username": "system",
                },
            )
#print(s.json())




################## request_init_data ##################
url = 'https://api.boardroom.info/v1/voters/' + str('0x34aa3f359a9d614239015126635ce7732c18fdf3')
r = requests.request('GET', url)

print(r.json().keys())
for i in r.json().keys():
    print(i)
#voting_power.append(round((float(r.json()['data']['protocols'][0]['lastCastPower'])/100000000)*100,2))

###########################################################
url1 = 'https://api.thegraph.com/subgraphs/name/withtally/protocol-gitcoin-bravo-v2'
#print((requests.get(url1)).json())
    
