from datetime import datetime

from dateutil.tz import tzlocal
import pynwb

start_time = datetime(2018, 4, 3, 11, tzinfo=tzlocal())
create_date = datetime(2018, 4, 15, 12, tzinfo=tzlocal())

nwbfile = pynwb.NWBFile('PyNWB tutorial', 
                  'NWB123', 
                  start_time,
                  file_create_date=create_date,
                  notes='Example NWB file created with pynwb v%s'%pynwb.__version__)

io = pynwb.NWBHDF5IO('simple_example.nwb', mode='w')
io.write(nwbfile)
io.close()
