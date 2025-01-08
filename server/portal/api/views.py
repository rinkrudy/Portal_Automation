from rest_framework.response import Response
from rest_framework.decorators import api_view,action
from rest_framework import status, viewsets
import os
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.conf import settings
from datetime import datetime

from .models import PatentDocuments, RequestDocument, TaskStatus, Transaction
from .serializers import RequestDocumentSerializer,   PatentDocumentsSerializer, TaskStatusSerializer, TransactionSerializer
from django.shortcuts import get_object_or_404

from celery import shared_task
import pandas as pd
import json

from .tasks import process_workflow



# Create your views here.

@api_view(['GET'])
def index(request):
    print('hello')
    return HttpResponse('hello')

@api_view(['POST'])
def create_request_document(request):
    request_info = json.loads(request.data.get('request_info'))


    # RequestDocument 생성
    document = RequestDocument.objects.create(
        user_id = request_info["user_id"],
        request_key= request_info["request_key"],
        process_name = request_info["process_name"],
        path_result = '',
        status='ON_HOLD',
    )


    if request_info["process_name"] == "Health_Automation":
        excel_file = request.FILES['file']
        background_mode = request.POST.get('background_mode')
        print(background_mode)

        # 파일을 판다스 데이터프레임으로 변환
        print(excel_file)
        df = pd.read_excel(excel_file)
        # Status 생성
        task_status = TaskStatus.objects.create(
            task_id = document.request_key,
            total_count = len(df),
        )

        df_dict = df.to_dict()

        document.status = 'PROCESSING'
        document.save()

        # 데이터프레임 확인 및 필요한 처리
        process_workflow(df_dict, document.request_key, background_mode)

        

        return Response({'message': 'Request is being processed', 'request_key': request_info["request_key"]}, status=status.HTTP_200_OK)
    else:
        return Response({'message': f'There is not existed process {request_info["process_name"]}', 'request_key': request_info["request_key"]}, status=status.HTTP_400_BAD_REQUEST)
    
    # # PatentDocument 생성
    # patent_documents = request.data.get('patent_documents', [])
    # for patent_data in patent_documents:
    #     PatentDocuments.objects.create(
    #         request_key=document,
    #         group=patent_data['group'],
    #         country=patent_data['country'],
    #         status=patent_data['status'],
    #         app_number=patent_data['app_number'],
    #         result='조회결과'  # 초기 조회 결과
    #     )
    



@api_view(["POST"])
def upload_excel(request):
    print(request.data)
    try:
        # 'file'이라는 이름으로 파일을 전송받음
        excel_file = request.FILES['file']


        # 파일을 판다스 데이터프레임으로 변환
        df = pd.read_excel(excel_file)

        # 데이터프레임 확인 및 필요한 처리

        df_dict = df.to_dict()
        test_workflow_task(df_dict)

        # 성공 응답
        
        
    
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)




@api_view(["GET"])
def request_documents(request):
    # 모든 RequestDocument를 가져옵니다.
    documents = RequestDocument.objects.all()
    
    # 데이터를 직렬화합니다.
    serializer = RequestDocumentSerializer(documents, many=True)
    
    # 직렬화된 데이터를 JSON 응답으로 반환합니다.
    return Response(serializer.data)

@api_view(["GET"])
def request_job_status(request, key):
    request_key = key
    task_status = get_object_or_404(TaskStatus, task_id = request_key)

    status = TaskStatusSerializer(task_status)
    #RequestDocumentSerializer(documents, many=True)
    
    return Response(status.data)

@api_view(["GET"])
def request_transactions(request, key):
    request_key = key
    trasactions = Transaction.objects.filter(tx_key = request_key)

    if not trasactions.exists():
        # 만약 결과가 없을 경우, 404 에러 반환
        return Response({"error": "No transactions found for this request key"}, status=404)

    # 여러 개의 transactions를 처리할 수 있도록 수정
    tx_info = TransactionSerializer(trasactions, many=True)

    #RequestDocumentSerializer(documents, many=True)
    
    return Response(tx_info.data)




def download_file(request, file_name):
    file_path = os.path.join(settings.MEDIA_ROOT, file_name)
    
    if os.path.exists(file_path):
        with open(file_path, 'rb') as fh:
            response = HttpResponse(fh.read(), content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
            response['Content-Disposition'] = f'attachment; filename={file_name}'
            return response
    else:
        return HttpResponse("File not found.", status=404)


class RequestDocumentViewSet(viewsets.ModelViewSet):
    queryset = RequestDocument.objects.all()
    serializer_class = RequestDocumentSerializer

    def retrieve(self, request, pk=None):
        document = self.get_object()
        serializer = self.get_serializer(document)
        return Response(serializer.data)


def complete_processing(document_id):
    document = RequestDocument.objects.get(id=document_id)
    document.status = 'COMPLETED'
    document.save()

def start_processing(document_id):
    document = RequestDocument.objects.get(id=document_id)
    document.status = 'PROCESSING'
    document.save()


def handle_processing_error(document_id):
    document = RequestDocument.objects.get(id=document_id)
    document.status = 'ERROR'
    document.save()


@shared_task
def process_request_document(document_id):
    try:
        document = RequestDocument.objects.get(id=document_id)
        document.status = 'PROCESSING'
        document.save()
        
        # 실제 데이터 처리 로직 (비동기)
        # 예: 외부 API 호출, 데이터 처리 등
        patent_documents = document.patent_documents.all()
        for patent_doc in patent_documents:
            patent_doc.result = '실제 처리 결과'
            patent_doc.save()

        # 작업 완료 후 상태를 COMPLETED로 변경
        document.status = 'COMPLETED'
        document.save()
    
    except Exception as e:
        # 에러 발생 시 상태를 ERROR로 변경
        document.status = 'ERROR'
        document.save()
        print(f"Error processing document {document_id}: {e}")


