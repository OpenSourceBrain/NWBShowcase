import pynwb

import platform
import os
import time

def parse_arguments():
    """Parse command line arguments"""

    import argparse

    parser = argparse.ArgumentParser(
                                     description=('nwb_info: Infor on NWBv2 files'),
                                     usage=('nwb_info.py [-h|--help] [NWB file]'),
                                     formatter_class=argparse.RawTextHelpFormatter
                                     )

    shared_options = parser.add_argument_group(
                                               title='Shared options',
                                               description=('These options can be added to any of the '
                                               'mutually-exclusive options')
                                               )

    parser.add_argument(
                                '-verbose',
                                action='store_true',
                                default=False,
                                help='Verbose output'
                                )
    
    
            
    parser.add_argument('nwb_file',
                                type=str,
                                metavar='<NWB 2 file>',
                                help='NWB 2 file to process'
                                )
            

    return parser.parse_args()

def print_info(args):
    
    print('NWB info')
            
    print('  Info on Python (v%s) packages:'%platform.python_version())

    for m in ['pynwb', 'hdmf','numpy','pandas','scipy','six','h5py','pyabf']:
        installed_ver = False
        try:
            exec('import %s'%m)
            if m == 'hdmf':
                import hdmf._version
                installed_ver = 'v%s'%hdmf._version.get_versions()['version']
            else:
                installed_ver = 'v%s'%eval('%s.__version__'%m)
        except Exception as e:
            installed_ver = '???'
        print('    %s%s(installed: %s)'%(m, ' '*(20-len(m)), installed_ver))
      
 
    mod = time.ctime(os.path.getmtime(args.nwb_file))
 
    print('  Info on %s (%s bytes; modified: %s)'%(args.nwb_file, os.path.getsize(args.nwb_file), mod))
    
    from pynwb import NWBHDF5IO
    io = NWBHDF5IO(args.nwb_file, 'r')
    nwbfile_in = io.read()
    
    a = nwbfile_in
    #print(dir(a))
    #for s in dir(a):
    #    print('-- %s '%(s))
        
    key_fields = ['name','notes','subject']
    for k in key_fields:
        print('    %s = %s'%(k, getattr(nwbfile_in,k)))
        
    #print(nwbfile_in.fields.keys())
    #print(nwbfile_in.general)
    print('Finished looking at file %s'%args.nwb_file)

    
def main(args=None):
    """Main"""

    if args is None:
        args = parse_arguments()

    print_info(args)


if __name__ == "__main__":
    main()


