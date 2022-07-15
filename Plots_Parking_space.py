import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
import os
import time
import folium
api_key = **

from bokeh.io import show
from bokeh.plotting import gmap
from bokeh.models import GMapOptions

from bokeh.models import ColumnDataSource

data = pd.read_csv('/Users/shashwateshtripathi/Downloads/On-street_Parking_Bay_Sensors.csv')
bokeh_width, bokeh_height = 500,400
def plot(lat, lng, zoom=10, map_type='roadmap'):
    gmap_options = GMapOptions(lat=lat, lng=lng,
                               map_type=map_type, zoom=zoom)
    p = gmap(api_key, gmap_options, title='Pays de Gex',
             width=800, height=800)
    # definition of the column data source:
    source = ColumnDataSource(data)
    # see how we specify the x and y columns as strings,
    # and how to declare as a source the ColumnDataSource:
    center = p.circle('lon', 'lat', size=4, alpha=0.2,
                      color='yellow', source=source)
    show(p)
    return p





new={'status':[]}
for i in data['status']:
    if i=='Unoccupied':
        i='0'
        
    else:
        i='1'
    new['status'].append(i)

new = pd.DataFrame(new)
data.update(new)
data['status'] = pd.to_numeric(data['status'])
X = data.iloc[:,:].values

kmean=KMeans(n_clusters=2)
kmean.fit(X[:,(4,5)])
kmean.cluster_centers_
kmean.labels_

filtered1 = []
filtered2=[]
for i in X:
    if i[2]==0:
        filtered1.append(i)
    else:
        filtered2.append(i)
filtered1=np.asarray(filtered1)
filtered2=np.asarray(filtered2)
import mplleaflet
plt.plot(filtered1[:,5], filtered1[:,4], 'r.')
plt.plot(filtered2[:,5],filtered2[:,4],'b.')
#p=plot(filtered1[0,5], filtered1[0,4])
m=folium.Map((filtered1[0,4],filtered1[0,5]),zoom_start=12)
for index,data in data.iterrows():
    location = [data["lat"],data["lon"]]
    if data["status"]==1:
        folium.Marker(location,popup='Status:occupied',icon = folium.Icon(color="red")).add_to(m)
    else:
        folium.Marker(location,popup='Status:unoccupied',icon = folium.Icon(color="green")).add_to(m)
m.save("lol.html")
