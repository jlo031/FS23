# ---- This is <FS23_data_transfer_workflow.py> ----

"""
Extract features from Sentinel-1 input image
""" 

import argparse
import os
import sys
import pathlib
import shutil
import zipfile
import subprocess
from loguru import logger

import datetime
from datetime import timezone

import config.fs23_folder_structure as FS23

import satsearch_and_download.sentinel_download as sd

# -------------------------------------------------------------------------- #
# -------------------------------------------------------------------------- #

# PARAMETER DEFINITIONS

# search interval in hours
delta_t_in_hours = 12

# search area geojson file 
search_ROI = FS23.WORK_DIR / 'ROIs' / 'FS23_satsearch_area.geojson'




# do not overwrite anything (usually)
overwrite = False

# loglevel
loglevel = 'INFO'
loglevel = 'DEBUG'

# -------------------------------------------------------------------------- #
# -------------------------------------------------------------------------- #

# FIND AND DOWNLOAD ALL S1 DATA FROM LAST TIME INTERVAL

# --------------- #

# get current time in UTC
current_time = datetime.datetime.now(timezone.utc)

# calculate datetime.timedelta from overlap_interval
timedelta = datetime.timedelta(hours=delta_t_in_hours)

# find starttime from current time and time delta
starttime = current_time - timedelta

# build starttime and endtime strings for satsearch
starttime_string =  f'{starttime.year}-{starttime.month}-{starttime.day} {starttime.hour}:{starttime.minute}'
endtime_string =  f'{current_time.year}-{current_time.month}-{current_time.day} {current_time.hour}:{current_time.minute}'

# get download_dir from config
download_dir = FS23.S1_L1_DIR

# --------------- #

logger.info(f'starttime_string: {starttime_string}')
logger.info(f'endtime_string:   {endtime_string}')

sd.search_and_download_products_from_scihub(
    'S1',
    search_ROI,
    starttime_string,
    endtime_string,
    download_dir,
    area_relation='Intersects',
    scihub_username = 'JLohse',
    scihub_password = 'dummy_password',
    overwrite = overwrite,
    loglevel = loglevel,
)

# -------------------------------------------------------------------------- #
# -------------------------------------------------------------------------- #

# UNZIP ALL S1 PRODUCTS AND MAKE LIST OF DOWNLOADED PRODUCTS

# --------------- #

# get list of all zip files in L1 folder
zip_file_list = [ f for f in os.listdir(FS23.S1_L1_DIR) if f.endswith('.zip') ]

# loop over all zip_files
for zip_file in zip_file_list:

    # build full path to current zip_file
    zip_path = FS23.S1_L1_DIR / zip_file

    # create ZipFile object
    zip_ref = zipfile.ZipFile(zip_path)

    # unpack into L1 folder
    zip_ref.extractall(FS23.S1_L1_DIR)

    # close ZipFile object
    zip_ref.close()

    # remove zip_path
    zip_path.unlink(missing_ok=True)

# --------------- #

# get list of all SAFE folder in L1 folder  
S1_product_list = [ f.split('.SAFE')[0] for f in os.listdir(FS23.S1_L1_DIR) if f.endswith('.SAFE') ]
S1_product_list.sort()

n_products = len(S1_product_list)

# -------------------------------------------------------------------------- #
# -------------------------------------------------------------------------- #

# PROCESS ALL S1 PRODUCTS

# --------------- #

# loop over all S1 products
for i,S1_base in enumerate(S1_product_list):

    logger.info(f'Processing S1 product {i+1}/{n_products}')

# --------------- #

    # feature extraction and geocoding for ML 5x5 and 200m pixel spacing
    ML = '5x5'
    ps = 200

    final_output_path = FS23.S1_GEO_DIR / f'{S1_base}_intensities_epsg_3996_pixelspacing_{ps}_ML_{ML}.tiff'

    if final_output_path.is_file() and not overwrite:
        logger.info('Product already processed for current settings')
    else:
        subprocess.call(f"python /home/jlo031/work/FS23/S1_extract_features.py {S1_base} -ML {ML}", shell=True)
        subprocess.call(f"python /home/jlo031/work/FS23/S1_geocode_features.py {S1_base} -ML {ML} -pixel_spacing {ps}", shell=True)

# --------------- #

    # feature extraction and geocoding for ML 9x9 and 400 and 800m pixel spacing
    ML = '9x9'
    ps1 = 400
    ps2 = 800

    final_output_path_1 = FS23.S1_GEO_DIR / f'{S1_base}_intensities_epsg_3996_pixelspacing_{ps1}_ML_{ML}.tiff'
    final_output_path_2 = FS23.S1_GEO_DIR / f'{S1_base}_intensities_epsg_3996_pixelspacing_{ps2}_ML_{ML}.tiff'

    if final_output_path_1.is_file() and final_output_path_2.is_file() and not overwrite:
        logger.info('Product already processed for current settings')
    else:
        subprocess.call(f"python /home/jlo031/work/FS23/S1_extract_features.py {S1_base} -ML {ML}", shell=True)
        subprocess.call(f"python /home/jlo031/work/FS23/S1_geocode_features.py {S1_base} -ML {ML} -pixel_spacing {ps1}", shell=True)
        subprocess.call(f"python /home/jlo031/work/FS23/S1_geocode_features.py {S1_base} -ML {ML} -pixel_spacing {ps2}", shell=True)

# --------------- #

    # feature extraction and geocoding for ML 9x9 and 400 and 800m pixel spacing
    ML = '1x1'
    ps1 = 40
    ps2 = 80

    final_output_path_1 = FS23.S1_GEO_DIR / f'{S1_base}_intensities_epsg_3996_pixelspacing_{ps1}_ML_{ML}.tiff'
    final_output_path_2 = FS23.S1_GEO_DIR / f'{S1_base}_intensities_epsg_3996_pixelspacing_{ps2}_ML_{ML}.tiff'

    if final_output_path_1.is_file() and final_output_path_2.is_file() and not overwrite:
        logger.info('Product already processed for current settings')
    else:
        subprocess.call(f"python /home/jlo031/work/FS23/S1_extract_features.py {S1_base} -ML {ML}", shell=True)
        subprocess.call(f"python /home/jlo031/work/FS23/S1_geocode_features.py {S1_base} -ML {ML} -pixel_spacing {ps1}", shell=True)
        subprocess.call(f"python /home/jlo031/work/FS23/S1_geocode_features.py {S1_base} -ML {ML} -pixel_spacing {ps2}", shell=True)

# --------------- #

    # clean up feature folder
    shutil.rmtree(FS23.S1_FEAT_DIR, ignore_errors=True)

# -------------------------------------------------------------------------- #
# -------------------------------------------------------------------------- #

# ---- End of <FS23_data_transfer_workflow.py> ----


