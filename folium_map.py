import folium
import json
import pandas as pd
import numpy as np
import geopandas as gpd
import matplotlib.pyplot as plt


world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))

tf_data = pd.read_csv('data/labels.csv')
world = world.rename(columns={'name':'country'})
world = world.merge(tf_data, on='country')
fig, ax = plt.subplots()
ax.set_aspect('equal')
world.plot(column='labels')
plt.savefig('data/graph.png');
