#! /usr/bin/env python3

headerhelp = \
''' 
    Parses an EPU micrograph
'''

from argparse import ArgumentParser, RawDescriptionHelpFormatter
parser = ArgumentParser(formatter_class=RawDescriptionHelpFormatter,
                        description=headerhelp)
parser.add_argument('mrcbig', help='Raw MRC file')
parser.add_argument('mrcsmall', help='EPU integrated MRC files')
args = parser.parse_args()


import mrcfile

with mrcfile.open(args.mrcsmall) as mrc:
    if len(mrc.extended_header):
        exthead = dict([[mrc.extended_header.dtype.names[i],str(mrc.extended_header[0][i])] for i in range(len(mrc.extended_header.dtype.names))])
    else:
        exthead = None

with mrcfile.open(args.mrcbig) as mrc:
    bh = mrc.header

print("Number of frames:      %d" % bh.nz)
if exthead:
    print("Pixel sizes (Å):       %.3f %.3f" % (float(exthead['Pixel size X'])*1e10, float(exthead['Pixel size Y'])*1e10))
    print("HT voltage (kV):       %.1f"      % (float(exthead['HT'])/1000))
    print("Total dose (e/Å²):     %.3f"      % (float(exthead['Dose'])*1e-20))
    print("Magnification          %dx"       % (float(exthead['Magnification'])))
    print("Exposure time (s):     %.1f"      % (float(exthead['Integration time'])))
    print("Dose per frame (e/Å²): %.3f"      % (float(exthead['Dose'])*1e-20/bh.nz))
else:
    print("No extended header found")
