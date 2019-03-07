# LD bounding_box

Python script to open a file system of vector and raster GIS data, find the extent and output this into a spreadsheet in a format suitable for Marc cataloguing.    

Place the bounding_box.py script in the same directory as the GIS data.

Replace the path variable on line 6 (`path = './test_data'`) to point to your GIS data (eg `path = './'` if in the same directory as the GIS data).

Install the dependencies, GDAL can sometimes be difficult to install.

On mac (High Sierra) the following worked for me:

`brew install gdal`

Followed by creating and activating a virtual env:

`python3 -m venv gdal_env`
`source gdal_env/bin/activate`

And then installing the dependencies inside the virtual enve:

`pip install gdal`
`pip install osr`

Run the script within the virtual env:

`python bounding_box.py`
