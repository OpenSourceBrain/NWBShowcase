

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

    for m in sorted(['pynwb', 'hdmf','numpy','pandas','scipy','six','hdf5','h5py','pyabf','imageio','pillow','PIL','dateutil','av','tifffile']):
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

    if args is not None: 
        print('\nInfo on %s (%s bytes; modified: %s)'%(args.nwb_file, os.path.getsize(args.nwb_file), mod))

        import h5py
        h5py_file = h5py.File(args.nwb_file, 'r')
        h5py_file
        for a in h5py_file.attrs:
            print('    Attr   %s =\t %s'%(a, h5py_file.attrs[a]))
            
        general = h5py_file.get('general')
        for ff in ['lab','experimenter', 'institution', 'lab', 'notes']:
            print('    Field  %s =\t %s'%(ff, general.get(ff)[()] if ff in general else '---'))

        print('Successfully read file with h5py v%s\n'%h5py.__version__)
        #exit()
        try:
            from pynwb import NWBHDF5IO, __version__
            from pynwb import __version__ as pynwb_version
            io = NWBHDF5IO(args.nwb_file, 'r')
            nwbfile_in = io.read()
            print('Successfully opened file with pynwb v%s'%pynwb_version)

            a = nwbfile_in

            key_fields = ['name','notes','subject']
            for k in key_fields:
                print('    %s = %s'%(k, getattr(nwbfile_in,k)))
            #print(nwbfile_in.fields.keys())
            print('Notes: %s'%nwbfile_in.notes)
            print('Finished looking at file %s'%args.nwb_file)

            return nwbfile_in
        except Exception as e:
            print('Error loading via pynwb!')
            print(e)

    
def main(args=None):
    """Main"""

    if args is None:
        args = parse_arguments()

    print_info(args)


if __name__ == "__main__":
    main()


