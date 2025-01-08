from rest_framework import serializers
from .models import PatentDocuments, RequestDocument, TaskStatus, HospitalInfo, DoctorInfo, PlaceInfo, Transaction

class PatentDocumentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = PatentDocuments
        fileds = ['id', 'request_key', 'group', 'country', 'status', 'app_number', 'result']


class RequestDocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = RequestDocument
        fields = ['id',  'process_name', 'request_key', 'status', 'user_id','date', 'path_result']


class TaskStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskStatus
        fields = '__all__'



class HospitalInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = HospitalInfo
        fields = '__all__'



class DoctorInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = DoctorInfo
        fields = '__all__'



class PlaceInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlaceInfo
        fields = '__all__'


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = '__all__'

