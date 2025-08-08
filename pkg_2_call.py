from handler import handlerDict
from FRC_ import FRC_
import json



class MotionMethod():
    def __init__(self, sequence, sock=None):
        self.handler = handlerDict()
        self.getPackage = FRC_()
        self.sequence = sequence
        self.curr_x, self.curr_y, self.curr_z, self.curr_w, self.curr_p, self.curr_r = 0.0, 0.0, 0.0, 0.0, 0.0, 0.0
        self.curr_j1, self.curr_j2, self.curr_j3, self.curr_j4, self.curr_j5, self.curr_j6 = 0.0, 0.0, 0.0, 0.0, 0.0, 0.0
        self.UtoolNumber = 1
        self.UFrameNumber = 1
        self.sequenceDiff = 0
        pass

    def linear_move(self, x, y, z=None, w=None, p=None, r=None, uFrameNumber=None, uToolNumber=None):
        self.curr_x, self.curr_y, self.curr_z = x, y, z
        self.curr_w, self.curr_p, self.curr_r = w, p, r
    # Prepare the motion package
        if z is None:
            z = self.curr_z
        if w is None:
            w = self.curr_w
        if p is None:
            p = self.curr_p
        if r is None:
            r = self.curr_r
        if uFrameNumber is None:
            uFrameNumber = self.UFrameNumber
        if uToolNumber is None:
            uToolNumber = self.UtoolNumber
        # Update current position
        
        motion_pkg = self.getPackage.LinearMotion(
            self.sequence, uFrameNumber, uToolNumber,
            x, y, z, w, p, r
        )
        # If motion_pkg is bytes, decode and load as dict
        if isinstance(motion_pkg, bytes):
            motion_pkg = motion_pkg.decode('utf-8')
            motion_pkg = json.loads(motion_pkg)
        return motion_pkg

    def joint_motion(self, x, y, z, w, p, r, uFrameNumber=None, uToolNumber=None): 
        self.curr_x, self.curr_y, self.curr_z = x, y, z
        self.curr_w, self.curr_p, self.curr_r = w, p, r
        if uFrameNumber is None:
            uFrameNumber = self.UFrameNumber
        if uToolNumber is None:
            uToolNumber = self.UtoolNumber
        motion_pkg = self.getPackage.JointMotion(
            self.sequence, uFrameNumber, uToolNumber, self.curr_x, self.curr_y, self.curr_z, self.curr_w, self.curr_p, self.curr_r
        )
        # If motion_pkg is bytes, decode and load as dict
        if isinstance(motion_pkg, bytes):
            motion_pkg = motion_pkg.decode('utf-8')
            motion_pkg = json.loads(motion_pkg)
        return motion_pkg
    
    def joint_motion_relative(self, j1, j2, j3, j4, j5, j6, uFrameNumber=None, uToolNumber=None):
        self.curr_j1 = j1
        self.curr_j2 = j2
        self.curr_j3 = j3
        self.curr_j4 = j4
        self.curr_j5 = j5
        self.curr_j6 = j6
        if uFrameNumber is None:
            uFrameNumber = self.UFrameNumber
        if uToolNumber is None:
            uToolNumber = self.UtoolNumber
        motion_pkg = self.getPackage.JointMotionRelative(
            self.sequence, uFrameNumber, uToolNumber,
            self.curr_j1, self.curr_j2, self.curr_j3,
            self.curr_j4, self.curr_j5, self.curr_j6
        )
        # If motion_pkg is bytes, decode and load as dict
        if isinstance(motion_pkg, bytes):
            motion_pkg = motion_pkg.decode('utf-8')
            motion_pkg = json.loads(motion_pkg)
        return motion_pkg

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







