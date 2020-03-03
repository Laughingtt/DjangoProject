from django.contrib import admin
from crm import models

admin.site.register(models.Customer)
admin.site.register(models.ClassList)
admin.site.register(models.Campuses)
admin.site.register(models.ContractTemplate)
admin.site.register(models.ConsultRecord)
admin.site.register(models.StudyRecord)
