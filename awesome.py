import numpy as np
import matplotlib.pyplot as plot
import model_class.interface as intr

"""creates nested eta boundaries at t= [0,725] from gcmplt.cdf"""
# a = intr.eta()
# a.eta_values()

"""#creates homogeneous eta boundaries, with a given value (0 in this case)"""
# a1 = intr.eta()
# a1.eta_values_homog() 

"""creates neste TS boundaries at t=[0,725] from gcmplt.cdf"""
# b = intr.TS_boundaries('ts',15)
# b.TS_values()

"""creates TS boundaries, with a given value (0 in this case)"""
b1 = intr.TS_boundaries('ts',15)
b1.TS_values_homog(7)

# """creates the initial conditions""" #TESTING!!
# c = intr.TS_initial_conditions()
# #c.TS_initial_conditions_heter()

# xg  = c.g(7).ravel()
# yg  = c.g(6).ravel()
# ig  = c.g(1)
# jg  = c.g(0)
# z = c.f_xr['layer_bnds'].data
# xcg = c.f_xr['lon'].data.ravel()#[np.squeeze([c.f_xr['depth'].data>0])]
# ycg = c.f_xr['lat'].data.ravel()#[np.squeeze([c.f_xr['depth'].data>0])]
# nz= c.sig_lev

# igg,jgg=c.ij_regrid(ig,jg)
# Vari1  = c.interpola(xcg,ycg,xg,yg,c.f_xr['temp'][10,:,:].data,z.size)
# Vari1[Vari1==0] = np.nan
# Varii1 = c.regrid2depth(ig,jg,Vari1,z.size)
# Variii1= c.interpolate_in_depth2(z,nz,Varii1) 
# Vari2  = c.interpola(xcg,ycg,xg,yg,c.f_xr['salt'][10,:,:].data,z.size)
# Varii2 = c.regrid2depth(ig,jg,Vari2,z.size)
# Variii2= c.interpolate_in_depth2(z,nz,Varii2)

# Variii1[np.isnan(Variii1)]=0

# c.write_init_tands(igg.ravel(),jgg.ravel(),Variii1,Variii2,nz.size)


