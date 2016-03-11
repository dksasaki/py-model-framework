from model_class.grid_class import secom_read
import xray as xr
import matplotlib.pyplot as plt
import numpy as np
import model_class.model_boundaries as mb
from model_class.read_class import secom_read_data
from scipy.spatial import kdtree as kd

class secom_nesting(secom_read_data):
    #this method reads the model_grid grid and extracts the boundaries of the model that will be nest,rced
    def __init__(self):
        super(secom_nesting, self).__init__()
        self.zip_ar = lambda x,y : np.array(zip(x,y))

    def boundaries_location(self):
        #getting the model_grid boundaries
        bnd = mb.secom_model_boundaries()
        bnd.find_boundaries()
        self.xb = bnd.xb
        self.yb = bnd.yb

    #this method find the nearest points between the mother grid and the boundaries of the nested grid
    def nearest_boundaries_location(self):
        mdgrd =  self.zip_ar( self.c('lon').ravel(),self.c('lat').ravel() )  
        #a nearest point search is determined by KDTtree, based on the model grid
        kdt = kd.KDTree(mdgrd)

        #nearest model grid pontos and distance to the desired boundaries
        self.mdi_dist, self.mdi = kdt.query(self.zip_ar(self.xb,self.yb)) 
        self.d = np.array([mdgrd[j].tolist() for j in self.mdi])

    def all_neigbours_nearest_bl(self):
        f = lambda f,ind : [f[i[0],i[1]] for i in ind]
        

        self.i = np.array(self.mdi)/self.c('xpos').max().astype('int')
        self.j = np.array(self.mdi)%self.c('xpos').max().astype('int')

        self.ann= lambda p,q : np.array([f(self.c('lon'), zip(self.i+p,self.j+q)),f(self.c('lat'), zip(self.i+p,self.j+q))]).T

        #self.annbl_i = [i-1,i,i+1]
        #self.annbl_j = [j-1,j,j+1]






    #this method interpolates the data of the mother dataset to the nested boundaries


#mdgrd = np.array(zip(a.c('lon').ravel(),a.c('lat').ravel()))

