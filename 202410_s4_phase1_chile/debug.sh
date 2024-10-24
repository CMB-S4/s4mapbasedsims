export PYTHONUNBUFFERED=1
export OMP_NUM_THREADS=48
cfg=ame_a1.toml
cfg=cib_cib1.toml
ch=SAT_f220
ch=CHLAT_f020
ipython --pdb -- $(which mapsims_run) --verbose --channels=$ch common.toml $cfg
