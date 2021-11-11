# Run this app with python app.py and
# visit http://127.0.0.1:8050/ in your web browser.

import dash
from dash import dcc
from dash import html
import plotly.express as px
import pandas as pd
import dash_bootstrap_components as dbc

app = dash.Dash(external_stylesheets=[dbc.themes.CYBORG])


# import relay data
data = pd.read_json('relay_data_clean.json')


colors = {
    'background': '#111111',
    'background2': '#696969',
    'text': '#7FDBFF'
}

# create a df with num relays per ISP and graph it
df_ada_staked_per_pool = data.copy()
data.fillna('', inplace=True)
df_ada_staked_per_pool = df_ada_staked_per_pool.drop_duplicates(
    subset=['pool_id'], keep='first')
pools_per_isp = df_ada_staked_per_pool.groupby(
    'isp').pool_id.nunique().to_frame()
pools_per_isp.rename(columns={'pool_id': 'Number of Pools'}, inplace=True)
ada_per_isp = (df_ada_staked_per_pool.groupby(
    'isp').live_stake.sum()/1000000).to_frame()
ada_per_isp = ada_per_isp.merge(
    pools_per_isp, left_index=True, right_index=True)
###############################################################################
# the line below needs to be modified to fix the setting with copy warning
ada_per_isp_100mil = ada_per_isp[ada_per_isp['live_stake'] > 100000000]
ada_per_isp_100mil.sort_values(by='live_stake', ascending=False, inplace=True)
###############################################################################
ada_per_isp_100mil = ada_per_isp_100mil.reset_index().replace(
    {'isp': {'amazon.com Inc.': 'amazon.com, Inc'}}).groupby('isp', sort=False).sum()
ada_per_isp_100mil.rename(index={'': 'Unknown'}, inplace=True)

# Top 100 isps by number of relays
num_relays_per_isp = data.groupby(['isp']).size().to_frame()
num_relays_per_isp.rename(columns={0: 'Number of Relays'}, inplace=True)
num_relays_per_isp.sort_values(
    by='Number of Relays', ascending=False, inplace=True)
top_100_isp = num_relays_per_isp.head(100)
top_100_isp = top_100_isp.reset_index().replace(
    {'isp': {'amazon.com Inc.': 'amazon.com, Inc'}}).groupby('isp', sort=False).sum()
top_100_isp.sort_values(by='Number of Relays', ascending=False, inplace=True)


# plot the data

fig1 = px.scatter(ada_per_isp_100mil,
                  x=ada_per_isp_100mil.index,
                  y=ada_per_isp_100mil.live_stake.values,
                  color=ada_per_isp_100mil.index,
                  width=1400,
                  height=800,
                  size=ada_per_isp_100mil['Number of Pools'],
                  labels={'isp': '', 'y': 'ADA Staked'},
                  title='ADA Staked per ISP',
                  opacity=0.98,)
fig1.update_layout(title='Ada Staked Per ISP', paper_bgcolor='black', plot_bgcolor='black', font_color='white')
fig1.update_xaxes(tickangle=90)


fig2 = px.bar(top_100_isp, x=top_100_isp.index, y=top_100_isp['Number of Relays'], color=top_100_isp.index,
              width=1400, height=800, title='Top 100 ISPs by Number of Relays', opacity=0.98)
fig2.update_layout(title='Top 100 ISP sorted by Number of Relays', paper_bgcolor='black', plot_bgcolor='black' ,font=dict(color='white'))


fig3 = px.scatter_geo(data,
                      lat='latitude',
                      lon='longitude',
                      #      locationmode='country names',
                      #      locations="city",
                      color="pool_id",  # which column to use to set the color of markers
                      hover_name="ticker",  # column added to hover information
                      hover_data=['country_name', 'city',
                                  'live_stake', 'delegators', 'homepage'],
                      #      size="delegators", # size of markers
                      projection="natural earth",
                      width=1400,
                      height=800)

fig3.update_layout(
    geo = dict(
        showland = True,
        landcolor = "rgb(212, 212, 212)",
        subunitcolor = "rgb(255, 255, 255)",
        countrycolor = "rgb(255, 255, 255)",
        showlakes = True,
        lakecolor = "rgb(104, 120, 201)",
        showsubunits = True,
        showcountries = True,
        showocean = True,
        bgcolor = "rgb(0, 0, 0)",
        ),
    title='Map of All Relays on Cardano',
    paper_bgcolor='black',
    font=dict(color='white'),
)

app.layout = html.Div([
    dcc.Tabs([
        dcc.Tab(label='Relay Map', children=[
            dcc.Graph(figure=fig3,style={'background-color': colors['background']})
        ]),
        dcc.Tab(label='ADA Staked per ISP', children=[
            dcc.Graph(figure=fig1,style={'background-color': colors['background']})
        ]),
        dcc.Tab(label='Top 100 ISPs by Number of Relays', children=[
            dcc.Graph(figure=fig2,style={'background-color': colors['background']})
        ])
    ])
])

if __name__ == '__main__':
    app.run_server(debug=True)