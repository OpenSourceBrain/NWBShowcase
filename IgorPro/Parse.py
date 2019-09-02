
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


found = 0
added = {}
added_stim = {}
'''
for i,r in enumerate(records):

    #print('=========[%s]====='%i)
    name = r.wave['wave']['wave_header']['bname'] if hasattr(r,'wave') else '???'
   
    if 'RecordA9' in name:
        found+=1
        print('=========[%s (%s) of %i found]====='%(i,name,found))
        
        
'''
pprint(filesystem)

for d in filesystem['root']:
    print('===  IgorPro folder: %s'%d)
    if 'nm10Dec' in d:
        for dd in filesystem['root'][d]:
            print('Folder %s/%s'%(d,dd))
            if 'RecordA' in dd:
                #print(' >>  %s: %s'%(dd, filesystem['root'][d][dd]))
                found+=1
                record = filesystem['root'][d][dd]
                wave = record.wave['wave']
                name = wave['wave_header']['bname']
                print('=========[%s, of %i found]====='%(name,found))

                #print('Record %s: %s'%(i,r))
                notes = wave['note'].replace('\r','\n')
                properties = {}
                for p in notes.split('\n'):
                    properties[p.split(':')[0]] = p.split(':')[-1]
               
                print properties
                folder = d
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
                '''
                print '-----------  %s ------'%name
                print wave
                #print '..........'
                print notes
                '''
                data_info(wave['wData'])
                print

                voltages[folder].plot(wave['wData'])
                
            if 'Step_CC' in dd:
                for ddd in filesystem['root'][d][dd]:
                    print(' - Folder %s/%s/%s'%(d,dd,ddd))
                    if 'uDAC_0' in ddd:
                        
                        print(' >>  %s/%s/%s: %s'%(d,dd,ddd, filesystem['root'][d][dd][ddd]))
                        
                        record = filesystem['root'][d][dd][ddd]
                        wave = record.wave['wave']
                        name = wave['wave_header']['bname']

                        #print('Record %s: %s'%(i,r))
                        notes = wave['note'].replace('\r','\n')
                        
                        folder = d
                        if not folder in added_stim:
                            added_stim[folder] = []
                        added_stim[folder].append(name)
                        if not folder in currents:
                            fig1 = plt.figure(figsize=(12, 6), dpi=80)
                            curr = fig1.add_subplot(111)
                            currents[folder] = curr

                        data_info(wave['wData'])
                        print

                        currents[folder].plot(wave['wData'])
                
for aa in [added, added_stim]:
    for a in aa:
        print('All added to %s (%i): %s'%(a,len(aa[a]),aa[a]))
    
plt.show()