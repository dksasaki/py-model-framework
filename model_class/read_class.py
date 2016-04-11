import xray as xr
import matplotlib.pyplot as plt
import numpy as np
import model_class.model_boundaries as mb

class secom_read_data(object):
    """Reads secom's nc RESULTS
    self.c(var): recovers the dataset's coordinates
    self.v(t,d,var): recovers the dataset's coordinates ()
    t   = time index
    d   = depth index
    var = variable/coordinate name (string format)
    """

    def __init__(self):
        self.f_xr = xr.open_dataset('/home/otel/Dropbox/trabalho_irado/Doutorado/MODEL/RESULTS/gcmplt.cdf')
        self.c = lambda var :     self.f_xr[var].data #coordinates
        self.v = lambda t,d,var : self.f_xr[var][t,d,:,:].data
        self.g_mask = lambda f,m : np.ma.masked_array(f,mask = [f==m])
        self.v_sb_smpl = lambda t,d,lon,lat,var : self.f_xr[var][t,d,:,:][lat,:][:,lon].data
        self.v_smpl_mrg= lambda f1,f2,ax : np.concatenate(f1,f2,axis=ax)
        
    
        
