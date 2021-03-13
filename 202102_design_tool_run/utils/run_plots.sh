nsplits=1
while read ch; do
   papermill -p ch $ch -p nsplits $nsplits verification_atmo_noise.ipynb ../verification_notebooks/${ch}_${nsplits}.ipynb 
done <LAT_chs.txt
