#---- This is <fs23_folder_structure.py> ----

"""
Folder configuration for FS23 cruise work
""" 

import pathlib
import socket

# -------------------------------------------------------------------------- #
# -------------------------------------------------------------------------- #

# This is the work dir (one level up from config) of the project

WORK_DIR = pathlib.Path(__file__).parent.parent

# -------------------------------------------------------------------------- #
# -------------------------------------------------------------------------- #

# This is the main project data folder
# Everything else is based off of this
# The main folder is set depending on the platform you are working on

if socket.gethostname() == 'rcm1.phys.uit.no':
    DATA_DIR = pathlib.Path('/Data/jlo031/ResearchData/IFT/EarthObservation/belgica_bank/FS23_DATA_TRANSFER')
elif socket.gethostname() == 'rcm2.phys.uit.no':
    DATA_DIR = pathlib.Path('/Data/jlo031/ResearchData/IFT/EarthObservation/belgica_bank/FS23_DATA_TRANSFER')
elif socket.gethostname() == 'gizmo' or socket.gethostname() == 'sully':
    DATA_DIR = pathlib.Path('/media/Data/FS23')

# This directory is for usage on rcm2 server
SCRATCH_DIR = pathlib.Path('/scratch/jlo031/FS23/')

# -------------------------------------------------------------------------- #

# Base folders for satellite data

SAT_DATA_DIR = DATA_DIR / 'satellite_data'

S1_DIR  = SAT_DATA_DIR / 'Sentinel-1'
S2_DIR  = SAT_DATA_DIR / 'Sentinel-2'
S3_DIR  = SAT_DATA_DIR / 'Sentinel-3'

RS2_DIR = SAT_DATA_DIR / 'Radarsat-2'
RCM_DIR = SAT_DATA_DIR / 'Radarsat_Constellation_Mission'

# -------------------------------------------------------------------------- #

# Folders for S1 processing
S1_L1_DIR     = S1_DIR / 'L1'
S1_FEAT_DIR   = S1_DIR / 'features'
S1_RESULT_DIR = S1_DIR / 'classification_results'
S1_RGB_DIR    = S1_DIR / 'RGB'
S1_GEO_DIR    = S1_DIR / 'geocoded'

##S1_GEO_ORBIT_DIR = S1_GEO_DIR / 'orbits'
##S1_GEO_AOI_DIR   = S1_GEO_DIR / 'AOIs'

# -------------------------------------------------------------------------- #

# Folders on /scratch for batch processing

if socket.gethostname() == 'rcm1.phys.uit.no':
    S1_FEAT_DIR = SCRATCH_DIR / 'Sentinel-1/features'
    S1_RGB_DIR  = SCRATCH_DIR / 'Sentinel-1/RGB'

    S1_FEAT_DIR.mkdir(parents=True, exist_ok=True)
    S1_RGB_DIR.mkdir(parents=True, exist_ok=True)


if socket.gethostname() == 'rcm2.phys.uit.no':
    S1_FEAT_DIR = SCRATCH_DIR / 'Sentinel-1/features'
    S1_RGB_DIR  = SCRATCH_DIR / 'Sentinel-1/RGB'

    S1_FEAT_DIR.mkdir(parents=True, exist_ok=True)
    S1_RGB_DIR.mkdir(parents=True, exist_ok=True)

# -------------------------------------------------------------------------- #
# -------------------------------------------------------------------------- #

# FIGURES

FIG_DIR = DATA_DIR / 'figures'

S1_FIG_DIR = FIG_DIR / 'Sentinel-1'

S1_IMG_FIG_DIR = S1_FIG_DIR / 'images'
S1_AOI_FIG_DIR = S1_FIG_DIR / 'AOIs'

# -------------------------------------------------------------------------- #
# -------------------------------------------------------------------------- #

# check and create directories

# build and create necessary folders
S1_DIR.mkdir(parents=True, exist_ok=True)
S2_DIR.mkdir(parents=True, exist_ok=True)
S3_DIR.mkdir(parents=True, exist_ok=True)

RS2_DIR.mkdir(parents=True, exist_ok=True)
RCM_DIR.mkdir(parents=True, exist_ok=True)

S1_L1_DIR.mkdir(parents=True, exist_ok=True)
S1_FEAT_DIR.mkdir(parents=True, exist_ok=True)
S1_RESULT_DIR.mkdir(parents=True, exist_ok=True)
S1_RGB_DIR.mkdir(parents=True, exist_ok=True)
S1_GEO_DIR.mkdir(parents=True, exist_ok=True)

##S1_GEO_ORBIT_DIR.mkdir(parents=True, exist_ok=True)
##S1_GEO_AOI_DIR.mkdir(parents=True, exist_ok=True)

FIG_DIR.mkdir(parents=True, exist_ok=True)
S1_FIG_DIR.mkdir(parents=True, exist_ok=True)
S1_IMG_FIG_DIR.mkdir(parents=True, exist_ok=True)
S1_AOI_FIG_DIR.mkdir(parents=True, exist_ok=True)

# -------------------------------------------------------------------------- #
# -------------------------------------------------------------------------- #

osm_landmask = DATA_DIR / 'osm_shapefiles' / 'land-polygons-split-4326' / 'land_polygons.shp'

# -------------------------------------------------------------------------- #
# -------------------------------------------------------------------------- #

# ---- End of <fs23_folder_structure.py> ----
