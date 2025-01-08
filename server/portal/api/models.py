from django.db import models
from django.contrib.auth.hashers import make_password


class Process(models.Model):
    key = models.CharField(max_length=100, unique=True)
    name = models.CharField(max_length=100, unique=True)
    list_version = models.JSONField(null=True, blank=True)
    description = models.CharField(max_length=200, blank=True)


class ProcessVersion(models.Model):
    key = models.CharField(max_length=100, unique=True)
    version = models.CharField(max_length=20)
    description = models.CharField(max_length=200, blank=True)
    process_key = models.ForeignKey(Process, related_name='key', on_delete=models.CASCADE)


class Flow(models.Model):
    key = models.CharField(max_length=100, unique=True) # 플로우의 고유 식별자
    flow_name = models.CharField(max_length=100, unique=True) # 플로우의 이름
    process_info = models.JSONField(null=True, blank=True)


class Tenant(models.Model):
    key = models.CharField(max_length=100, unique=True)
    

class User(models.Model):
    key = models.CharField(max_length=100, unique=True)
    id = models.CharField(max_length=100, unique=True)
    name = models.CharField(max_length=100)
    password = models.CharField(max_length=128)



    def set_password(self, raw_password):
        self.password = make_password(raw_password)


class Job(models.Model):
    key = models.CharField(max_length=100, unique=True)
    user = models.ForeignKey(User, related_name = "key", on_delete=models.CASCADE)




    
    


class RequestDocument(models.Model):
    STATUS_CHOICES = [
        ('ON_HOLD', 'On hold'),
        ('PROCESSING', 'Processing'),
        ('COMPLETED', 'Completed'),
        ('CANCELLED', 'Cancelled'),
        ('ERROR', 'Error')
    ]
    request_key = models.CharField(max_length=100, unique=True)
    user_id = models.CharField(max_length=100)
    process_name = models.CharField(max_length=100)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='ON_HOLD')
    path_result = models.CharField(max_length=100)
    date = models.DateTimeField(auto_now=True)

    # 기타 필드들...
    def __str__(self):
        return self.request_key


class PatentDocuments(models.Model):
    COUNTRY_CHOICES = [
        ('KR', 'Korea'),
        ('UR', 'USA'),
        ('JR', 'Japan'),
        ('CN', 'China'),
    ]

    STATUS_CHOICES = [
        ('공개', 'Public'),
        ('출원', 'Application'),
    ]


    request_key = models.ForeignKey(RequestDocument, related_name='patent_documents', on_delete=models.CASCADE)
    group = models.CharField(max_length=100)
    country = models.CharField(max_length=2, choices=COUNTRY_CHOICES)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)
    app_number = models.CharField(max_length=100)
    result = models.CharField(max_length=255, default='조회결과', editable=False)

    def __str__(self):
        return f"{self.group.name} - {self.app_number}"



class TaskStatus(models.Model):
    STEP = [
        "CREATED",
        "MAPPING_MEDICAL_CARE",
        "FIND_DOCTOR",
        "FIND_PLACE",
        "MEASURE_DISTANCE",
        "FINISHED"
    ]
    task_id = models.CharField(max_length=255, unique=True)  # 작업 ID
    step  = models.CharField(max_length=50, default=STEP[0])

    # Count Values
    work_count_doctor = models.IntegerField(default=0)
    work_count_place =  models.IntegerField(default=0)
    work_count_measure =  models.IntegerField(default=0)

    total_count = models.IntegerField(default=0)

    failed_count_doctor = models.IntegerField(default=0)
    failed_count_place = models.IntegerField(default=0)
    failed_count_measure = models.IntegerField(default=0)

    status = models.CharField(max_length=50, default='pending')  # 작업 상태 ('pending', 'processing', 'completed', 'failed')
    progress = models.IntegerField(default=0)  # 작업 진행률 (0-100%)

    # 기타 필드들...
    def __str__(self):
        return self.task_id

    # 불가, 필요, 성공
    # failed_doc

class HospitalInfo(models.Model):
    hospital_number = models.CharField(max_length=50, unique=True)
    hospital_name = models.CharField(max_length=50)
    hospital_address = models.CharField( max_length=255, unique=True)
    verify_date = models.DateTimeField()
    coord_lon = models.FloatField(default=-1)
    coord_lat = models.FloatField(default=-1)

    def __str__(self):
        return self.hospital_number


class DoctorInfo(models.Model):
    hospital_key = models.CharField(max_length=255)
    doctor_name = models.CharField(max_length=50)

    def __str__(self):
        return self.doctor_name
    
class PlaceInfo(models.Model):
    place_key = models.CharField(max_length=255, unique=True)
    place_name = models.CharField(max_length=255, unique=True)
    place_address = models.CharField(max_length=255, unique=True)
    coord_lon = models.FloatField(default=-1)
    coord_lat = models.FloatField(default=-1)


class Transaction(models.Model):
    tx_key = models.CharField(max_length=255)
    hospital_name = models.CharField(max_length=50)
    hospital_number = models.CharField(max_length=50)
    doctor_name = models.CharField(max_length=50)
    place_name = models.CharField(max_length=50)

    doctor_exist = models.CharField(default="미확인", max_length=50)
    medical_exist = models.CharField(default="미확인", max_length=50)
    place_exist =models.CharField(default="미확인", max_length=50)
    hospital_address = models.CharField(max_length=255, default="")
    searched_address = models.CharField(default="미확인", max_length=255)
    distance = models.FloatField(default=-1)


    



    




