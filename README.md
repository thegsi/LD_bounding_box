# LD bounding_box

Python script to open a file system of vector and raster GIS data, find the extent and output this into a spreadsheet in a format suitable for Marc cataloguing.    

Place the bounding_box.py script in the same directory as the GIS data.

Replace the path variable on line 6 (`path = './test_data'`) to point to your GIS data (eg `path = './'` if in the same directory as the GIS data).

Install the dependencies using:

`pip install gdal`
`pip install osr`

Run the script with:

`python bounding_box.py`
