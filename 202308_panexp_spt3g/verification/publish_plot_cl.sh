for pol in T E B
do
    URL=$(gh gist create --public "plot_cl_${pol}.ipynb")
    echo "* [${pol}${pol}](${URL/gist.github.com/nbviewer.org\/gist})" >> README.md
done
