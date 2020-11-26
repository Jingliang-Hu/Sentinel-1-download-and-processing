import os
import glob
from osgeo import gdal
from tqdm import tqdm

files = glob.glob('../data/Sentinel-1/*/geocoded_subset_dat/*/*.tif')
out_data_dir = '../data/Sentinel-1_analysis_ready/'

for i in tqdm(range(len(files))):
#for i in range(1):
    '''
    load data information and initial output data directory
    '''
    lee_data_file = files[i]
    info = lee_data_file.split('/')
    place = info[3]
    time = info[5][:4]+'_'+ info[5][-2:]
    out_data_file_name ='/'+ place+'_'+time+'.tif'
    place_folder = out_data_dir+place
    if not os.path.exists(place_folder):
        os.mkdir(place_folder)

    '''
    load lee filtered data
    '''   
    fid = gdal.Open(lee_data_file)
    lee = fid.ReadAsArray()
    row = fid.RasterYSize
    col = fid.RasterXSize
    bnd = fid.RasterCount
    proj = fid.GetProjection()
    geoInfo = fid.GetGeoTransform()
    del fid

    '''
    load unfiltered data
    '''
    unfil_data_file = lee_data_file.replace('geocoded_subset_dat','geocoded_subset_unfilt_dat')
    unfil_data_file = unfil_data_file.replace('Deb_Spk_TC','Deb_TC')
    fid = gdal.Open(unfil_data_file)
    unfil = fid.ReadAsArray()
    del fid


    '''
    save the analysis ready data
    '''
    driver = gdal.GetDriverByName('GTiff')
    f = driver.Create(place_folder+out_data_file_name, col, row, 8, gdal.GDT_Float32)
    f.SetProjection(proj)
    f.SetGeoTransform(geoInfo)
    for idxBnd in range(4):
        outBand = f.GetRasterBand(idxBnd+1)
        outBand.WriteArray(lee[idxBnd,:,:])
        outBand.FlushCache()
        del(outBand)

    for idxBnd in range(4):
        outBand = f.GetRasterBand(idxBnd+5)
        outBand.WriteArray(unfil[idxBnd,:,:])
        outBand.FlushCache()
        del(outBand)


