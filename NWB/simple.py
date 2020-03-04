from datetime import datetime

from dateutil.tz import tzlocal
import pynwb
import platform


start_time = datetime.now(tz=tzlocal())
create_date = datetime.now(tz=tzlocal())

import hdmf._version
hdmf_ver = 'v%s'%hdmf._version.get_versions()['version']
info = 'Example NWB file created with pynwb v%s (hdmf %s), Python v%s'%(pynwb.__version__,hdmf_ver,platform.python_version())
nwbfile = pynwb.NWBFile('PyNWB example file', 
                  'NWB123', 
                  start_time,
                  file_create_date=create_date,
                  notes=info)

nwb_file_name='simple_example.nwb'

print('Saving NWB file: %s'%nwbfile)
io = pynwb.NWBHDF5IO(nwb_file_name, mode='w')

print("Written: %s"%info)
io.write(nwbfile)
io.close()
