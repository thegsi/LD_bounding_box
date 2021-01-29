import os
import pandas as pd
from PIL import Image

path = './test_data'

def getFiles (path):
    paths = []
    for (dirpath, dirnames, filenames) in os.walk(path):
        paths.append([dirpath, filenames] )
    return paths

paths = getFiles(path)

dims = []
for p in paths:
    for f in p[1]:
        fileName = p[0] + '/' + f
        print(fileName)
        if '.tif' in fileName:
            image = Image.open(fileName)
            width, height = image.size
            dims.append({'fileName': fileName, 'width': width, 'height': height})

columns = ['width_e', 'height_d']
index = [dim['fileName'] for dim in dims]
df = pd.DataFrame(columns=columns, index=index)

for dim in dims:
    df['width'][dim['fileName']] = dim['width']
    df['height'][dim['fileName']] = dim['height']

df.to_csv('dimensions.csv', sep=',', encoding='utf-8')
