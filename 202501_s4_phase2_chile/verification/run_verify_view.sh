#!/bin/bash

components=(
    "combined_cmb_lensing_signal"
    "combined_foregrounds_lowcomplexity_norg"
    "combined_cmb_unlensed_dipole"
    "combined_foregrounds_mediumcomplexity_norg"
    "combined_foregrounds_highcomplexity_norg"
)

components=(
    "combined_cmb_lensing_signal"
)

echo "# Visual inspection of maps" >> README.md
echo "" >> README.md

for component in "${components[@]}"
do
        papermill verify_map_view.ipynb verify_map_view_$component.ipynb -p component $component
        #URL=$(gh gist create --public "verify_map_view_$component.ipynb")
        #echo "* [${component}](${URL/gist.github.com/nbviewer.org\/gist})" >> README.md
done