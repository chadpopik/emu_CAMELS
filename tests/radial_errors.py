import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d
from matplotlib import cm
import scipy.interpolate
import numpy as np
import warnings
import random
import time
import ostrich.emulate
import ostrich.interpolate
import sklearn.gaussian_process.kernels as skgp_kernels
from sklearn.linear_model import Ridge
from sklearn.preprocessing import PolynomialFeatures
from sklearn.pipeline import make_pipeline
import functions as fs
import sys


home='/home/cemoser/Repositories/ostrich/Emulator_profiles/'
suite=sys.argv[1]
vary_str=sys.argv[2]
prof=sys.argv[3]
func_str=sys.argv[4]

print("---------------------------")
print(suite,prof,"feedback",vary_str)
print("---------------------------")

mass=fs.mass
mass_str=fs.mass_str
snap=fs.snap
z=fs.choose_redshift(suite)
vary,sims=fs.choose_vary(vary_str)
samples=fs.cartesian_prod(vary,z,mass) 
nsamp=samples.shape[0]

start=time.time()
usecols,ylabel=fs.choose_profile(prof)

x,y,errup,errlow,stddev=fs.load_profiles_3D(usecols,home,suite,sims,snap,mass_str,prof)

y=np.transpose(y)
errup=np.transpose(errup)
errlow=np.transpose(errlow)
stddev=np.transpose(stddev)

'''
emulator = ostrich.emulate.PcaEmulator.create_from_data(
    samples,
    y,
    ostrich.interpolate.RbfInterpolator,
    interpolator_kwargs={'function': func_str},
    num_components=12,
)


def get_errs(samps,data,true_coord,true_data):
    emulator = ostrich.emulate.PcaEmulator.create_from_data(
        samps,
        data.reshape(data.shape[0],-1),
        ostrich.interpolate.RbfInterpolator,
        interpolator_kwargs={'function': func_str},
        num_components=12,
    )
    emulated = emulator(true_coord)
    emulated=emulated.reshape(len(data))
    err=((emulated - true_data)/true_data).squeeze()
    return emulated,err

time1=time.time()
errs_drop_1 = np.zeros_like(y)
emulated_drop_1=np.zeros_like(y)
with warnings.catch_warnings():
    warnings.simplefilter('ignore')
    for i in range(nsamp):
        emulated_drop_1[:,i],errs_drop_1[:,i] = get_errs(
            np.delete(samples, i,0),
            np.delete(y,i,1),
            samples[i:i+1],
            y[:,i],
        )
time2=time.time()
print("Time for drop-1 test:%.2f minutes, %.2f hours"%(((time2-time1)/60.),((time2-time1)/3600.)))
np.savetxt('errs_drop1_emulate3d_'+suite+'_'+vary_str+'_'+prof+'.txt',errs_drop_1)
np.savetxt('emulated_drop1_emulate3d_'+suite+'_'+vary_str+'_'+prof+'.txt',emulated_drop_1) 
'''

time2=time.time()
errs_drop_1=np.genfromtxt('./Error_histograms/errs_drop1_'+suite+'_'+vary_str+'_'+prof+'_4Mbins_RbfInterp_lin.txt')
emulated_drop_1=np.genfromtxt('./Error_histograms/emulated_drop1_'+suite+'_'+vary_str+'_'+prof+'_4Mbins_RbfInterp_lin.txt')

#radial error plots
for i in np.arange(nsamp):
    a,b,c=fs.deconstruct_3D(i) #a is the ASN1 index, b is the z index, c is the mass index 
    newy=y[:,i]
    newerrup=errup[:,i]
    newerrlow=errlow[:,i]

    plt.figure(figsize=(10,4))
    plt.subplot(1,2,1)
    plt.loglog(x,10**newy,label='data for %s=%.2f, z=%.2f, M=%s'%(vary_str,vary[a],z[b],mass_str[c]))
    plt.loglog(x,10**emulated_drop_1[:,i],label='emu',color='k')
    #plt.fill_between(newx,10**(newy+newyerr),10**(newy-newyerr),facecolor='cornflowerblue',alpha=0.4)
    plt.fill_between(x,10**(newy)+10**(newerrup),10**newy-10**newerrlow,facecolor='cornflowerblue',alpha=0.4)                                                                                                                   
    plt.xlabel('R (Mpc)',size=12)
    plt.ylabel(ylabel,size=12)
    plt.legend(loc='best',fontsize=8)

    plt.subplot(1,2,2)
    errs = np.log10(np.abs(errs_drop_1[:,i]))
    plt.semilogx(x,errs,linestyle='dashed',color='k')
    plt.axhline(-1, label=r'$10\%$ error level', color='red')
    plt.axhline(-2, label=r'$1\%$ error level', color='orange')
    plt.axhline(-3, label=r'$0.1\%$ error level', color='green')

    plt.ylabel(r'log($\%$ error)',size=12)
    plt.xlabel('R (Mpc)',size=12)
    plt.legend(loc='best',fontsize=8)
    plt.savefig('/home/cemoser/Repositories/ostrich/Tests/Radial_errors/radial_errs_Rbf_'+func_str+'_'+suite+'_'+prof+'_'+vary_str+'_'+str(vary[a])+'_z'+str(z[b])+'_M'+mass_str[c]+'.png',bbox_inches='tight')
    plt.close()

end=time.time()

print("Time for plotting: %.2f minutes, %.2f hours"%(((end-time2)/60.),((end-time2)/3600.)))
