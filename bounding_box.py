import gdal
import ogr
import osr
import os

path = './test_data'

def getFiles (path):
    paths = []
    for (dirpath, dirnames, filenames) in os.walk(path):
        paths.append([dirpath, filenames] )
    return paths

paths = getFiles(path)
coordinates = []

for p in paths:
    for f in p[1]:
        fileName = p[0] + '/' + f
        dataset = gdal.OpenEx(fileName, gdal.OF_RASTER)
        print(fileName)
        if dataset is None:
            dataset = gdal.OpenEx(fileName, gdal.OF_VECTOR)
            if dataset != None:
                # VECTOR
                lyr = dataset.GetLayer()
                numLayers = dataset.GetLayerCount()
                # print('numLayers', numLayers)

                for l in range(numLayers):
                    # Obtain Layer extent
                    layer = dataset.GetLayer(l)
                    spatialRef = layer.GetSpatialRef()
                    extent = layer.GetExtent()

                    source = osr.SpatialReference()
                    source.ImportFromWkt(str(spatialRef))
                    target = osr.SpatialReference()
                    target.ImportFromEPSG(4326)
                    transform = osr.CoordinateTransformation(source, target)

                    ul = transform.TransformPoint(extent[0], extent[2])
                    lr = transform.TransformPoint(extent[1], extent[3])
                    # print(ul)
                    # print(lr)
                    bbox = { 'fileName': fileName, 'ul': ul, 'lr': lr }
                    coordinates.append(bbox)

            elif dataset is None:
                print ('Open failed')
        else:
            # RASTER
            # projection = dataset.GetProjectionRef()
            # print('GetProjectionRef', projection)

            # Obtain coordinates
            ulx, xres, xskew, uly, yskew, yres  = dataset.GetGeoTransform()
            lrx = ulx + (dataset.RasterXSize * xres)
            lry = uly + (dataset.RasterYSize * yres)

            # Transform projection
            source = osr.SpatialReference()
            source.ImportFromWkt(dataset.GetProjection())
            target = osr.SpatialReference()
            target.ImportFromEPSG(4326)
            transform = osr.CoordinateTransformation(source, target)

            # Transform points
            ul = transform.TransformPoint(ulx, uly)
            lr = transform.TransformPoint(lrx, lry)
            # print(ul)
            # print(lr)
            bbox = { 'fileName': fileName, 'ul': ul, 'lr': lr }
            coordinates.append(bbox)

print(coordinates)

def decdeg2dms(dd):
    is_positive = dd >= 0
    dd = abs(dd)
    minutes, seconds = divmod(dd*3600,60)
    degrees, minutes = divmod(minutes,60)
    degrees = degrees if is_positive else -degrees
    return (degrees,minutes,seconds)

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
