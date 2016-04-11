import matplotlib.pyplot as plt
import numpy as np
import model_class.places as pl
import model_class.secom_interface as si
plt.close('all')
plt.ion()

ndepths = 5
T=[27.59,27.59,26.88,25.57,23.02,21.76,20.26,18.73,15.99,12.43,
                                      9.10,6.19,3.40,3.70,3.70]; T = T[:ndepths]
S=[36.87,36.87,36.90,36.93,36.95,36.85,36.69,36.42,35.79,35.27,34.81,
                                       34.51,34.51,34.94,34.94]; S = S[:ndepths]

eta = 'eta_bound'


q = lambda f,ind : [f[i[0],i[1]] for i in ind]

a = si.secom()
a.nearest_boundaries() #this method find the nearest points between the mother grid and the boundaries of the nested grid  
a.boundaries_nearest_neighbors() #this method finds all the neighbors of the poinst defined by the self.neares_boundaires_location method

b = pl.mapa()
b.Embaiamento_sp()
b.mapa.drawcoastlines()

b.mapa.plot(a.g_mask(a.c('lon'),0),a.g_mask(a.c('lat'),0),c='0.5',latlon=True, zorder=1) #plota grade
b.mapa.plot(a.g_mask(a.c('lon'),0).T,a.g_mask(a.c('lat').T,0),c='0.5',latlon=True,zorder=1) #plota grade
b.mapa.plot(a.ann[0],a.ann[1],'or',latlon=True) #plota os pontos da grade grossa vizinhos aos pontos da grade fina
b.mapa.plot(a.xb,a.yb,'m', latlon=True,linewidth=5) #plota os contornos da grade fina

a.eta_boundaries(eta) #cria o arquivo eta_bound
a.TS_boundaries_homog(5,T,S,'homog_bound') #cria o arquivo homog_bound

 #####
 #interpola
from model_class.read_class import secom_read_data
from scipy import interpolate


c = secom_read_data()

#coarser grid
x = c.c('lon')[a.ann_i[:,0],a.ann_i[:,1]]
y = c.c('lat')[a.ann_i[:,0],a.ann_i[:,1]]
T = c.f_xr['temp'][0,:,:,:]
S = c.f_xr['salt'][0,:,:,:]

#from model_class.model_boundaries import boundaries 
#bnd = boundaries()
#var = a.interpolate_coarser2finer(x,y,a.xb,a.yb,T.data,a.ann_i)
#var = np.append(var,a.interpolate_coarser2finer(x,y,a.xb,a.yb,S.data,a.ann_i),axis=1)
#a.define_TS_values_heter(var[:,:5].T,var[:,5:].T,5)
#a.write_TS_boundaries('TS_bounds')

#bla = np.array([T[:,i[0],i[1]].data for i in a.ann_i]) #T in a.ann_i sites


#ginterp = interpolate.griddata((x,y),bla[:,0],(a.xb,a.yb),method='linear')

#b.mapa.scatter(a.xb,a.yb,c=ginterp,vmin=20,vmax=26,latlon=True,zorder=2)
#b.mapa.colorbar()
#b.mapa.scatter(x,y,c = np.array(bla[:,0]),vmin=20,vmax=26,latlon=True,zorder=3)
#b.mapa.colorbar()
#plt.savefig('teste_malha2.eps',bbox_inches='tight')


####
#eta boundaries
