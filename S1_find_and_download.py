# ---- This is <S1_find_and_download.py> ----

"""
Extract features from Sentinel-1 input image
""" 

import argparse
import os
import sys
import pathlib
from loguru import logger

import satsearch_and_download.sentinel_download as sd

import config.fs23_folder_structure as FS23

# -------------------------------------------------------------------------- #
# -------------------------------------------------------------------------- #

p = argparse.ArgumentParser(
    formatter_class=argparse.RawDescriptionHelpFormatter,
    description=__doc__
)
p.add_argument(
    'area',
    help='path to geojson file defining the area of interest'
)
p.add_argument(
    'starttime',
    help="sensing start time 'YYYY-MM-DD HH:MM'"
)
p.add_argument(
    'endtime',
    help="sensing end time 'YYYY-MM-DD HH:MM'"
)
p.add_argument(
    '-overwrite',
    action='store_true',
    help='overwrite existing files'
)
p.add_argument(
    '-loglevel',
     choices = ["CRITICAL", "ERROR", "WARNING", "INFO", "DEBUG"],
     default = 'INFO',
     help = 'loglevel setting (default=INFO)',
)
args = p.parse_args()

# remove default logger handler and add personal one
logger.remove()
logger.add(sys.stderr, level=args.loglevel)

# -------------------------------------------------------------------------- #
# -------------------------------------------------------------------------- #

starttime    = args.starttime
endtime      = args.endtime
area         = args.area
overwrite    = args.overwrite
loglevel     = args.loglevel

# -------------------------------------------------------------------------- #
# -------------------------------------------------------------------------- #

download_dir = FS23.S1_L1_DIR

sd.search_and_download_products_from_scihub(
    'S1',
    area,
    starttime,
    endtime,
    download_dir,
    area_relation = 'Intersects',
    scihub_username = 'JLohse',
    scihub_password = 'dummy_password',
    loglevel = loglevel,
    overwrite = overwrite
)

# -------------------------------------------------------------------------- #
# -------------------------------------------------------------------------- #

# ---- End of <S1_find_and_download.py> ----
