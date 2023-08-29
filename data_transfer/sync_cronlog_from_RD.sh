# ---- This is <sync_cronlog_from_rcm2.sh> ----
#
# Synchronize cronlog from rcm2 server
#
# -------------------------------------------------------------------------- #
# -------------------------------------------------------------------------- #

# define REMOTE_SERVER and REMOTE_DIR
REMOTE_SERVER="rcm2.phys.uit.no"
REMOTE_DIR="/home/jlo031"

# define LOCAL_DIR
LOCAL_DIR="/home/jo/work/FS23/data_transfer"

# define LOGFILE
LOGFILE="cron_FS23_workflow.log"

echo " "
echo "Running 'sync_cronlog_from_rcm2.sh'"
echo "# ------------------------------- #"
echo " "

echo "REMOTE_DIR: ${REMOTE_DIR}"
echo "LOCAL_DIR:  ${LOCAL_DIR}"
echo " "

echo "RUNNING: rsync -avz jlo031@${REMOTE_SERVER}:${REMOTE_DIR}/${LOGFILE} ${LOCAL_DIR}/${LOGFILE}"
echo " "
rsync -avz jlo031@${REMOTE_SERVER}:${REMOTE_DIR}/${LOGFILE} ${LOCAL_DIR}/${LOGFILE}

# -------------------------------------------------------------------------- #
# -------------------------------------------------------------------------- #

# ---- End of <sync_cronlog_from_rcm2.py> ----
