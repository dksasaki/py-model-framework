from model_class.grid_class import secom_read
import xray as xr
import matplotlib.pyplot as plt
import numpy as np
import model_class.model_boundaries as mb
from model_class.read_class import secom_read_data
from scipy.spatial import kdtree as kd

class secom_nesting(secom_read_data):
    """
    This method interpolates the data of a coarser grid in a finer grid.
    - self.boundaries_location
        Locates the boundaries of the model_grid file.
    - self.nearest_boundaries_location.
        Locates the closest poinst in the coarser grid related to the finer grid boundaries points.
        They are defined as self.d
    - self.all_neigbours_nearest_bl
        
    """
    
    def __init__(self):
        super(secom_nesting, self).__init__()
        self.zip_ar     = lambda x,y : np.array(zip(x,y))
        self.mtx_val    = lambda f,ind : [f[i[0],i[1]] for i in ind] #gets the a value of f (f is a mxn matrix),
                                                                     #according to the given ind indexes.
        self.zip_mtx_val= lambda f1,f2,p,q : np.array([self.mtx_val(f1,zip(p,q)), \
                                             self.mtx_val(f2,zip(p,q))]).T #pair of list, that get a the value of
                                                                           #f1 and f2 in p and q positions


    def boundaries_location(self):
        """
        Gets the model_grid boundaries.
        They are defined as:
        - self.xb (model_grid longitude boundary)
        - self.yb (model_grid latitude boundary)
        """
        bnd = mb.secom_model_boundaries()
        bnd.find_boundaries()
        self.xb = bnd.xb
        self.yb = bnd.yb

    def nearest_boundaries_location(self):
        """
        This method find the nearest points between the mother grid and the boundaries of the nested grid.
        """
        mdgrd =  self.zip_ar( self.c('lon').ravel(),self.c('lat').ravel() )  
        #a nearest point search is determined by KDTtree, based on the model grid
        kdt = kd.KDTree(mdgrd)

        #nearest model grid distance and points to the desired boundaries
        self.mdi_dist, self.mdi = kdt.query(self.zip_ar(self.xb,self.yb)) 
        self.d = np.array([mdgrd[j].tolist() for j in self.mdi])

    def all_neigbours_nearest_bl(self):
        """
        This method finds all the neighbors of the poinst defined by the self.nearest_boundaries_location method.
        It defines the self.ann the lon,lat of the neighbor points
        """
        self.i_pos   = np.array(self.mdi)/self.c('xpos').max().astype('int') #lon indexes from the coarser grid
        self.j_pos   = np.array(self.mdi)%self.c('xpos').max().astype('int') #lat indexes from the coarser grid

        self.ann = []

        for i in zip([0,1,-1,0,0],[0,0,0,1,-1]): 
            aux = self.zip_mtx_val(self.c('lon'),self.c('lat'),self.i_pos+i[0],self.j_pos+i[1])
            self.ann.append([aux[:,0],aux[:,1]])

    def f7(seq):
        seen = set()
        seen_add = seen.add
        return [x for x in seq if not (x in seen or seen_add(x))]

        new_list = reduce(lambda x,y: x+[y][:1-int(y in x)], a.ann[0][0], []) ??


    #this method interpolates the data of the mother dataset to the nested boundaries


#mdgrd = np.array(zip(a.c('lon').ravel(),a.c('lat').ravel()))

