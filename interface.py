from model_class.secom_interface import eta_interface, TS_interface, init_tands_interface
from model_class.model_nesting import model_nesting
from model_class.interpolate_grid import interpolations
from model_class.read_class import secom_nc, secom_model_grid
from scipy import interpolate
import matplotlib.pyplot as plt
import numpy as np

plt.ion()
ndepths=15

class eta(eta_interface,model_nesting,interpolations,secom_nc):
    def __init__(self):
        eta_interface.__init__(self,'bla')
        model_nesting.__init__(self)
        interpolations.__init__(self)
        secom_nc.__init__(self)
        self.boundaries_nearest_neighbors()


    def boundaries_nearest_neighbors(self):
         self.nearest_boundaries_location(self.c('lon'),self.c('lat'),self.xb,self.yb)
         self.all_neigbours_nearest_i_bl(self.mdi,self.c('xpos'))
         self.all_neigbours_nearest_bl(self.c('lon'),self.c('lat'))


    def eta_values(self):
        """ """
        x  = self.c('lon')[self.ann_i[:,0],self.ann_i[:,1]]
        y  = self.c('lat')[self.ann_i[:,0],self.ann_i[:,1]]

        t = np.arange(10)

        for i in t:
            eta= self.f_xr['elev'][i,:,:]
            self.var = self.interpolate_coarser2finer_2D(x,y,self.xb,self.yb,eta.data,self.ann_i)
            self.eta_boundaries_values(self.var,[i]) #nested eta evolution in time
        self.file_close()

    def eta_values_homog(self):
        """ """

        self.etaI1 = np.array(self.etaI1)*0
        self.etaJ1 = np.array(self.etaJ1)*0
        self.etaI0 = np.array(self.etaI1)*0
        self.etaJ1 = np.array(self.etaJ1)*0
        self.define_eta_boundaries_array_i() # self.EBDRY is defined here
        for i in [0,725]:
            self.eta_boundaries_values(self.EBDRY,[i])
        self.file_close()


class TS_boundaries(TS_interface,secom_nc,model_nesting,interpolations):
    def __init__(self,f_name,ndepths):
        interpolations.__init__(self)
        TS_interface.__init__(self,f_name,ndepths)
        model_nesting.__init__(self)
        secom_nc.__init__(self)
        self.boundaries_nearest_neighbors()

    def TS_values(self):
        x = self.c('lon')[self.ann_i[:,0],self.ann_i[:,1]]
        y = self.c('lat')[self.ann_i[:,0],self.ann_i[:,1]]
        z = self.f_xr['layer_bnds'].data
        T = self.f_xr['temp'][0,:,:,:]
        S = self.f_xr['salt'][0,:,:,:]
        nz= self.sig_lev

        var          = self.interpolate_coarser2finer_2D_depth(x,y,self.xb,self.yb,T.data,self.ann_i)
        self.TBDRYSL = self.interpolate_in_depth(z,nz,var)
        var1         = self.interpolate_coarser2finer_2D_depth(x,y,self.xb,self.yb,S.data,self.ann_i)
        self.SBDRYSL = self.interpolate_in_depth(z,nz,var1)

        self.write_TS_boundaries(self.ITAS,self.JTAS,self.TBDRYSL,self.SBDRYSL)
        self.file_close()

    def boundaries_nearest_neighbors(self):
         self.nearest_boundaries_location(self.c('lon'),self.c('lat'),self.xb,self.yb)
         self.all_neigbours_nearest_i_bl(self.mdi,self.c('xpos'))
         self.all_neigbours_nearest_bl(self.c('lon'),self.c('lat'))

    def TS_values_homog(self,ndepths):
        self.define_TS_boundaries_i()
        self.define_TS_values(ndepths)
        self.define_TS_boundaries()
        T = np.ones(ndepths)*20 
        S = np.ones(ndepths)*35
        self.TBDRYSL, self.SBDRYSL = self.define_TS_values_homog(T,S,ndepths)

        self.write_TS_boundaries(self.ITAS,self.JTAS,self.TBDRYSL, self.SBDRYSL)
        self.file_close()

class TS_initial_conditions(init_tands_interface,interpolations,secom_nc,secom_model_grid):
    def __init__(self):
        secom_model_grid.__init__(self)
        secom_nc.__init__(self)
        init_tands_interface.__init__(self)

    def TS_initial_conditions_heter(self,ndepths):
        xg  = self.g(7).ravel()
        yg  = self.g(6).ravel()
        ig  = self.g(1)
        jg  = self.g(0)
        z = a.f_xr['layer_bnds'].data
        xcg = self.f_xr['lon'].data.ravel()#[np.squeeze([self.f_xr['depth'].data>0])]
        ycg = self.f_xr['lat'].data.ravel()#[np.squeeze([self.f_xr['depth'].data>0])]
        nz= self.sig_lev

        igg,jgg=self.ij_regrid(ig,jg)

        Vari1  = self.interpola(xcg,ycg,xg,yg,self.f_xr['temp'][0,:,:].data,z.size)
        Varii1 = self.regrid2depth(ig,jg,Vari1,z.size)
        Variii1= self.interpolate_in_depth2(z,nz,Varii1) 
        Vari2  = self.interpola(xcg,ycg,xg,yg,self.f_xr['salt'][0,:,:].data,z.size)
        Varii2 = self.regrid2depth(ig,jg,Vari2,z.size)
        Variii2= self.interpolate_in_depth2(z,nz,Varii2)

        print igg.shape
        self.write_init_tands(igg.ravel(),jgg.ravel(),Variii1,Variii2,nz.size)


