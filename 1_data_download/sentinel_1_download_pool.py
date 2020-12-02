# DLR-TUM SiPEO TEAM
# So2Sat Project
# Sentinel-1 data sets download prototype
# PhD Candidate: Jingliang Hu
# Email: jingliang.hu@dlr.de
# 19.12.2017
# 09.2020 modified for time series data download
import os
import sys
sys.path.insert(1,'../src')
import download_lib as d_lib
import pandas as pd
from sentinelsat.sentinel import SentinelAPI
import sentinelsat
print(sentinelsat.__file__)

start_point = 1

###############################################################################
# the link to sentinel data hub, user account and password
url = 'https://scihub.copernicus.eu/dhus'
# -------------------------------------------
# HERE PUT IN YOUR USER ACCOUNT AND PASSWORD

if start_point == 0:
    username ='sipeo_so2sat_demo'
    password='sipeo_so2sat'


api = SentinelAPI(username, password, url)
###############################################################################


###############################################################################
# parameter setting
roi_geojson_file = '../tile-covering-33n.json'
# roi_geojson_file = '../tile-covering-34s.json'

# time requirement
startDate = ["20191201"]
endDate  =  ["20191230"]

# directory of data to be saved
outdir = '../data'
###############################################################################




'''
load roi of tiles
'''
import json
# roiFile = 'tile-covering-34s.json'
with open(roi_geojson_file) as f:
    data = json.load(f)



'''
Data downloading pool
'''
idx = 0
for feat in data['features']:
    print('############################################')
    tile_name = str(feat['properties']['zone'])+'_'+str(feat['properties']['i'])+'_'+str(feat['properties']['j'])
    ###############################################################################
    #
    #               read the region of interested ROI
    #
    coord = feat['geometry']['coordinates']
    lomax = max([coord[0][0][0], coord[0][1][0], coord[0][2][0], coord[0][3][0], coord[0][4][0]])
    lomin = min([coord[0][0][0], coord[0][1][0], coord[0][2][0], coord[0][3][0], coord[0][4][0]])
    lamax = max([coord[0][0][1], coord[0][1][1], coord[0][2][1], coord[0][3][1], coord[0][4][1]])
    lamin = min([coord[0][0][1], coord[0][1][1], coord[0][2][1], coord[0][3][1], coord[0][4][1]])
    coordinate = [lomin,lomax,lamin,lamax]
    footprint, roiPolygon = d_lib.roi_buffer_footprint(coordinate)
    ###############################################################################
    #
    #               aquire the meta data of overlapped data sets
    #
    # query the data in region of interested
    print('Querying for tile: %s' %(tile_name))
    products = api.query(
                        footprint,
                        beginposition=(startDate[0],endDate[0]),
                        endposition=(startDate[0], endDate[0]),
                        platformname='Sentinel-1',
                        producttype='SLC',
                        sensoroperationalmode='IW',
                        polarisationmode='VV VH'
                        )
    print('Find %d data sets intersect with ROI' %(len(products)))
    # save searched meta information into a data frame        
    products_df  = api.to_dataframe(products)
    # find the data contain the roi region
    for index, row in products_df.iterrows():
        product_tbd = d_lib.single_data_cover_roi(row, roiPolygon)
        if isinstance(product_tbd,int):
            products_df = products_df.drop(index)
    print('Find %d data sets contrains  ROI' % (len(products_df)))
    # construct a dataframe to save datasets to be downloaded
    if idx == 0:
        idx += 1
        products_to_be_downloaded = products_df
    else:
        products_to_be_downloaded = pd.concat([products_to_be_downloaded, products_df])
    # delete repeated datasets
    nb_all = len(products_to_be_downloaded)
    products_to_be_downloaded = products_to_be_downloaded.drop_duplicates()
    nb_left = len(products_to_be_downloaded)
    print('%d data sets already in data downloading pool' % (nb_all-nb_left))


products_to_be_downloaded.to_csv(os.path.join(outdir,'sentinel-1_download_pool_'+startDate[0]+'_'+endDate[0]+'.csv'))



