from model_class.grid_class import secom_read
import matplotlib.pyplot as plt
import numpy as np

class secom_model_boundaries(secom_read):
    """
    This class finds the boundaries of a model_grid file.
    The function self.g reads the model_grid file and it is defined as:

    self.g(1) = indexes in J direction
    self.g(2) = indexes in I direction
    self.g(3) = ?
    self.g(4) = ?
    self.g(5) = latitude values
    self.g(6) = lonigitude values
    self.g(7) = ?

    Some methods of this function were inherited from secom_read class.
    """
    def find_boundaries(self):
        """
        This function finds the indexes of the boundaries of a grid.
        It takes the points which are wet in the mdodel grid.

        The following indexes are written to define the boundaries for the model.
        self.I0, self.J0, self.I1, self.J1 

        self.xb : longitude of the boundaries
        self.yb : latitude of the boundaries
        """
        #min i direction boundary
        self.I0j = self.g(0)[self.i_g_min_gre(4,0,1)][:-1] #j(i_min) indexes, where the cells are wet
        self.I0i = self.g(1)[self.i_g_min_gre(4,0,1)][:-1] #i(i_min) indexes, where the cells are wet
        self.I0  = [i.tolist() for i in [self.I0j,self.I0i+0,self.I0j,self.I0i+1]] 
        plt.plot(self.g(7)[self.i_g_min_gre(4,0,1)],self.g(6)[self.i_g_min_gre(4,0,1)])

        #max j direction boundary
        self.J1j = self.g(0)[self.i_g_max_gre(4,0,0)][1:-1]
        self.J1i = self.g(1)[self.i_g_max_gre(4,0,0)][1:-1]
        self.J1  = [i.tolist() for i in [self.J1j-0,self.J1i,self.J1j-1,self.J1i]]
        plt.plot(self.g(7)[self.i_g_max_gre(4,0,0)][1:-1],self.g(6)[self.i_g_max_gre(4,0,0)][1:-1])

        #max i direction boundary
        self.I1j = self.g(0)[self.i_g_max_gre(4,0,1)][:-1]
        self.I1i = self.g(1)[self.i_g_max_gre(4,0,1)][:-1]
        self.I1  = [i.tolist() for i in [self.I1j,self.I1i-0,self.I1j,self.I1i-1]]
        plt.plot(self.g(7)[self.i_g_max_gre(4,0,1)],self.g(6)[self.i_g_max_gre(4,0,1)])


        #min j direction boundary #!MAY NEED REVIEW
        self.J0j = self.g(0)[self.i_g_min_gre(4,0,0)][1:-1]
        self.J0i = self.g(1)[self.i_g_min_gre(4,0,0)][1:-1]
        self.J0  = [i.tolist() for i in [self.J0j+0, self.J0i,self.J0j+1, self.J0i]]

        #determines the latitude and longitude of the boundaries
        i = self.i_g_min_gre(4,0,1)+self.i_g_max_gre(4,0,1)+self.i_g_max_gre(4,0,0)
        self.xb = self.g(7)[i]
        self.yb = self.g(6)[i]


    def define_TS_boundaries_i(self):
        self.find_boundaries()
        b  = [self.I0j,self.J1j,self.I1j,self.J0j]
        c  = [self.I0i,self.J1i,self.I1i,self.J0i]
        b1 = self.g_matrix_flat(b)
        c1 = self.g_matrix_flat(c)
        self.bounds_TS_i = [b1,c1]

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
        self.define_TS_boundaries_i()
        self.n_boundaries = np.array(self.bounds_TS_i).shape[-1]
        self.TSbounds = np.zeros([2*ndepths,self.n_boundaries])

    def define_TS_values_homog(self,T,S):
        """
        First 15 columns of self.TSbounds: temperature
        Last  15 columns of self.TSbounds: salinity
        """
        for i in range(self.n_boundaries):
            self.TSbounds[0:15,i] = T
            self.TSbounds[15:,i]  = S


    def define_TS_boundaries(self):
        #run define_TS_values before this one
        self.TSbounds = self.TSbounds.tolist()

    def define_eta_boundaries_i(self):
        #self.bounds_eta_i = []
        self.find_boundaries()
        c = map(self.g_T_flatten,[self.I0,self.J1,self.I1,self.J0])
        self.bounds_eta_i = self.g_matrix_flat(c)

    def define_eta_boundaries(self):
        #self.define_eta_boundaries_i()
        c = [self.etaI0,self.etaJ1,self.etaI1,self.etaJ0]
        self.etabounds = self.g_matrix_flat(c)

    def define_eta_values(self):
        self.define_eta_boundaries_i()
        self.etaJ0  = (np.ones(self.J0i.shape)).tolist()
        self.etaI0  = (np.ones(self.I0i.shape)).tolist()
        self.etaI1  = (np.ones(self.I1i.shape)).tolist()
        self.etaJ1  = (np.ones(self.J1i.shape)).tolist()


    def write_boundaries(self,x,fmto,columns):
        """this function is used in write_eta_boundaries"""
        for j,i in enumerate(x):
            self.f1.write(fmto % i)
            #print j
            #print len(x)
            if (j+1) % columns == 0 and (j!=len(x)-1):
                self.f1.write('\n')

    def write_eta_boundaries(self,f_name):
        self.f1 = open(f_name,'w+')
        self.f1.write("%5.0f DATA\n" % (len(self.bounds_eta_i)/4))
        self.write_boundaries(self.bounds_eta_i,'%5.0f',16)
        
        for i in [0,725]:
            self.f1.write('\n%10.5f\n' % i)
            self.write_boundaries(self.etabounds,'%10.5f',8)
        self.f1.close()

    def write_TS_boundaries(self,f_name):
        q =map(np.array,[self.bounds_TS_i,self.TSbounds])
        self.r = np.concatenate((q[0],q[1]), axis = 0)
        r1 = self.g_T_flatten(self.r)


        self.f1 = open(f_name,'a+')
        k = 0
        self.f1.write('\nTS\n')
        for k in [0,725]:
            self.f1.write('%10.5f\n' % k)
            for i in self.r.T:
                self.f1.write('%5.0f' % i[0])
                self.f1.write('%5.0f' % i[1])
                for j in i[2:]:
                    self.f1.write('%5.2f' % j)
                self.f1.write('\n')
        self.f1.close()
