# DLR-TUM SiPEO TEAM
# So2Sat Project
# Sentinel-1 data sets download prototype
# PhD Candidate: Jingliang Hu
# Email: jingliang.hu@dlr.de
# 19.12.2017
# 09.2020 modified for time series data download

import sys
sys.path.insert(1,'../src')
import download_lib as d_lib
import time
import os
import logging
import glob
from shapely.wkt import loads
from osgeo import ogr,osr,gdal
import pandas as pd
from sentinelsat.sentinel import SentinelAPI
import sentinelsat
print(sentinelsat.__file__)
import numpy as np

start_point = 0

###############################################################################
# the link to sentinel data hub, user account and password
url = 'https://scihub.copernicus.eu/dhus'
# -------------------------------------------
# HERE PUT IN YOUR USER ACCOUNT AND PASSWORD

if start_point == 0:
    username ='sipeo_so2sat_demo'
    password='sipeo_so2sat'

###############################################################################


###############################################################################
# parameter setting
roi_geojson_file = '../Multi_Class_Land_Cover_Change_AOIs.geojson'
roiType = 'geojson'
# time requirement
# startDate = ["20170301","20170601","20170901"]
# endDate   = ["20170331","20170630","20170930"]
startDate = ["20191201","20191101","20191001","20190901","20190801","20190701","20190601","20190501","20190401","20190301","20190201","20190101","20181201","20181101","20181001","20180901","20180801","20180701","20180601","20180501","20180401","20180301","20180201","20180101"]
endDate   = ["20191230","20191130","20191030","20190930","20190830","20190730","20190630","20190530","20190430","20190330","20190228","20190130","20181230","20181130","20181030","20180930","20180830","20180730","20180630","20180530","20180430","20180330","20180228","20180130"]
# directory of data to be saved
outdir = '../data/Sentinel-1/'


###############################################################################
# get ROIs
f = ogr.Open(roi_geojson_file)
lye = f.GetLayer()

nb_rois = lye.GetFeatureCount()
cityname = []
roi_ext = []
for i in range(nb_rois):
    feat = lye.GetFeature(i)
    cityname.append(feat.GetField(0))
    geom = feat.geometry()
    roi_ext.append(geom.ExportToWkt())

# loop over cities
for idx_city in range(len(cityname)-start_point-1,-1,-6):
    city = cityname[idx_city]
    roi_path = city

    ###############################################################################
    #
    #               read the region of interested ROI
    #
    if roiType.lower() == 'kml':
        city = city.split("/")[-1].split(".")[0]
        # directory to the ROI.kml file
        kmlpath = roi_path
        # read footprint from roi kml for data searching
        driver = ogr.GetDriverByName('kml')
        kml = driver.Open(kmlpath)
        kmllayer = kml.GetLayer();
        coordinate = kmllayer.GetExtent()
    elif roiType.lower()=='geotiff':
        city = city.split("/")[-1].split(".")[0]
        # directory to the ROI.kml file
        tifpath = roi_path
        tifdat = gdal.Open(tifpath)
        ulx, xres, xskew, uly, yskew, yres  = tifdat.GetGeoTransform()
        lrx = ulx + (tifdat.RasterXSize * xres)
        lry = uly + (tifdat.RasterYSize * yres)
        # Setup the source projection - you can also import from epsg, proj4...
        source = osr.SpatialReference()
        source.ImportFromWkt(tifdat.GetProjection())
        # The target wgs84/lonlat projection
        target = osr.SpatialReference()
        target.ImportFromEPSG(4326)
        # Create the transform - this can be used repeatedly
        transform = osr.CoordinateTransformation(source, target)
        # Transform the point. You can also create an ogr geometry and use the more generic `point.Transform()`
        ul = transform.TransformPoint(ulx, uly)
        lr = transform.TransformPoint(lrx, lry)
        # ROI coordinates in WGS84/lonlat
        coordinate = [ul[0],lr[0],lr[1],ul[1]]
    elif roiType.lower()=='geojson':
        tmp = roi_ext[idx_city].split('((')[1].split('))')[0].split(',')
        x_coord = []
        y_coord = []
        for tmp_idx in range(len(tmp)):
            x_tmp,y_tmp = tmp[tmp_idx].split(' ')
            x_coord.append(float(x_tmp))
            y_coord.append(float(y_tmp))
        coordinate = [min(x_coord),max(x_coord),min(y_coord),max(y_coord)]
    else:
        print('----------------- Wrong given ROI data type, only KML and GEOTIFF for now  ---------------------\n')
        break


    footprint, roiPolygon = d_lib.roi_buffer_footprint(coordinate)

    # get meta information of a verified data
    examplery_data = glob.glob(outdir + '/' + city + '/original_dat/201912/*.zip')
    meta_info = d_lib.retrieve_mata_data(examplery_data[0].split('/')[-1],username,password)


    ###############################################################################    
    for tt in range(len(startDate)-1,0,-1):
        ###############################################################################
        # path setting (do not change)
        outdatapath = outdir + '/' + city + '/original_dat'+'/'+startDate[tt][:6]+'/'
        if not os.path.exists(outdatapath):
            os.makedirs(outdatapath)
        elif os.path.exists(outdatapath+'data_downloaded.ok'):
            print('\n------------------- Data has been downloaed for '+city+' in '+startDate[tt][:6]+' -------------------------\n')
            continue

        print('\n------------------- searching and downloading data sets of '+city+' in '+startDate[tt][:6]+' -------------------------\n')
        ###############################################################################
        #
        #               aquire the meta data of overlapped data sets
        #
        # part one
        # query the data in region of interested
        api = SentinelAPI(username, password, url)
        print('querying\n')
        logging.info('querying\n')
        products = api.query(
                            footprint,
                            beginposition=(startDate[tt],startDate[tt-1]),
                            endposition=(startDate[tt], startDate[tt-1]),
                            platformname='Sentinel-1',
                            producttype='SLC',
                            sensoroperationalmode='IW',
                            polarisationmode='VV VH',
                            relativeorbitnumber=meta_info['relativeorbitnumber']
                            )
        print(len(products))
        logging.info(len(products))
        if len(products)==0:
            print('----------------- '+city+' in '+startDate[tt][:6]+': no data set was found at all, change time period ---------------------\n')
            continue
        # save searched meta information into a data frame        
        products_df  = api.to_dataframe(products)

        # find the data with the slicenumber and S1A or S1B 
        for index, row in products_df.iterrows():
            # check slice number
            if row['slicenumber'] != meta_info['slicenumber']:
                continue
            # check S1A or S1B
            if row['title'].split('_')[0]!=meta_info['title'].split('_')[0]:
                continue

            product_tbd = d_lib.single_data_cover_roi(row, roiPolygon)
            if not isinstance(product_tbd,int):
                break;

        del api
        # download the found data
        if not isinstance(product_tbd,int):
            while not os.path.exists(outdatapath+'data_downloaded.ok'):
                download_info = d_lib.run_download(product_tbd['uuid'], outdatapath, username, password)
                if not os.path.exists(outdatapath+'data_downloaded.ok'):
                    # pause the programme to avoid the ERROR: "429 Too Many Requests"
                    secs = 500
                    print('pause '+str(secs)+'secs to avoid ERROR429')
                    time.sleep(secs)







