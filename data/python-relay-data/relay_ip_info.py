#Importing packages
#
# You can delete whatever package(s) you want..
#
import json
import time
import requests
import math as m
import pandas as pd
import numpy as np
import datetime as dt

# Leave This code here and lookup at pandas documentation 
# if you need to know about chained assignments
pd.options.mode.chained_assignment = None  # default='warn'

# Because most of my data sets I have made can have up to 30+ columns and 20+ rows
# code below will increase pandas defaults for max rows 
# and columns that you can display in a Juptyer Notebook
pd.options.display.max_columns = 60
pd.options.display.max_rows = 1000


# Get access token from file
with open('access_key.txt', 'r') as file:
    access_key = file.read().replace('\n', '')
access_key = access_key.split('=')[1]

# # Get the data from the API
url = 'http://api.ipstack.com/100.7.78.240?&fields=country_code,country_name,city,latitude,longitude'
payload = {'access_key': '{key}'.format(key=access_key)}
reqs = requests.get(url, params=payload).json()
print(reqs)


df = pd.read_json('blockfrost_stakepools_info_latest.json')

df[['ipv4', 'ipv6', 'dns', 'dns_srv', 'port']] = df[['ipv4', 'ipv6', 'dns', 'dns_srv', 'port']].fillna(value='')


def get_ip_host(df, outputfileName):
	
	ip_host_lst = []
	columns_list = list(df.columns)

	if type(df) != pd.DataFrame:
		raise TypeError('df must be a pandas dataframe')
	if type(outputfileName) != str:
		raise TypeError('outputfileName must be a string')


	for i in range(len(df)):
		# Raise type error if the data is not a string
		if type(df['dns'][i]) != str:
			print(df['dns'][i])
			raise TypeError('dns must be a string')

		if type(df['dns_srv'][i]) != str:
			print(df['dns_srv'][i])
			raise TypeError('dns_srv must be a string')

		if type(df['ipv4'][i]) != str:
			print(df['ipv4'][i])
			raise TypeError('ipv4 must be a string')

		if type(df['ipv6'][i]) != str:	
			print(df['ipv6'][i])
			raise TypeError('ipv6 must be a string')

		# This code maps the ip host to its pool_id as a tuple
    
		if len(df['dns'][i]) > 0 or len(df['dns'][i]) > 4:
			ip_host_lst.append(tuple((df['pool_id'][i], df['hex'][i], df['vrf_key'][i], df['blocks_minted'][i], 
                             df['live_stake'][i], df['live_size'][i], df['live_saturation'][i], df['live_delegators'][i], 
                             df['active_stake'][i], df['active_size'][i], df['declared_pledge'][i], df['live_pledge'][i], 
                             df['margin_cost'][i], df['fixed_cost'][i], df['reward_account'][i], df['owners'][i], df['registration'][i], 
                             df['retirement'][i], df['dns'][i], df['port'][i], df['url'][i], df['hash'][i], df['ticker'][i], df['name'][i],
                             df['description'][i], df['homepage'][i])))

		if len(df['dns_srv'][i]) > 0 or len(df['dns_srv'][i]) > 4:
			ip_host_lst.append(tuple((df['pool_id'][i], df['hex'][i], df['vrf_key'][i], df['blocks_minted'][i], df['live_stake'][i], 
                             df['live_size'][i], df['live_saturation'][i], df['live_delegators'][i], df['active_stake'][i], df['active_size'][i],
                             df['declared_pledge'][i], df['live_pledge'][i], df['margin_cost'][i], df['fixed_cost'][i], df['reward_account'][i],
                             df['owners'][i], df['registration'][i], df['retirement'][i], df['dns_srv'][i], df['port'][i], df['url'][i], 
                             df['hash'][i], df['ticker'][i], df['name'][i], df['description'][i], df['homepage'][i])))
		# 	ip_host_lst.append(tuple((df['dns_srv'][i], df['port'][i], df['pool_id'][i],
		# 	df['live_stake'][i], df['delegators'][i], df['description'][i],
		# 	df['hash'][i], df['hex'][i], df['homepage'][i], df['name'][i],
		# 	df['ticker'][i], df['url'][i])))

		if len(df['ipv4'][i]) > 0 or len(df['ipv4'][i]) > 4:
			ip_host_lst.append(tuple((df['pool_id'][i], df['hex'][i], df['vrf_key'][i], df['blocks_minted'][i], df['live_stake'][i], 
                             df['live_size'][i], df['live_saturation'][i], df['live_delegators'][i], df['active_stake'][i], df['active_size'][i], 
                             df['declared_pledge'][i], df['live_pledge'][i], df['margin_cost'][i], df['fixed_cost'][i], df['reward_account'][i], 
                             df['owners'][i], df['registration'][i], df['retirement'][i], df['ipv4'][i], df['port'][i],
                             df['url'][i], df['hash'][i], df['ticker'][i], df['name'][i],
                             df['description'][i], df['homepage'][i])))

		# 	ip_host_lst.append(tuple((df['ipv4'][i], df['port'][i], df['pool_id'][i],
		# 	df['live_stake'][i], df['delegators'][i], df['description'][i],
		# 	df['hash'][i], df['hex'][i], df['homepage'][i], df['name'][i],
		# 	df['ticker'][i], df['url'][i])))

		if len(df['ipv6'][i]) > 0 or len(df['ipv6'][i]) > 4:
          		ip_host_lst.append(tuple((df['pool_id'][i], df['hex'][i], df['vrf_key'][i], df['blocks_minted'][i], df['live_stake'][i], 
                                df['live_size'][i], df['live_saturation'][i], df['live_delegators'][i], df['active_stake'][i], 
                                df['active_size'][i], df['declared_pledge'][i], df['live_pledge'][i], df['margin_cost'][i], 
                                df['fixed_cost'][i], df['reward_account'][i], df['owners'][i], df['registration'][i], 
                                df['retirement'][i], df['ipv6'][i], df['port'][i],
                                df['url'][i], df['hash'][i], df['ticker'][i], df['name'][i],
                             	df['description'][i], df['homepage'][i])))

		# 	ip_host_lst.append(tuple((df['ipv6'][i], df['port'][i], df['pool_id'][i],
		# 	df['live_stake'][i], df['delegators'][i], df['description'][i],
		# 	df['hash'][i], df['hex'][i], df['homepage'][i], df['name'][i],
		# 	df['ticker'][i], df['url'][i])))
	
	if len(ip_host_lst) == 0:
		print('No IPs found')

	if len(ip_host_lst) != len(df):
		print('Number of rows in host lst: '+str(len(ip_host_lst)), 'Number of Rows in original df: '+str(len(df)), sep='\n')
	
	ip_host_df = pd.DataFrame(pd.Series(ip_host_lst))
	ip_host_df.columns = ['ip_host']

	
	return ip_host_df.to_csv(r''+outputfileName+'.csv', index=False)


get_ip_host(df, 'all_relays_resolved_latest')

testing = pd.read_csv('all_relays_resolved_latest.csv')

# Need to convert the all_relays.csv data to a tuple object from the string
# we will use literal_eval to convert the string to a tuple

import ast

testing['ip_host_tuple'] = testing['ip_host'].apply(ast.literal_eval)
testing


# Let's make a function to resolve hostnames to IP addresses
import dns.resolver
def resolve_hostname(hostname):
	try:
		ip = dns.resolver.resolve(hostname, 'A')
		return ip[0].to_text()
	except:
		return ''


new_df = pd.DataFrame()
new_df['pool_id'], new_df['hex'], new_df['vrf_key'], new_df['blocks_minted'], new_df['live_stake'], new_df['live_size'], new_df['live_saturation'], new_df['live_delegators'], new_df['active_stake'], new_df['active_size'], new_df['declared_pledge'], new_df['live_pledge'], new_df['margin_cost'], new_df['fixed_cost'], new_df['reward_account'], new_df['owners'], new_df['registration'], new_df['retirement'],new_df['ip_host'], new_df['port'], new_df['url'], new_df['hash'], new_df['ticker'], new_df['name'], new_df['description'], new_df['homepage'] = testing.ip_host_tuple.str

new_df['resolved_ip'] = new_df['ip_host'].apply(resolve_hostname)


# sprinkle some magic to get the resolved IPs and the IPs in ip_host into a single column
for i in range(len(new_df)):
	if len(new_df['resolved_ip'][i]) == 0:
		new_df['resolved_ip'][i] = new_df['ip_host'][i]

new_df.to_csv('relays_latest_resolved_hosts.csv', index=False)
new_df.to_json('relays_latest_resolved_hosts.json', orient='records')


hosts = pd.read_csv('relays_latest_resolved_hosts.csv')


def get_ip_data(df, outputfileName):
	new_df = pd.DataFrame()
	
	for i in range(len(df)):
		url = 'http://api.ipstack.com/'+df['resolved_ip'][i]+'?&fields=country_code,country_name,city,connection,region_code,region_name,zip,latitude,longitude'
		reqs = requests.get(url, params=payload).json()
		new_df = new_df.append(reqs, ignore_index=True)
		time.sleep(1)
	result = df.merge(new_df, left_index=True, right_index=True)
	current_date = dt.datetime.now().strftime("_%m_%d_%Y")
	
	return result.to_json(r''+outputfileName+current_date+'.json', orient='records'), result.to_csv(r''+outputfileName+'.csv', index=False)


get_ip_data(hosts, 'cardano_relay_data')


# df_all_relays_location = pd.read_json('all_relays_data.json')
df_test_locations = pd.read_json('cardano_relay_data'+dt.datetime.now().strftime("_%m_%d_%Y")+'.json')




