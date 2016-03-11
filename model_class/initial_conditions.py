from model_class.grid_class import secom_read
import numpy as np

class secom_initial_conditions(secom_read):
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
        super(secom_initial_conditions, self).__init__()
        self.depth_homog = lambda T,KSL: np.ones(KSL)*T
        self.init_var = lambda T,KSL,m,n : np.matlib.repmat(self.depth_homog(T,KSL),m+2,n+2).reshape(m+2,n+2,len(self.depth_homog(T,KSL))) #2 is summed in order to compensate the -2 in self.g

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


