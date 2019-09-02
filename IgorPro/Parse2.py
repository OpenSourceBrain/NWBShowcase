
import os.path
from pprint import pformat, pprint
from igor.binarywave import load as loadibw
from igor.packed import load as loadpxp
from igor.packed import walk as _walk
from igor.record.base import TextRecord
from igor.record.folder import FolderStartRecord, FolderEndRecord
from igor.record.variables import VariablesRecord
from igor.record.wave import WaveRecord

import glob

import matplotlib
import matplotlib.pyplot as plt
    
fig1 = plt.figure(figsize=(12, 6), dpi=80)
curr = fig1.add_subplot(111)
fig2 = plt.figure(figsize=(12, 6), dpi=80)
volt = fig2.add_subplot(111)

filename = 'B95_Ch0_IDRest_107.ibw'

for filename in glob.glob("B95*.ibw"):

    data = loadibw(filename)
    pprint(data)

    print data['version']
    print data['wave']['wData']

    if 'Ch0' in filename:
        curr.plot(data['wave']['wData'])
    if 'Ch3' in filename:
        volt.plot(data['wave']['wData'])

plt.show()


