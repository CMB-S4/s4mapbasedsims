while read ch; do
   papermill -p ch $ch -p nsplits 7 validation_atmo_noise.ipynb validation_notebooks/$ch.ipynb 
done <all_chs.txt
