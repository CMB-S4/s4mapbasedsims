for telescope in SPLAT CHLAT
do
    for pol in I Q U
    do
        papermill plot_cl.ipynb out_plot_cl/plot_cl_${telescope}_${pol}.ipynb -p input_telescope $telescope -p pol $pol
    done
done
