#!/usr/bin/env python3

import os
import subprocess
import argparse

parser = argparse.ArgumentParser(description='G3SETUP')
parser.add_argument('-i', dest='x', action='store', type=str, required=True,
                    help='input file ')

args = parser.parse_args()

x = args.x

xpref = x.split('.')[0]
xmp2low = xpref + '.MP2_6-31pGd.com'
xmp2high = xpref + '.MP2_GTMP2LARGE.com'
xccsdt = xpref + '.CCSD-T_6-31pGd.in'

qminstr_vac = f"qmin {x} -c 0 -m 1 -p qchem -t CCSD-T -b 6-31+G*"
subprocess.call(qminstr_vac, shell=True)
qminstr_wat = f"qmin {x} -c 0 -m 1 -t MP2 -b 6-31+G*"
subprocess.call(qminstr_wat,shell=True)
qminstr_pent = f"qmin {x} -c 0  -m 1 -t MP2 -b GTMP2LARGE"
subprocess.call(qminstr_pent, shell=True)
print('done')
print('\n\nSUBMITTING\n\n')
subprocess.call(f'rjsub {xmp2low} -time 24h ', shell=True)
subprocess.call(f'rjsub {xmp2high} -time 24h ', shell=True)
subprocess.call(f'pysub {xccsdt} -vmem 64000 -jobfs 500000 -walltime 96 -subdir Partial_Uncouplers_CCSDTs ', shell=True)
print('\n\nDONE\n\n')
    

