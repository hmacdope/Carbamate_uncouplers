#!/usr/bin/env python3

import os
import subprocess

flist = os.listdir()
xyzs = [f for f in flist if '.xyz' in f]

for x in xyzs:
    print(f'XYZ {x}\n\n\n')
    qminstr_vac = f"qmin {x} --opt --freq -c 0 -t M062X -b 6-311+G* -d --norass --calcfc"
    subprocess.call(qminstr_vac, shell=True)
    qminstr_wat = f"qmin {x} --opt --freq -c 0 -t M062X -b 6-311+G* -d --norass --solvate water --calcfc"
    subprocess.call(qminstr_wat,shell=True)
    qminstr_pent = f"qmin {x} --opt --freq -c 0 -t M062X -b 6-311+G* -d --norass --solvate Pentadecane --calcfc"
    subprocess.call(qminstr_pent, shell=True)
    print('done')
print('\n\nSUBMITTING\n\n')
subprocess.call('mrjsub -time 48h -mem 20gb',shell=True)
print('\n\nDONE\n\n')
    

