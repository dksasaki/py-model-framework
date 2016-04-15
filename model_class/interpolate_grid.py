from scipy import interpolate
import numpy as np

class interpolations(object):

    def interpolate_coarser2finer_2D(self,x,y,xi,yi,Var,I):
        aux = np.array([Var[i[0],i[1]] for i in I]) #T in a.ann_i sites
        Vari = interpolate.griddata((x,y),aux,(xi,yi),method='linear')

        return Vari

    def interpolate_coarser2finer_2D_depth(self,x,y,xi,yi,Var,I):
        aux = np.array([Var[:,i[0],i[1]] for i in I]) #T in a.ann_i sites
        d   = aux.shape[1]
        Vari= np.zeros((xi.shape[0],d))
        for i in range(d):
            Vari[:,i] = interpolate.griddata((x,y),aux[:,i],(xi,yi),method='linear')

        return Vari

    def interpolate_in_depth(self,z,zi,Var):
        shp = Var.shape
        ndepths = z.size

        shp1= [shp[0],ndepths]

        im, zm = np.meshgrid(np.arange(shp[0]),z)
        imi, zmi = np.meshgrid(np.arange(shp[0]),zi)

        im = im.T.ravel()
        zm= zm.T.ravel()

        imi = imi.T.ravel()
        zmi= zmi.T.ravel()

        Vari = interpolate.griddata((im,zm),Var.ravel(),(imi,zmi)).reshape(shp[0],zi.size)

        return Vari

    def interpola(self,x,y,xi,yi,var,ndepths):
        Vari = np.zeros((xi.shape[0],ndepths))

        for k in range(ndepths):
            Vari[:,k] = interpolate.griddata((x,y),var[k,:,:].ravel(),(xi,yi),method='nearest')
        Vari[Vari==Vari.min()]=Vari.max()
        return Vari


    def interpolate_in_depth2(self,z,zi,Var):
        shp = Var.shape

        b = lambda x : [i for i in Var[x,:]]

        vari = []
        for i in range(shp[0]):
            q = interpolate.interp1d(z,b(i))
            vari.append(q(zi))

        return np.array(vari)
