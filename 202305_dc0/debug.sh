#for cfg in cib.toml # ksz.toml tsz.toml radio.toml cmb.toml cmb_unlensed.toml
# for cfg in cmb.toml cmb_unlensed.toml
export PYTHONUNBUFFERED=1
#export OMP_PROC_BIND=true
#export OMP_PLACES=threads
#export OMP_NUM_THREADS=68
#export HDF5_USE_FILE_LOCKING=FALSE
cfg=ame_a1.toml
ipython --pdb -- $(which mapsims_run) --verbose --channels='SAT_f030' common.toml $cfg
