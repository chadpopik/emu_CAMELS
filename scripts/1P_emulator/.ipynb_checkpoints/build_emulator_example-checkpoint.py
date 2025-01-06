import helper_functions_1P as fs

home='/home/jovyan/home/emu_CAMELS/emulator_profiles/1P_set/' #point to your profiles
suite='SIMBA'
vary_str='ASN1'
prof='rho_mean' #rho_mean,rho_med,pth_mean,pth_med
func_str='linear' #this is the Rbf interpolation function

mass=fs.mass
mass_str=fs.mass_str
snap=fs.snap
z=fs.choose_redshift(suite)
vary,sims=fs.choose_vary(vary_str)
samples=fs.cartesian_prod(vary,z,mass) 
nsamp=samples.shape[0]

samples,x,y,emulator=fs.build_emulator_3D(home,suite,vary_str,prof,func_str)

#now we can get an emulated profile with different parameters
A=0.7
z=0.2
M=12.7
params=[[A,z,M]] #the order here is important- A, then z, then M
emulated=emulator(params)

