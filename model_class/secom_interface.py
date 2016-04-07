from model_class.grid_class import secom_read
from model_class.read_class import secom_read_data
from model_class.model_boundaries import model_boundaries
from model_class.model_nesting import model_nesting
import model_class.model_boundaries as mb

class secom(model_nesting,secom_read,secom_read_data,model_boundaries):
    def __init__(self):
         model_nesting.__init__(self)
         secom_read.__init__(self)
         secom_read_data.__init__(self)
         model_boundaries.__init__(self)
         self.find_boundaries()
        

    def find_boundaries(self):
         self.boundaries_coordinates(self.g(1),self.g(0),self.g(7),self.g(6),self.g(4))
         self.boundaries_grid(self.g(1),self.g(0),self.g(7),self.g(6),self.g(4))

    def eta_boundaries(self,output_file):
        print output_file
        self.define_eta_boundaries_values()
        self.define_eta_boundaries_i()
        self.define_eta_boundaries()
        self.write_eta_boundaries(output_file)

    def TS_boundaries(self,ndepths,T,S,output_file):
        self.define_TS_boundaries_i()
        self.define_TS_values(ndepths)
        self.define_TS_values_homog(T,S)
        self.define_TS_boundaries()
        self.write_TS_boundaries(output_file)

    def nearest_boundaries(self):
         self.nearest_boundaries_location(self.c('lon'),self.c('lat'))

    def boundaries_nearest_neighbors(self):
         self.all_neigbours_nearest_i_bl(self.mdi,self.c('xpos'))
         self.all_neigbours_nearest_bl(self.c('lon'),self.c('lat'))
