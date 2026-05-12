Directory for the Arctic PFAS simulation whose outputs will be used in PINN bias correction.

**data/** holds original source files (ERA5 forcing, LLC270 grid, etc.). Nothing here is modified or tracked by git.

**experiment/** contains the run directory — everything needed to run the simulation once transferred to HPC. Experiments that I wish to save will be in a parent directory.

**input_gen/** contains scripts that transform files in data/ into MITgcm-ready inputs, deposited here and manually copied into experiment/. The manual transfer step prevents accidental overwrites.
