import matplotlib.pyplot as plt
import numpy as np
import model_class.places as pl
import model_class.model_nesting as mn

q = lambda f,ind : [f[i[0],i[1]] for i in ind]

a = mn.secom()
a.find_boundaries() 
a.nearest_boundaries() #this method find the nearest points between the mother grid and the boundaries of the nested grid  
a.boundaries_nearest_neighbors() #this method finds all the neighbors of the poinst defined by the self.neares_boundaires_location method

b = pl.mapa()
b.Embaiamento_sp()
b.mapa.drawcoastlines()

b.mapa.plot(a.g_mask(a.c('lon'),0),a.g_mask(a.c('lat'),0),'k',latlon=True)
b.mapa.plot(a.g_mask(a.c('lon'),0).T,a.g_mask(a.c('lat').T,0),'k',latlon=True)
b.mapa.plot(a.xb,a.yb,'m', latlon=True)
#b.mapa.plot(a.d[:,0],a.d[:,1],'.r',linewidth=3,latlon=True)

b.mapa.plot(a.ann[0],a.ann[1],'or',latlon=True)

