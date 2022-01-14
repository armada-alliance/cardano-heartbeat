#Importing packages
#
# You can delete whatever package(s) you want..
#
import os
import json
import time
import requests
import math as m
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np



# Leave This code here and lookup at pandas documentation 
# if you need to know about chained assignments
pd.options.mode.chained_assignment = None  # default='warn'



# Get our block frost api key from the file
with open('keys.txt', 'r') as file:
    api_key = file.read().replace('\n', '')
api_key = api_key.split('=')[1]

from blockfrost import BlockFrostApi, ApiError, ApiUrls

api = BlockFrostApi(
	project_id=api_key,
	base_url=ApiUrls.mainnet.value,
)


try:
    health = api.health()
    print(health)   # prints object:    HealthResponse(is_healthy=True)
    health = api.health(return_type='json') # Can be useful if python wrapper is behind api version
    print(health)   # prints json:      {"is_healthy":True}
    health = api.health(return_type='pandas')
    print(health)   # prints Dataframe:         is_healthy
                    #                       0         True

    
    account_rewards = api.account_rewards(
        stake_address='stake1ux3g2c9dx2nhhehyrezyxpkstartcqmu9hk63qgfkccw5rqttygt7',
        count=5,
        return_type='pandas'
    )
    print(account_rewards)  # prints 221
    print(len(account_rewards))  # prints 20

    account_rewards = api.account_rewards(
        stake_address='stake1ux3g2c9dx2nhhehyrezyxpkstartcqmu9hk63qgfkccw5rqttygt7',
        count=5,
        gather_pages=True, # will collect all pages
    )
    print(account_rewards[0].epoch)  # prints 221
    print(len(account_rewards))  # prints 57

    address = api.address(
        address='addr1qxqs59lphg8g6qndelq8xwqn60ag3aeyfcp33c2kdp46a09re5df3pzwwmyq946axfcejy5n4x0y99wqpgtp2gd0k09qsgy6pz')
    print(address.type)  # prints 'shelley'
    for amount in address.amount:
        print(amount.unit)  # prints 'lovelace'

except ApiError as e:
    print(e)


df = pd.DataFrame()

for i in range(1,100):
        try:
                pool_ids = api.pools(
                        gather_pages=True,
                        count=100,
                        page=i,)
                if len(pool_ids)==0:
                        break
                pools_list = pd.DataFrame(pool_ids)
                df = df.append(pools_list)
        except ApiError as e:
                print(e)

def get_pool_relay_data(dataframe):
        
        df = pd.DataFrame()
        df2 = pd.DataFrame()
        df3 = pd.DataFrame()
        
        for i in range(0,len(dataframe)):
                try:
                        pool_info = api.pool(pool_id=dataframe.iloc[i,0], return_type='pandas')
                        relays_info = api.pool_relays(pool_id=dataframe.iloc[i,0], return_type='json')
                        meta_info = api.pool_metadata(pool_id=dataframe.iloc[i,0], return_type='json')
                        if len(relays_info) > 0:
                                t = 0
                                while t < len(relays_info):
                                        df = df.append(pool_info, ignore_index=True)
                                        df2 = df2.append(pd.Series(relays_info[t]), ignore_index=True)
                                        df3 = df3.append(pd.Series(meta_info), ignore_index=True)
                                        t += 1
                                        time.sleep(0.45)
                except ApiError as e:
                        if e.status_code == 402 or e.status_code == 429:
                                break
                        print(e)
        result = pd.concat([df, df2], axis=1)
        return result.to_json('blockfrost_pool_relay_info_latest',orient='records'),df3.to_json('blockfrost_pool_metadata_latest',orient='records')

get_pool_relay_data(df)

alldata = pd.read_json('blockfrost_pool_relay_info_latest')

df1 = pd.read_json('blockfrost_pool_metadata_latest', orient='records')

new_df = pd.concat([alldata, df1], axis=1)

new_df = new_df.loc[:,~new_df.columns.duplicated()]

new_df.to_json(r'blockfrost_stakepools_info_latest.json', orient='records')