# Helper Files
The helper files are required for running Python jobs on the University of Liverpool's HTCondor network. They are used for extracting Python distributions, mananagine input/output files and running the Python program on the target machine.

Helper suffixes
```
No suffix | No indexed input or output files transferred along with the job
_o        | Indexed output files to be transferred when the job finishes running
_i        | Indexed input files to be transferred when the job starts running
_io       | Both indexed input and output files to be transferred
```

**Note:** Helper files prefixed with `conda` will extract a packaged Conda environment before running the Python file. You can find more information about packaging Conda environments [here](https://conda.github.io/conda-pack/).