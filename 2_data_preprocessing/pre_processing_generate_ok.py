import glob
import os
from tqdm import tqdm

files = glob.glob('data/Sentinel-1/*/geo*/*/*.tif')

for i in tqdm(range(len(files))):
    ok_file = '/'.join(files[i].split('/')[:-1]) + '/ok.process'
    os.system('touch '+ok_file)


