from os import environ, system, path
from subprocess import call

num_files = 8

all_datarefs = ['180817_ME_9_CC','170502_AL_257_CC', # CC
               '170328_AL_238_VC','170315_AL_216_VC', # VC
               '171220_NC_156_ST100_C','170328_AB_277_ST50_C', # ST
                '171207_NC_146_FN', '171017_KK_13_FN'] # FN


for file_number in range(num_files):

    mat_file = '%s.mat'%all_datarefs[file_number]

    # check if file exists
    if not path.exists(mat_file):

        # Download the appropriate files
        if file_number in [0,1]:
            cmd = 'wget ftp://parrot.genomics.cn/gigadb/pub/10.5524/100001_101000/100535/CurrentClamp/StepProtocol/'+mat_file
        elif file_number in [2,3]:
            cmd = 'wget ftp://parrot.genomics.cn/gigadb/pub/10.5524/100001_101000/100535/VoltageClamp/VCStep/'+mat_file
        elif file_number in [4,5]:
            cmd = 'wget ftp://parrot.genomics.cn/gigadb/pub/10.5524/100001_101000/100535/VoltageClamp/VCSawTooth/%s/'%('100ms' if file_number==4 else '50ms')+mat_file
        else:
            cmd = 'wget ftp://parrot.genomics.cn/gigadb/pub/10.5524/100001_101000/100535/CurrentClamp/FrozenNoise/'+mat_file

        system(cmd)
        print('%s file successfully downloaded...'%mat_file)

    # run code
    environ['file_number'] = '%s'%file_number
    ret = call(['runipy','TestData.ipynb'])
    print('Return value: %s'% ret)
    if ret!=0: exit(ret)
