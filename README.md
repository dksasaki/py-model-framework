# py-model-framework 
This framework creates the input data for our model.
It is written in Python.

### INPUT DATA REQUIREMENTS
It requires:
netcdf model output (coarser\_grid\_output directory):
*      model coordinates indexes
*      model coordinates
*      temperature results
*      salinity results
*      eta results

model\_grid (input\_data directory):
*    model\_grid file (see ECOMSED manual):
*     model_grid requires all the points in the I,J domain 

If you want to install python packages in a very simple way, click [here](docs/python_install.md)

### WHAT CAN BE DONE WITH THIS FRAMEWORK?
It is possible (for eta and TS):
*  to nest data from the netcdf model output into the model\_grid boundaries and initial\_conditions.
*  to create homogenous boundaries.

Time changing nesting will be implemented. 

The required libraries are numpy, matplotlib, xray, basemap, scipy. 


