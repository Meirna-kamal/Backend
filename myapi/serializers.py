from rest_framework import serializers
from rest_framework.serializers import Serializer,FileField,CharField
from .models import file

class filePostSerializer(Serializer):
    file_uploaded = FileField()
    class Meta:
        fields = ['file_uploaded']
class postStatusSerializer(Serializer):
    class Meta:
        model=file
        fields=('status',)
class postExerciseSerializer(serializers.ModelSerializer):
    class Meta:
        model=file
        fields = ['exercise']