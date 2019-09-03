
## NOTE: some local changes were needed to the python package for igor to gte it to load the data!
from igor.packed import load as loadpxp


from datetime import datetime
from dateutil.tz import tzlocal
import os.path
from pprint import pprint
import numpy
import platform
import matplotlib.pyplot as plt
import pynwb

filename = '141117c2.pxp'
filename = '141210c3.pxp'

protocols = {'nm10Dec2014c3_000': 'Control', 'nm10Dec2014c3_002': 'Norepinephrine', 'nm10Dec2014c3_003':'Washout'}
protocol_info = {'nm10Dec2014c3_000': 'Prior to drug application', 'nm10Dec2014c3_002': 'Application of norepinephrine (noradrenaline)', 'nm10Dec2014c3_003':'Following wash out of drug'}

path = os.path.join('./', filename)
records,filesystem = loadpxp(path)


from datetime import datetime
now = datetime.now() # current date and time
date_time = now.strftime("%d %B %Y, %H:%M:%S")
gen_info = 'NWB file generated on %s with pynwb v%s and Python %s' %(date_time, pynwb.__version__,platform.python_version())
print gen_info 

sub = pynwb.file.Subject(
    description='Mouse',
    species='Mus musculus',
)

nwbfile = pynwb.NWBFile('Golgi cell ephys recordings', filename, datetime.now(tzlocal()),
                  experimenter='Frederic Lanore',
                  lab='Silver Lab',
                  institution='University College London',
                  related_publications='Lanore et al. 2019, Norepinephrine controls the gain of the inhibitory circuit in the cerebellar input layer, https://www.biorxiv.org/content/10.1101/567172v1',
                  experiment_description=('Electrophysiological recordings from cerebellar Golgi cells'),
                  session_id=filename.split('.')[0],
                  subject=sub)

def data_info(wdata):
    print('Data %s, shape: %s, %s -> %s (max %s, min %s)'%(type(wdata), wdata.shape, wdata[0], wdata[-1], wdata.max(), wdata.min()))
    
voltages = {}
currents = {}

found = 0
added = {}
added_stim = {}

#pprint(filesystem)

for d in filesystem['root']:
    print('===  IgorPro folder: %s'%d)
    if 'nm10Dec' in str(d):
        for dd in filesystem['root'][d]:
            print('Folder %s/%s'%(d,dd))
            if 'RecordA' in str(dd):
                #print(' >>  %s: %s'%(dd, filesystem['root'][d][dd]))
                
                #TODO: fix hardcoding!!!
                timestamps = numpy.array([s*0.0001 for s in range(10000)])
                
                rec_index = int(dd[7:])
                print('Get equivalent stimulus')
                stim_id = 'uDAC_0_%s'%rec_index
                
                record = filesystem['root'][d]['Step_CC'][stim_id]
                path = '%s/%s/%s/%s'%('root',d,'Step_CC', stim_id)
                wave = record.wave['wave']
                name = wave['wave_header']['bname']
                data = wave['wData']
                print('=========[stim: %s, of %i found]====='%(name,found))
                stim_ampl  = data.min() if data.max()== 0 else data.max()
                data_info(data)
                
                #print('Record %s: %s'%(i,r))
                notes = str(wave['note']).replace('\r','\n')

                folder = d
                if not folder in added_stim:
                    added_stim[folder] = []
                added_stim[folder].append(name)
                if not folder in currents:
                    fig1 = plt.figure(figsize=(12, 6), dpi=80)
                    curr = fig1.add_subplot(111)
                    plt.legend()
                    currents[folder] = curr

                protocol = protocols[folder]
                pi = protocol_info[folder]
                desc = '%s, injected current %snA'%(pi,stim_ampl)
                print desc
                ts_stim = pynwb.TimeSeries('%s_%s'%(protocol,name), 
                              data, 
                              'pA', 
                              timestamps=timestamps, 
                              description=desc,
                              comments='Extracted from IgorPro file: %s; path in file: %s; %s'%(filename, path, gen_info))

                nwbfile.add_stimulus(ts_stim)

                currents[folder].plot(timestamps, wave['wData'], label=desc)
                
                found+=1
                record = filesystem['root'][d][dd]
                
                path = '%s/%s/%s'%('root',d,dd)
                wave = record.wave['wave']
                name = wave['wave_header']['bname']
                print('=========[volts: %s, of %i found]====='%(name,found))

                #print('Record %s: %s'%(i,r))
                notes = str(wave['note']).replace('\r','\n')
                properties = {}
                for p in notes.split('\n'):
                    properties[p.split(':')[0]] = p.split(':')[-1]
               
                print(properties)
                folder = d
                if not folder in added:
                    added[folder] = []
                added[folder].append(name)
                if not folder in voltages:
                    fig2 = plt.figure(figsize=(12, 6), dpi=80)
                    volt = fig2.add_subplot(111)
                    plt.legend()
                    voltages[folder] = volt
        
                data = wave['wData']
                data_info(data)
                #print
                
                data_info(timestamps)
                
                protocol = protocols[folder]
                pi = protocol_info[folder]
                desc = '%s; recorded voltage for %snA'%(pi, stim_ampl)
                print desc
                ts = pynwb.TimeSeries('%s_%s'%(protocol,name), 
                              data, 
                              'mV', 
                              timestamps=timestamps, 
                              description=desc,
                              comments='Extracted from IgorPro file: %s; %s; %s'%(filename, path, gen_info))

                nwbfile.add_acquisition(ts)
                voltages[folder].plot(timestamps,data, label=desc)
            
                
for aa in [added, added_stim]:
    for a in aa:
        print('All added to %s (%i): %s'%(a,len(aa[a]),aa[a]))
        
        
nwb_file_name = '%s.nwb'%filename.split('.')[0]
io = pynwb.NWBHDF5IO(nwb_file_name, mode='w')
io.write(nwbfile)
io.close()
print("Written NWB file to %s"%nwb_file_name)
    
plt.legend()
plt.show()