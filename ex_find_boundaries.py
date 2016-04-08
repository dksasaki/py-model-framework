import matplotlib.pyplot as plt
import numpy as np
import model_class.places as pl
import model_class.secom_interface as si
plt.close('all')
plt.ion()

ndepths = 15
T=[27.59,27.59,26.88,25.57,23.02,21.76,20.26,18.73,15.99,12.43,
                                      9.10,6.19,3.40,3.70,3.70];
S=[36.87,36.87,36.90,36.93,36.95,36.85,36.69,36.42,35.79,35.27,34.81,
                                       34.51,34.51,34.94,34.94];
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
#b.mapa.plot(a.ann[0],a.ann[1],'or',latlon=True) #plota os pontos da grade grossa vizinhos aos pontos da grade fina
#b.mapa.plot(a.xb,a.yb,'m', latlon=True,linewidth=5) #plota os contornos da grade fina

a.eta_boundaries(eta) #cria o arquivo eta_bound
a.TS_boundaries(15,T,S,'homog_bound') #cria o arquivo homog_bound

 #####
 #interpola
from model_class.read_class import secom_read_data
from scipy import interpolate


c = secom_read_data()

#coarser grid
x = c.c('lon')[a.ann_i[:,0],a.ann_i[:,1]]
y = c.c('lat')[a.ann_i[:,0],a.ann_i[:,1]]
T = c.f_xr['temp'][0,:,:]
S = c.f_xr['salt'][0,:,:]

from model_class.model_boundaries import TS
TSa = TS()
var = TSa.interpolate_coarser2finerTS(x,y,a.xb,a.yb,T.data,S.data,a.ann_i)