import numpy as np
from model_class.grid_class import secom_read
from model_class.read_class import secom_read_data
from model_class.model_boundaries1 import model_boundaries
import model_class.model_boundaries1 as mb
from scipy.spatial import kdtree as kd
class model_nesting(object):
    """
    lon : mxn numpy matrix
    lat : mxn numpy matrix
    im  : mx1 numpy array - m direction indexes
    indx: indexes of desired lon,lat pairs (the pairs are a (p*k)x1 list)
            ex: [lon,lat] = [[20,30], [21,32], [22,33]]
                if indx = 0
                [lon,lat][indx] --> [20,30]



    """
    def __init__(self):
        self.zip_ar     = lambda x,y : np.array(zip(x,y))
        self.mtx_val    = lambda f,ind : [f[i[0],i[1]] for i in ind] #gets the a value of f (f is a mxn matrix),
                                                                     #according to the given ind indexes.
        self.zip_mtx_val= lambda f1,f2,p,q : np.array([self.mtx_val(f1,zip(p,q)), \
                                             self.mtx_val(f2,zip(p,q))]).T #pair of list, that get a the value of
        pass


    def nearest_boundaries_location(self,lon,lat):
        """
        This method find the nearest points between the mother grid and the boundaries of the nested grid.
        """
        mdgrd =  np.array(zip( lon.ravel(),lat.ravel() ))
        kdt = kd.KDTree(mdgrd)
        self.mdi_dist, self.mdi = kdt.query(np.array(zip( self.xb,self.yb)) )

    def all_neigbours_nearest_i_bl(self,indx,im):
         """
         This method finds all the neighbors of the poinst defined by the self.nearest_boundaries_location method.
         It defines the self.ann - lon,lat of the neighbor points to the nearest points
         """
         self.i_pos   = np.array(indx)/im.max().astype('int') #lon indexes from the coarser grid
         self.j_pos   = np.array(indx)%im.max().astype('int') #lat indexes from the coarser grid

         ann_i= []

         for i in zip([0,1,-1,0,0],[0,0,0,1,-1]): 
            ann_i.append([(self.i_pos+i[0]).tolist(),(self.j_pos+i[1]).tolist()])

         self.ann_i = self.remove_repeated(ann_i)

    def all_neigbours_nearest_bl(self,lon,lat):
        i = self.ann_i[:,0]
        j = self.ann_i[:,1]

        self.ann = [lon[i,j],lat[i,j]]

    def remove_repeated(self,g):
         m = np.array(g).shape[2]*np.array(g).shape[0]
         n = np.array(g).shape[1]
         d = np.array(g).transpose(2,0,1).reshape(m,n)
         e = set(zip(d[:,0].tolist(),d[:,1].tolist()))
         f = np.array([[i[0],i[1]] for i in  e])

         return f


class secom(model_nesting,secom_read,secom_read_data,model_boundaries):
    def __init__(self):
         model_nesting.__init__(self)
         secom_read.__init__(self)
         secom_read_data.__init__(self)
         model_boundaries.__init__(self)
         self.find_boundaries()
        

    def find_boundaries(self):
         self.boundaries_coordinates(self.g(1),self.g(0),self.g(7),self.g(6),self.g(4))
         self.boundaries_grid(self.g(1),self.g(0),self.g(7),self.g(6),self.g(4))

    def eta_boundaries(self,output_file):
        print output_file
        self.define_eta_boundaries_values()
        self.define_eta_boundaries_i()
        self.define_eta_boundaries()
        self.write_eta_boundaries(output_file)

    def TS_boundaries(self,ndepths,T,S,output_file):
        self.define_TS_boundaries_i()
        self.define_TS_values(ndepths)
        self.define_TS_values_homog(T,S)
        self.define_TS_boundaries()
        self.write_TS_boundaries(output_file)

    def nearest_boundaries(self):
         self.nearest_boundaries_location(self.c('lon'),self.c('lat'))

    def boundaries_nearest_neighbors(self):
         self.all_neigbours_nearest_i_bl(self.mdi,self.c('xpos'))
         self.all_neigbours_nearest_bl(self.c('lon'),self.c('lat'))
