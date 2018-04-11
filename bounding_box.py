import sys
import gdal
import ogr
import os

path = './test_data'

def getFiles (path):
    paths = []
    for (dirpath, dirnames, filenames) in os.walk(path):
        paths.append([dirpath, filenames] )
    return paths

paths = getFiles(path)

for p in paths:
    for f in p[1]:
        fileName = p[0] + '/' + f
        dataset = gdal.OpenEx(fileName, gdal.OF_RASTER)
        if dataset is None:
            dataset = gdal.OpenEx(fileName, gdal.OF_VECTOR)
            # if dataset is None:
            #     print ('Open failed')
        #     else:
        #         print(fileName)
        # else:
        #     print(fileName)
        if dataset != None:
            print(fileName)
            lyr = dataset.GetLayer()
            # Obtain Layer extent
            numLayers = dataset.GetLayerCount()
            # print('numLayers', numLayers)

            for l in range(numLayers):
                layer = dataset.GetLayer(l)
                extent = layer.GetExtent()
                print(fileName)
                print(extent)

# dataset = gdal.OpenEx(fileName, gdal.OF_VECTOR)
# if dataset is None:
#     print ('Open failed')
#     sys.exit( 1 )


# lyr = dataset.GetLayer()

# Obtain Layer extent
# numLayers = dataset.GetLayerCount()
# print('numLayers', numLayers)
#
# for l in range(numLayers):
#     layer = dataset.GetLayer(l)
#     extent = layer.GetExtent()
#     print(extent)


# Obtain feature extent
# for feature in lyr:
#     geom = feature.GetGeometryRef()
#     extent = geom.GetEnvelope()
#     print(extent)
