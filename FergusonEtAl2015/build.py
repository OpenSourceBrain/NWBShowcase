from datetime import datetime, tzinfo, timedelta
import hdmf._version
from dateutil.tz import tzlocal
import platform
import math
import numpy as np
import uuid

import pyabf
import pynwb
print('Using pynwb v%s'%pynwb.__version__)

from pynwb.icephys import CurrentClampStimulusSeries, CurrentClampSeries

# greek unicode
ohm = '\u03A9'
micro = '\u03BC'

# for McGill Uni in Montreal, Quebec
class TZ(tzinfo):
    def utcoffset(self, dt):
        return -timedelta(hours=4)
    def dst(self, dt):
        return timedelta(0)
    def tzname(self,dt):
        return "-04:00"
    def  __repr__(self):
        return f"{self.__class__.__name__}()"


#### Global variables ####

# random UUID for globally unique tag
unique_identifier = uuid.uuid4()

all_files = ['PYR1.abf','PYR2.abf','PYR3.abf','PYR4.abf','PYR5_rebound.abf']

cells = ['Pyramidal cell 1, strongly adapting',
         'Pyramidal cell 2, strongly adapting',
         'Pyramidal cell 3, weakly adapting',
         'Pyramidal cell 4, weakly adapting',
         'Pyramidal cell 5, rebound firing']

current_steps = [10.,25.,10.,10.,-25.] # pA
initial_currents = [-2.7,-48.8,2.0,-48.1,0.0] # pA                               ## based on approximate rheobase current at (https://www.zenodo.org/record/17794#.Xu-yR8JlBhF)


hdmf_ver = 'v%s'%hdmf._version.get_versions()['version']

notes = ('NWB2 file with ephys created with pynwb v%s (HDMF %s) '
         'and Python %s')%(pynwb.__version__,hdmf_ver,platform.python_version())

stim_notes = ('Depolarizing current steps, aCSF perfusion rate of 20-25 '
            'ml/min, temperature 30+/- 2 celsius')


#### File-dependent variables ####

# Iterate over each cell, current step size, and files
for cell, current_step, initial_current, f in zip(cells,current_steps,initial_currents,all_files):

    abf = pyabf.ABF(f) # read data set

    print("--- Loaded file: %s"%abf)
    reference = f.split('.')[0]

    ###################################
    #### Date and time information ####
    ###################################

    date, time = abf.abfDateTimeString.split('T')

    date = date.split('-')
    time = time.split(':')

    year, month, day = int(date[0]), int(date[1]), int(date[2])
    hour, minute = int(time[0]), int(time[1])
    sec = int(time[2].split('.')[0])

    start_time = datetime(year,month,day,hour,minute,sec,tzinfo=TZ())
    create_date = datetime.now(tz=tzlocal())
    reference_time = abf.abfDateTime


    #############################
    #### Subject information ####
    #############################

    # subject-related elements
    subject = pynwb.file.Subject(
        species='transgenic mouse',
        genotype='PV-tdTomato',
        sex='Unspecified', # unspecified in publication                          ## Publication says 3 mice with 2 females, but cells are not explicit
        age='P20D-P90D'                                                          ## ISO 8601 Duration format
    )

    ##############################
    #### Instantiate NWB file ####
    ##############################

    protocol = abf.protocol

    nwbfile = pynwb.NWBFile(
                 session_description='Ferguson et al. %s'%f,
                 identifier=str(unique_identifier),                              ## "identifier" should be a globally unique value, UUID recommended, no need for human-readible
                 session_start_time=start_time,
                 file_create_date=create_date,
                 notes=notes,
                 experimenter='Katie A. Ferguson',
                 experiment_description=('Data set of CA1 pyramidal cell '
                                        'recordings using an intact whole '
                                        'hippocampus preparation, including '
                                        'recordings of rebound firing'),
                 institution='University of Toronto',
                 lab='Skinner Lab',

                # subject-related field
                subject=subject,                                                 ## See subject class above

                # recording-related fields
                protocol=protocol,
                stimulus_notes=stim_notes,
                pharmacology=('synaptic blockers: 5 %sM '
                            '6,7-dinitroquinoxaline-2,3-dione disodium '
                            'salt(DNQX), 5 %sM  bicuculline, and 25 %sM '
                            'DL-2-amino-5-phosphonopentanoic acid '
                            'sodium salt (DL-AP5) '
                            '(Abcam, Toronto, Canada)')%(micro,micro,micro),
                keywords=['pyramidal cells','neuroscience','patch clamps']
        )

    #############################################
    #### Intracellular electrode information ####
    #############################################

    # device metadata
    device = nwbfile.create_device(name='device',
                                   description=('Axopatch-1C amplifier (Axon '
                                                'Instruments) and '
                                                'pClamp9 software'),
                                   manufacturer=('Molecular Devices, '
                                                'Sunnyvale, CA'))

    slice_prep = '~45 degree cut from surface'
    location = ('pyramidal cell layer, middle portion of hippocampus '
            '(intermediate between septal and temporal poles of preparation)')


    electrode = nwbfile.create_icephys_electrode(name='icephys_electrode',       ## Give preference to default processing module names.
                                description=('Patch pipettes pulled from '
                                            'borosilicate glass capillaries '
                                            '(2.5-4 M%s)')%ohm,
                                slice=slice_prep,
                                location=location,
                                device=device,
    )

    ####################################
    #### Specific sweep information ####
    ####################################

    max_sweeps = abf.sweepCount
    for sweep in range(max_sweeps):

        #######################
        #### Clamp current ####
        #######################

        abf.setSweep(sweep, channel=0) # sweeps start at 0

        # add clamp current data
        data = abf.sweepY
        sampling_rate = 1000.*abf.dataPointsPerMs # kHz->Hz                      ## If sampling rate is constant, use rate instead of timestamps
        # timestamps = abf.sweepX                                                ## In addition, timestamps don't represent absolute time with inter-stimulus interval times

        # unit = abf.adcUnits[channel] # not used
        conversion = 1e-12 # pA->A

        inj_current = (sweep + 1.) * current_step + initial_current
        description = ('Sweep %i, applied current'
                        '(pulse ~%s pA%s)')%(sweep,inj_current,
                                            '' if not 'PYR5_rebound' in f
                                            else ', cell held at -52mV')

        gain = 1. # Unspecified placeholder                                      ## Assumed unity gain amplifier

        csss = CurrentClampStimulusSeries(
                         name='CurrentClampStimulusSeries_%i'%sweep,             ## As a default, name class instances with the same name as the class
                         description=description,
                         stimulus_description=protocol + ' protocol',
                         sweep_number=sweep,

                         data=data,
                         rate=sampling_rate,
                         unit='amperes',
                         conversion=conversion,

                         electrode=electrode,
                         gain=gain,

                         comments='Extracted from ABF file: %s'%f
        )


        ##########################
        #### Voltage response ####
        ##########################

        abf.setSweep(sweep, channel=1) # sweeps start at 0

        # add voltage data
        data = abf.sweepY
        sampling_rate = 1000.*abf.dataPointsPerMs # ms->S                        ## If sampling rate is constant, use rate instead of timestamps
        # timestamps = abf.sweepX                                                ## In addition, timestamps don't represent absolute time with inter-stimulus interval times

        # unit = abf.adcUnits[channel] # Not used
        conversion = 1e-3 # mV->V

        inj_current = (sweep + 1.) * current_step + initial_current
        description = ('Sweep %i, membrane potential response '
                        '(To pulse ~%s pA%s)')%(sweep,inj_current,
                                            '' if not 'PYR5_rebound' in f
                                            else ', cell held at -52mV')

        gain = 1.                                                                ## Assumed unity gain amplifier

        css = CurrentClampSeries(
                         name='CurrentClampSeries_%i'%sweep,                     ## As a default, name class instances with the same name as the class
                         description=description,
                         stimulus_description=protocol + ' protocol',
                         sweep_number=sweep,

                         data=data,
                         rate=sampling_rate,
                         unit='volts',
                         conversion=conversion,

                         electrode=electrode,
                         gain=gain,

                         comments=('Estimated junction potential: -15.2 mV,'
                                    'Extracted from ABF file: %s')%f,
        )

        #########################
        #### Update NWB file ####
        #########################

        nwbfile.add_stimulus(csss)
        nwbfile.add_acquisition(css)

    #######################
    #### Save NWB file ####
    #######################

    nwb_file_name = 'FergusonEtAl2015%s.nwb'%('' if 'PYR1' in f
                                                else '_%s'%reference)
    io = pynwb.NWBHDF5IO(nwb_file_name, mode='w')
    io.write(nwbfile,cache_spec=True)
    io.close()
    print("Written NWB file to %s"%nwb_file_name)
