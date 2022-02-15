#!/usr/bin/env python3

import os
import subprocess

flist = os.listdir()
xyzs = [f for f in flist if '.log' in f]

for x in xyzs:
    print(f'XYZ {x}\n\n\n')
    if 'Pentadecane' in x:
        qminstr_pent = f"qmin {x} --opt --freq -c 0 -t M062X -b 6-311+G* -d --norass --solvate Pentadecane"
        subprocess.call(qminstr_pent, shell=True)

    elif 'water' in x:
        qminstr_wat = f"qmin {x} --opt --freq -c 0 -t M062X -b 6-311+G* -d --norass --solvate water"
        subprocess.call(qminstr_wat,shell=True)

    else:
        qminstr_vac = f"qmin {x} --opt --freq -c 0 -t M062X -b 6-311+G* -d --norass"
        subprocess.call(qminstr_vac, shell=True)

print('done')
print('\n\nSUBMITTING\n\n')
subprocess.call('mrjsub',shell=True)
print('\n\nDONE\n\n')
    

