for pol in T E B
do
    papermill --prepare-only plot_cl.ipynb plot_cl_${pol}.ipynb -p pol $pol
done
