import numpy as np
import numpy.matlib
import matplotlib.pyplot as plt
import linecache
import re



class secom_read(object):
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
        vertlev = int(re.findall('\d+',linecache.getline(self.direc+'/model_grid',3))[0])
        self.f = np.genfromtxt(self.direc+'model_grid',skip_header=5+vertlev).T
        nx  = (self.f[0].max()+1).astype('int')
        ny  = (self.f[1].max()+1).astype('int')
        self.g   = lambda x : self.f[x].reshape(nx-2,ny-2)


if __name__ == '__main__':
    a = secom_model_boundaries()
    #a.model_grid_read()
    a.find_boundaries()
    a.define_eta_boundaries_i()
    a.define_eta_values()
    a.etaI0 = np.array(a.etaI0)*0
    a.etaI1 = np.array(a.etaI1)*0
    a.etaJ1 = np.array(a.etaJ1)*(-0.01)

    a.define_eta_boundaries()
    a.write_eta_boundaries('bla')