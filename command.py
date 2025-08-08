from handler import handlerDict
from FRC_ import FRC_



class Command:
    def __init__(self):
        self.handler = handlerDict()
        self.getPackage = FRC_()
        pass
    def button_reset(self):
        pkg = self.getPackage.Reset()
        pkg = self.handler.dict_to_json(pkg)
        return pkg
    
    def button_connect(self):
        pkg = self.getPackage.Connect()
        pkg = self.handler.dict_to_json(pkg)
        return pkg

    def button_pause(self):
        pkg = self.getPackage.Pause()
        pkg = self.handler.dict_to_json(pkg)
        return pkg

    def button_abort(self):
        pkg = self.getPackage.Abort()
        pkg = self.handler.dict_to_json(pkg)
        return pkg

    def button_continue(self):
        pkg = self.getPackage.Continue()
        pkg = self.handler.dict_to_json(pkg)
        return pkg
       

    def button_disconnect(self):
        pkg = self.getPackage.Disconnect()
        pkg = self.handler.dict_to_json(pkg)
        return pkg
 

    def button_get_status(self):
        pkg = self.getPackage.GetStatus()
        pkg = self.handler.dict_to_json(pkg)
        return pkg

    def button_get_curr_pos(self):
        pkg = self.getPackage.ReadCartesianPosition()
        pkg = self.handler.dict_to_json(pkg)
        return  pkg

    def button_initialize(self):
        pkg = self.getPackage.Initialize()
        pkg = self.handler.dict_to_json(pkg)
        return pkg