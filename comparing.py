import json
import os
from SquatTypes2 import Comparing_Algorithm
import requests

response_API = requests.get('http://127.0.0.1:8000/getExercise/')
data = response_API.text
loaded_data = json.loads(data)
if loaded_data==1:
    exerciseType='Wall Squat'
elif loaded_data==2:
    exerciseType='Regular Squat'
elif loaded_data==3:
    exerciseType='Pulse Squat'
else:
    exerciseType='Deep Squat'
print(exerciseType)

cwd = os.path.dirname(os.path.realpath(__file__))
dir_n_files = os.listdir(cwd)
for j in range(0,len(dir_n_files),1):
    if dir_n_files[j].endswith('.json'):
        jsonPath=r'{}\{}'.format(cwd, dir_n_files[j])
        jsonFile=open(jsonPath)
        data = json.load(jsonFile)
        output=Comparing_Algorithm(jsonPath,exerciseType)
        print(output)
        True_Min_index=output[2]
        True_Max_index=output[1]
        Status_of_Min_Hip_Knee_Angles=output[7]
        Min_Hip_Knee_Angles_comments=output[8]
        Max_Back_Angle_Status=output[9]
        Max_Back_Angle_Status_comments=output[10]
        Min_Back_Angle_Status=output[11]
        Min_Back_Angle_Status_comments=output[12]
        Knee_WRT_Toes_25_26=output[3]
        Knee_WRT_Toes_25_26_comments=output[4]
        Hip_WRT_Knee_23_24=output[5]
        Hip_WRT_Knee_23_24_comments=output[6]

        for i in range(0,len(data),1):
            if True_Max_index==Max_Back_Angle_Status:
                if i in True_Min_index:
                    k=True_Min_index.index(i)
                    data[i-1].update({"Angles":[Status_of_Min_Hip_Knee_Angles[k],Min_Back_Angle_Status[k]],"Positions":[Knee_WRT_Toes_25_26[k],Hip_WRT_Knee_23_24[k]],"comments":[Min_Hip_Knee_Angles_comments[k],Min_Back_Angle_Status_comments[k],Knee_WRT_Toes_25_26_comments[k],Hip_WRT_Knee_23_24_comments[k]],"squats":[output[0]]})
                elif i in True_Max_index:
                    k=True_Max_index.index(i)
                    data[i-1].update({"Angles":[1,Max_Back_Angle_Status[k]],"Positions":[1,1],"comments":[Max_Back_Angle_Status_comments[k]],"squats":[output[0]]})
                else:
                    data[i-1].update({"Angles":[2,2],"Positions":[2,2],"comments":[],"squats":[output[0]]})
            else:
                if i in True_Min_index:
                    k=True_Min_index.index(i)
                    data[i-1].update({"Angles":[Status_of_Min_Hip_Knee_Angles[k],Min_Back_Angle_Status[k]],"Positions":[Knee_WRT_Toes_25_26[k],Hip_WRT_Knee_23_24[k]],"comments":[Min_Hip_Knee_Angles_comments[k],Min_Back_Angle_Status_comments[k],Knee_WRT_Toes_25_26_comments[k],Hip_WRT_Knee_23_24_comments[k]],"squats":[output[0]]})
                elif i in True_Max_index[:-1]:
                    k=True_Max_index.index(i)
                    data[i-1].update({"Angles":[1,Max_Back_Angle_Status[k]],"Positions":[1,1],"comments":[Max_Back_Angle_Status_comments[k]],"squats":[output[0]]})
                else:
                    data[i-1].update({"Angles":[2,2],"Positions":[2,2],"comments":[],"squats":[output[0]]})
        with open(jsonPath, 'w') as fp:
            fp.write(
                '[' +
                ',\n'.join(json.dumps(i,separators=(',', ':')) for i in data) +
                ']\n')
url = 'http://127.0.0.1:8000/postStatus/'
myobj = {'Progress': 'Done'}
done = requests.post(url, json = myobj)