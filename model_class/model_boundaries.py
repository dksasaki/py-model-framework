from grid_class import secom_read
import matplotlib.pyplot as plt

class secom_model_boundaries(secom_read):
    def find_boundaries(self):
        """
        This function finds the indexes of the boundaries of a grid.
        It compares cells where depth>0 (wet) and the max indexes of the cells in i and j direction
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

    def find_lat_lon_boundaries(self):
        i = self.i_g_min_gre(4,0,1)+self.i_g_max_gre(4,0,1)+self.i_g_max_gre(4,0,0)
        self.xb = self.g(7)[i]
        self.yb = self.g(6)[i]


    def define_TS_boundaries_i(self):
        #run find_boundaries before this one
        b  = [self.I0j,self.J1j,self.I1j,self.J0j]
        c  = [self.I0i,self.J1i,self.I1i,self.J0i]
        b1 = self.g_matrix_flat(b)
        c1 = self.g_matrix_flat(c)
        self.bounds_TS_i = [b1,c1]

    def define_TS_values(self,ndepths):
        """
        run find_boundaries_i before this one.
        This function creates a matrix TSbounds[2*ndepths columns, boundaries length] of the vertical TS on the boundaries.
        """
        self.n_boundaries = np.array(a.bounds_TS_i).shape[-1]
        self.TSbounds = np.zeros([2*ndepths,self.n_boundaries])

    def define_TS_values_homog(self,T,S):
        for i in range(self.n_boundaries):
            a.TSbounds[0:15,i] = T
            a.TSbounds[15:,i]  = S


    def define_TS_boundaries(self):
        #run define_TS_values before this one
        self.TSbounds = self.TSbounds.tolist()

    def define_eta_boundaries_i(self):
        #self.bounds_eta_i = []
        c = map(self.g_T_flatten,[self.I0,self.J1,self.I1,self.J0])
        self.bounds_eta_i = self.g_matrix_flat(c)


    def define_eta_values(self):
        self.etaJ0  = (np.ones(self.J0i.shape)*0).tolist()
        self.etaI0  = (np.ones(self.I0i.shape)*1).tolist()
        self.etaI1  = (np.ones(self.I1i.shape)*1).tolist()
        self.etaJ1  = (np.ones(self.J1i.shape)*1).tolist()

    def define_eta_boundaries(self):
        c = [self.etaI0,self.etaJ1,self.etaI1,self.etaJ0]
        self.etabounds = self.g_matrix_flat(c)


    def write_boundaries(self,x,fmto,columns):
        """this function is used in write_eta_boundaries"""
        for j,i in enumerate(x):
            self.f1.write(fmto % i)
            print j
            print len(x)
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
            for i in a.r.T:
                self.f1.write('%5.0f' % i[0])
                self.f1.write('%5.0f' % i[1])
                for j in i[2:]:
                    self.f1.write('%5.2f' % j)
                self.f1.write('\n')
        self.f1.close()
