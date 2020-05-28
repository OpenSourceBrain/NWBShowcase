from datetime import datetime

import numpy as np
import pynwb
from dateutil.tz import tzlocal

from pynwb import NWBHDF5IO
from pynwb.device import Device
from pynwb.image import ImageSeries
import platform

def create_nwb_file():
    
    start_time = datetime.now(tz=tzlocal())
    create_date = datetime.now(tz=tzlocal())

    import hdmf._version
    hdmf_ver = 'v%s'%hdmf._version.get_versions()['version']
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

    N = 100
    timestamps = np.arange(N) 

    ts1 = pynwb.TimeSeries(name='test_sine_1', 
                        data=np.sin(timestamps/4),
                        timestamps=timestamps,
                        unit='mV',
                        comments='Just a sine wave...',
                        description='Description of this sine wave.')

    nwbfile.add_acquisition(ts1)
    
    ss1 = pynwb.behavior.SpatialSeries(name='spatial_series_1D', 
                        reference_frame='Zero is origin..?',
                        data=np.cos(timestamps/4),
                        timestamps=timestamps,
                        comments='A wave...',
                        description='Description of this...')

    nwbfile.add_acquisition(ss1)
    
    x = np.cos(timestamps/4)
    y = np.sin(timestamps/5)
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