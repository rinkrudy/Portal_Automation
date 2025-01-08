from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

# Django의 settings 모듈을 Celery가 사용할 수 있도록 설정
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'portal.settings')

app = Celery('portal')

# Django 설정에서 Celery 관련 설정을 로드
app.config_from_object('django.conf:settings', namespace='CELERY')

# 자동으로 태스크를 감지할 수 있게 설정
app.autodiscover_tasks()