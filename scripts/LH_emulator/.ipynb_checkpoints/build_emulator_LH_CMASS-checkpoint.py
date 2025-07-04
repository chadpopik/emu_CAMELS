import sys
sys.path.append('/home/jovyan/home/emu_CAMELS/scripts/1P_emulator/')
sys.path.append('/home/jovyan/home/src/ostrich')
sys.path.append('/home/jovyan/home/src/pality')

import numpy as np
import helper_functions_LH as fs


home='/home/jovyan/home/emu_CAMELS/emulator_profiles'
suite='IllustrisTNG' 
suiteset='LH'
prof='rho_mean'
func_str='linear'

samples,x,y,emulator=fs.build_emulator_CMASS(home,suite,suiteset,prof,func_str)


om=0.3
s8=0.8
asn1=0.5
agn1=1.2
asn2=0.7
agn2=1.5
z=0.53761
M=12.25
params=[[om,s8,asn1,agn1,asn2,agn2,z,M]]
emulated=emulator(params)
print(np.shape(emulated))
