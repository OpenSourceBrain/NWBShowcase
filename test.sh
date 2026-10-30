#!/bin/bash
set -ex

cd NWB
python simple.py
python nwb_info.py simple_example.nwb

python time_series_data.py
python nwb_info.py time_series_data.nwb

python datatypes.py
python nwb_info.py datatypes.nwb
ls -alt
