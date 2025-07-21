import json

class handlerDict:
    def __init__(self):
        pass
    
    # test_dict =  {"Command" : "FRC_SetUFrameUTool", 
    #             "UFrameNumber" : 1, 
    #             "UToolNumber" : 1,
    #             "Group":1
    #             }


    # convert data to dict
    def json_to_dict(self, pkg):
        if pkg is not None:
            dict = json.loads(pkg)
        else:
            dict = {}
        return dict
    
    # convert dict to data
    def dict_to_json(self, pkg):
        dict = json.dumps(pkg).strip() + '\r\n'
        return dict
    # find method in the dict
    def find_method(self, entire_dict, key):
        called_method_dict = entire_dict[key]
        return called_method_dict




  




