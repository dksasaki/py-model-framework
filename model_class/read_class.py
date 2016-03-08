import xray as xr
import matplotlib.pyplot as plt
import numpy as np

class secom_read_data(object):
    """Reads secom's nc RESULTS
    self.c(var): recovers the dataset's coordinates
    self.v(t,d,var): recovers the dataset's coordinates ()
    t   = time index
    d   = depth index
    var = variable/coordinate name (string format)
    """
    def __init__(self):
        self.f = xr.open_dataset('/home/otel/Dropbox/trabalho_irado/Doutorado/MODEL/RESULTS/gcmplt.cdf')
        self.c = lambda var :     self.f[var] #coordinates
        self.v = lambda t,d,var : self.f[var].data[t,d,:,:]

if __name__='__main__':

    plt.close('all')
    plt.ion()
