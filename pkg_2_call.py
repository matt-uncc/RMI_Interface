from handler import handlerDict
from FRC_ import FRC_



class MotionMethod:
    def __init__(self, sequence):
        self.handler = handlerDict()
        self.getPackage = FRC_()
        self.sequence = sequence
        pass

    def linear_move(self, x, y, z, w, p, r):
        motion_package = self.getPackage.LinearMotion(self.sequence, x, y, z, w, p, r)
        pkg = self.handler.dict_to_json(motion_package)
        return pkg

    # def joint_move(self,sequence, j1, j2, j3, j4, j5, j6):
    #     motion_package = self.getPackage.JointMotion(sequence, j1, j2, j3, j4, j5, j6)
    #     pkg = self.handler.dict_to_json(motion_package)
    #     return pkg

    # def linear_relative(self, sequence, x, y, z, w, p, r):
    #     motion_package = self.getPackage.LinearRelativeMotion(sequence, x, y, z, w, p, r)
    #     pkg = self.handler.dict_to_json(motion_package)
    #     return pkg
    
    # def joint_relative(self, sequence, j1, j2, j3, j4, j5, j6):
    #     motion_package = self.getPackage.JointRelativeMotion(sequence, j1, j2, j3, j4, j5, j6)
    #     pkg = self.handler.dict_to_json(motion_package)
    #     return pkg

    # def read_cartesian_position(self):
    #     pkg = self.getPackage.ReadCartesianPosition()
    #     pkg = self.handler.dict_to_json(pkg)
    #     return pkg
    














































# joint move

# def joint_move(j1, j2, j3, j4, j5, j6):
#     motion_package = getPackage.JointMotion(sequence, j1, j2, j3, j4, j5, j6)
#     pkg = handler.dict_to_json(motion_package)
#     return pkg





# def button_get_curr_pos():
#     pkg = getPackage.ReadCartesianPosition()
#     pkg = handler.dict_to_json(pkg)
#     rcvd = send_pkg(pkg)
#     update_position(rcvd)
#     return   

# def update_position(pkg):
#     global motion_data  # Avoid using 'dict' as a variable name
#     data = handler.json_to_dict(pkg)
#     print(data)

#     config = data.get('Configuration', {})
#     pos = data.get('Position', {})

#     lm = motion_data.setdefault('FRC_LinearMotion', {})
#     lm['UToolNumber'] = config.get('UToolNumber')
#     lm['UFrameNumber'] = config.get('UFrameNumber')
#     lm['Front'] = config.get('Front')
#     lm['Up'] = config.get('Up')
#     lm['Left'] = config.get('Left')
#     lm['Flip'] = config.get('Flip')
#     lm['Turn4'] = config.get('Turn4')
#     lm['Turn5'] = config.get('Turn5')
#     lm['Turn6'] = config.get('Turn6')



#     position = lm.setdefault('Position', {})
#     position['X'] = str(round(pos.get('X', 0.0), 3))
#     position['Y'] = str(round(pos.get('Y', 0.0), 3))
#     position['Z'] = str(round(pos.get('Z', 0.0), 3))
#     position['W'] = str(round(pos.get('W', 0.0), 3))
#     position['P'] = str(round(pos.get('P', 0.0), 3))
#     position['R'] = str(round(pos.get('R', 0.0), 3))

#     # Clear and insert rounded values into GUI text boxes
#     x_text.delete(0, 'end')
#     x_text.insert(0, str(position['X']))

#     y_text.delete(0, 'end')
#     y_text.insert(0, str(position['Y']))

#     z_text.delete(0, 'end')
#     z_text.insert(0, str(position['Z']))

#     w_text.delete(0, 'end')
#     w_text.insert(0, str(position['W']))

#     p_text.delete(0, 'end')
#     p_text.insert(0, str(position['P']))

#     r_text.delete(0, 'end')
#     r_text.insert(0, str(position['R']))



#     return

            






# def get_sequenceID(pkg):
#     global sequence
#     dict = handler.json_to_dict(pkg)
#     for item in dict:
#         if item == 'NextSequenceID':
#             sequence = dict['NextSequenceID']
#     return sequence







