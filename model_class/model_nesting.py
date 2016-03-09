from model_class.grid_class import secom_read
import xray as xr
import matplotlib.pyplot as plt
import numpy as np
import model_class.model_boundaries as mb
from model_class.read_class import secom_read_data
from scipy.spatial import kdtree as kd

class secom_nesting(secom_read_data):
    #this method reads the model_grid grid and extracts the boundaries of the model that will be nest,rced
    def boundaries_location(self):
        #getting the model_grid boundaries
        bnd = mb.secom_model_boundaries()
        bnd.find_boundaries()

        #getting lon,lat of the mother grid
        self.xb = bnd.xb
        self.yb = bnd.yb

    #this method find the nearest points between the mother grid and the boundaries of the nested grid
    def nearest_boundaries_location(self):
        a = np.array(zip(self.xb,self.yb))
        b = np.array(zip(self.c('lon').ravel(),self.c('lat').ravel()))

        q = kd.KDTree(b)
        i = q.query(a)
        self.d = np.array([b[j].tolist() for j in i[1]])

    #def 
    #this method interpolates the data of the mother dataset to the nested boundaries


