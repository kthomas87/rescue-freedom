import folium
import json
import pandas as pd
import numpy as np
import geopandas as gpd
import matplotlib.pyplot as plt


# world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))
#
tf_data = pd.read_csv('data/labels_w_countrycodes.csv')
# world = world.merge(tf_data, on='iso_a3')
# fig, ax = plt.subplots()
# ax.set_aspect('equal')
# world.plot(column='labels')
# plt.savefig('data/graph.png');
colors=('9e0142','d53e4f','f46d43','fdae61','fee08b','ffffbf','e6f598','abdda4','66c2a5','3288bd','5e4fa2', 'a020f0', 'ff0000', '191970')
# labels=range(15)
scales=[]
for row in tf_data['labels']:
    if row==3:
        scales.append(0)
    elif row==9:
        scales.append(1)
    elif row==1:
        scales.append(2)
    elif row==12:
        scales.append(3)
    elif row==5:
        scales.append(4)
    elif row==8:
        scales.append(5)
    elif row==2:
        scales.append(6)
    elif row==11:
        scales.append(7)
    elif row==6:
        scales.append(8)
    elif row==13:
        scales.append(9)
    elif row==0:
        scales.append(10)
    elif row==10:
        scales.append(11)
    elif row==4:
        scales.append(12)
    elif row==7:
        scales.append(13)
    else:
        scales.append(-5)

tf_data['scale']=scales


map = folium.Map()
world_geo = r'data/countries.geo.json'
map.choropleth(geo_path=world_geo, data=tf_data,
             columns=['iso_a3', 'scale'],
             threshold_scale=[0, 5, 9, 11, 12, 13],
             key_on='feature.id',
             fill_color='YlOrRd', fill_opacity=0.7, line_opacity=0.5,
             legend_name='Slavery Cluster',
             reset=True)
map.save('world.html')
# map.add_child(folium.GeoJson(data=file('data/countries.geo.json'))),
# name='Slavery',
# style_function= 'fillcolor':'green'
# map.save(outfile='data/test1.html')
