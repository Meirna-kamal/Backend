from natsort import natsorted
import os
import json
def Existed_JsonFiles():
    path_to_json = 'E:/GP_Threading/Backend/MyPersonalTrainer'
    json_files = [pos_json for pos_json in os.listdir(
        path_to_json) if pos_json.endswith('.json')]
    Sorted_List = natsorted(json_files)
    return (Sorted_List)
def extractJsonData():
    # print(os. getcwd())
    # path_parent = os. path. dirname(os. getcwd())
    # os. chdir(path_parent)
    # print(os. getcwd())
    # print('File name :    ', os.path.basename(__file__))

    output=Existed_JsonFiles()
    dir=os.path.dirname(__file__)
    chdir=dir[0:-5]
    
    jsonFile=open(r'{}\{}'.format(chdir,output[0]))
    data = json.load(jsonFile)
    # return data
    print(data)
extractJsonData()