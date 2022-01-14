
import json
import time
import requests
import math as m
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import descartes
import geopandas as gpd
from shapely.geometry import Point, Polygon
import seaborn as sns
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import MinMaxScaler
from sklearn.cluster import KMeans
from sklearn.model_selection import train_test_split 
from sklearn.linear_model import LinearRegression
from sklearn import metrics
from scipy.optimize import curve_fit
import plotly.express as px
import chart_studio
import chart_studio.plotly as py
import chart_studio.tools as tls
import folium
import ast


# Leave This code here and lookup at pandas documentation 
# if you need to know about chained assignments
pd.options.mode.chained_assignment = None  # default='warn'

df = pd.read_json('cardano_relay_data_01_07_2022.json')

testing = df.copy()

# This is code below will create a list of indexes of rows with missing data to be dropped
def drop_list(df):

	drop_list = []

	for i in range(len(df)):
		if df.connection[i] is None or len(df.connection[i]) < 2:
			drop_list.append(i)

	return drop_list




testing.drop(testing.index[drop_list(df)], inplace=True)

# create the isp and asn columns by using the get function with
testing['isp'] = testing.connection.apply(lambda x: x.get('isp', np.nan))
testing['asn'] = testing.connection.apply(lambda x: x.get('asn', np.nan))


# Save this to a json file called "cleaned"
testing.to_json('relay_data_clean.json')