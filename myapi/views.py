from django.core.files.storage import FileSystemStorage

from rest_framework.views import APIView
from rest_framework import generics,status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny

from .serializers import filePostSerializer,postStatusSerializer,postExerciseSerializer
from .models import file
from MyPersonalTrainer.settings import MEDIA_ROOT

import sys
import glob
import json
import os
import time
import subprocess
import threading
from natsort import natsorted

class HelloView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        content = {'message': 'Hello, World!'}
        return Response(content)

class HandleVideos(threading.Thread):
    def __init__(self,filePath):
        threading.Thread.__init__(self)
        self.filePath=filePath
    def run(self):
        # Get All JsonFiles and sort them in a list
        JsonFiles_List = Existed_JsonFiles()

        # Check if there are Old JsonFiles and delete them
        if JsonFiles_List:
            for Jsonfile in JsonFiles_List:
                os.remove(Jsonfile)
            print("Old Jsonfiles deleted successfuly")
        else:
            print("there are no jsonfiles")

        # Calling Deep-Learning Model
        Calling_DL=subprocess.Popen(['python', 'E:/GP_Threading/Backend/MyPersonalTrainer/Deep-Learning/main.py', '-v',self.filePath])
        Calling_DL.wait()

        # Sorting the created JsonFiles from the Deep-Learning
        JsonFiles_List = Existed_JsonFiles()

        # Validate The Created JsonFiles
        if JsonFiles_List:
            valid_JsonFiles = []
            Invalid_JsonFiles = []
            for Jsonfile in JsonFiles_List:
                with open(Jsonfile) as f:
                    if ValidateJsonFile(f):
                        valid_JsonFiles.append(Jsonfile)
                    else:
                        Invalid_JsonFiles.append(Jsonfile)
            print("The Valid JsonFiles are:", valid_JsonFiles)
            print("The invalid JsonFiles are:", Invalid_JsonFiles)
 

class fileUploadApi(APIView):
    permission_classes = (AllowAny,)
    serializer_class = filePostSerializer

    def get(self, request):
        return Response("GET API")

    def post(self, request):
        filelist = glob.glob(os.path.join(MEDIA_ROOT, "*"))
        for f in filelist:
            os.remove(f)
        file_uploaded = request.FILES.get('file_uploaded')
        fs = FileSystemStorage()
        fs.save(file_uploaded.name, file_uploaded)
        content_type = file_uploaded.content_type
        fileName = file_uploaded.name
        filePath = MEDIA_ROOT+'/'+fileName
        # file.objects.create(path=filePath)
        getFile=file.objects.filter().order_by('-id')[0]
        getFile.path=filePath
        getFile.save()
        # Get All JsonFiles and sort them in a list
        JsonFiles_List = Existed_JsonFiles()

        # Check if there are Old JsonFiles and delete them
        if JsonFiles_List:
            for Jsonfile in JsonFiles_List:
                os.remove(Jsonfile)
            print("Old Jsonfiles deleted successfuly")
        else:
            print("there are no jsonfiles")

        # Calling Deep-Learning Model
        Calling_DL=subprocess.Popen(['python', 'E:/GP_Threading/Backend/MyPersonalTrainer/Deep-Learning/main.py', '-v',filePath])
        Calling_DL.wait()

        # Sorting the created JsonFiles from the Deep-Learning
        JsonFiles_List = Existed_JsonFiles()

        # Validate The Created JsonFiles
        if JsonFiles_List:
            valid_JsonFiles = []
            Invalid_JsonFiles = []
            for Jsonfile in JsonFiles_List:
                with open(Jsonfile) as f:
                    if ValidateJsonFile(f):
                        valid_JsonFiles.append(Jsonfile)
                    else:
                        Invalid_JsonFiles.append(Jsonfile)
            print("The Valid JsonFiles are:", valid_JsonFiles)
            print("The invalid JsonFiles are:", Invalid_JsonFiles)
        returnData=extractJsonData()
        # response = "POST API and you have uploaded a {} file".format(
            # content_type)
        return Response(returnData)


def ValidateJsonFile(jsonFile):
    try:
        json.load(jsonFile)
    except ValueError as error:
        print(error)
        return False
    return True


def Existed_JsonFiles():
    path_to_json = 'E:/GP_Threading/Backend/MyPersonalTrainer'
    json_files = [pos_json for pos_json in os.listdir(
        path_to_json) if pos_json.endswith('.json')]
    Sorted_List = natsorted(json_files)
    return (Sorted_List)
def extractJsonData():
    output=Existed_JsonFiles()
    dir=os.path.dirname(__file__)
    chdir=dir[0:-5]
    jsonFile=open(r'{}\{}'.format(chdir,output[0]))
    data = json.load(jsonFile)
    return data
class PostStatus(APIView):
        permission_classes= ( AllowAny,)
        def post(self,request):
            Modeserializer=postStatusSerializer(data=request.data)
            if Modeserializer.is_valid():
                getProgress=file.objects.filter().order_by('-id')[0]
                getProgress.progress=1
                getProgress.save()
                return Response({"status": "success", "data": Modeserializer.data}, status=status.HTTP_200_OK)
            else:
                return Response({"status": "error", "data": Modeserializer.errors}, status=status.HTTP_400_BAD_REQUEST)

class Get_Status(APIView):
    permission_classes= ( AllowAny,)
    def get(self,request):
        status=file.objects.filter().order_by('-id')[0]
        JsonStatus=status.progress
        return Response (JsonStatus)

class PostExercise(APIView):
        permission_classes= ( AllowAny,)
        serializer_class=postExerciseSerializer
        def post(self,request):
            exerciseserializer=postExerciseSerializer(data=request.data)
            if exerciseserializer.is_valid():
                exerciseserializer.save()
                return Response({"status": "success", "data": exerciseserializer.data}, status=status.HTTP_200_OK)
            else:
                return Response({"status": "error", "data": exerciseserializer.errors}, status=status.HTTP_400_BAD_REQUEST)
class getExerciseType(APIView):
    permission_classes= ( AllowAny,)
    def get(self,request):
        lastExercise=file.objects.filter().order_by('-id')[0]
        exerciseType=lastExercise.exercise
        return Response (exerciseType)