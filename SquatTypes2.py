import json
import math
import os
import time
import matplotlib.pyplot as plt
from natsort import natsorted
import numpy as np


def Existed_JsonFiles():
    path_to_json = '/home/awatef/GP/MyPersonalTrainer'
    json_files = [pos_json for pos_json in os.listdir(
        path_to_json) if pos_json.endswith('.json')]
    Sorted_List = natsorted(json_files)
    return (Sorted_List)


# list_of_jsons = Existed_JsonFiles()
# list_of_jsons=['pulseSquat2.json']
jsonfile=['pulseSquat2.json']

Shoulder_Y_Positions=[]
Hip_Y_Positions=[]
Knee_Y_Positions=[]
Ankle_Y_Positions=[]

Shoulder_X_Positions=[]
Hip_X_Positions=[]
Knee_X_Positions=[]

Knee_X_Positions_25=[]
Knee_X_Positions_26=[]

Ankle_X_Positions=[]
Toes_X_Positions=[]


Index_Of_KeyPoints = []

# shoulder,hip,knee,foot,toes
Even_KeyPoints = ['12', '24', '26', '28', '30', '32']
Odd_KeyPoints = ['11', '23', '25', '27', '29', '31']

Knee_WRT_Toes_25_26 = []
Knee_Notes=[]
Hip_WRT_Knee_23_24 = []
Hip_Notes=[]

# Direction = "right"
New_Hip_Y_Positions = []
Indecies_Of_Deleted_Values = []
Max_Y_Hip=[]
Max_index = []
Min_Y_Hip=[]
Min_index = []

Max_Hip_Knee_Angles=[]
Min_Hip_Knee_Angles=[]
KneeAngle_Notes=[]
Min_Knee_Angle_Status=[]
Status_of_Max_Hip_Knee_Angles=[]

Max_Back_Angle=[]
Min_Back_Angle=[]
Min_Back_Angle_Status=[]
Max_Back_Angle_Status=[]
MinBackAngle_Notes=[]
MaxBackAngle_Notes=[]

# original_indecies_max=[]
# original_indecies_min=[]

Num_Of_Squats=0
Stage=0

phase1=[]
phase2=[]
phase3=[]
Up_Phases=None
Differnece_Between_KeyFrames=[]
cycles={}
New_Max_Y_Hip=None
New_Min_Y_Hip=None

def Knee_Angle(index):
    vector_Hip_Knee=[Hip_X_Positions[index]-Knee_X_Positions[index],Hip_Y_Positions[index]-Knee_Y_Positions[index]]
    vector_Knee_Ankle=[Knee_X_Positions[index]-Ankle_X_Positions[index],Knee_Y_Positions[index]-Ankle_Y_Positions[index]]
    magnitudeA=math.sqrt(vector_Hip_Knee[0]**2+vector_Hip_Knee[1]**2)
    magnitudeB=math.sqrt(vector_Knee_Ankle[0]**2+vector_Knee_Ankle[1]**2)
    dotProduct=(vector_Hip_Knee[0]*vector_Knee_Ankle[0])+(vector_Hip_Knee[1]*vector_Knee_Ankle[1])
    cosTheta=(dotProduct)/(magnitudeA*magnitudeB)
    theta=math.degrees(math.acos(cosTheta))
    knee_Angle=180-theta

    return knee_Angle

def Hip_Angle(index):

    vector_Shoulder_Hip=[Shoulder_X_Positions[index]-Hip_X_Positions[index],Shoulder_Y_Positions[index]-Hip_Y_Positions[index]]
    vector_Hip_Knee=[Hip_X_Positions[index]-Knee_X_Positions[index],Hip_Y_Positions[index]-Knee_Y_Positions[index]]
    magnitudeA=math.sqrt(vector_Hip_Knee[0]**2+vector_Hip_Knee[1]**2)
    magnitudeB=math.sqrt(vector_Shoulder_Hip[0]**2+vector_Shoulder_Hip[1]**2)
    dotProduct=(vector_Hip_Knee[0]*vector_Shoulder_Hip[0])+(vector_Hip_Knee[1]*vector_Shoulder_Hip[1])
    cosTheta=(dotProduct)/(magnitudeA*magnitudeB)
    theta=math.degrees(math.acos(cosTheta))
    hip_angle=180-theta

    return hip_angle

def Back_Angle(index):
    vector_Back=[Shoulder_X_Positions[index]-Hip_X_Positions[index],Shoulder_Y_Positions[index]-Hip_Y_Positions[index]]
    Y_Axis=[0,1]
    magnitudeA=math.sqrt(vector_Back[0]**2+vector_Back[1]**2)
    magnitudeB=math.sqrt(Y_Axis[0]**2+Y_Axis[1]**2)
    dotProduct=(vector_Back[0]*Y_Axis[0])+(vector_Back[1]*Y_Axis[1])
    cosTheta=(dotProduct)/(magnitudeA*magnitudeB)
    theta=math.degrees(math.acos(cosTheta))
    back_angle=180-theta
    
    return back_angle

def Extract_Positions_Of_KeyPoints(jsonfile):
    global New_Max_Y_Hip,New_Min_Y_Hip
    with open(jsonfile, 'r') as jsonfile:
        Json_File = json.loads(jsonfile.read())

        if Json_File[0].get('32')[0] < Json_File[0].get('30')[0]:
            Index_Of_KeyPoints = Even_KeyPoints
            direction="Left"
        elif Json_File[0].get('32')[0] > Json_File[0].get('30')[0]:
            Index_Of_KeyPoints = Odd_KeyPoints
            direction= "Right"

        for i in range (len(Json_File)):
                shoulder_y_value=Json_File[i].get(Index_Of_KeyPoints[0])[1]
                hip_y_value=Json_File[i].get(Index_Of_KeyPoints[1])[1]
                Knee_y_value=Json_File[i].get(Index_Of_KeyPoints[2])[1]  
                ankle_y_value=Json_File[i].get(Index_Of_KeyPoints[3])[1]             
                
                shoulder_x_value=Json_File[i].get(Index_Of_KeyPoints[0])[0]
                hip_x_value=Json_File[i].get(Index_Of_KeyPoints[1])[0]
                Knee_x_value=Json_File[i].get(Index_Of_KeyPoints[2])[0]
                ankle_x_value=Json_File[i].get(Index_Of_KeyPoints[3])[0]
                Toes_x_value=Json_File[i].get(Index_Of_KeyPoints[5])[0]
                
                Shoulder_Y_Positions.append(shoulder_y_value)
                Hip_Y_Positions.append(hip_y_value)
                Knee_Y_Positions.append(Knee_y_value)
                Ankle_Y_Positions.append(ankle_y_value)

                Shoulder_X_Positions.append(shoulder_x_value)
                Hip_X_Positions.append(hip_x_value)
                Knee_X_Positions.append(Knee_x_value)
                Ankle_X_Positions.append(ankle_x_value)
                Toes_X_Positions.append(Toes_x_value)


    '''
    remove the dublicated numbers of adjacents' indecies 
    '''
    for i in range(len(Hip_Y_Positions)):
        currentNum = Hip_Y_Positions[i]
        if i < len(Hip_Y_Positions)-1:
            nextNum = Hip_Y_Positions[i+1]
        if currentNum != nextNum:
            New_Hip_Y_Positions.append(Hip_Y_Positions[i])
        elif currentNum == nextNum:
            Indecies_Of_Deleted_Values.append(i)

    """
        Get The Max & Min Values of hip joint and the corresponding indices after removing
        repeated numbers
    """
    for i in range(0, len(New_Hip_Y_Positions)):
        prev = New_Hip_Y_Positions[i-1]
        currentvalue = New_Hip_Y_Positions[i]

        if i < len(New_Hip_Y_Positions)-1:
            next = New_Hip_Y_Positions[i+1]

        if (prev > currentvalue < next) and (currentvalue < (np.mean(New_Hip_Y_Positions))):
            Min_Y_Hip.append(currentvalue)
            Min_index.append(i)

        elif (prev < currentvalue > next) and (currentvalue > (np.mean(New_Hip_Y_Positions))):
            Max_Y_Hip.append(currentvalue)
            Max_index.append(i)
    
    # remove dublicated max&min values
    New_Max_Y_Hip=list(set(Max_Y_Hip))
    New_Min_Y_Hip=list(set(Min_Y_Hip))


    # """
    #     Get The indices of Max & Min Values of hip joint from thr original list
    # """
    # for index in range (len(Hip_Y_Positions)):
    #     for max_index in range (len(New_Max_Y_Hip)):
    #         if Hip_Y_Positions[index]==New_Max_Y_Hip[max_index]:
    #             original_indecies_max.append(index)
    #     for min_index in range (len(New_Min_Y_Hip)):
    #         if Hip_Y_Positions[index]==New_Min_Y_Hip[min_index]:
    #             original_indecies_min.append(index)
    return direction

def Number_Of_WallSquatCycles():
    global Num_Of_Squats,Stage,Differnece_Between_KeyFrames,Up_Phases    
    lenOfyList=len(Hip_Y_Positions)
    maxOfyList=max(Hip_Y_Positions)
    for i in range(0,lenOfyList,1):
        backAngle=Back_Angle(i)
        hip_angle=Hip_Angle(i)
        # for index in range ((lenOfMax)):
        if (175 <= hip_angle <= 180)and(Stage==0) and (175<= (backAngle) <=180): 
            Stage=1
            phase1.append(i)

        elif (Hip_Y_Positions[i] in (Min_Y_Hip)) and (Stage==1) and (90<= hip_angle<=115):
            Stage=2
            phase2.append(i)
        
        elif (maxOfyList-5)<=Hip_Y_Positions[i]<=(maxOfyList) and (Stage==2) and (175<= (backAngle) <=180):
            Num_Of_Squats=Num_Of_Squats+1
            Stage=1
            phase3.append(i)
    
    Up_Phases=natsorted(phase1+phase3)
    Minlength=min(len(phase2),len(Up_Phases))
    for i in range (Minlength):
        firsthalf=abs(Up_Phases[i]-phase2[i])
        if len(Up_Phases) == len(Minlength):
            if i < len(Up_Phases)-1:
                secondhalf=abs(phase2[i]-Up_Phases[i+1])
        else:
            if i<len(Up_Phases): 
                secondhalf=abs(phase2[i]-Up_Phases[i+1])    
        Differnece_Between_KeyFrames.append(abs(firsthalf-secondhalf))

def Number_Of_SquatCycles():
    global Num_Of_Squats,Stage,Differnece_Between_KeyFrames,Up_Phases    
    lenOfyList=len(Hip_Y_Positions)
    for i in range(0,lenOfyList,1):
        backAngle=Back_Angle(i)
        hip_angle=Hip_Angle(i)
        # for index in range ((lenOfMax)):
        if (Hip_Y_Positions[i] in (New_Max_Y_Hip))and(Stage==0) and (170<= (backAngle) <=180): 
            Stage=1
            phase1.append(i)
        
        elif (Hip_Y_Positions[i] in (New_Min_Y_Hip)) and (Stage==1) and (140<= backAngle<=180):
            Stage=2
            phase2.append(i)
        
        elif(Hip_Y_Positions[i] in (New_Max_Y_Hip)) and (Stage==2) and (160<= (backAngle) <=180):
            Num_Of_Squats=Num_Of_Squats+1
            Stage=1
            phase3.append(i)
    
    Up_Phases=natsorted(phase1+phase3)
    # print(len(Up_Phases),len(phase2))
    Minlength=min(len(phase2),len(Up_Phases))
    for i in range (Minlength):
        firsthalf=abs(Up_Phases[i]-phase2[i])
        if len(Up_Phases)==len(phase2):
            if i < Minlength-1:
                secondhalf=abs(phase2[i]-Up_Phases[i+1])  
        else:
            if i <len(Up_Phases):  
                secondhalf=abs(phase2[i]-Up_Phases[i+1]) 
        Differnece_Between_KeyFrames.append(abs(firsthalf-secondhalf))

def Number_Of_PulseSquatCycles():
    global Num_Of_Squats,Stage,Differnece_Between_KeyFrames,Up_Phases    
    lenOfyList=len(Hip_Y_Positions)
    # print(lenOfMin,lenOfMax)
    for i in range(0,lenOfyList,1):
        backAngle=Back_Angle(i)
        hip_angle=Hip_Angle(i)
        knee_angle=Knee_Angle(i)
        # for index in range ((lenOfMax)):
        if (Hip_Y_Positions[i] in (New_Max_Y_Hip))and(Stage==0) and (175<= (backAngle) <=180): 
            Stage=1
            phase1.append(i)

        elif (Knee_Y_Positions[i]<= Hip_Y_Positions[i]<=1.1*Knee_Y_Positions[i]) and (Stage==1) and (80<= knee_angle<=90):
            Stage=2
            phase2.append(i)
        
        elif (1.03*Knee_Y_Positions[i]< Hip_Y_Positions[i]<=1.3*Knee_Y_Positions[i]) and (Stage==2) and (65<= knee_angle<=80):
            Num_Of_Squats=Num_Of_Squats+1
            Stage=1
            phase3.append(i)
    
    Up_Phases=natsorted(phase1+phase3)
    Minlength=min(len(phase2),len(Up_Phases))
    for i in range (Minlength):
        firsthalf=abs(Up_Phases[i]-phase2[i])
        if len(Up_Phases)==len(phase2):
            if i < Minlength-1:
                secondhalf=abs(phase2[i]-Up_Phases[i+1])  
        else:
            if i <len(Up_Phases):  
                secondhalf=abs(phase2[i]-Up_Phases[i+1])
        Differnece_Between_KeyFrames.append(abs(firsthalf-secondhalf))
                                    
def Positions_Conditions(Direction,factor1,factor2):
    for i in range(len(Differnece_Between_KeyFrames)):
        if 0<= Differnece_Between_KeyFrames[i]<=60: 
            if Direction=='Left':                 
            # check knee position
                if Knee_X_Positions[phase2[i]] >= 0.9*Toes_X_Positions[phase2[i]]:
                    Knee_WRT_Toes_25_26.append(1)
                    Knee_Notes.append('Correct Knee Position at cycle no'+str(i+1))
                else:
                    Knee_WRT_Toes_25_26.append(0)
                    Knee_Notes.append('Wrong Knee Position,your knee should not exceed your toes at cycle'+str(i+1) )
            elif Direction=='Right':                 
            # check knee position
                if Knee_X_Positions[phase2[i]] <= Toes_X_Positions[phase2[i]]:
                    Knee_WRT_Toes_25_26.append(1)
                    Knee_Notes.append('Correct Knee Position at cycle no'+str(i+1))
                else:
                    Knee_WRT_Toes_25_26.append(0)
                    Knee_Notes.append('Wrong Knee Position,your knee should not exceed your toes at cycle'+str(i+1) )                    
            # check hip position
            
            if ((factor1*Knee_Y_Positions[phase2[i]]) <= Hip_Y_Positions[phase2[i]] <= factor2*(Knee_Y_Positions[phase2[i]])):
                Hip_WRT_Knee_23_24.append(1)
                Hip_Notes.append('Correct Hip position at cycle'+str(i+1))
            
            else:
                Hip_WRT_Knee_23_24.append(0)
                Hip_Notes.append('Wrong Hip position,Your Hip should be at least at knee position at cycle'+str(i+1))
                                    

def Angles_Conditions(minKnee,maxKnee,Up_minBack,Up_MaxBack,Down_minBack,Down_maxBack):
    for i in range(len(Differnece_Between_KeyFrames)):
        if 0<= Differnece_Between_KeyFrames[i]<=60:
            if len(Up_Phases)==len(Differnece_Between_KeyFrames):
                if i < len(Up_Phases)-1:
                    cycles['keyFramesOf_Cycle'+str(i+1)]=[str(Up_Phases[i]),str(phase2[i]),str(Up_Phases[i+1])]
            else:
                if i <len(Up_Phases):  
            # append indecies of keyFrames of each squat cycle
                    cycles['keyFramesOf_Cycle'+str(i+1)]=[str(Up_Phases[i]),str(phase2[i]),str(Up_Phases[i+1])]
            
            # Angle between hip&knee at min position
            knee_Angle=Knee_Angle(phase2[i])
            Min_Hip_Knee_Angles.append(knee_Angle)
            if minKnee<= knee_Angle <=maxKnee:
                Min_Knee_Angle_Status.append(1)
                KneeAngle_Notes.append('Correct knee angle at cycle'+str(i+1))
            
            else :
                Min_Knee_Angle_Status.append(0)
                KneeAngle_Notes.append('Wrong knee angle at cycle'+str(i+1)+'Your knee angle should be between 70 and 90 degree')
            
            # Angle of back at Min position
            
            back_angle=Back_Angle(phase2[i])
            Min_Back_Angle.append(back_angle)
            if Down_minBack<= (back_angle) <= Down_maxBack:
                Min_Back_Angle_Status.append(1)
                MinBackAngle_Notes.append('Correct Back angle at cycle'+str(i+1))            
            else:
                Min_Back_Angle_Status.append(0)
                MinBackAngle_Notes.append('Wrong Back angle at cycle'+str(i+1)+'Your Back Angle should be between 70 and 90 degree')


            back_angle=Back_Angle(Up_Phases[i])
            Max_Back_Angle.append(back_angle)
            
            if Up_minBack<= (back_angle) <= Up_MaxBack:
                Max_Back_Angle_Status.append(1)
                MaxBackAngle_Notes.append('Correct Back angle at cycle'+str(i+1))
            
            else:
                Max_Back_Angle_Status.append(0)        
                MaxBackAngle_Notes.append('Wrong Back angle at cycle'+str(i+1)+'Your Back Angle should be between 175 and 180 degree')


def Comparing_Algorithm(jsonfile,type):

    Direction_Side=Extract_Positions_Of_KeyPoints(jsonfile)
    if type =='Wall Squat':
        Number_Of_WallSquatCycles()
        Positions_Conditions(Direction_Side,factor1=1,factor2=1.15)
        Angles_Conditions(minKnee=70,maxKnee=100,Up_minBack=175,Up_MaxBack=180,Down_minBack=175,Down_maxBack=180)
    
    elif type == 'Regular Squat':
        Number_Of_SquatCycles()
        Positions_Conditions(Direction_Side,factor1=0.85,factor2=1.15)
        Angles_Conditions(minKnee=60,maxKnee=110,Up_minBack=160,Up_MaxBack=180,Down_minBack=155,Down_maxBack=180)

    elif type == 'Pulse Squat':
        Number_Of_PulseSquatCycles()
        Positions_Conditions(Direction_Side,factor1=1,factor2=1.15)
        Angles_Conditions(minKnee=60,maxKnee=110,Up_minBack=160,Up_MaxBack=180,Down_minBack=155,Down_maxBack=180)
    
    elif type == 'Deep Squat':
        Number_Of_SquatCycles()
        Positions_Conditions(Direction_Side,factor1=0.8,factor2=1)
        Angles_Conditions(minKnee=45,maxKnee=80,Up_minBack=170,Up_MaxBack=180,Down_minBack=140,Down_maxBack=180)
           
    print(Direction_Side)
    return Num_Of_Squats,Up_Phases,phase2,Knee_WRT_Toes_25_26,Knee_Notes,Hip_WRT_Knee_23_24,Hip_Notes,Min_Knee_Angle_Status,KneeAngle_Notes,Max_Back_Angle_Status,MaxBackAngle_Notes,Min_Back_Angle_Status,MinBackAngle_Notes            
# # Extract_Positions_Of_KeyPoints()
# # Number_Of_WallSquatCycles()
# Comparing_Algorithm(jsonfile,type='Pulse Squat') 
# # print('maxback',180-Back_Angle(5))
# # print('minback',90-Back_Angle(40))

# # print('direction',Direction)
# # print('HipYPosition=',Hip_Y_Positions)
# # print('Max',Max_index)
# # print('Min',Min_index)
# # print(Hip_Y_Positions[299])
# print('Knee_WRT_Toes', Knee_WRT_Toes_25_26)
# # print('kneeNotes',Knee_Notes)
# print('Hip_WRT_Knee', Hip_WRT_Knee_23_24)
# # print('HipNotes',Hip_Notes)

# # print('Min_Hip_Knee_Angles', Min_Hip_Knee_Angles)
# print('Min_Knee_Angle_Status', Min_Knee_Angle_Status)
# # print('kneeAngleNotes',KneeAngle_Notes)

# # print('maxback',Max_Back_Angle)
# # print('minback',Min_Back_Angle)
# print('Min_Back_Status',Min_Back_Angle_Status)
# # print('MinBackNotes',MinBackAngle_Notes)

# print('Max_Back_Status',Max_Back_Angle_Status)
# # print('MaxBackNotes',MaxBackAngle_Notes)

# # print('phase1=',phase1)
# # print('phase3=',phase3)
# print('Up_Phases',Up_Phases)
# print('phase2=',phase2)

# print('Differnece_Between_KeyFrames',Differnece_Between_KeyFrames)
# print('cycles',cycles)
# # print(Hip_Y_Positions[5])
# # print(180-Back_Angle(167))
# # print('MAX',Max_Y_Hip)
# # print('min',Min_Y_Hip)
# # print('NewMAX',New_Max_Y_Hip)
# # print('Newmin',New_Min_Y_Hip)
# # print('hip=',Hip_Angle(0))
# # print(Hip_Y_Positions)
# # print(Knee_Y_Positions)

# # print(Knee_Y_Positions[54])
# # print(Toes_X_Positions[0])

# # print('back',Back_Angle(193))
# # print(Knee_Angle(98))


# # plt.subplot(121)
# # plt.plot(Hip_Y_Positions, color='r', label='Hip_joint')
# # plt.plot(Knee_Y_Positions, color='g', label='Hip_joint')

# # plt.ylabel("Y-Values")
# # # plt.title("Tracking y_positions of four Differnece_Between_KeyFrameserent joints")
# # plt.title("Number of Squats = "+str(Num_Of_Squats))
# # plt.legend(loc='upper right')
# # plt.show()
