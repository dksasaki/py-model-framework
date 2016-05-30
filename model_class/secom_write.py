import numpy as np

class secom_write(object):

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



class data_group_e(object):

    def comment(self):
        pass

    def initial_TS_data_op(self):
        """
        OPTTSI = "FIXED" - initial temperature and salinity data are constant for each standard level.
                 "DATA"  - initial temperature and salinity vary horizontally and vertically - data read in from data file "init_tands"
        """

    def initial_TorS_data(self):
        """
        TSI = temperature in oC
        SSI = salinity in psu

        *DRY (don't repeat yourself) principle replaces TSI and SSI for var in this method
        """

class initial_condition(object):
    def __init__(self):
        self.f1 = open('init_tands','w+')

    def write_init_tands(self,x,y,T,S,KSL):
        """
        I = number of grid element in direction 1
        j = number of grid element in direction 2
        TS= temperature in o C at each standard level
        SS=salinity in psu at each standard level
        """

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



class data_group_f_1(object):
    def __init__(self,f_name):
        self.f1 = open(f_name,'w+')

    def comment(self):
        pass
    def number_grid_elements(self):
        """
        Writes NUMEBC
        NUMEBC  =total number of elevation boundary grid elements.
        If NUMEBC = 0,then go to Data Group G (Discharge Information)
        """
        #self.NUMEBC = len(self.bounds_eta_i)/4
        self.f1.write("%5.0f DATA\n" % (self.NUMEBC))

    def loc_grid_elements(self):
        self.write_boundaries(self.bounds_eta_i,'%5.0f',16)

    def time_observation(self,i):
        """
        WRITES TIME
        TIME = time in hours
               0.0 for initial time
        """
        self.f1.write('\n%10.5f\n' % i)

    def elevation_data(self,etabounds):
        self.write_boundaries(etabounds,'%10.5f',8)

    def write_boundaries(self,x,fmto,columns):
        """this function is used in write_eta_boundaries"""
        for j,i in enumerate(x):
            self.f1.write(fmto % i)
            if (j+1) % columns == 0 and (j!=len(x)-1):
                self.f1.write('\n')

    def file_close(self):
        self.f1.close()

class data_group_f_2(object):
    def __init__(self,f_name):
        self.f1 = open(f_name,'w+')

    def comment(self):
        self.f1.write('\nTS\n')

    def time_observation(self,i):
        """
        WRITES TIME
        TIME = time in hours
               0.0 for initial time
        """
        self.f1.write('%10.5f\n' % i)

    def write_TS_boundaries(self,ITAS,JTAS,TBDRYSL,SBDRYSL):
        """
        ITAS = i number of grid element where temperature and salinity are specified
        JTAS = j number of grid element where temperature and salinity are specified
        TBDRYSL = temperature in oC at time "TIME" for each standard level
                   (not sigma level)
        SBDRYSL = salinity in psu at time "TIME" for each standard level (not sigma level)
        """


        q =map(np.array,[np.array([ITAS,JTAS]),np.append(self.TBDRYSL,self.SBDRYSL,axis=1)])
        print q[0].shape
        print q[1].shape
        self.r = np.concatenate((q[0],q[1].T), axis = 0)
        r1 = self.g_T_flatten(self.r)

        for i in self.r.T:
            #print('%5.0f,%5.0f' % (i[0],i[1]))
            self.f1.write('%5.0f' % i[1])
            self.f1.write('%5.0f' % i[0])
            print i[0],i[1]
            for j in i[2:]:
                self.f1.write('%5.2f' % j)
                #print('%5.2f' % j)
            self.f1.write('\n')

    def TS_boundaries_values(self,ITAS,JTAS,TBDRYSL,SBDRYSL,TIME):
        self.time_observation(TIME)
        self.write_TS_boundaries(ITAS,JTAS,TBDRYSL,SBDRYSL)


    def file_close(self):
        self.f1.close()
