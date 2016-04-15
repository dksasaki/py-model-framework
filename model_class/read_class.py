import xray as xr
import matplotlib.pyplot as plt
import numpy as np
import numpy.matlib
import linecache
import re

class secom_nc(object):
    """Reads secom's nc RESULTS
    self.c(var): recovers the dataset's coordinates
    self.v(t,d,var): recovers the dataset's coordinates ()
    t   = time index
    d   = depth index
    var = variable/coordinate name (string format)
    """

    def __init__(self):
        self.f_xr = xr.open_dataset('coarser_grid_input/gcmplt.cdf')
        self.c = lambda var :     self.f_xr[var].data #coordinates
        self.v = lambda t,d,var : self.f_xr[var][t,d,:,:].data
        self.g_mask = lambda f,m : np.ma.masked_array(f,mask = [f==m])
        self.v_sb_smpl = lambda t,d,lon,lat,var : self.f_xr[var][t,d,:,:][lat,:][:,lon].data
        self.v_smpl_mrg= lambda f1,f2,ax : np.concatenate(f1,f2,axis=ax)


class secom_model_grid(object):
    def __init__(self):
        #functional programming methods based on python modules
        #INDEXING
        self.i_g_max     = lambda x : (self.g(x).astype('int')==self.g(x).max()).squeeze() #indexes where a given g is max
        self.i_g_min     = lambda x : (self.g(x).astype('int')==self.g(x).min()).squeeze() #indexes where a given g is min
        self.i_g_greater = lambda  x,value : self.g(x)>value #index where a value is greater than a given g
        self.i_g_max_gre = lambda g1, value, g2 : self.i_g_greater(g1,value)*self.i_g_max(g2) #combines i_g_max and self.i_g_greater
        self.i_g_min_gre = lambda g1, value, g2 : self.i_g_greater(g1,value)*self.i_g_min(g2) #combines i_g_min and self.i_g_greater

        #NUMPY OPERATIONS
        self.g_T_flatten   = lambda x : np.array(x).T.flatten().tolist() #transpose and flat a list
        self.g_extend      = lambda g1, g2: g1.extend(g2) #extend the list g2 to list g1        #min i boundary
        self.g_matrix_flat = lambda g : [item for sublist in g for item in sublist] #flattening g = [[a],[b],[c],[d]] into [a,b,c,d]
        self.g_array         = lambda g: np.array(g)
        self.g_shape       = lambda g: g_array(g).shape #gives the shape of a list
        self.g_mask = lambda f,m : np.ma.masked_array(f,mask = [f==m])
        self.model_grid_read()
        pass

    def file(self):
        self.direc = 'input_data/'

    def model_grid_read(self):
        self.file()
        self.vertlev = int(re.findall('\d+',linecache.getline(self.direc+'/model_grid',3))[0])
        self.f = np.genfromtxt(self.direc+'model_grid',skip_header=5+self.vertlev).T
        nx  = (self.f[0].max()+1).astype('int')
        ny  = (self.f[1].max()+1).astype('int')
        self.g   = lambda x : self.f[x].reshape(nx-2,ny-2)

        with open(self.direc+'model_grid') as f:
            self.nlines = sum(1 for _ in f)

        self.sig_lev = np.genfromtxt(self.direc+'model_grid',skip_header=3, skip_footer=self.nlines-self.vertlev-3)


        
