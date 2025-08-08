from handler import handlerDict

handler = handlerDict()
# create a dictionary from text file
with open('from_manual.txt', 'r') as file:
    file_content = file.read()
    dict = handler.json_to_dict(file_content)


class FRC_():
    def __init__(self):
        self.dict = dict
        
    # communication
    def Connect(self):
        pkg = self.dict['FRC_Connect']
        return pkg
    
    def Disconnect(self):
        pkg = self.dict['FRC_Disconnect']
        return pkg
    
    def Terminate(self):
        pkg = self.dict['FRC_Terminate']
        return pkg
    
    # command
    
    def Initialize(self, GroupMask = 1, RTSA = 'ON'):
        pkg = self.dict['FRC_Initialize']
        pkg['GroupMask'] = GroupMask
        pkg['RTSA'] = RTSA
        return pkg
    
    def Abort(self):
        pkg = self.dict['FRC_Abort']
        return pkg
    
    def Pause(self):
        pkg = self.dict['FRC_Pause']
        return pkg
    
    def Continue(self):
        pkg = self.dict['FRC_Continue']
        return pkg
    
    def Reset(self):
        pkg = self.dict['FRC_Reset']
        return pkg
    
    def SetUFrameUTool(self, UFrameNumber = 1, UToolNumber =1):
        pkg = self.dict['FRC_SetUFramUTool']
        pkg['UFrameNumber'] = UFrameNumber
        pkg['UToolNumber'] = UToolNumber
        return pkg
    
    def GetStatus(self):
        pkg = self.dict['FRC_GetStatus']
        return pkg
    
    def ReadCartesianPosition(self, group=1):
        pkg = self.dict['FRC_ReadCartesianPosition']
        pkg['group'] = group
        return pkg
    
    def ReadJointAngles(self, group=1):
        pkg = self.dict['FRC_ReadJointAngles']
        pkg['group'] = group
        return pkg
    
    # instruction
    def LinearMotion(self,sequence,UFrameNum, UToolNum, x , y ,z, w, p, r):
        pkg = self.dict['FRC_LinearMotion']
        pkg['SequenceID'] = sequence
        pkg['Configuration']["UFrameNumber"] = UFrameNum
        pkg['Configuration']['UToolNumber'] = UToolNum
        pkg['Position']['X'] = x
        pkg['Position']['Y'] = y
        pkg['Position']['Z'] = z
        pkg['Position']['W'] = w
        pkg['Position']['P'] = p
        pkg['Position']['R'] = r
        return pkg
    
    def JointMotion(self, sequence, UFrameNum, UToolNum, x, y, z, w, p, r):
        pkg = self.dict['FRC_JointMotion']
        pkg['SequenceID'] = sequence
        pkg['Configuration']["UFrameNumber"] = UFrameNum    
        pkg['Configuration']['UToolNumber'] = UToolNum
        pkg['Position']['X'] = x
        pkg['Position']['Y'] = y
        pkg['Position']['Z'] = z
        pkg['Position']['W'] = w
        pkg['Position']['P'] = p
        pkg['Position']['R'] = r
        return pkg
    def JointMotionRelative(self, sequence, UFrameNum, UToolNum, j1, j2, j3, j4, j5, j6):
        pkg = self.dict['FRC_JointRelative']
        pkg['SequenceID'] = sequence
        pkg['Configuration']["UFrameNumber"] = UFrameNum    
        pkg['Configuration']['UToolNumber'] = UToolNum
        pkg['Position']['J1'] = j1
        pkg['Position']['J2'] = j2
        pkg['Position']['J3'] = j3
        pkg['Position']['J4'] = j4
        pkg['Position']['J5'] = j5
        pkg['Position']['J6'] = j6
        return pkg

    def Call(self, method_name, sequence_id=1):
        pkg = self.dict['FRC_Call']
        pkg['ProgramName'] = method_name
        pkg['SequenceID'] = sequence_id
        return pkg
          

