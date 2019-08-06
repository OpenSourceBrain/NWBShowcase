from datetime import datetime

from dateutil.tz import tzlocal
import pynwb
import math

start_time = datetime(2019, 1, 1, 11, tzinfo=tzlocal())
create_date = datetime.now(tz=tzlocal())

dataset = 'zf_20151104-f1' 

coords_file = 'data/%s/%s_cell_coordinates.csv'%(dataset,dataset)

cell_data = {}

activity_file = 'data/%s/%s_activity_matrix.csv'%(dataset,dataset)


with open(activity_file) as f:
    cell_index = 1
    
    
    for l in f.readlines():
        entries = l.split(',')
        cell_data[cell_index] = []
        #print('Found %i entries for cell %i'%(len(entries),cell_index))
        for c in entries:
            cell_data[cell_index].append(float(c))
        cell_index+=1



nwbfile = pynwb.NWBFile('Triplett et al. 2018', 
                  'TSD', 
                  start_time,
                  file_create_date=create_date,
                  notes='Calcium imaging file created with pynwb v%s'%pynwb.__version__,
                  experimenter='Marcus Triplett',
                  experiment_description='Calcium imaging of spontaneous activity in larval zebrafish tectum',
                  institution='University of Queensland')

for i in range(len(cell_data)):
    cell_id = i+1
    #print('Adding cell data %i'%cell_id)
    data = cell_data[cell_id]
    
    # TODO: Not correct units!!!
    timestamps = [t for t in range(len(data))]

    ts = pynwb.TimeSeries('Sweep_%i'%cell_id, data, 'SIunit', timestamps=timestamps)

    nwbfile.add_acquisition(ts)
    


nwb_file_name = 'TriplettEtAl2018.nwb'
io = pynwb.NWBHDF5IO(nwb_file_name, mode='w')
io.write(nwbfile)
io.close()