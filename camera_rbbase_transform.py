import numpy as np

class Transform():
    def __init__(self):
        pass

    def transform_matrix():
        tf_mat = np.eye(4)
        return tf_mat
    def rot_mat_x(phi):
        rot_mat = np.eye(3)
        rot_mat[1,1] = np.cos(phi)
        rot_mat[1,2] = -np.sin(phi)
        rot_mat[2,1] = np.sin(phi)
        rot_mat[2,2] = np.cos(phi)
        return rot_mat
    def rot_mat_y(theta):
        rot_mat = np.eye(3)
        rot_mat[0,0] = np.cos(theta)
        rot_mat[0,2] = np.sin(theta)
        rot_mat[2,0] = -np.sin(theta)
        rot_mat[2,2] = np.cos(theta)
        return rot_mat
    def rot_mat_z(psi):
        rot_mat = np.eye(3)
        rot_mat[0,0] = np.cos()
        rot_mat[0,2] = np.sin(psi)
        rot_mat[2,0] = -np.sin(psi)
        rot_mat[2,2] = np.cos(psi)
        return rot_mat
    
    def cam_2_rb(self,rx, ry ,rz):
        cam_rb_tf = self.transform_matrix()
        cam_rb_tf[0, 3] = rx
        cam_rb_tf[1, 3] = ry
        cam_rb_tf[2, 3] = rz
        return  
    
    def obj_2_cam(self, rx, ry , rz, w, p ,r):
        obj_cam_tf = self.transform_matrix()
        # set translation
        obj_cam_tf[0,3] = rx
        obj_cam_tf[1,3] = ry
        obj_cam_tf[2,3] = rz
        # create rotation matrix
        rot_mat = self.rot_mat_x(w)@self.rot_mat_y(p)@self.rot_mat_z(r)
        obj_cam_tf[0:3, 0:3] = rot_mat
        return obj_cam_tf
    