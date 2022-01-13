import os
import pandas as pd
from PIL import Image
import warnings

Image.MAX_IMAGE_PIXELS = None
warnings.simplefilter('ignore', Image.DecompressionBombWarning)

path = './data'

def getFiles (path):
    paths = []
    for (dirpath, dirnames, filenames) in os.walk(path):
        clean_filenames = []
        barred_file_exts = ['jpg', 'csv', 'xls', 'lsx', 'ovr', 'aux', 'xml', 'asc']
        for f in filenames:
            if f[-3:] not in barred_file_exts:
                clean_filenames.append(f)

        paths.append([dirpath, clean_filenames] )
    return paths

paths = getFiles(path)

dims = []
for p in paths:
    for f in p[1]:
        fileName = p[0] + '/' + f
        # print(fileName)
        if '.tif' in fileName:
            image = Image.open(fileName)
            width, height = image.size
            dims.append({'fileName': fileName, 'width': width, 'height': height})

columns = ['height_d', 'width_e']
index = [dim['fileName'] for dim in dims]
df = pd.DataFrame(columns=columns, index=index)

for dim in dims:
    for k in dim.keys():
        if k == 'width':
            width = dim[k]
    df['width_e'][dim['fileName']] = width
    df['height_d'][dim['fileName']] = dim['height']

df.to_csv('dimensions.csv', sep=',', encoding='utf-8')
