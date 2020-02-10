import pynwb


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
    for m in ['pynwb', 'hdmf','numpy','pandas','scipy']:
        installed_ver = False
        try:
            exec('import %s'%m)
            installed_ver = 'v%s'%eval('%s.__version__'%m)
        except:
            pass
        print('  %s%s(installed: %s)'%(m, ' '*(20-len(m)), installed_ver))
                

    
def main(args=None):
    """Main"""

    if args is None:
        args = parse_arguments()

    print_info(args)


if __name__ == "__main__":
    main()


