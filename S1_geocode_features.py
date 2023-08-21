# ---- This is <S1_geocode_features.py> ----

"""
Geocode features from Sentinel-1 input image
""" 

import argparse
import os
import sys
import pathlib
from loguru import logger

import geocoding.generic_geocoding as gen_geocoding
import geocoding.S1_geocoding as S1_geo

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
    '-pixel_spacing',
    default=40,
    help = 'output pixel spacing (default=40)'
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

S1_base       = args.S1_base
ML            = args.ML
pixel_spacing = args.pixel_spacing
overwrite     = args.overwrite
loglevel      = args.loglevel

# -------------------------------------------------------------------------- #
# -------------------------------------------------------------------------- #

logger.info(f'Processing input image: {S1_base}')

S1_safe_folder = FS23.S1_L1_DIR / f'{S1_base}.SAFE'

if not S1_safe_folder.is_dir():
    logger.error(f"Could not find S1 SAFE folder at '{S1_safe_folder}'")

S1_feat_folder = FS23.S1_FEAT_DIR / f'ML_{ML}' / S1_base
S1_rgb_folder  = FS23.S1_RGB_DIR / f'ML_{ML}'
S1_geo_folder  = FS23.S1_GEO_DIR

logger.debug(f'S1_safe_folder: {S1_safe_folder}')
logger.debug(f'S1_feat_folder: {S1_feat_folder}')
logger.debug(f'S1_rgb_folder:  {S1_rgb_folder}')
logger.debug(f'S1_geo_folder:  {S1_geo_folder}')

# -------------------------------------------------------------------------- #
# -------------------------------------------------------------------------- #

# set some fixed parameters

target_epsg   = 3996
tie_points    = 21
srcnodata     = 0
dstnodata     = 0
order         = 3
resampling    = 'near'
keep_gcp_file = False

method = 'SAFE'
#method = 'lat_lon'

# -------------------------------------------------------------------------- #
# -------------------------------------------------------------------------- #

# geocode features in feature_list

feature_list = [
    'Sigma0_HH_db',
    'Sigma0_HV_db',
    #'IA',
    #'landmask',
]


for feature in feature_list:

    logger.info(f'Processing feature: {feature}')

    img_path         = S1_feat_folder / f'{feature}.img'
    output_tiff_path = S1_geo_folder / f'{S1_base}_{feature}_epsg_{target_epsg}_pixelspacing_{pixel_spacing}_ML_{ML}.tiff'

    if method == 'lat_lon':

        lat_path = S1_feat_folder / 'lat.img'
        lon_path = S1_feat_folder / 'lon.img'

        gen_geocoding.geocode_image_from_lat_lon(
            img_path,
            lat_path,
            lon_path,
            output_tiff_path,
            target_epsg,
            pixel_spacing,
            tie_points = tie_points,
            srcnodata = srcnodata,
            dstnodata = dstnodata,
            order = order,
            resampling = resampling,
            keep_gcp_file = keep_gcp_file,
            overwrite = overwrite,
            loglevel = loglevel
        )

    elif method == 'SAFE':

        S1_geo.geocode_S1_image_from_safe_gcps(
            img_path,
            S1_safe_folder,
            output_tiff_path,
            target_epsg,
            pixel_spacing,
            srcnodata = srcnodata,
            dstnodata = dstnodata,
            order = order,
            resampling = resampling,
            keep_gcp_file = keep_gcp_file,
            overwrite = overwrite,
            loglevel = loglevel
        )


# stack HH and HV bands (for false-color RGB in QGIS)
gen_geocoding.geo_utils.stack_geocoded_images(
    S1_geo_folder / f'{S1_base}_Sigma0_HH_db_epsg_{target_epsg}_pixelspacing_{pixel_spacing}_ML_{ML}.tiff',
    S1_geo_folder / f'{S1_base}_Sigma0_HV_db_epsg_{target_epsg}_pixelspacing_{pixel_spacing}_ML_{ML}.tiff',
    S1_geo_folder / f'{S1_base}_intensities_epsg_{target_epsg}_pixelspacing_{pixel_spacing}_ML_{ML}.tiff',
    overwrite = overwrite,
    loglevel = loglevel
)

# -------------------------------------------------------------------------- #
# -------------------------------------------------------------------------- #

# ---- End of <S1_geocode_features.py> ----
