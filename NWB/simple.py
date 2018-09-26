from datetime import datetime
from pynwb import NWBFile

start_time = datetime(2018, 4, 3, 11, 0, 0)
create_date = datetime(2018, 4, 15, 12, 0, 0)

nwbfile = NWBFile('PyNWB tutorial', 'demonstrate NWBFile basics', 'NWB123', start_time,
                  file_create_date=create_date)

from pynwb import NWBHDF5IO

io = NWBHDF5IO('simple_example.nwb', mode='w')
io.write(nwbfile)
io.close()
