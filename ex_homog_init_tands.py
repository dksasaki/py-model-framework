import numpy as np
import matplotlib.pyplot as plt
import model_class.initial_conditions as ic

ndepths = 15
T=[27.59,27.59,26.88,25.57,23.02,21.76,20.26,18.73,15.99,12.43,
                                      9.10,6.19,3.40,3.70,3.70];
S=[36.87,36.87,36.90,36.93,36.95,36.85,36.69,36.42,35.79,35.27,34.81,
                                       34.51,34.51,34.94,34.94];


i_cond = ic.secom_initial_conditions()
i_cond.write_init_tands(T,S,ndepths)