from datetime import datetime

import numpy as np
import pynwb
from dateutil.tz import tzlocal

from pynwb import NWBHDF5IO
from pynwb.device import Device
from pynwb.image import ImageSeries
import platform

def create_nwb_file():
    '''
    acquisition.test_sine_1
    acquisition.test_sine_2
    :return:
    '''
    start_time = datetime.now(tz=tzlocal())
    create_date = datetime.now(tz=tzlocal())

    import hdmf
    hdmf_ver = 'v%s'%hdmf.__version__
    info = 'An example NWB file created with pynwb v%s (hdmf %s), Python v%s'%(pynwb.__version__,hdmf_ver,platform.python_version())
    
    # FIXME: this attr breaks nwb-explorer
    # date_of_birth=create_date 
    sub = pynwb.file.Subject(
        age='33.',
        description='Synthetic data: %s'%info,
        genotype='AA.',
        sex='F.',
        species='Homo Sapiens.',
        subject_id='HM-AA-875362791629.',
        weight='233lb.'
    )

    nwbfile = pynwb.NWBFile('Some data for testing NWB Explorer - some sine waves and images',
                            'TSD123',
                            start_time,
                            file_create_date=create_date,
                            notes=info,
                            experimenter='Norman Woodford Bailey II',
                            experiment_description='We used a Python script to synthetize this data.',
                            institution='Institute AACDDSAQ',
                            session_id='NR-22232',
                            keywords=['behavioural', 'EEG'],
                            pharmacology='No anesthesia or painkillers were used during this session.',
                            protocol='IACUC protocol.',
                            related_publications='Pending DOI confirmation.',
                            slices='No slices created.',
                            source_script='create_nwb_file',
                            source_script_file_name='generate_timeseries_data.py',
                            data_collection='Numpy was use for data generation.',
                            surgery='No surgery was performed.',
                            virus='No virus was used.',
                            stimulus_notes='No stimulus',
                            lab='AADS-UUSKD Lab.',
                            subject=sub)

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
    timestamps = np.arange(N, dtype=np.float64) 

    ts1 = pynwb.TimeSeries(name='test_sine_1', 
                        data=np.sin(timestamps/4),
                        timestamps=timestamps,
                        unit='mV',
                        comments='Just a sine wave...',
                        description='Description of this sine wave.')

    ts2 = pynwb.TimeSeries(name='test_sine_2', 
                        data=np.cos(timestamps/4),
                        unit='pA',
                        timestamps=timestamps,
                        comments='Just another sine wave....',
                        description='Another description of this TimeSeries dataset.',
                        )
    
    nwbfile.add_acquisition(ts1)
    nwbfile.add_acquisition(ts2)

    nwbfile.add_acquisition(create_image('test_image_1', nwbfile))
    
    
    print("Written: %s"%info)

    return nwbfile


def create_image(name, nwbfile):
    import imageio.v2 as imageio
    n = 82
    base_url = "https://raw.githubusercontent.com/OpenSourceBrain/NWBShowcase/master/NWB/images/"
    base_url = "images/"
    
    images_url = [base_url + 'MyNetwork_T' + str(i) + '.png' for i in range(n)]  

    images = np.array([imageio.imread(url) for url in images_url])
    
    ## Fake timestamping to overcome py2 travis
    # timestamp = datetime.now().timestamp()
    timestamp = 1563907835.857213
    timestamps = np.arange(n) + timestamp

    return ImageSeries(name='test_image_series',
                               external_file=images_url,
                               timestamps=timestamps,
                               starting_frame=np.zeros(n, dtype=int), 
                               format='external', 
                               description='Series of images from a simulation of the cerebellum via neuroConstruct')


with NWBHDF5IO('time_series_data.nwb', 'w') as io:
    io.write(create_nwb_file())