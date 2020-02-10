from datetime import datetime

from dateutil.tz import tzlocal
import pynwb

start_time = datetime(2018, 4, 3, 11, tzinfo=tzlocal())
create_date = datetime(2018, 4, 15, 12, tzinfo=tzlocal())

import hdmf._version
hdmf_ver = 'v%s'%hdmf._version.get_versions()['version']
info = 'Example NWB file created with pynwb v%s (hdmf %s)'%(pynwb.__version__,hdmf_ver)
nwbfile = pynwb.NWBFile('PyNWB tutorial', 
                  'NWB123', 
                  start_time,
                  file_create_date=create_date,
                  notes=info)

nwb_file_name='simple_example.nwb'
io = pynwb.NWBHDF5IO(nwb_file_name, mode='w')

print("Written: %s"%info)
io.write(nwbfile)
io.close()
