import os
import glob
from osgeo import gdal
from tqdm import tqdm
import numpy as np

files = glob.glob('../data/Sentinel-1/*/geocoded_subset_dat/*/*.tif')
out_data_dir = '../data/Visual_anaylsis_ready/'

for i in tqdm(range(len(files))):
#for i in range(1):
    '''
    load data information and initial output data directory
    '''
    lee_data_file = files[i]
    info = lee_data_file.split('/')
    place = info[3]
    time = info[5][:4]+'_'+ info[5][-2:]
    out_data_file_name ='/'+ place+'_'+time+'_lee.tif'
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
    Visualize and save lee filtered data
    '''
    VH = np.log10(lee[0,:,:])
    maxx = np.quantile(VH,0.98)
    minn = np.quantile(VH,0.02)
    VH[VH<minn]=minn
    VH[VH>maxx]=maxx
    VH = (255*(VH-minn)/(maxx-minn)).astype(np.uint8)
    driver = gdal.GetDriverByName('GTiff')
    f = driver.Create(place_folder+out_data_file_name, col, row, 1, gdal.GDT_Byte)
    f.SetProjection(proj)
    f.SetGeoTransform(geoInfo)
    outBand = f.GetRasterBand(1)
    outBand.WriteArray(VH)
    outBand.FlushCache()
    del outBand
    del f
    del driver
    '''
    load unfiltered data
    '''
    unfil_data_file = lee_data_file.replace('geocoded_subset_dat','geocoded_subset_unfilt_dat')
    unfil_data_file = unfil_data_file.replace('Deb_Spk_TC','Deb_TC')
    fid = gdal.Open(unfil_data_file)
    unfil = fid.ReadAsArray()
    del fid
    '''
    Visualize and save unfiltered data
    '''
    VH = np.log10(np.square(unfil[0,:,:])+np.square(unfil[1,:,:]))
    maxx = np.quantile(VH,0.98)
    minn = np.quantile(VH,0.02)
    VH[VH<minn]=minn
    VH[VH>maxx]=maxx
    VH = (255*(VH-minn)/(maxx-minn)).astype(np.uint8)
    out_data_file_name ='/'+ place+'_'+time+'_unfilt.tif'
    driver = gdal.GetDriverByName('GTiff')
    f = driver.Create(place_folder+out_data_file_name, col, row, 1, gdal.GDT_Byte)
    f.SetProjection(proj)
    f.SetGeoTransform(geoInfo)
    outBand = f.GetRasterBand(1)
    outBand.WriteArray(VH)
    outBand.FlushCache()
    del outBand
    del f
    del driver



