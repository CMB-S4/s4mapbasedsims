while read ch; do
   papermill -p ch $ch validation_atmo_noise.ipynb validation_notebooks/$ch.ipynb 
done <LAT_chs.txt
