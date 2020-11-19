import os
import sys
sys.path.insert(1,'../src/pre_processing')
import glob
file_of_locations = glob.glob('../data/Sentinel-1/*')

# loop goes to every city/ location
for i in range(len(file_of_locations)):
    if not os.path.isdir(file_of_locations[i]):
        print(file_of_locations[i])
        continue

    command_lee_filter = 'python ../src/pre_processing/geocoding_core.py ' + file_of_locations[i] + ' ../src/pre_processing/templates/gpt_template_preprocessing_lee_geojson_UTM.xml Multi_Class_Land_Cover_Change_AOIs.geojson'
    os.system(command_lee_filter)

    command_unfil = 'python ../src/pre_processing/geocoding_core.py ' + file_of_locations[i] + ' ../src/pre_processing/templates/gpt_template_preprocessing_unfilt_geojson_UTM.xml Multi_Class_Land_Cover_Change_AOIs.geojson'
    os.system(command_unfil)



