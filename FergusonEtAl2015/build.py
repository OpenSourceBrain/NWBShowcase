import pyabf
from datetime import datetime


from dateutil.tz import tzlocal
import pynwb
print('Using pynwb v%s'%pynwb.__version__)
import math


all_files = ['PYR1.abf','PYR2.abf','PYR3.abf','PYR4.abf','PYR5_rebound.abf']

for f in all_files:
    abf = pyabf.ABF(f) # read one data set

    print("--- Loaded file: %s"%abf)
    reference = f.split('.')[0]

    start_time = datetime(2019, 1, 1, 11, tzinfo=tzlocal())
    create_date = datetime.now(tz=tzlocal())

    nwbfile = pynwb.NWBFile('Ferguson et al. %s'%f, 
                      'Ferguson et al. %s'%f, 
                      start_time,
                      file_create_date=create_date,
                      notes='Ephys created with pynwb v%s'%pynwb.__version__,
                      experimenter='Katie A. Ferguson',
                      experiment_description='Data set of CA1 pyramidal cell recordings using an intact whole hippocampus preparation, including recordings of rebound firing',
                      institution='University of Toronto')

    maxi = abf.sweepCount
    for i in range(maxi):
        abf.setSweep(i, channel=1) # sweeps start at 0
        timestamps = abf.sweepX
        data = abf.sweepY

        ts = pynwb.TimeSeries('Sweep_%i'%i, 
                              data, 
                              'mV', 
                              timestamps=timestamps, 
                              description='Sweep %i, membrane potential'%i,
                              comments='Extracted from ABF file: %s'%f)

        nwbfile.add_acquisition(ts)

        abf.setSweep(i, channel=0) # sweeps start at 0
        timestamps = abf.sweepX
        data = abf.sweepY
        in_current = i * (10.0 if reference in ['PYR1','PYR3','PYR4'] else 25.0)
        if reference == 'PYR5_rebound':
            in_current = 25.0 - i * (25.0)
        ts_stim = pynwb.TimeSeries('Sweep_%i'%i, 
                                   data, 
                                   'pA', 
                                   timestamps=timestamps, 
                                   description='Sweep %i, applied current (pulse ~%spA)'%(i,in_current),
                                   comments='Extracted from ABF file: %s'%f)

        nwbfile.add_stimulus(ts_stim)

    nwb_file_name = 'FergusonEtAl2015%s.nwb'%('' if 'PYR1' in f else '_%s'%reference)
    io = pynwb.NWBHDF5IO(nwb_file_name, mode='w')
    io.write(nwbfile)
    io.close()
    print("Written NWB file to %s"%nwb_file_name)