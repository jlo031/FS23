# ---- This is <sync_LOCAL_from_EODISK.sh> ----
#
# Synchronize local "geocoded" data folder with corresponding folder on EO_disk
#
# -------------------------------------------------------------------------- #
# -------------------------------------------------------------------------- #

# define REMOTE_SERVER and REMOTE_DATA_DIR
REMOTE_SERVER="rcm2.phys.uit.no"
REMOTE_DATA_DIR="/Data/jlo031/ResearchData/IFT/EarthObservation/belgica_bank/FS23_DATA_TRANSFER/satellite_data/Sentinel-1/geocoded"

# define EODISK_DATA_DIR
EODISK_DATA_DIR="/media/jo/EO_disk/data/FS23/satellite_data/Sentinel-1/geocoded"

# define LOCAL_DATA_DIR
LOCAL_DATA_DIR="/media/Data/FS23/satellite_data/Sentinel-1/geocoded"

# settings
ML='1x1'
PS='80'

# specify settings
SETTINGS_DIR="ML_${ML}_pixepspacing_${PS}"

echo " "
echo "Running 'sync_LOCAL_from_EODISK.sh'"
echo "# ------------------------------- #"
echo " "

echo "REMOTE_DATA_DIR: ${REMOTE_DATA_DIR}"
echo "EODISK_DATA_DIR: ${EODISK_DATA_DIR}"
echo "LOCAL_DATA_DIR:  ${LOCAL_DATA_DIR}"
echo " "


# build full directories for current settings
sync_from_dir="${EODISK_DATA_DIR}/ML_${ML}_pixelspacing_${PS}"
sync_to_dir="${LOCAL_DATA_DIR}/ML_${ML}_pixelspacing_${PS}"

echo "sync_from_dir: ${sync_from_dir}"
echo "sync_to_dir: ${sync_to_dir}"
echo " "

echo "RUNNING: rsync -avz ${sync_from_dir}/ ${sync_to_dir}"
echo " "
rsync -avz ${sync_from_dir}/ ${sync_to_dir}
##rsync -avz --info=progress2 --info=name0 ${sync_from_dir}/ ${sync_to_dir}

# -------------------------------------------------------------------------- #
# -------------------------------------------------------------------------- #

# ---- End of <sync_LOCAL_from_EODISK.sh> ----
