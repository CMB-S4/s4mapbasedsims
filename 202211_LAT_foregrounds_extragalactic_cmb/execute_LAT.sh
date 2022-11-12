NSIDE=4096
export OMP_NUM_THREADS=68
#for cfg in cib.toml # ksz.toml tsz.toml radio.toml cmb.toml cmb_unlensed.toml
# for cfg in cmb.toml cmb_unlensed.toml
export PYTHONUNBUFFERED=1
for cfg in ame.toml freefree.toml
do
    mapsims_run --verbose --channels='telescope:LAT' --nside=$NSIDE common.toml $cfg
done
