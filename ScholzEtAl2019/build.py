from os import environ, system, path
from subprocess import call
import h5py
import numpy as np

# only files labeled "moving" on OSF
all_filenames = ['AML18_moving.hdf5', 'AML175_moving.hdf5', 'AML32_moving.hdf5']
num_files = len(all_filenames)

for file_number in range(num_files):
    
    filename = all_filenames[file_number]
    
    # check if file exists
    if not path.exists(filename):
        
        if '18' in filename:
            cmd = 'wget https://osf.io/5298q/download -O AML18_moving.hdf5'
        elif '175' in filename:
            cmd = 'wget https://osf.io/sgnrh/download -O AML175_moving.hdf5'
        elif '32' in filename:
            cmd = 'wget https://osf.io/jn9a7/download -O AML32_moving.hdf5'
        else:
            raise Exception('%s is not supported by this conversion script.')
    

        system(cmd)
        
        
    # load file here to iterate over experiments in file
    celegans_h5 = h5py.File(filename, 'r')

    # get experiments
    experiments  = np.array(celegans_h5['/'])
    num_experiments = len(experiments)

    # some datasets have multiple experiments
    for experiment_number in range(num_experiments):
        print('\n------------------> Converting %s for %s <-----------------\n '%(experiments[experiment_number],filename))

        # run code
        environ['file_number'] = '%s'%file_number
        environ['filename'] = filename
        environ['experiment_number'] = '%s'%experiment_number
        environ['experiment'] = experiments[experiment_number]

        call(['runipy','TestData.ipynb'])
