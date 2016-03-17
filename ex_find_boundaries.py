import xray as xr
import matplotlib.pyplot as plt
import numpy as np
from scipy.spatial import kdtree as kd
import model_class.model_nesting as mn

import model_class.places as pl

#This script uses 2 grids. The mother grid and the nested grid.


plt.ion()

q = lambda f,ind : [f[i[0],i[1]] for i in ind]

a = mn.secom_nesting()
a.boundaries_location() 
a.nearest_boundaries_location() #this method find the nearest points between the mother grid and the boundaries of the nested grid  
a.all_neigbours_nearest_bl() #this method finds all the neighbors of the poinst defined by the self.neares_boundaires_location method

b = pl.mapa()
b.Embaiamento_sp()
b.mapa.drawcoastlines()

b.mapa.plot(a.g_mask(a.c('lon'),0),a.g_mask(a.c('lat'),0),'k',latlon=True)
b.mapa.plot(a.g_mask(a.c('lon'),0).T,a.g_mask(a.c('lat').T,0),'k',latlon=True)
b.mapa.plot(a.xb,a.yb,'m', latlon=True)
#b.mapa.plot(a.d[:,0],a.d[:,1],'.r',linewidth=3,latlon=True)

#self.ann is a lambda function which finds the neighbours of self.nearest_boundaries_location, using its neightboindexes
for i in a.ann: 
	b.mapa.plot(i[0],i[1],'og',latlon=True)

