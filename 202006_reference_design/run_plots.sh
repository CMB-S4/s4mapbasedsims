nsplits=7
while read ch; do
   papermill -p ch $ch -p nsplits $nsplits validation_atmo_noise_dec_2020.ipynb validation_notebooks/${ch}_${nsplits}.ipynb 
done <SAT_chile_chs.txt
