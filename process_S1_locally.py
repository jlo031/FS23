# ---- This is <process_S1_locally.py> ----

"""
Process S1 image locally on KPH
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

import numpy as np

import config.fs23_folder_structure as FS23

import satsearch_and_download.sentinel_download as sd

# -------------------------------------------------------------------------- #
# -------------------------------------------------------------------------- #

# PARAMETER DEFINITIONS

# do not overwrite anything (usually)
overwrite = False

# loglevel
loglevel = 'INFO'

# define S1 basename
S1_base = 'S1A_EW_GRDM_1SDH_20230902T081844_20230902T081944_050146_06090B_65CA'

# -------------------------------------------------------------------------- #
# -------------------------------------------------------------------------- #

# UNZIP PRODUCT
# --------------- #

# get path to zip file
zip_path = FS23.S1_L1_DIR / 'zip' / f'{S1_base}.zip'

# create ZipFile object
zip_ref = zipfile.ZipFile(zip_path)

# unpack into L1 folder
zip_ref.extractall(FS23.S1_L1_DIR)

# close ZipFile object
zip_ref.close()

# remove zip_path
##zip_path.unlink(missing_ok=True)

# -------------------------------------------------------------------------- #
# -------------------------------------------------------------------------- #

# PROCESS ALL S1 PRODUCTS

# --------------- #

# build full paths to processing scripts from local FS23.WORK_DIR
# full paths are needed for crontab, which runs on default from the home directory

feature_extraction_script = FS23.WORK_DIR / 'S1_extract_features.py'
geocoding_script = FS23.WORK_DIR / 'S1_geocode_features.py'

if not feature_extraction_script.is_file():
    logger.error(f'Could not find feature_extraction_script: {feature_extraction_script}')
else:
    logger.info(f'feature_extraction_script: {feature_extraction_script}')

if not geocoding_script.is_file():
    logger.error(f'Could not find geocoding_script: {geocoding_script}')
else:
    logger.info(f'geocoding_script: {geocoding_script}')

# --------------- #

# define different settings for geocoding

settings = dict()

settings[1] = dict()
##settings[2] = dict()
##settings[3] = dict()
##settings[4] = dict()
##settings[5] = dict()
##settings[6] = dict()
##settings[7] = dict()

settings[1]['ML'] = '1x1'
settings[1]['PS'] = 40
##settings[2]['ML'] = '5x5'
##settings[2]['PS'] = 200
##settings[3]['ML'] = '1x1'
##settings[3]['PS'] = 80
##settings[4]['ML'] = '9x9'
##settings[4]['PS'] = 400
##settings[5]['ML'] = '1x1'
##settings[5]['PS'] = 120
##settings[6]['ML'] = '9x9'
##settings[6]['PS'] = 800
##settings[7]['ML'] = '9x9'
##settings[7]['PS'] = 1200

n_settings = len(settings)

# build geocoded directories for different settings and create folders if needed
for s in np.arange(1,n_settings+1):
    ML_current = settings[s]['ML']
    PS_current = settings[s]['PS']
    settings[s]['dir'] = FS23.S1_GEO_DIR / f"ML_{ML_current}_pixelspacing_{PS_current}"
    settings[s]['dir'].mkdir(parents=True, exist_ok=True)

# --------------- #

logger.info(f'Processing S1 product: {S1_base}')

# loop over all settings
for key in settings.keys():

    # get current multi-looking, pixelspacing, and output_dir
    ML = settings[key]['ML']
    PS = settings[key]['PS']
    output_dir = settings[key]['dir']

    # build path to final output tiff file
    tiff_file = f'{S1_base}_intensities_epsg_3996_pixelspacing_{PS}_ML_{ML}.tiff'
    final_output_path = output_dir / tiff_file

    if final_output_path.is_file() and not overwrite:
        logger.info(f'Product already processed for current settings (ML={ML}, PS={PS})')
    else:
        logger.info(f'Processing product for current settings (ML={ML}, PS={PS})')
        subprocess.call(f"python {feature_extraction_script} {S1_base} -ML {ML}", shell=True)
        subprocess.call(f"python {geocoding_script} {S1_base} -ML {ML} -pixel_spacing {PS}", shell=True)

        # move tiff file to final output folder
        shutil.move((FS23.S1_GEO_DIR/tiff_file).as_posix(), final_output_path.as_posix())

        # remove HH and HV tiff files
        (FS23.S1_GEO_DIR/f'{S1_base}_Sigma0_HH_db_epsg_3996_pixelspacing_{PS}_ML_{ML}.tiff').unlink(missing_ok=True)
        (FS23.S1_GEO_DIR/f'{S1_base}_Sigma0_HV_db_epsg_3996_pixelspacing_{PS}_ML_{ML}.tiff').unlink(missing_ok=True)

# --------------- #

# clean up feature folder
shutil.rmtree(FS23.S1_FEAT_DIR, ignore_errors=True)

# -------------------------------------------------------------------------- #
# -------------------------------------------------------------------------- #

# ---- End of <process_S1_locally.py> ----


