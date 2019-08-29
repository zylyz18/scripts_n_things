

import yt
import caesar
import numpy as np
import os, sys


snapshot = sys.argv[1]
caesar_snap = sys.argv[2]
save_dir = sys.argv[3]

ds = yt.load(snapshot)
obj = caesar.load(caesar_snap)

obj.yt_dataset = ds

dd = obj.yt_dataset.all_data()

scalefactor = dd[("PartType4", "StellarFormationTime")]
star_masses = dd[("PartType4", "Masses")]

# Compute the age of all the star particles from the provided scale factor at creation                               
formation_z = (1.0 / scalefactor) - 1.0

# Compute the age of all the star particles from the provided scale factor at creation                              
yt_cosmo = yt.utilities.cosmology.Cosmology()
stellar_formation_age = yt_cosmo.t_from_z(formation_z).in_units("Gyr")
# Age of the universe right now                                                                                     
simtime = yt_cosmo.t_from_z(ds.current_redshift).in_units("Gyr")
stellar_ages = (simtime - stellar_formation_age).in_units("Gyr")


sfr_50 = []
for INDEX in range(2000):
    
    stellar_mass = star_masses[obj.galaxies[INDEX].slist].in_units('Msun')
    star_ages = stellar_ages[obj.galaxies[INDEX].slist]
    w50 = np.where(star_ages.in_units('Myr').value < 50)[0]
    if len(w50) == 0:
        sfr_50myr = 1.0e-10
        sfr_50.append(sfr_50myr)
    else:
        sfr_50myr = np.sum(stellar_mass[w50])/50.e6
        sfr_50.append(sfr_50myr)




np.savez(save_dir+'caesar_sfr50.npz', sfr_50=sfr_50)