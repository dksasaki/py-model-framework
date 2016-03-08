from mpl_toolkits.basemap import Basemap
import numpy as np
import matplotlib.pyplot as plt

class mapa(object):
    """Those examples of objects meridional and zonal limits"""
    def __init__(self):
        self.lon0 = None
        self.lat0 = None
        self.lonF = None
        self.latF = None
        self.map =  lambda : Basemap(projection='mill',lat_ts=10,llcrnrlon=self.lon0, urcrnrlon=self.lon1, llcrnrlat=self.lat0, urcrnrlat=self.lat1, resolution=self.res)

    def Araca(self):
        self.lat0 = -23.9
        self.lat1 = -23.7
        self.lon0 = -45.5
        self.lon1 = -45.3
        self.res  = 'f'
        self.parallel = [-23.75,-23.85]
        self.meridian = [-45.45,-45.35]
        self.map = self.mapa()

    def Canal_ssb(self):
        self.lat0 = -23.9
        self.lat1 = -23.7
        self.lon0 = -45.5
        self.lon1 = -45.3
        self.res  = 'f'
        self.parallel = [-23.75,-23.85]
        self.meridian = [-45.45,-45.35]
        self.map = self.mapa()

    def Embaiamento_sp(self):
        #boundaries - mill
        self.lat0 = -30
        self.lat1 = -21
        self.lon0 = -50
        self.lon1 = -40
        #basemap
        self.res  = 'h'
        self.parallel = [-27,-24]
        self.meridian = [-47,-43]
        self.map = self.mapa()

    def Sp_coast(self):
        #boundaries - mill
        self.lat0 = -26.5
        self.lat1 = -22.5
        self.lon0 = -49
        self.lon1 = -43.5
        #basemap
        self.res  = 'h'
        self.parallel = [-25,-23]
        self.meridian = [-48,-46,-44]
        self.map = self.mapa()
