from model_class.grid_class import secom_read
from model_class.model_boundaries import TS
from model_class.read_class import secom_read_data
from model_class.model_nesting import model_nesting
from scipy import interpolate
import numpy as np

class secom_initial_conditions(secom_read,TS,secom_read_data,model_nesting):
    """
    This class creates init_tands:
    
    self.write_init_tands uses functional style functions:
    1)variables:
        KSL: number of sigma levels
        T  : variable
        m  : m size of mxn matrix
        n  : n size of mxn matrix
    2)functions
        - self.depth_homog(T,KSL):
            Creates an array with KSL length and T values
        - self.init_var(T,KSL,m,n):
            Creates an mxnxKSL matrix with T values
    3)inherited functions
        - self.i_g_greater:
            Look at model_class.grid_class
    """

    def __init__(self):
        secom_read.__init__(self)
        self.depth_homog = lambda T,KSL: np.ones(KSL)*T
        self.init_var = lambda T,KSL,m,n : np.matlib.repmat(self.depth_homog(T,KSL),m+2,n+2).reshape(m+2,n+2,len(self.depth_homog(T,KSL))) #2 is summed in order to compensate the -2 in self.g
        TS.__init__(self)
        secom_read_data.__init__(self)
        model_nesting.__init__(self)


    def define_init_grid(self,i,j,x,y):
        self.xg = x[i] 
        self.yg = y[i]

    def interpola(self,x,y,xi,yi,var,ndepths):
        Vari = np.zeros((xi.shape[0],ndepths))

        for k in range(ndepths):
            Vari[:,k] = interpolate.griddata((x,y),var[k,:,:].ravel(),(xi,yi),method='nearest')
        Vari[Vari==Vari.min()]=Vari.max()
        return Vari
    
    def ij_regrid(self,ig,jg):
        shp = ig.shape
        i,j = np.meshgrid(np.arange(shp[1]+2)+1,np.arange(shp[0]+2)+1)
        i,j = i.T.reshape(50,150),j.T.reshape(50,150)
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


   # def interp_grid_coarser2finer3d(self)

    def write_init_tands(self,T,S,KSL):
        self.f1 = open('init_tands','w+')
        m,n = self.i_g_greater(4,0).shape

        T1 = self.init_var(T,KSL,m,n)
        S1 = self.init_var(S,KSL,m,n)

        y, x ,z = T1.shape

        for j in range(y):
            for i in range(x):
                self.f1.write('%5.0f' % (j+1))
                self.f1.write('%5.0f' % (i+1))
                for k in T1[j,i,:]:
                    self.f1.write('%5.2f' % k)
                for k in S1[j,i,:]:
                    self.f1.write('%5.2f' % k)

                self.f1.write('\n')

        self.f1.close()

    def write_init_tands2(self,x,y,T,S,KSL):
        self.f1 = open('init_tands','w+')
        cont = 0

        for j in range(x.shape[0]):
            self.f1.write('%5.0f' % y[j])
            self.f1.write('%5.0f' % x[j])
            for k in T[j,:]:
                self.f1.write('%5.2f' % k)
            for k in S[j,:]:
                self.f1.write('%5.2f' % k)
            self.f1.write('\n')

        self.f1.close()



