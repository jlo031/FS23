# ---- This is <S1_extract_features.py> ----

"""
Extract features from Sentinel-1 input image
""" 

import argparse
import os
import sys
import pathlib
from loguru import logger

import S1_processing.S1_feature_extraction as S1_feat
import geocoding.landmask as landmask

import config.fs23_folder_structure as FS23

# -------------------------------------------------------------------------- #
# -------------------------------------------------------------------------- #

p = argparse.ArgumentParser(
    formatter_class=argparse.RawDescriptionHelpFormatter,
    description=__doc__
)
p.add_argument(
    'S1_base',
    help='S1 image basename'
)
p.add_argument(
    '-ML',
    default='1x1',
    help = 'multilook window size (default=1x1)'
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
p.add_argument(
    '-get_rgb',
    action='store_true',
    help='extract RGB image'
)
p.add_argument(
    '-get_swath_mask',
    action='store_true',
    help='get swath_mask'
)
p.add_argument(
    '-get_IA',
    action='store_true',
    help='get IA'
)
p.add_argument(
    '-get_lat_lon',
    action='store_true',
    help='get lat/lon'
)
p.add_argument(
    '-get_landmask',
    action='store_true',
    help='get landmask'
)
args = p.parse_args()

# remove default logger handler and add personal one
logger.remove()
logger.add(sys.stderr, level=args.loglevel)

# -------------------------------------------------------------------------- #
# -------------------------------------------------------------------------- #

S1_base    = args.S1_base
ML         = args.ML
overwrite  = args.overwrite
loglevel   = args.loglevel

get_rgb        = args.get_rgb
get_swath_mask = args.get_swath_mask
get_IA         = args.get_IA
get_lat_lon    = args.get_lat_lon
get_landmask   = args.get_landmask

# -------------------------------------------------------------------------- #
# -------------------------------------------------------------------------- #

logger.info(f'Processing input image: {S1_base}')

S1_safe_folder = FS23.S1_L1_DIR / f'{S1_base}.SAFE'

if not S1_safe_folder.is_dir():
    logger.error(f"Could not find S1 SAFE folder at '{S1_safe_folder}'")

S1_feat_folder = FS23.S1_FEAT_DIR / f'ML_{ML}' / S1_base
S1_rgb_folder  = FS23.S1_RGB_DIR / f'ML_{ML}'

logger.debug(f'S1_safe_folder: {S1_safe_folder}')
logger.debug(f'S1_feat_folder: {S1_feat_folder}')
logger.debug(f'S1_rgb_folder:  {S1_rgb_folder}')

# -------------------------------------------------------------------------- #
# -------------------------------------------------------------------------- #

# extract both intensities (linear and dB):

for intensity in ['HH', 'HV']:

    # intensity in linear domain
    if get_rgb:
        S1_feat.get_S1_intensity(
            S1_safe_folder,
            S1_feat_folder,
            intensity,
            ML = ML,
            loglevel = loglevel,
            overwrite = overwrite
        )

    # intensity in linear domain
    S1_feat.get_S1_intensity(
        S1_safe_folder,
        S1_feat_folder,
        intensity,
        ML = ML,
        dB = True,
        loglevel = loglevel,
        overwrite = overwrite
    )

# -------------------------------------------------------------------------- #

# extract S1 meta data (swath mask, IA, lat/lon):

# swath mask
if get_swath_mask:
    S1_feat.get_S1_swath_mask(
        S1_safe_folder,
        S1_feat_folder,
        loglevel = loglevel,
        overwrite = overwrite
    )

# incident angle
if get_IA:
    S1_feat.get_S1_IA(
        S1_safe_folder,
        S1_feat_folder,
        loglevel = loglevel,
        overwrite = overwrite
    )

# lat/lon bands
if get_lat_lon:
    S1_feat.get_S1_lat_lon(
        S1_safe_folder,
        S1_feat_folder,
        loglevel = loglevel,
        overwrite = overwrite
    )

# -------------------------------------------------------------------------- #
# -------------------------------------------------------------------------- #

# make false-color RGB image
# reads the files 'Sigma0_HH.img' and 'Sigma0_HV.img' from feat_folder
# performs the dB conversions and scaling
# assigns red (HV), green (HH), and blue (HH) channels and stacks 3 bands
# writes to 8bit RGB tif
# parameters for scaling (min/max) and colors (rgb) can be adjusted

if get_rgb:
    S1_feat.make_S1_rgb(
        S1_feat_folder,
        S1_rgb_folder,
        loglevel = loglevel,
        overwrite = overwrite
    )

# -------------------------------------------------------------------------- #
# -------------------------------------------------------------------------- #

# extract a landmask
if get_landmask:
    landmask.convert_osm_landmask_2_SAR_geometry(
        S1_feat_folder / 'lat.img',
        S1_feat_folder / 'lon.img',
        FS23.osm_landmask,
        S1_feat_folder / 'landmask.img',
        tie_points = 21,
        overwrite = overwrite,
        loglevel = loglevel
    )

# -------------------------------------------------------------------------- #
# -------------------------------------------------------------------------- #

# ---- End of <S1_extract_features.py> ----
