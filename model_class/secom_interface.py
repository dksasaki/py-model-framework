from model_class.grid_class import secom_read
from model_class.read_class import secom_read_data
from model_class.model_boundaries import boundaries
from model_class.model_nesting import model_nesting
import numpy as np

class secom(model_nesting,secom_read,secom_read_data,boundaries):
    def __init__(self):
         model_nesting.__init__(self) 
         secom_read.__init__(self)      #model_grid is read here
         secom_read_data.__init__(self) #gcmplt.cdf is read here
         boundaries.__init__(self)
         self.find_boundaries()
        

    def find_boundaries(self):
         self.boundaries_coordinates(self.g(1),self.g(0),self.g(7),self.g(6),self.g(4))
         self.boundaries_grid(self.g(1),self.g(0),self.g(7),self.g(6),self.g(4))

    def eta_boundaries_homog(self,output_file):
        print output_file
        self.define_eta_boundaries_values()
        self.define_eta_boundaries_i()
        self.define_eta_boundaries_homog()
        self.write_eta_boundaries(output_file)

    def eta_boundaries_heter(self,output_file):
        self.boundaries_nearest_neighbors()
        self.define_eta_boundaries_values()
        self.define_eta_boundaries_i()
        self.define_eta_boundaries_homog()

        x  = self.c('lon')[self.ann_i[:,0],self.ann_i[:,1]]
        y  = self.c('lat')[self.ann_i[:,0],self.ann_i[:,1]]
        eta= self.f_xr['elev'][10,:,:]
        var = self.interpolate_coarser2finer_2D(x,y,self.xb,self.yb,eta.data,self.ann_i)
        self.define_eta_boundaries_heter(var)
        self.define_eta_boundaries_i()

        self.write_eta_boundaries(output_file)


    def TS_boundaries_homog(self,ndepths,T,S,output_file):
        self.define_TS_boundaries_i()
        self.define_TS_values(ndepths)
        self.define_TS_values_homog(T,S,ndepths)
        self.define_TS_boundaries()
        self.write_TS_boundaries(output_file)

    def TS_boundaries_heter(self,ndepths,output_file):

        x = self.c('lon')[self.ann_i[:,0],self.ann_i[:,1]]
        y = self.c('lat')[self.ann_i[:,0],self.ann_i[:,1]]
        T = self.f_xr['temp'][0,:,:,:]
        S = self.f_xr['salt'][0,:,:,:]

        self.define_TS_boundaries_i()
        self.define_TS_values(ndepths)
        self.define_TS_boundaries()

        var = self.interpolate_coarser2finer(x,y,self.xb,self.yb,T.data,self.ann_i)
        var = np.append(var,self.interpolate_coarser2finer_3D(x,y,self.xb,self.yb,S.data,self.ann_i),axis=1)
        self.define_TS_values_heter(var[:,:5].T,var[:,5:].T,5)
        self.write_TS_boundaries(output_file)



    def boundaries_nearest_neighbors(self):
         self.nearest_boundaries_location(self.c('lon'),self.c('lat'))
         self.all_neigbours_nearest_i_bl(self.mdi,self.c('xpos'))
         self.all_neigbours_nearest_bl(self.c('lon'),self.c('lat'))
