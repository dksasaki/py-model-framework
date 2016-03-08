from grid_class import secom_read
import numpy as np

class secom_initial_conditions(secom_read):
    """This class creates init_tands"""
    def define_grid_cells_hor_homog(self,KSL,T,S):
        """
        KSL: number of sigma levels
        T  : temperature array
        S  : salinity array
        """
        self.T1 = np.ones(KSL)*T
        self.S1 = np.ones(KSL)*S

    def define_grid_TS_values(self):
        m,n = self.i_g_greater(4,0).shape
        self.init_T = np.matlib.repmat(self.T1,m+2,n+2).reshape(m+2,n+2,len(self.T1)) #2 is summed in order to compensate the -2 in self.g
        self.init_S = np.matlib.repmat(self.S1,m+2,n+2).reshape(m+2,n+2,len(self.T1))

    def write_init_tands(self):
        self.f1 = open('init_tands','w+')
        y, x ,z = self.init_T.shape

        for j in range(y):
            for i in range(x):
                self.f1.write('%5.0f' % (j+1))
                self.f1.write('%5.0f' % (i+1))
                for k in self.init_T[j,i,:]:
                    self.f1.write('%5.2f' % k)
                for k in self.init_S[j,i,:]:
                    self.f1.write('%5.2f' % k)

                self.f1.write('\n')

        self.f1.close()


