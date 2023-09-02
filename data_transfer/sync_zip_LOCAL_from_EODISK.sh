# ---- This is <sync_zip_LOCAL_from_EODISK.sh> ----
#
# Synchronize local "geocoded" data folder with corresponding folder on EO_disk
#
# -------------------------------------------------------------------------- #
# -------------------------------------------------------------------------- #

# define REMOTE_SERVER and REMOTE_DATA_DIR
REMOTE_SERVER="rcm2.phys.uit.no"
REMOTE_DATA_DIR="/Data/jlo031/ResearchData/IFT/EarthObservation/belgica_bank/FS23_DATA_TRANSFER/satellite_data/Sentinel-1/L1/zip_files/for_sync"

# define EODISK_DATA_DIR
EODISK_DATA_DIR="/media/jo/EO_disk/data/FS23/satellite_data/Sentinel-1/L1/zip"

# define LOCAL_DATA_DIR
LOCAL_DATA_DIR="/media/Data/FS23/satellite_data/Sentinel-1/L1/zip"


echo " "
echo "Running 'sync_zip_LOCAL_from_EODISK.sh'"
echo "# ------------------------------- #"
echo " "

echo "REMOTE_DATA_DIR: ${REMOTE_DATA_DIR}"
echo "EODISK_DATA_DIR: ${EODISK_DATA_DIR}"
echo "LOCAL_DATA_DIR:  ${LOCAL_DATA_DIR}"
echo " "

echo "RUNNING: rsync -avz ${EODISK_DATA_DIR}/ ${LOCAL_DATA_DIR}"
echo " "
rsync -avz ${EODISK_DATA_DIR}/ ${LOCAL_DATA_DIR}
##rsync -avz --info=progress2 --info=name0 ${sync_from_dir}/ ${sync_to_dir}

# -------------------------------------------------------------------------- #
# -------------------------------------------------------------------------- #

# ---- End of <sync_zip_LOCAL_from_EODISK.sh> ----
