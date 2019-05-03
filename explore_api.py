import json
import pandas as pd
from stravalib.client import Client
from pprint import pprint
import matplotlib.pyplot as plt
from mpl_toolkits import basemap
import numpy as np

# # import request
# code = 'bc1de4a08a69a21980171c6f0f079b8876aad740'
# client = Client()
# code = client.exchange_code_for_token(login_details['Client ID'],
#                                      login_details['Client Secret'],
#                                      code)
# print(url)

client = Client(access_token='e405704ed45de2d99d83c8e981a067e980f0aa8b')

activities = client.get_activities()
sample = list(activities)[0]
pprint(sample.to_dict())


# Get all my activities get the date and the GPS coords
# Might need to make sure there are GPS coords
activity_coords = []
for activity in activities:
    poly_coord = {'Poly': activity.to_dict()['map']['summary_polyline'],
                  'Date': activity.to_dict()['start_date'].split('T')[0]}
    if poly_coord['Poly'] is not None:
        activity_coords.append(poly_coord)
# for activity in activities:
#     print(activity.to_dict()['upload_id'])
# activity_coords

# from __future__ import print_statement
# import time
# import swagger_client
# from swagger_client.rest import ApiException
# from pprint import pprint
#
# # Configure OAuth2 access token for authorization: strava_oauth
# swagger_client.configuration.access_token = 'YOUR_ACCESS_TOKEN'
#
# # create an instance of the API class
# api_instance = swagger_client.ActivitiesApi()
# before = 56 # Integer | An epoch timestamp to use for filtering activities that have taken place before a certain time. (optional)
# after = 56 # Integer | An epoch timestamp to use for filtering activities that have taken place after a certain time. (optional)
# page = 56 # Integer | Page number. (optional)
# perPage = 56 # Integer | Number of items per page. Defaults to 30. (optional) (default to 30)
#
# try:
#     # List Athlete Activities
#     api_response = api_instance.getLoggedInAthleteActivities(before=time.time(), after=after)
#     pprint(api_response)
# except ApiException as e:
#     print("Exception when calling ActivitiesApi->getLoggedInAthleteActivities: %s\n" % e)

import polyline

coord = polyline.decode('kil`I||ts@cNn]|AyCbT`wB{CTqEgIyNab@`BsClFqA|BmIoJ}^UcLrAqJ|KeW')

fig = plt.figure(figsize=(12,12))
fig.suptitle('Strava Activity in Des Moines, Iowa')
ax = plt.Axes(fig, [0., 0., 1., 1.], )
ax.set_aspect('equal')
ax.set_axis_off()
fig.add_axes(ax)

# for coo in coo_list:
lat,lon = map(list, zip(*coord))
plt.plot(lon, lat, lw=0.5, alpha=.9)

fig = plt.figure(figsize=(12, 12))
fig.suptitle('My Strava Summary')
ax = plt.Axes(fig, [0., 0., 1., 1.], )
ax.set_aspect('equal')
ax.set_axis_off()
fig.add_axes(ax)

for act in activity_coords:
    coord = polyline.decode(act['Poly'])
    lat, lon = map(list, zip(*coord))
    plt.plot(lon, lat, lw=0.5, alpha=.9, label=act['Date'])

plt.legend(loc=0)

fig=plt.figure()
ax=fig.add_axes([0.1,0.1,0.8,0.8])
# setup mercator map projection.
m = basemap.Basemap(llcrnrlon=-9.5,llcrnrlat=52.5,urcrnrlon=-8.5,urcrnrlat=53,\
                    rsphere=(6378137.00,6356752.3142),\
                    resolution='f',projection='merc',\
                    lat_0=40.,lon_0=-20.,lat_ts=20.)
# nylat, nylon are lat/lon of New York
nylat = 40.78; nylon = -73.98
# lonlat, lonlon are lat/lon of London.
lonlat = 51.53; lonlon = 0.08
# draw great circle route between NY and London
for act in activity_coords:
    coord = polyline.decode(act['Poly'])
    lat, lon = map(list, zip(*coord))
    m.plot(lon,lat,latlon=True,linewidth=1)
m.drawcoastlines()
m.fillcontinents()
# draw parallels
# m.drawparallels(np.arange(10,90,20),labels=[1,1,0,1])
# draw meridians
# m.drawmeridians(np.arange(-180,180,30),labels=[1,1,0,1])
ax.set_title('Exercise on Map')
plt.show()


