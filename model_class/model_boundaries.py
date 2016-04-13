import matplotlib.pyplot as plt
import numpy as np
from scipy import interpolate

class eta(object):
    #def __init__(self):
    #    boundaries.__init__(self)

    def define_eta_boundaries_i(self):
        """
        This script uses the results of self.boundaries_grid
        """
        #self.bounds_eta_i = []
        #self.find_boundaries()
        c = map(self.g_T_flatten,[self.J0,self.I0,self.J1,self.I1])
        self.bounds_eta_i = self.g_matrix_flat(c)


    def define_eta_boundaries_homog(self):
        """
        This script uses the results of self.eta_boundaries_values
        """
        #self.define_eta_boundaries_i()
        c = [self.etaJ0,self.etaI0,self.etaJ1,self.etaI1]
        self.etabounds = self.g_matrix_flat(c)

    def define_eta_boundaries_heter(self,var):
        """
        This script uses the results of self.eta_boundaries_values
        """
        #self.define_eta_boundaries_i()
        c = [self.etaJ0,self.etaI0,self.etaJ1,self.etaI1]
        self.etabounds = var


    def define_eta_boundaries_values(self):
        """
        This script uses the results of self.boundaries_coordinates
        """
        self.etaJ0  = (np.ones(self.jmin.shape[0])).tolist()
        self.etaI0  = (np.ones(self.imin.shape[0])).tolist()
        self.etaI1  = (np.ones(self.imax.shape[0])).tolist()
        self.etaJ1  = (np.ones(self.jmax.shape[0])).tolist()

    def write_boundaries(self,x,fmto,columns):
        """this function is used in write_eta_boundaries"""
        for j,i in enumerate(x):
            self.f1.write(fmto % i)
            #print j
            #print len(x)
            if (j+1) % columns == 0 and (j!=len(x)-1):
                self.f1.write('\n')

    def write_eta_boundaries(self,f_name):
        print f_name
        self.f1 = open(f_name,'w+')
        self.f1.write("%5.0f DATA\n" % (len(self.bounds_eta_i)/4))
        self.write_boundaries(self.bounds_eta_i,'%5.0f',16)
        
        for i in [0,725]:
            self.f1.write('\n%10.5f\n' % i)
            self.write_boundaries(self.etabounds,'%10.5f',8)
        self.f1.close()

    def interpolate_coarser2finer_2D(self,x,y,xi,yi,Var,I):
        aux = np.array([Var[i[0],i[1]] for i in I]) #T in a.ann_i sites
        Vari = interpolate.griddata((x,y),aux,(xi,yi),method='linear')

        return Vari



class TS(object):
    #def __init__(self):
    #    boundaries.__init__(self)

    def define_TS_boundaries_i(self):
        #self.find_boundaries()
        self.bounds_TS_i = [self.xb_i,self.yb_i]

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

    def define_TS_values_homog(self,T,S,ndepths):
        """
        First 15 columns of self.TSbounds: temperature
        Last  15 columns of self.TSbounds: salinity
        """
        for i in range(self.n_boundaries):
            self.TSbounds[0:ndepths,i] = T
            self.TSbounds[ndepths:,i]  = S

    def define_TS_values_heter(self,T,S,ndepths):
        self.define_TS_values(ndepths)
        self.TSbounds[0:ndepths,:] = T
        self.TSbounds[ndepths:,:]   = S

    def interpolate_coarser2finer_3D(self,x,y,xi,yi,Var,I):
        aux = np.array([Var[:,i[0],i[1]] for i in I]) #T in a.ann_i sites
        d   = aux.shape[1]
        print aux
        Vari= np.zeros((xi.shape[0],d))
        for i in range(d):
            Vari[:,i] = interpolate.griddata((x,y),aux[:,i],(xi,yi),method='linear')

        return Vari

    #def interpolate_coarser2finerTS(self,x,y,xi,yi,T,S,I):
    #    aux = np.array([T[:,i[0],i[1]] for i in I]) #T in a.ann_i sites
    #    var = np.zeros((xi.shape[0],aux.shape[1],2))
    #    print(var.shape)
    #    for j,i in enumerate([T,S]):
    #        for k in range(aux.shape[1]):
    #            ginterp = self.interpolate_coarser2finer(x,y,xi,yi,i,I)
    #            var[:,k,j] = ginterp
    #    return var


    def define_TS_boundaries(self):
        #run define_TS_values before this one
        self.TSbounds = self.TSbounds.tolist()

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
                #print('%5.0f,%5.0f' % (i[0],i[1]))
                self.f1.write('%5.0f' % i[1])
                self.f1.write('%5.0f' % i[0])
                for j in i[2:]:
                    self.f1.write('%5.2f' % j)
                    #print('%5.2f' % j)
                self.f1.write('\n')
        self.f1.close()

class boundaries(eta,TS):
    def __init__(self):
        eta.__init__(self)
        TS.__init__(self)
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
        #creates the "boundary grid"
         self.Imax = self.direc_max_bound(im,jn,im,dep).astype('int')
         self.Jmax = self.direc_max_bound(im,jn,jn,dep).astype('int')
         self.Imin = self.direc_min_bound(im,jn,im,dep).astype('int')
         self.Jmin = self.direc_min_bound(im,jn,jn,dep).astype('int')

         self.I1 = self.boundaries(self.Imax,0,-1) #boundaries grid coordinate
         self.J1 = self.boundaries(self.Jmax,-1,0) #boundaries grid coordinate
         self.I0 = self.boundaries(self.Imin,0,1) #boundaries grid coordinate
         self.J0 = self.boundaries(self.Jmin,1,0) #boundaries grid coordinate

    def boundaries_coordinates(self,im,jn,lon,lat,dep):
        #boundaries coordinates [lon,lat] values
         self.xmax = self.direc_max_bound(lon,lat,im,dep)
         self.ymax = self.direc_max_bound(lon,lat,jn,dep)
         self.xmin = self.direc_min_bound(lon,lat,im,dep)
         self.ymin = self.direc_min_bound(lon,lat,jn,dep)

         self.imax = self.direc_max_bound(im,jn,im,dep) #boundaries indexes
         self.jmax = self.direc_max_bound(im,jn,jn,dep) #boundaries indexes
         self.imin = self.direc_min_bound(im,jn,im,dep) #boundaries indexes
         self.jmin = self.direc_min_bound(im,jn,jn,dep) #boundaries indexes

         print self.ymin
         for i in [self.xmax,self.ymax,self.xmin,self.ymin]:
            if i.sum() != 0:
                 plt.plot(i[:,0], i[:,1],'.')

         bound = np.array(self.ymin.tolist()+self.xmin.tolist()+self.ymax.tolist()+self.xmax.tolist())
         self.xb = bound[:,0] #boundaries coordinates
         self.yb = bound[:,1] #boundaries coordinates

         bound = np.array(self.jmin.tolist()+self.imin.tolist()+self.jmax.tolist()+self.imax.tolist())
         self.xb_i = bound[:,0] #boundaries coordinates
         self.yb_i = bound[:,1] #boundaries boundaries_coordinates