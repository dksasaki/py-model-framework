from model_class import secom_interface as si
from model_class.read_class import secom_read_data
import model_class.initial_conditions as ic
import numpy as np

a = si.secom()
a.find_boundaries()
a.boundaries_nearest_neighbors()

c = secom_read_data()
ndepths = 5

T=[27.59,27.59,26.88,25.57,23.02,21.76,20.26,18.73,15.99,12.43,
                                      9.10,6.19,3.40,3.70,3.70]; T = T[:ndepths]
S=[36.87,36.87,36.90,36.93,36.95,36.85,36.69,36.42,35.79,35.27,34.81,
                                       34.51,34.51,34.94,34.94]; S = S[:ndepths]


"""
takes gcmplt.cdf variables and the nested model_grid boundary location
and creates the TS boundaries for model_grid
"""
a.TS_boundaries_heter(ndepths,'TS_bounds')



"""
takes the T S variables and the nested model_grid boundary location
and creates the TS boundaries for model_grid
"""
a.TS_boundaries_homog(ndepths,T,S,'homog_bound')





"""
Creates the initial T and S conditions for the whole mode_grid 
"""
i_cond = ic.secom_initial_conditions()
i_cond.write_init_tands(T,S,ndepths) #write init_tands



"""
Creates eta boundariy conditions
"""
output_file='eta_bound'
etab = si.secom()
etab.eta_boundaries(output_file)

etab.etaI0 = np.array(etab.etaI0)*0
etab.etaI1 = np.array(etab.etaI1)*0
etab.etaJ1 = np.array(etab.etaJ1)*(-0.01)

etab.define_eta_boundaries()
etab.write_eta_boundaries(output_file)