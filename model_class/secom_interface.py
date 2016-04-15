from model_class.boundaries import boundaries
from model_class.secom_write import data_group_f_1, data_group_f_2, initial_condition
import numpy as np

class eta_interface(boundaries,data_group_f_1):
    def __init__(self,f_name):
        boundaries.__init__(self)
        data_group_f_1.__init__(self,f_name)
        self.find_boundaries()
        self.define_eta_boundaries_array()
        self.define_eta_boundaries_array_i()
        self.eta_boundaries()


    def find_boundaries(self):
        """
        find the boundaries of the model_grid file
        """
        self.boundaries_coordinates(self.g(1),self.g(0),self.g(7),self.g(6),self.g(4))
        self.boundaries_grid(self.g(1),self.g(0),self.g(7),self.g(6),self.g(4))
        aux = map(self.g_T_flatten,[self.JETA,self.IETA,self.JCON,self.ICON])
        self.bounds_eta_i = aux[0]+aux[1]+aux[2]+aux[3]


    def define_eta_boundaries_array(self):
        """
        EBDRY = boundary elevation data
        """
        self.etaJ0  = (np.ones(self.jmin.shape[0])).tolist()
        self.etaI0  = (np.ones(self.imin.shape[0])).tolist()
        self.etaI1  = (np.ones(self.imax.shape[0])).tolist()
        self.etaJ1  = (np.ones(self.jmax.shape[0])).tolist()

    def define_eta_boundaries_array_i(self):
        """
        prepares data for writing 
        """
        c  = [self.etaJ0,self.etaI0,self.etaJ1,self.etaI1]
        self.EBDRY = self.g_matrix_flat(c)

    def eta_boundaries(self):
        self.find_boundaries()
        self.define_eta_boundaries_array()
        self.number_grid_elements()
        self.loc_grid_elements()

    def eta_boundaries_values(self,EBDRY,TIME):
        for i in TIME:
            self.time_observation(i)
            self.elevation_data(EBDRY)

class TS_interface(boundaries,data_group_f_2):
    def __init__(self,f_name,ndepths):
        boundaries.__init__(self)
        data_group_f_2.__init__(self,f_name)
        self.find_boundaries()
        self.define_TS_boundaries_i()
        self.define_TS_values(ndepths)
        self.define_TS_boundaries()

    def find_boundaries(self):
        """
        find the boundaries of the model_grid file
        """
        self.boundaries_coordinates(self.g(1),self.g(0),self.g(7),self.g(6),self.g(4))
        self.boundaries_grid(self.g(1),self.g(0),self.g(7),self.g(6),self.g(4))

    def define_TS_boundaries_i(self):
        #self.find_boundaries()
        self.ITAS = self.xb_i
        self.JTAS = self.yb_i



    def define_TS_values(self,ndepths):
        """
        This function creates a matrix self.TSbounds[2*ndepths columns, boundaries length]
        of the vertical TS on the boundaries.
        This matrix may receive homogenous values in:
        a) self.define_TS_value_homog
        b) The user may specify the values:
            1 - boundary where I=min with crescent J 
            2 - boundary where J=min with crescent I
            3 - boundary where I=max with crescent J
            4 - boundary where J=min with crescent I 
        """
        self.n_boundaries = np.array([self.ITAS,self.JTAS]).shape[-1]
        self.TSbounds = np.zeros([2*ndepths,self.n_boundaries])

    def define_TS_boundaries(self):
        #run define_TS_values before this one
        self.TSbounds = self.TSbounds.tolist()



class init_tands_interface(initial_condition):
    def __init__(self):
        initial_condition.__init__(self)

    def define_init_grid(self,i,j,x,y):
        self.xg = x[i] 
        self.yg = y[i]
    
    def ij_regrid(self,ig,jg):
        shp = ig.shape
        i,j = np.meshgrid(np.arange(shp[1]+2)+1,np.arange(shp[0]+2)+1)
        i,j = i.T.reshape(shp[0]+2,shp[1]+2),j.T.reshape(shp[0]+2,shp[1]+2)
        return i,j

    def regrid(self,x,y,var):
        shp = x.shape
        var = var.reshape(shp[1],shp[0])
        return var

    def enquad(self,var):
        shp = var.shape
        i,j = np.meshgrid(np.arange(shp[1]+2)+1,np.arange(shp[0]+2)+1)
        enq = np.zeros((shp[0]+2,shp[1]+2))
        enq[1:-1,1:-1] = var
        return enq
        
    def regrid2depth(self,ig,jg,var,ndepths):
        igg,jgg=self.ij_regrid(ig,jg)
        reg = np.zeros((igg.shape[0]*igg.shape[1],ndepths))
        for i in range(ndepths):
            reg[:,i] = self.enquad(self.regrid(ig,jg,var[:,i])).ravel()

        return reg

