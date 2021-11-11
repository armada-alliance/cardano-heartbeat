# -*- coding: utf-8 -*-

# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

import dash
from dash import dcc
from dash import html
import plotly.express as px
import pandas as pd
import json
import time
import requests
import math as m
import matplotlib.pyplot as plt
import numpy as np
import descartes
import geopandas as gpd



#import relay data
data = pd.read_json('relay_data_clean.json')

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

colors = {
    'background': '#111111',
    'background2': '#696969',
    'text': '#7FDBFF'
}

# create a df with num relays per ISP and graph it
df_ada_staked_per_pool = data.copy()
data.fillna('', inplace=True)
df_ada_staked_per_pool = df_ada_staked_per_pool.drop_duplicates(subset=['pool_id'], keep='first')
pools_per_isp = df_ada_staked_per_pool.groupby('isp').pool_id.nunique().to_frame()
pools_per_isp.rename(columns={'pool_id': 'Number of Pools'}, inplace=True)
ada_per_isp = (df_ada_staked_per_pool.groupby('isp').live_stake.sum()/1000000).to_frame()
ada_per_isp = ada_per_isp.merge(pools_per_isp, left_index=True, right_index=True)
ada_per_isp_100mil = ada_per_isp[ada_per_isp['live_stake'] > 100000000]
ada_per_isp_100mil.sort_values(by='live_stake', ascending=False, inplace=True)
ada_per_isp_100mil =  ada_per_isp_100mil.reset_index().replace({'isp': {'amazon.com Inc.':'amazon.com, Inc'}}).groupby('isp', sort=False).sum()
ada_per_isp_100mil.rename(index={'': 'Unknown'}, inplace=True)

#Top 100 isps by number of relays
num_relays_per_isp = data.groupby(['isp']).size().to_frame()
num_relays_per_isp.rename(columns={0:'Number of Relays'}, inplace=True)
num_relays_per_isp.sort_values(by='Number of Relays', ascending=False, inplace=True)
top_100_isp = num_relays_per_isp.head(100)
top_100_isp =  top_100_isp.reset_index().replace({'isp': {'amazon.com Inc.':'amazon.com, Inc'}}).groupby('isp', sort=False).sum()
top_100_isp.sort_values(by='Number of Relays', ascending=False, inplace=True)


# plot the data             

fig1 = px.scatter(ada_per_isp_100mil,
		x=ada_per_isp_100mil.index,
		y=ada_per_isp_100mil.live_stake.values,
		color=ada_per_isp_100mil.index,
		width=1400,
		height=800,
		size=ada_per_isp_100mil['Number of Pools'],
		labels={'isp':'','y': 'ADA Staked'},
		title='ADA Staked per ISP',
		opacity=0.98,)

fig2 = px.bar(top_100_isp, x=top_100_isp.index, y=top_100_isp['Number of Relays'], color=top_100_isp.index, width=1400, height=800,title='Top 100 ISPs by Number of Relays', opacity=0.98)

fig3 = px.scatter_geo(data,
		     lat = 'latitude',
                     lon = 'longitude',
                #      locationmode='country names',
                #      locations="city",
                     color="pool_id", # which column to use to set the color of markers
                     hover_name="ticker", # column added to hover information
                     hover_data = [ 'country_name', 'city', 'live_stake', 'delegators', 'homepage'],
                #      size="delegators", # size of markers
                     projection="natural earth",
		     width=1400,
		     height=800)


fig1.update_yaxes(automargin=True)
fig1.update_xaxes(tickangle=90)
fig1.update_layout(plot_bgcolor=colors['background'], paper_bgcolor=colors['background'], font={'color': colors['text']})

fig2.update_yaxes(automargin=True)
fig2.update_xaxes(automargin=True)
fig2.update_layout(plot_bgcolor=colors['background'], paper_bgcolor=colors['background'], font={'color': colors['text']})

fig3.update_yaxes(automargin=True)
fig3.update_xaxes(automargin=True)
fig3.update_layout(plot_bgcolor=colors['background'], paper_bgcolor=colors['background'], font={'color': colors['text']})


app.layout = html.Div(children=[
	
	html.Div([
		# html.Div([
		# 	html.H1(children='Relay Data Dashboard', style={'color': colors['text']}),
		# 	html.P(children='This dashboard shows the number of relays staked by each ISP, the total ADA staked by each ISP, and the top 100 ISPs.', style={'color': colors['text']}),
		# 	html.P(children='The data is updated every 5 seconds.', style={'color': colors['text']}),
		# ], className='twelve columns', style={'background-color': colors['background']}),
		html.Div([
			# html.H2(children='ISPs with over 100 million ADA staked', style={'color': colors['text']}),
			dcc.Graph(id='ada-per-isp', figure=fig3)
		], className='twelve columns', style={'background-color': colors['background']}),
		html.Div([
			# html.H2(children='', style={'color': colors['text']}),
			dcc.Graph(id='top-100-isp', figure=fig2)
		], className='twelve columns', style={'background-color': colors['background']}),
		html.Div([
			dcc.Graph(id='map', figure=fig2)
		], className='twelve columns', style={'background-color': colors['background']}),
	], className='row'),
])


if __name__ == '__main__':
    app.run_server(debug=True)

