# Sentinel-1 download and processing
This repository is a running example for Sentinel-1 data download and preprocessing.

# Environment
Software: ESA SNAP gpt

Python libs: gdal, shapely, sentinelsat 

# Description
Sentinel-1 data download: 

Donwloads data from sentinel data hub using the sentinelsat lib

Input: 
1. roi files: kml files, geotiff files, or geojson files; codes need to be customized for different use cases
2. time period
3. directory for saving data

Sentinel-1 data preprocessing:

Preprocess downloaded zip data file to required SAR product using the ESA SNAP GPT. 

Support parallel processing

Input:
1. GPT xml template

Output:
Sentinel-1 data VV-VH data; filtered and unfiltered; 

# Publication
Details about the processing chain can be found in the following paper:

>Hu, Jingliang, Pedram Ghamisi, and Xiao Xiang Zhu. "Feature extraction and selection of sentinel-1 dual-pol data for global-scale local climate zone classification." ISPRS International Journal of Geo-Information 7.9 (2018): 379. (DOI: https://doi.org/10.3390/ijgi7090379)

This repository has been used for projects whose outcomes results in papers listed here:

> Hu, Jingliang, Pedram Ghamisi, and Xiao Xiang Zhu. "Feature extraction and selection of sentinel-1 dual-pol data for global-scale local climate zone classification." ISPRS International Journal of Geo-Information 7.9 (2018): 379. (DOI: https://doi.org/10.3390/ijgi7090379)

>Zhu, Xiao Xiang, et al. "So2Sat LCZ42: A Benchmark Data Set for the Classification of Global Local Climate Zones [Software and Data Sets]," in IEEE Geoscience and Remote Sensing Magazine, vol. 8, no. 3, pp. 76-89, Sept. 2020, doi: 10.1109/MGRS.2020.2964708.

