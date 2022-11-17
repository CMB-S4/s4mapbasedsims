NSIDE=4096
#for cfg in cib.toml # ksz.toml tsz.toml radio.toml cmb.toml cmb_unlensed.toml
# for cfg in cmb.toml cmb_unlensed.toml
export PYTHONUNBUFFERED=1
export OMP_PROC_BIND=true
export OMP_PLACES=threads
export OMP_NUM_THREADS=68
export HDF5_USE_FILE_LOCKING=FALSE
for cfg in dust.toml
do
    mapsims_run --verbose --channels='telescope:LAT' --nside=$NSIDE common.toml $cfg
done
