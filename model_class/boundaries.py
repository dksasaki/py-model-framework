import matplotlib.pyplot as plt
import numpy as np
from model_class.read_class import secom_model_grid,secom_nc

class boundaries(secom_model_grid):
    def __init__(self):
        secom_model_grid.__init__(self)
        #secom_nc.__init__(self)


        #boolean type grid where values >0
        self.pos_i_points = lambda dep : np.array([dep>0])

        #boolean type grid where values equals max and min value
        self.max_i_points = lambda  indx : np.array([indx == indx.max()])
        self.min_i_points = lambda  indx : np.array([indx == indx.min()])

        #boolean type grid where values >0 and equals max and min values 
        self.comb_max_pos = lambda indx, dep : (self.pos_i_points(dep)*self.max_i_points(indx)).squeeze()
        self.comb_min_pos = lambda indx, dep : (self.pos_i_points(dep)*self.min_i_points(indx)).squeeze()

        #var grid with values >0 and equals max and min values
        self.wet_bound_max_points =lambda var,indx,dep : var[self.comb_max_pos(indx,dep)]
        self.wet_bound_min_points =lambda var,indx,dep : var[self.comb_min_pos(indx,dep)]

        #var grid with values >0 and equals max and min values, considering var1 and var2 indexes
        self.direc_max_bound = lambda var1,var2,indx,dep : np.array(zip(self.wet_bound_max_points(var1,indx,dep), \
                                                    self.wet_bound_max_points(var2,indx,dep)))
        self.direc_min_bound = lambda var1,var2,indx,dep : np.array(zip(self.wet_bound_min_points(var1,indx,dep), \
                                                    self.wet_bound_min_points(var2,indx,dep)))

        #flattening g = [[a],[b],[c],[d]] into [a,b,c,d]
        self.g_matrix_flat = lambda g : [item for sublist in g for item in sublist] 


    def boundaries(self,direc,c,d):
         if direc.size == 0:
             index = []
         else:
            index = [i.tolist() for i in [direc[:,1],direc[:,0],direc[:,1]+c,direc[:,0]+d]]
         return index

    def boundaries_grid(self,im,jn,lon,lat,dep):
        """
        DATA GROUP F: Open Boundary Condition Information
        OPTION 1 - TIME VARIABLE DATA
        
        Location of Grid Elements
        
        IETA = I number of grid element where elevation is specified
        JETA = J number of grid element where elevation is specified
        ICON = I number of connecting grid element (nearest interior 
            non- boundary grid element)
        JCON = J number of connecting grid element (nearest interior
            non- boundary gridelement)

        """
        self.Imax = self.direc_max_bound(im,jn,im,dep).astype('int')[1:-1]
        self.Jmax = self.direc_max_bound(im,jn,jn,dep).astype('int')[1:-1]
        self.Imin = self.direc_min_bound(im,jn,im,dep).astype('int')[1:-1]
        self.Jmin = self.direc_min_bound(im,jn,jn,dep).astype('int')[1:-1]

        self.ICON = self.boundaries(self.Imax,0,-1) #boundaries grid coordinate
        self.JCON = self.boundaries(self.Jmax,-1,0) #boundaries grid coordinate
        self.IETA = self.boundaries(self.Imin,0,1) #boundaries grid coordinate
        self.JETA = self.boundaries(self.Jmin,1,0) #boundaries grid coordinate

    def boundaries_coordinates(self,im,jn,lon,lat,dep):
        #boundaries coordinates [lon,lat] values
        self.xmax = self.direc_max_bound(lon,lat,im,dep)[1:-1]
        self.ymax = self.direc_max_bound(lon,lat,jn,dep)[1:-1]
        self.xmin = self.direc_min_bound(lon,lat,im,dep)[1:-1]
        self.ymin = self.direc_min_bound(lon,lat,jn,dep)[1:-1]

        self.imax = self.direc_max_bound(im,jn,im,dep)[1:-1] #boundaries indexes
        self.jmax = self.direc_max_bound(im,jn,jn,dep)[1:-1] #boundaries indexes
        self.imin = self.direc_min_bound(im,jn,im,dep)[1:-1] #boundaries indexes
        self.jmin = self.direc_min_bound(im,jn,jn,dep)[1:-1] #boundaries indexes

        bound = np.array(self.ymin.tolist()+self.xmin.tolist()+self.ymax.tolist()+self.xmax.tolist())
        self.xb = bound[:,0] #boundaries coordinates
        self.yb = bound[:,1] #boundaries coordinates

        bound = np.array(self.jmin.tolist()+self.imin.tolist()+self.jmax.tolist()+self.imax.tolist())
        self.xb_i = bound[:,0] #boundaries coordinates
        self.yb_i = bound[:,1] #boundaries boundaries_coordinates