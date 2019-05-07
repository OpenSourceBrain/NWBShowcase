from datetime import datetime

from dateutil.tz import tzlocal
import pynwb
import math

start_time = datetime(2019, 1, 1, 11, tzinfo=tzlocal())
create_date = datetime.now(tz=tzlocal())

nwbfile = pynwb.NWBFile('Example time series data', 
                  'TSD', 
                  start_time,
                  file_create_date=create_date,
                  notes='Example NWB file created with pynwb v%s'%pynwb.__version__,
                  experimenter='Padraig Gleeson',
                  experiment_description='Add example data',
                  institution='UCL',
                  )
                  
timestamps = [i/1000.0 for i in range(2000)]
data = [math.sin(t/0.05) for t in timestamps]

test_ts = pynwb.TimeSeries('test_sine_timeseries', data, 'SIunit', timestamps=timestamps)

nwbfile.add_acquisition(test_ts)

nwb_file_name = 'time_series_data.nwb'
io = pynwb.NWBHDF5IO(nwb_file_name, mode='w')
io.write(nwbfile)
io.close()
print("Written NWB file to %s using pynwb v%s"%(nwb_file_name,pynwb.__version__))
