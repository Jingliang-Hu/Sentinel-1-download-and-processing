import os
import sys
sys.path.insert(1,'../src/pre_processing')
import glob
import multiprocessing as mp


file_of_locations = glob.glob('../data/Sentinel-1/*')


command_lee_filter = []
command_unfil = []
# loop goes to every city/ location
for i in range(len(file_of_locations)):
    if not os.path.isdir(file_of_locations[i]):
        continue

    command_lee_filter.append('python ../src/pre_processing/geocoding_core.py ' + file_of_locations[i] + ' ../src/pre_processing/templates/gpt_template_preprocessing_lee_geojson_UTM.xml ../Multi_Class_Land_Cover_Change_AOIs.geojson')
    command_unfil.append('python ../src/pre_processing/geocoding_core.py ' + file_of_locations[i] + ' ../src/pre_processing/templates/gpt_template_preprocessing_unfilt_geojson_UTM.xml ../Multi_Class_Land_Cover_Change_AOIs.geojson')




pool = mp.Pool(10)

results_lee = [pool.apply(os.system, args=(comm,)) for comm in command_lee_filter]
results_unfil = [pool.apply(os.system, args=(comm,)) for comm in command_unfil]

pool.close()



