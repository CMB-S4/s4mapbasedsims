NSIDE=512
for cfg in *$NSIDE*.toml cmb*.toml cib.toml ksz.toml tsz.toml
do
    mapsims_run --nside=$NSIDE common.toml $cfg
done
