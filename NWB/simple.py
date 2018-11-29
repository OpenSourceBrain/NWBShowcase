from datetime import datetime

from dateutil.tz import tzlocal
from pynwb import NWBFile

start_time = datetime(2018, 4, 3, 11, tzinfo=tzlocal())
create_date = datetime(2018, 4, 15, 12, tzinfo=tzlocal())

nwbfile = NWBFile('PyNWB tutorial', 'NWB123', start_time,
                  file_create_date=create_date)

from pynwb import NWBHDF5IO

io = NWBHDF5IO('simple_example.nwb', mode='w')
io.write(nwbfile)
io.close()
