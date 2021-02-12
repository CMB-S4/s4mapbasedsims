NSIDE=4096
export OMP_NUM_THREADS=32
for cfg in *$NSIDE*.toml cmb*.toml cib.toml ksz.toml tsz.toml
do
    mapsims_run --channels='telescope:LAT' --nside=$NSIDE common.toml $cfg
done
