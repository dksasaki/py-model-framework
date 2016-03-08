import numpy as np
import matplotlib.pyplot as plt
import model_class.model_boundaries as mb

output_file = 'eta_bound'


etab = mb.secom_model_boundaries()
etab.define_eta_values()

etab.etaI0 = np.array(etab.etaI0)*0
etab.etaI1 = np.array(etab.etaI1)*0
etab.etaJ1 = np.array(etab.etaJ1)*(-0.01)

a.define_eta_boundaries()
a.write_eta_boundaries(output_file)