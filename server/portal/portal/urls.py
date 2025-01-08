"""
URL configuration for portal project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path
from api import views
from api.views import RequestDocumentViewSet, create_request_document,request_documents, upload_excel, download_file, request_job_status, request_transactions
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'request-documents', RequestDocumentViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    re_path(r'^api/test$', views.index),
    path('api/upload_excel/', upload_excel, name='upload_excel'),
    path('api/create-request-document/', create_request_document, name='create_request_document'),
    path('api/request-documents/', request_documents, name='request_documents'),
    path('api/request-job-status/<str:key>/', request_job_status, name="request_job_status"),
    path('api/request-transactions/<str:key>/', request_transactions, name="request_transactions"),
    # 다른 URL 패턴들
    path('download/<str:file_name>/', download_file, name='download_file'),
]
