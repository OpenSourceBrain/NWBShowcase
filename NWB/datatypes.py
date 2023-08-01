from datetime import datetime

import numpy as np
import pynwb
import math
from dateutil.tz import tzlocal

from pynwb import NWBHDF5IO
from pynwb.device import Device
from pynwb.image import ImageSeries
import platform

def _info(a):
    print('%i points: [%s, %s, ..., %s]; max %s, min %s'%(len(a), a[0], a[1], a[-1], a.max(), a.min()))

def create_nwb_file():
    
    start_time = datetime.now(tz=tzlocal())
    create_date = datetime.now(tz=tzlocal())

    import hdmf._version
    hdmf_ver = 'v%s'%hdmf.__version__
    info = 'An example NWB file created with pynwb v%s (hdmf %s), Python v%s'%(pynwb.__version__,hdmf_ver,platform.python_version())
    
    nwbfile = pynwb.NWBFile('Example with various datatypes - primarily for testing NWB Widgets',
                            'Datatypes',
                            start_time,
                            file_create_date=create_date,
                            notes=info,
                            experimenter='Norman Woodford Bailey II',
                            experiment_description='We used a python script to synthetize this data.',
                            institution='Institute X',
                            lab='No Lab.')

    # Device
    device = nwbfile.create_device(name='Tetrode')

    # Electrode Group
    electrode_group = nwbfile.create_electrode_group(name='Tetrode',
                                                 description='Tetrode group',
                                                 location='CA1',
                                                 device=device)
    # Add Electrodes
    for idx in range(1, 5):
        nwbfile.add_electrode(x=1.0, y=2.0, z=3.0,
                          imp=float(-idx),
                          location='CA1', 
                          filtering='Description of hardware filtering.',
                          group=electrode_group)
    # Electrode table
    electrode_table_region = nwbfile.create_electrode_table_region([0, 2], 'The first and third electrodes.')

    N = 2001
    timestamps = np.arange(N, dtype=np.float64) 
    
    s_timestamps = 1.0 + np.arange(N)*0.001
    _info(s_timestamps)
    ms_timestamps = s_timestamps*1000
    _info(ms_timestamps)
    
    mvolts = 50.*np.sin(s_timestamps*10)-20
    _info(mvolts)
    volts=mvolts*0.001
    _info(volts)
    
    ts1 = pynwb.TimeSeries(name='test_volt_s_sine', 
                        data=volts,
                        timestamps=s_timestamps,
                        unit='V',
                        comments='Just a sine wave (V/s)...',
                        description='Description of this sine wave.')

    nwbfile.add_acquisition(ts1)
    
    ts2 = pynwb.TimeSeries(name='test_mvolt_s_sine', 
                        data=mvolts,
                        timestamps=s_timestamps,
                        unit='mV',
                        comments='Just a sine wave (mV/s)...',
                        description='Description of this sine wave.')

    nwbfile.add_acquisition(ts2)
    
    ts3 = pynwb.TimeSeries(name='test_mvolt_s_conversion_sine', 
                        data=volts,
                        timestamps=s_timestamps,
                        conversion=1000.0,
                        unit='mV',
                        comments='Just a sine wave (mV/s + conversion)...',
                        description='Description of this sine wave.')

    nwbfile.add_acquisition(ts3)
    
    
    
    ts4 = pynwb.TimeSeries(name='test_volt_s_rate_sine', 
                        data=volts,
                        starting_time = s_timestamps[0],
                        rate = 1/(s_timestamps[1]-s_timestamps[0]),
                        unit='V',
                        comments='Just a sine wave (V/s)...',
                        description='Description of this sine wave.')

    nwbfile.add_acquisition(ts4)
    
    ts4 = pynwb.TimeSeries(name='test_mvolt_s_rate_sine', 
                        data=mvolts,
                        starting_time = s_timestamps[0],
                        rate = 1/(s_timestamps[1]-s_timestamps[0]),
                        unit='mV',
                        comments='Just a sine wave (mV/s)...',
                        description='Description of this sine wave.')

    nwbfile.add_acquisition(ts4)
    
    
    ss1 = pynwb.behavior.SpatialSeries(name='spatial_series_1D', 
                        reference_frame='Zero is origin..?',
                        data=np.cos(timestamps/4.),
                        timestamps=timestamps,
                        comments='A wave...',
                        description='Description of this...')

    nwbfile.add_acquisition(ss1)
    
    x = np.cos(timestamps/4.)
    y = np.sin(timestamps/5.)
    ss2 = pynwb.behavior.SpatialSeries(name='spatial_series_2D', 
                        reference_frame='Zero is origin..?',
                        data=np.array([x,y]).T,
                        timestamps=timestamps,
                        comments='A wave...',
                        description='Description of this...')
    
    
    pos1 = pynwb.behavior.Position(spatial_series=ss2, name='Tracked 2D position')
    
    nwbfile.add_acquisition(pos1)
    
    print("Written: %s"%info)

    return nwbfile


with NWBHDF5IO('datatypes.nwb', 'w') as io:
    io.write(create_nwb_file())