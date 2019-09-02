
import os.path
from igor.packed import load as loadpxp
from pprint import pprint

filename = '141117c2.pxp'
filename = '141210c3.pxp'


path = os.path.join('./', filename)
records,filesystem = loadpxp(path)


import matplotlib.pyplot as plt

def data_info(wdata):
    print('Data %s, shape: %s, %s -> %s (max %s, min %s)'%(type(wdata), wdata.shape, wdata[0], wdata[-1], wdata.max(), wdata.min()))
    
voltages = {}
currents = {}

fig1 = plt.figure(figsize=(12, 6), dpi=80)
curr = fig1.add_subplot(111)
fig2 = plt.figure(figsize=(12, 6), dpi=80)
volt = fig2.add_subplot(111)

found = 0
added = {}

for i,r in enumerate(records):

    #print('=========[%s]====='%i)
    name = r.wave['wave']['wave_header']['bname'] if hasattr(r,'wave') else '???'
   
    if 'RecordA9' in name:
        found+=1
        print('=========[%s (%s) of %i found]====='%(i,name,found))
        
        #print('Record %s: %s'%(i,r))
        notes = r.wave['wave']['note'].replace('\r','\n')
        properties = {}
        for p in notes.split('\n'):
            properties[p.split(':')[0]] = p.split(':')[-1]
        print(r.header)
        print(dir(r))
        print properties
        folder = properties['Folder'] if 'Folder' in properties else 'F???'
        if not folder in added:
            added[folder] = []
        added[folder].append(name)
        if not folder in voltages:
            fig1 = plt.figure(figsize=(12, 6), dpi=80)
            curr = fig1.add_subplot(111)
            currents[folder] = curr
            fig2 = plt.figure(figsize=(12, 6), dpi=80)
            volt = fig2.add_subplot(111)
            voltages[folder] = volt

        print '-----------  %s ------'%r.wave['wave']['wave_header']['bname']
        print r.wave['wave']
        #print '..........'
        print notes
        data_info(r.wave['wave']['wData'])
        print
        
        voltages[folder].plot(r.wave['wave']['wData'])
        
print('All added: %s'%added)
#plt.show()

pprint(filesystem)