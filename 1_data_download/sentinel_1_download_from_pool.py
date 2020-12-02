import os
import sys
import time
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
pool_csv = '../data/sentinel-1_download_pool_20191201_20191230.csv'
###############################################################################


download_pool = pd.read_csv(pool_csv)

for idx in range(len(download_pool)):
    while not os.path.exists(outdir+'/'+download_pool['title'][idx]+'.ok'):
        download_info = d_lib.run_download_from_pool(download_pool['uuid'][idx], outdir, username, password)
        if not os.path.exists(out_dir+'/'+download_pool['title'][idx]+'.ok'):
            secs = 500
            print('pause '+str(secs)+'secs')
            time.sleep(secs)







