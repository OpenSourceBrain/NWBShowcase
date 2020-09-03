

import platform
import os
import time
import numpy

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


def _h5_info(h5_item, prefix):
    
    if len(h5_item.attrs)>0:
        #print('    %s %s =\t %s'%(prefix if len(prefix)>0 else '(root)', a, h5_item.attrs[a]))
        for k in h5_item.attrs:
            v = h5_item.attrs[k]
            attr_info='%s = \t%s '%(k,v)
            print('        %s'%(attr_info))
            
    for k,v in    h5_item.items():
        #print(dir(v))
        if 'Dataset' in str(type(v)):
            #print(dir(v))
            data = v.dtype
            
            max_len = 80
            data_value = v[()]
            str_data = str(data_value)
            trunc_str_data = '\''+str_data[:max_len]+('...\' (%i chars)'%len(str_data) if len(str_data)>max_len else '\'')
            if type(data_value)==bytes:
                data = 'B: '+trunc_str_data
                '''elif type(data_value)==unicode:
                data = 'U: '+trunc_str_data'''
            elif type(data_value)==str:
                data = trunc_str_data
            elif type(data_value)==numpy.ndarray:
                data = 'ndarray: '+str_data
            else:
                data = '%s (??) = %s'%(type(data_value),str_data)
                
            print('    %s/%s = \t%s'%(prefix, k,data))
            if len(v.attrs)>0:
                #print('    %s %s =\t %s'%(prefix if len(prefix)>0 else '(root)', a, h5_item.attrs[a]))
                for kk in v.attrs:
                    vv = v.attrs[kk]
                    attr_info='%s = \t%s '%(kk,vv)
                    print('        %s'%(attr_info))
            
        elif 'Group' in str(type(v)):
            print('    %s/%s'%(prefix, k))
            _h5_info(v, '%s/%s'%(prefix,k))
        else:
            print('    %s/%s = %s (%s) %s'%(prefix, k,v,type(v),[a for a in v.attrs] if len(v.attrs)>0 else ''))
            
            
def array_info(a, name):
    print('Array %s: len %i, %s->%s, max %s, min %s'%(name, len(a), a[0],a[-1], max(a), min(a)))
    

def print_info(nwb_file, verbose=True):
    
    print('NWB info')
            

    if verbose:
        print('  Info on Python (v%s) packages:'%platform.python_version())

        for m in sorted(['pynwb', 'hdmf', 'nwbwidgets', 'numpy','pandas','scipy','six','hdf5','h5py','pyabf','imageio','pillow','PIL','dateutil','av','tifffile']):
            installed_ver = False
            try:
                exec('import %s'%m)
                installed_ver = 'yes, unknown version'
                try:
                    installed_ver = 'v%s'%eval('%s.__version__'%m)
                except:
                    pass
            except Exception as e:
                installed_ver = 'no'
            print('    %s%s(installed: %s)'%(m, ' '*(20-len(m)), installed_ver))
      
 
    mod = time.ctime(os.path.getmtime(nwb_file))

    if nwb_file is not None: 
        print('\nInfo on %s (%s bytes; modified: %s)'%(nwb_file, os.path.getsize(nwb_file), mod))

        import h5py
        h5py_file = h5py.File(nwb_file, 'r')
        h5py_file
        for a in h5py_file.attrs:
            print('    Attr   %s =\t %s'%(a, h5py_file.attrs[a]))
            
        if nwb_file.endswith('.nwb'):
            general = h5py_file.get('general')
            if general is not None:
                for ff in ['lab','experimenter', 'institution', 'lab', 'notes']:
                    val = '---'
                    if ff in general:
                        v = general.get(ff)
                        val = v[()] if v is not None else '?'
                    print('    Field  %s =\t %s'%(ff, val))
        
        if verbose:
            print('\nHDF5 summary:')
            _h5_info(h5py_file,'')

        print('Successfully read file with h5py v%s\n'%h5py.__version__)
        #exit()
        
        if nwb_file .endswith('.nwb'):
            from pynwb import NWBHDF5IO, __version__
            from pynwb import __version__ as pynwb_version
            #io = NWBHDF5IO(nwb_file, 'r', load_namespaces=True)
            silver_ext = False
            if not silver_ext:
                io = NWBHDF5IO(nwb_file, 'r', load_namespaces=True)
                print('Loaded without explicitly referring to Silverlab extensions')
            else:
                from pynwb import get_class, load_namespaces, NWBHDF5IO

                load_namespaces('/Users/padraig/git/PySilverLabNWB/src/silverlabnwb/silverlab.namespace.yaml')
                get_class('ZplanePockelsDataset', 'silverlab_extended_schema')
                io = NWBHDF5IO(nwb_file, 'r')
                print('Loaded with Silverlab extensions')
                
            nwbfile_in = io.read()
            print('Successfully opened file with pynwb v%s'%pynwb_version)

            a = nwbfile_in

            key_fields = ['name','notes','subject','experimenter']
            for k in key_fields:
                print('    %s = %s'%(k, getattr(nwbfile_in,k)))
            #print(nwbfile_in.fields.keys())
            print('Notes: %s'%nwbfile_in.notes)
            print('Finished looking at file %s'%nwb_file)

            return nwbfile_in

    
def main(args=None):
    """Main"""

    if args is None:
        args = parse_arguments()

    print_info(args.nwb_file, args.verbose)


if __name__ == "__main__":
    main()


