# OpenYAFF
[![build Actions Status](https://github.com/svandenhaute/openyaff/workflows/Python%20Application/badge.svg)](https://github.com/svandenhaute/openyaff/actions)
[![codecov](https://codecov.io/gh/svandenhaute/openyaff/branch/main/graph/badge.svg?token=SS8G6Q890J)](https://codecov.io/gh/svandenhaute/openyaff)


OpenYAFF is a conversion and validation tool that generates [OpenMM](openmm.org) "System" instances based on [YAFF](https://github.com/molmod/yaff) force fields.


1)
Install in the correct conda environment!

To install OpenYAFF use:

"pip install git+https://github.com/beschmid/openyaff.git"

and install OpenMM with

"pip install OpenMM"


2)
To run OpenYAFF use:

"openyaff initialize system.file.chk pars.file.txt"

Check the config.yml file -- yaff part

To get the topology.pdb file run:

"openyaff --pdb save system.file.chk config.yml pars.file.txt"

To get the system.xml run:

"openyaff convert config.yml system.file.chk pars.file.txt"

To check the validity of the generated files run:

"openyaff validate config.yml system.file.chk pars.file.txt"
