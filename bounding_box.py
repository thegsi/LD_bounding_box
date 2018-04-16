import gdal
import osr
import os
import pandas as pd

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

            bbox = { 'fileName': fileName, 'ul': ul, 'lr': lr }
            coordinates.append(bbox)

# Convert to degrees, minutes, seconds
def decdeg2dms(dd):
    is_positive = dd >= 0
    dd = abs(dd)
    minutes, seconds = divmod(dd*3600,60)
    degrees, minutes = divmod(minutes,60)
    degrees = degrees if is_positive else -degrees
    return (int(degrees), int(minutes),int(round(seconds, 1)))

def decdeg2dmsTuples(ddInfo):
    w = decdeg2dms(ddInfo['ul'][0])
    e = decdeg2dms(ddInfo['lr'][0])
    n = decdeg2dms(ddInfo['ul'][1])
    s = decdeg2dms(ddInfo['ul'][1])
    return { 'fileName': ddInfo['fileName'],'w': w,'e': e,'n': n,'s': s }

dmsBoundaries = [decdeg2dmsTuples(ddInfo) for ddInfo in coordinates]

# Convert to csv
columns = ['West', 'East', 'North', 'South', '255C']
index = [boundary['fileName'] for boundary in dmsBoundaries]
df = pd.DataFrame(columns=columns, index=index)

def formatCoord (bounds, direction):
    threeDigitBounds = '{:03}'.format(bounds[0]).replace('-', '0')

    if bounds[0] >= 0:
        if direction == 'WE':
            threeDigitBounds = 'E' + threeDigitBounds
        elif direction == 'NS':
            threeDigitBounds = 'N' + threeDigitBounds
    elif int(bounds[0]) < 0:
        if direction == 'WE':
            threeDigitBounds = 'W' + threeDigitBounds
        elif direction == 'NS':
            threeDigitBounds = 'S' + threeDigitBounds

    return threeDigitBounds + '{:02}'.format(bounds[1]) + '{:02}'.format(bounds[2])

def formatCoordDMS (boundary):
    # W0033343 to
    # (E010°48′40″--E010°48′54″/N063°32′40″--N063°32′34″) / W E N S
    return boundary[:4] + '°' + boundary[4:6] + '\'' + boundary[6:8] + '"'

for boundary in dmsBoundaries:
    df['West'][boundary['fileName']] = formatCoord(boundary['w'], 'WE')
    df['East'][boundary['fileName']] = formatCoord(boundary['e'], 'WE')
    df['North'][boundary['fileName']] = formatCoord(boundary['n'], 'NS')
    df['South'][boundary['fileName']] = formatCoord(boundary['s'], 'NS')

    df['255C'][boundary['fileName']] = '(%s--%s/%s--%s)' % (formatCoordDMS(df['West'][boundary['fileName']]), formatCoordDMS(df['East'][boundary['fileName']]), formatCoordDMS(df['North'][boundary['fileName']]), formatCoordDMS(df['South'][boundary['fileName']]))
    print(df['255C'][boundary['fileName']])

df.to_csv('boundaries.csv', sep=',', encoding='utf-8')
