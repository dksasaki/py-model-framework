import xray as xr
import matplotlib.pyplot as plt
import numpy as np
import model_class.model_boundaries as mb
import model_class.read_class as rc
from scipy.spatial import kdtree as kd

plt.ion()

a = mn.secom_nesting()
a.boundaries_location()
a.nearest_boundaries_location()


plt.plot(a.g_mask(a.c('lon'),0),a.g_mask(a.c('lat'),0),'k')
plt.plot(a.g_mask(a.c('lon'),0).T,a.g_mask(a.c('lat').T,0),'k')
plt.plot(a.xb,a.yb,'.m')
plt.plot(a.d[:,0],a.d[:,1],'.r',linewidth=3)
