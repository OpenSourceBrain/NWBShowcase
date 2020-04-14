# NWB Showcase

Open Source Brain Showcase project containing examples of [Neurodata Without Borders (NWB)](https://www.nwb.org/) data. OSB is developing the infrastructure to visualise and analyse experimental data which has been shared publicly in NWB format.

This repository will contain **some example datasets** which we will convert to NWB to test this functionality. 

The target format will be NWB v2.0 and we intend to make use of [PyNWB](https://github.com/NeurodataWithoutBorders/pynwb) for reading/writing the NWB files.

## Simple scripts to generate NWB using PyNWB

[This script](https://github.com/OpenSourceBrain/NWBShowcase/blob/master/NWB/simple.py) illustrates a minimal Python script necessary to generate [a valid NWB file](https://github.com/OpenSourceBrain/NWBShowcase/blob/master/NWB/simple_example.nwb).

To run this, [install PyNWB](https://pynwb.readthedocs.io/en/stable/getting_started.html#installation) and run:

    python simple.py

It will produce a file [simple_example.nwb](https://github.com/OpenSourceBrain/NWBShowcase/blob/master/NWB/simple_example.nwb) in HDF5 format. To view the contents of this file (or any file in HDF5) you can use [HDFView](https://portal.hdfgroup.org/display/HDFVIEW/HDFView).
 
However, this NWB file doesn't have any real data in it yet. The script [time_series_data.py](https://github.com/OpenSourceBrain/NWBShowcase/blob/master/NWB/time_series_data.py) will add some simple time series traces (sine waves) and a set of images to the NWB file to provide some example data

    python time_series_data.py

The [generated file](https://github.com/OpenSourceBrain/NWBShowcase/blob/master/NWB/time_series_data.nwb) can be loaded into [HDFView](https://portal.hdfgroup.org/display/HDFVIEW/HDFView) and the structure of groups/datasets for NWB explored. Navigating to **/acquisition/test_sine_1/data**, opening the dataset, and then generating a Line Plot from it results in:

<img src="images/time_series_hdfview.png" width=300/>

Other information located in the NWB file about the experiment (e.g. at **/general/experimenter**) can also be viewed.



[![Build Status](https://travis-ci.org/OpenSourceBrain/NWBShowcase.svg?branch=master)](https://travis-ci.org/OpenSourceBrain/NWBShowcase)

