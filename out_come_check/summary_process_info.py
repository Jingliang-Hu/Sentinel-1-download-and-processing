import pandas as pd
import os
import glob
from osgeo import ogr,osr,gdal


startDate = ["20191201","20191101","20191001","20190901","20190801","20190701","20190601","20190501","20190401","20190301","20190201","20190101","20181201","20181101","20181001","20180901","20180801","20180701","20180601","20180501","20180401","20180301","20180201","20180101"]
endDate   = ["20191231","20191130","20191031","20190930","20190831","20190731","20190630","20190531","20190430","20190331","20190228","20190131","20181231","20181130","20181031","20180930","20180831","20180731","20180630","20180531","20180430","20180331","20180228","20180131"]
out_excel_file = "sentinel_1_precessed_info.xlsx"
roi_geojson_file = 'Multi_Class_Land_Cover_Change_AOIs.geojson'
processed_data_path = '/datastore01/DATA/misc/sentinel_1_auto_download/data/Sentinel-1_analysis_ready/'
original_data_path  = '/datastore01/DATA/misc/sentinel_1_auto_download/data/Sentinel-1/'

# get ROIs
f = ogr.Open(roi_geojson_file)
lye = f.GetLayer()

nb_rois = lye.GetFeatureCount()
cityname = []
for i in range(nb_rois):
    feat = lye.GetFeature(i)
    cityname.append(feat.GetField(0))

info = []


# loop over cities
for idx_city in range(len(cityname)):
    info_city = []
    for tt in range(0,len(startDate)):
        check_file = glob.glob(processed_data_path+cityname[idx_city]+'/*'+startDate[tt][:4]+'_'+startDate[tt][4:6]+'.tif')
        if len(check_file) == 1:
            info_city.append(1)
        else:
            data_dirs = glob.glob(original_data_path+cityname[idx_city]+'/*/'+startDate[tt][:6])
            for item in data_dirs:
                os.system('rm -r '+item)
            info_city.append(0)

    info.append(info_city)


df = pd.DataFrame(info, index=cityname, columns=startDate)
df.to_excel(out_excel_file)











