import xray as xr
import matplotlib.pyplot as plt
import numpy as np
from scipy.spatial import kdtree as kd
import model_class.model_nesting as mn

import model_class.places as pl

plt.ion()

q = lambda f,ind : [f[i[0],i[1]] for i in ind]

a = mn.secom_nesting()
a.boundaries_location()
a.nearest_boundaries_location()
a.all_neigbours_nearest_bl()

b = pl.mapa()
b.Embaiamento_sp()
b.mapa.drawcoastlines()

b.mapa.plot(a.g_mask(a.c('lon'),0),a.g_mask(a.c('lat'),0),'k',latlon=True)
b.mapa.plot(a.g_mask(a.c('lon'),0).T,a.g_mask(a.c('lat').T,0),'k',latlon=True)
b.mapa.plot(a.xb,a.yb,'m', latlon=True)
#b.mapa.plot(a.d[:,0],a.d[:,1],'.r',linewidth=3,latlon=True)

for i,j in zip([0,0],[1,0],[-1,0],[0,1],[0,-1]):
	b.mapa.plot(a.ann(i,j)[:,0],a.ann(i,j)[:,1],'or',latlon=True)

