import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project_lianxi.settings')

import django
django.setup()

from app01 import models

ret = models.Book.objects.all()
print(ret)